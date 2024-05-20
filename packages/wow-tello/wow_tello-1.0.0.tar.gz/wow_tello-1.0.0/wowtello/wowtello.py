import socket
import threading
import time
from abc import *
import numpy as np
import h264decoder
import cv2

__WOW_TELLO_DRONE_VERSION__ = "1.3.0"

TELLO_CMD_PORT = 8889
TELLO_DATA_PORT = 8890
TELLO_VIDEO_PORT = 11111

RESPONSE_OK = "ok"
RESPONSE_ERROR = "error"
RESPONSE_UNKNOWN_COMMAND = "unknown command"

RESP_NONE = 0
RESP_OK = 1
RESP_ERROR = 2
RESP_UNKNOWN = 3
RESP_TIMEOUT = 4

_WOW_TELLO_DEBUG_ENABLE = False

def wprt(str):
	global _WOW_TELLO_DEBUG_ENABLE
	if _WOW_TELLO_DEBUG_ENABLE:
		print(str)

# constrain 함수
# x 값을 min, max제한을 두어 리턴한다.
def constrain(x, min, max):
	if x < min:
		return min
	elif x > max:
		return max
	
	return x

#######################################################################################
#
# 텔로 기본 통신 모듈 클래스
#
#######################################################################################
# 추상 클래스로 생성
class TelloComModule(metaclass=ABCMeta):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 소켓 생성
	receive_thread_lock = threading.Lock()

	def init_socket(self):
		self.sock.bind(('0.0.0.0', TELLO_CMD_PORT))
		wprt("명령어 통신 소켓 초기화")

		self.receive_thread = threading.Thread(target=self._receive_thread_)
		self.receive_thread.setDaemon(True)
		self.receive_thread.start()
		wprt("명령어 통신 쓰레드 실행")

	# 소켓에서 받은 데이터를 상속받은 클래스에서 처리하기 위해 추상 메소드로 구현
	@abstractmethod
	def receive_data_handler(self, addr, data):
		pass
		
	def _receive_thread_(self):
		response = ''
		addr = ('', 0)
		while True:
			try:
				response, addr = self.sock.recvfrom(128)
				response = response.decode() # Bytes를 str로 변환

				if _WOW_TELLO_DEBUG_ENABLE:
					print("\nresponse addr : ", addr, response)
				self.receive_thread_lock.acquire() # 내부 리스트 접근 쓰레드 Lock
				self.receive_data_handler(addr, response) # 데이터 처리 추상 메소드 실행
				self.receive_thread_lock.release()

			except socket.error as exc:
				print ("Caught exception socket.error : %s" % exc)

			except Exception as e:
				# print ("Tello ERROR :", e)
				pass

			finally:
				if self.receive_thread_lock.locked():
					self.receive_thread_lock.release()

			time.sleep(0.005)

#######################################################################################
#
# 텔로 비행 데이터 수신 모듈 클래스
#
#######################################################################################
class TelloFlightData:
	mid = 0 # 인식된 미션패드 번호
	mx = 0 # 미션패드 x좌표
	my = 0 # 미션패드 y좌표
	mz = 0 # 미션패드 z좌표
	mpitch = 0 # 미션패드 p축
	mroll = 0 # 미션패드 r축
	myaw = 0 # 미션패드 y축
	pitch = 0 # pitch 축 자세계
	roll = 0 # roll 축 자세계
	yaw = 0 # yaw 축 자세계
	vel_x = 0 # x 축 속도
	vel_y = 0 # y 축 속도
	vel_z = 0 # z 축 속도
	temp_lowest = 0 # 최저 온도
	temp_highest = 0 # 최고 온도
	tof = 0 # time of flight 거리 cm
	height = 0 # 고도 cm
	battery = 0 # 배터리 잔량
	baro = 0 # 기압 고도 cm
	time = 0 # 비행시간(모터가 동작하는 기준)
	acc_x = 0 # x 축 가속도
	acc_y = 0 # y 축 가속도
	acc_z = 0 # z 축 가속도

class TelloFlightDataReceiver(metaclass=ABCMeta):
	tfd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 소켓 생성
	tfd_receive_thread_lock = threading.Lock()

	def tfd_init_socket(self):
		self.tfd_sock.bind(('0.0.0.0', TELLO_DATA_PORT))
		# print("비행 정보 수신 소켓 초기화")

		self.tfd_receive_thread = threading.Thread(target=self._tfd_receive_thread_)
		self.tfd_receive_thread.setDaemon(True)
		self.tfd_receive_thread.start()
		# print("비행 정보 수신 쓰레드 실행")

	# 소켓에서 받은 데이터를 상속받은 클래스에서 처리하기 위해 추상 메소드로 구현
	# data에는 TelloFlightData 객체가 입력된다.
	@abstractmethod
	def tfd_receive_data_handler(self, addr, data):
		pass
		
	def tfd_parse_data(self, str_data):
		tfd = TelloFlightData()
		elements = str_data.split(';')
		elements_len = len(elements)
		for i in elements:
			element = i.split(':')
			if len(element) != 2:
				continue

			data_name = element[0]
			data_value = element[1]
			if data_name == 'mid':
				# dbg print('mid 설정', end=' ')
				tfd.mid = int(data_value)
			elif data_name == 'x':
				# dbg print('mx 설정', end=' ')
				tfd.mx = int(data_value)
			elif data_name == 'y':
				# dbg print('my 설정', end=' ')
				tfd.my = int(data_value)
			elif data_name == 'z':
				# dbg print('mz 설정', end=' ')
				tfd.mz = int(data_value)
			elif data_name == 'mpry':
				pry = data_value.split(',')
				if len(pry) == 3:
					# dbg print('pry 설정', end=' ')
					tfd.mpitch = int(pry[0])
					tfd.mroll = int(pry[1])
					tfd.myaw = int(pry[2])
			elif data_name == 'pitch':
				# dbg print('p 설정', end=' ')
				tfd.pitch = int(data_value)
			elif data_name == 'roll':
				# dbg print('r 설정', end=' ')
				tfd.roll = int(data_value)
			elif data_name == 'yaw':
				# dbg print('y 설정', end=' ')
				tfd.yaw = int(data_value)
			elif data_name == 'vgx':
				# dbg print('vgx 설정', end=' ')
				tfd.vel_x = int(data_value)
			elif data_name == 'vgy':
				# dbg print('vgy 설정', end=' ')
				tfd.vel_y = int(data_value)
			elif data_name == 'vgz':
				# dbg print('vgz 설정', end=' ')
				tfd.vel_z = int(data_value)
			elif data_name == 'templ':
				# dbg print('templ 설정', end=' ')
				tfd.temp_lowest = int(data_value)
			elif data_name == 'temph':
				# dbg print('temph 설정', end=' ')
				tfd.temp_highest = int(data_value)
			elif data_name == 'tof':
				# dbg print('tof 설정', end=' ')
				tfd.tof = int(data_value)
			elif data_name == 'h':
				# dbg print('h 설정', end=' ')
				tfd.height = int(data_value)
			elif data_name == 'bat':
				# dbg print('bat 설정', end=' ')
				tfd.battery = int(data_value)
			elif data_name == 'baro':
				# dbg print('baro 설정', end=' ')
				tfd.baro = float(data_value)
			elif data_name == 'time':
				# dbg print('time 설정', end=' ')
				tfd.time = int(data_value)
			elif data_name == 'agx':
				# dbg print('agx 설정', end=' ')
				tfd.acc_x = float(data_value)
			elif data_name == 'agy':
				# dbg print('agy 설정', end=' ')
				tfd.acc_y = float(data_value)
			elif data_name == 'agz':
				# dbg print('agz 설정', end=' ')
				tfd.acc_z = float(data_value)

		# dbg print('')
		return tfd

	def _tfd_receive_thread_(self):
		while True:
			try:
				response, addr = self.tfd_sock.recvfrom(1024)
				response = response.decode() # Bytes를 str로 변환
				#print("\ndata addr : ", addr, response)
				tfd_data = self.tfd_parse_data(response)
				self.tfd_receive_thread_lock.acquire() # 내부 리스트 접근 쓰레드 Lock
				self.tfd_receive_data_handler(addr, tfd_data) # 데이터 처리 추상 메소드 실행
				self.tfd_receive_thread_lock.release()

			except socket.error as exc:
				print ("Caught exception socket.error : %s" % exc)
				if self.tfd_receive_thread_lock.locked():
					self.tfd_receive_thread_lock.release()

			except Exception as e:
				if self.tfd_receive_thread_lock.locked():
					self.tfd_receive_thread_lock.release()

#######################################################################################
#
# 텔로 비디오 모듈 클래스
#
#######################################################################################
# 추상 클래스로 생성
class TelloVideoModule():
	video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 소켓 생성
	video_stream_thread_lock = threading.Lock()
	decoder = h264decoder.H264Decoder() # 카메라 데이터를 변환하는 디코더 생성

	__frame = None

	def init_video_socket(self):
		self.video_sock.bind(('0.0.0.0', TELLO_VIDEO_PORT))
		#print("카메라 스트리밍 소켓 초기화")

		self.video_stream_thread = threading.Thread(target=self._video_stream_thread_)
		self.video_stream_thread.setDaemon(True)
		self.video_stream_thread.start()
		#print("카메라 스트리밍 쓰레드 실행")

	def _h264_decode(self, packet_data):
		"""
		decode raw h264 format data from Tello
		
		:param packet_data: raw h264 data array
		
		:return: a list of decoded frame
		"""
		res_frame_list = []
		frames = self.decoder.decode(packet_data)
		for framedata in frames:
			(frame, w, h, ls) = framedata
			if frame is not None:
				# print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

				frame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
				frame = frame.reshape((h, ls // 3, 3))
				frame = frame[:, :w, :]
				res_frame_list.append(frame)

		return res_frame_list

	def get_frame(self):
		cv2_frame = None
		self.video_stream_thread_lock.acquire() # 쓰레드 Lock
		if self.__frame is not None:
			cv2_frame = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2BGR)
		self.video_stream_thread_lock.release()
		return cv2_frame

	def loop(self):		
		while True:
			if self.__frame is not None:
				frame = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2BGR)
				cv2.imshow('screen01', frame)

			key = cv2.waitKey(1)

	def _video_stream_thread_(self):
		packet_data = b""
		while True:
			try:
				res_string, addr = self.video_sock.recvfrom(2048)
				#print(res_string, addr)
				packet_data += res_string

				# end of frame
				if len(res_string) != 1460:
					for frame in self._h264_decode(packet_data):
						self.video_stream_thread_lock.acquire() # 쓰레드 Lock
						#cv2_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
						self.__frame = frame
						self.video_stream_thread_lock.release()
						if self.__frame is None or self.__frame.size == 0:
							continue

					packet_data = b""

			except socket.error as exc:
				print ("Caught exception socket.error : %s" % exc)
				if self.video_stream_thread_lock.locked():
					self.video_stream_thread_lock.release()

			except Exception as e:
				print ("_video_stream_thread_.error : %s" % e)
				if self.video_stream_thread_lock.locked():
					self.video_stream_thread_lock.release()


'''
하나의 소켓에서 여러 대의 텔로 데이터를 수신해야하기 떄문에
Control Tower를 하나 둔다.
'''
class TelloControlTower(TelloComModule, TelloFlightDataReceiver):
	traffic_list = [] # 트래픽 목록 생성
	tello_ip_list = [] # 한 네트워크에 tello가 존재하는 IP 리스트. 자동으로 채워지진 않고, searchTrafficInNetwork를 실행해야 한다.

	def __init__(self):
		try:
			#print("#######################################__INIT__#######################################")
			self.flight_data_check_time = 0 # 비행 정보 수신 상태를 표시해주는 주기
			self.video_frame = None

			self.traffic_list = []
			self.tello_ip_list = []

			self.init_socket()

			self.lock = threading.Lock()
		except Exception as e:	
			print("객체 초기화 중 에러!!\n__name__ :" + str(__name__) + "\nException :" + str(e))

	# TelloComModule에 대한 추상 메소드 구현
	def receive_data_handler(self, addr, data):
		# print("\nresponse addr : ", addr, data)
	
		if data == 'ok' and not(addr[0] in self.tello_ip_list):
			self.tello_ip_list.append(addr[0])
			print('Found new drone device')

		traffic = self.searchTrafficByIP(addr[0])

		if traffic is not None: #만약 목록에 해당 IP의 Traffic이 등록되어 있을 때
			traffic.append_queue(data)

	def tfd_receive_data_handler(self, addr, data):
		traffic = self.searchTrafficByIP(addr[0])

		if traffic is not None: #만약 목록에 해당 IP의 Traffic이 등록되어 있을 때
			traffic.flight_data = data

	def appendTraffic(self, traffic):
		try:
			traffic.registerSock(self.sock) # Tower의 socket 등록
			self.traffic_list.append(traffic) #Tower에서 관리하는 기체 등록

		except Exception as e:
			print("올바르지 않은 인자 값이 입력되었습니다.", e)

	def deleteTraffic(self, traffic):
		idx = self.searchTraffic(traffic)
		if idx >= 0:
			self.traffic_list.remove(idx)

	# 모든 트래픽에 데이터 전송
	def sendDataAllTraffic(self, cmd):
		for t in self.traffic_list:
			self.sock.sendto(cmd.encode('utf-8'), t.ip)

	# 트래픽 목록에서 트래픽 검색
	# -1 : 목록에 해당 트래픽 없음
	# 0 이상 : 해당 Index
	def searchTraffic(self, traffic):
		ret = -1
		try:
			ret = self.traffic_list.index(traffic)
		except ValueError as ve:
			print("ValueError", ve)
		except Exception as e:
			print("Exception", e)
            
		return ret

	def searchTrafficByIP(self, ip):
		for t in self.traffic_list:
			# print("searchTrafficByIP :",t.mAddr[0], ip)
			if t.mAddr[0] == ip:
				return t

		return None

	def start_to_receive_flight_data(self):
		self.tfd_init_socket()

	def checkAllTrafficIsConnected(self):
		ret = True
		for t in self.traffic_list:
			if not t.is_connected():
				ret = False

		return ret
	
	def waitAllCommandProcessed(self, timeout = 30, response = RESP_OK):
		ret = False
		response_check_list = [False] * len(self.traffic_list)
		timeout_time = time.time()
		while True:
			all_checked = True # 모든 트래픽의 명령이 처리되었는지 확인하는 변수
			for i in range(len(self.traffic_list)):
				if self.traffic_list[i].get_response_check() == response:
					response_check_list[i] = True
				
				# 응댑 대기 상태가 아닌 것은 넘어가야 함
				# 하나라도 응답 체크가 안되었으면 all_checked는 False
				if self.traffic_list[i].is_wait_response and not response_check_list[i]:
					all_checked = False

			if all_checked:
				ret = True
				break
			if time.time() - timeout_time >= timeout:
				break

		return ret
	
	def searchTrafficInNetwork(self, base_ip = '192.168.20.', start_addr = 2, end_addr = 254):
		self.tello_ip_list.clear()
		for i in range(start_addr, (end_addr - start_addr) + 1):
			#command = input('Input the command : ')
			command = "command"
			ip = base_ip + str(i)
			tello_address = (ip, 8889)
			self.sock.sendto(command.encode('utf-8'), tello_address)
			time.sleep(0.01)
		time.sleep(1)


# 군집드론으로 사용하기 위한 클래스
class TelloTraffic():
	ip = '127.0.0.1'
	mAddr = (ip, TELLO_CMD_PORT)
	is_wait_response = False # 현재 응답을 기다리는 상태일 때 True
	response_timeout = time.time() # 응답 대기 시간 체크 변수
	response_cmd = None # 대기하는 응답 커맨드
	sended_cmd = None # 전송한 커맨드
	retry_count = 0 # 재전송 카운트

	sock = None

	data_queue = [] # 수신된 데이터의 큐

	force_quit_wait_response = False

	is_connected_to_device = False

	flight_data = TelloFlightData()

	global_wait_flag = True

	def __init__(self, ip, dummy_traffic = False):
		try:
			#print("#######################################__INIT__#######################################")
		
			self.ip = ip
			self.mAddr = (self.ip, TELLO_CMD_PORT)

			self.flight_data_check_time = 0 # 비행 정보 수신 상태를 표시해주는 주기
			self.video_frame = None

			self.data_queue = [] # 수신된 데이터의 큐

			self.last_send_command_time = time.time()
			
			self.is_dummy_traffic = dummy_traffic

			if dummy_traffic:
				self.connected_to_device() # 더미 트래픽이면 일단 연결된 상태로 둔다.
			else:
				self.lock = threading.Lock()
				self.send_command_lock = threading.Lock()
				self.process_thread = threading.Thread(target=self.__process_thread)
				self.process_thread.setDaemon(True)
				self.process_thread.start()
		except Exception as e:	
			print("객체 초기화 중 에러!!\n__name__ :" + str(__name__) + "\nException :" + str(e))

	def __process_thread(self):
		while self.sock is None:
			time.sleep(1)

		while True:
			try:
				if not self.is_connected():
					if self.send_command("command", timeout=0.5) == RESP_OK:
						self.send_command("sdk?", None)
						self.send_command("sn?", None)
						self.send_command("battery?", None)
						self.connected_to_device()
				else:
					if (time.time() - self.last_send_command_time >= 10) and (not self.is_wait_response):
						ret = self.send_command("command", timeout=0.5)
						if ret == RESP_OK:
							#self.connected_to_device()
							pass
						elif ret == RESP_TIMEOUT:
							self.disconnected_to_device()
					
				time.sleep(1)
			except Exception as e:
				print(e)

	def registerSock(self, sock):
		self.sock = sock

	def setWaitFlag(self, flag):
		self.global_wait_flag = flag

	# 연결상태를 연결 끊김으로 변경한다.
	def disconnected_to_device(self):
		self.is_connected_to_device = False

	# 연결상태를 연결됨으로 변경한다.
	def connected_to_device(self):
		self.is_connected_to_device = True

	def is_connected(self):
		return self.is_connected_to_device

	def append_queue(self, data):
		self.lock.acquire()
		# print("큐 추가", self.ip, data)
		self.data_queue.append(data)
		if len(self.data_queue) >= 0xFF: #만약 큐의 크기가 너무 클 경우 큐를 초기화
			self.data_queue.clear()
		self.lock.release()

	def get_queue_size(self):
		self.lock.acquire()
		ret = len(self.data_queue)
		self.lock.release()
		return ret

	# Queue 데이터 POP
	# 데이터가 없을 때 None
	def pop_queue(self):
		ret = None
		self.lock.acquire()
		if len(self.data_queue) > 0:
			ret = self.data_queue.pop(0)
		self.lock.release()

		return ret

	def clear_queue(self):
		self.lock.acquire()
		self.data_queue.clear()
		self.lock.release()

	# global_wait_flag를 False로 해놓고 직접 응답을 확인할 때 사용한다.
	def start_response_check(self):
		if self.is_wait_response:
			print("먼저 대기중인 명령이 있음")
		self.is_wait_response = True
		self.clear_queue()
		self.response_timeout = time.time()
		self.response_cmd = None
		
	# global_wait_flag를 False로 해놓고 직접 응답을 확인할 때 사용한다.
	def get_response_check(self, response = RESPONSE_OK):
		ret = RESP_NONE
		if self.is_dummy_traffic:
			return RESP_OK

		if self.response_cmd is None or self.response_cmd != response:
			self.response_cmd = self.pop_queue()

		try:
			if self.response_cmd is not None: # 만약 데이터가 수신되었을 때
				if RESPONSE_ERROR in self.response_cmd:
					print("응답 에러 :", self.response_cmd)
					ret = RESP_ERROR

				elif RESPONSE_UNKNOWN_COMMAND in self.response_cmd:
					print("알 수 없는 명령")
					ret = RESP_UNKNOWN

				elif response in self.response_cmd: # 대기하려는 응답데이터일 때
					# print("응답 수신")
					ret = RESP_OK

				else:
					print("정의되지 않은 응답 :", self.response_cmd)
					ret = RESP_ERROR

				self.stop_response_check() # 응답이 들어왔으면 response_check를 정지한다.
				# 응답 확인해서 다시 요청하던가 해야 함
		except Exception as e:
			print("응답 체크 예외 상황 확인. 응답 CMD :", self.response_cmd, "\nException :", e)

		return ret
	
	# global_wait_flag를 False로 해놓고 직접 응답을 확인할 때 사용한다.
	def stop_response_check(self):
		self.is_wait_response = False
		self.clear_queue()

	# 명령어 전송
	# 만약 response가 None일 때 응답 대기 없이 명령어만 전송
	# 만약 response에 문자열 입력 시 해당 커맨드가 들어올 때 까지 대기, 명령 재전송
	def send_command(self, cmd, response = RESPONSE_OK, timeout = 1, max_retry = 3):
		ret = RESP_NONE
		if self.is_dummy_traffic:
			return RESP_OK
		
		if self.sock is not None:
			self.sended_cmd = cmd
			self.send_command_lock.acquire()
			self.force_quit_wait_response = False
			
			if not self.is_wait_response: #만약 응답 대기중이 아닐 때 응답 데이터 큐 클리어
				self.clear_queue()
			
			if _WOW_TELLO_DEBUG_ENABLE:
				print(self.ip, "에서 명령어 전송", cmd)
			self.last_send_command_time = time.time()
			self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

			if response is not None and self.global_wait_flag: # 만약 응답을 받아야 할 때
				self.is_wait_response = True
				self.response_timeout = time.time()
				while not self.force_quit_wait_response:
					data = self.pop_queue()
					if data is not None: # 만약 데이터가 수신되었을 때
						if RESPONSE_ERROR in data:
							print("응답 에러 :", data)
							ret = RESP_ERROR
							break

						elif RESPONSE_UNKNOWN_COMMAND in data:
							print("알 수 없는 명령")
							ret = RESP_UNKNOWN
							break

						elif response in data: # 대기하려는 응답데이터일 때
							# print("응답 수신")
							ret = RESP_OK
							break

						else:
							print("정의되지 않은 응답 :", data)
							ret = RESP_ERROR
							break

					if time.time() - self.response_timeout >= timeout:
						self.response_timeout = time.time()
						self.retry_count += 1
						if self.retry_count > max_retry: # 재요청 횟수가 3회 초과일 때
							self.retry_count = 0
							# print("응답 시간 초과")
							ret = RESP_TIMEOUT
							break
						self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

					time.sleep(0.05) # 50ms마다 체크

				self.is_wait_response = False

			elif not self.global_wait_flag: # global_wait_flag가 false일 경우 직접 응답 체크위해 관련 변수를 초기화 시킨다.
				self.start_response_check()

			self.send_command_lock.release()

		else:
			print("소켓이 등록되어 있지 않아, 명령을 전송할 수 없습니다.")

		return ret

	# 강제 명령어 전송
	# 비상정지, 정지 등 응답 필요 없이 다른 블록 수행보다 우선되어야 하는 경우
	# 타 블록 응답과 무관하게 명령을 전송한다.
	def force_send_command(self, cmd):
		if self.sock is not None:
			self.force_quit_wait_response = True
			self.is_wait_response = False
			self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

	def get_data(self, cmd, timeout = 1):
		self.send_command(cmd, None)
		timeout_time = time.time()
		while True:
			data = self.pop_queue()
			if data is not None:
				return data
			
			if time.time() - timeout_time >= timeout:
				break

			time.sleep(0.1)

		return None

	def takeoff(self):
		wprt('이륙')
		retry_count = 0
		while self.send_command('takeoff', timeout=10, max_retry=0) != RESP_OK:
			retry_count += 1
			if retry_count >= 3:
				wprt("이륙 실패")
				return
		
		wprt("이륙 성공")

	def land(self):
		wprt('착륙 시작')
		self.send_command('land', timeout=30, max_retry=0)
		wprt('착륙 완료')

	def emergency(self):
		wprt('비상정지')
		self.force_send_command('emergency')

	def up(self, x):
		wprt('%s 만큼 상승' % x)
		self.send_command('up %s' % x, timeout=30, max_retry=0)
		
	def down(self, x):
		wprt('%s 만큼 하강' % x)
		self.send_command('down %s' % x, timeout=30, max_retry=0)
		
	def left(self, x):
		wprt('%s 만큼 왼쪽으로 이동' % x)
		self.send_command('left %s' % x, timeout=30, max_retry=0)
		
	def right(self, x):
		wprt('%s 만큼 오른쪽으로 이동' % x)
		self.send_command('right %s' % x, timeout=30, max_retry=0)
		
	def forward(self, x):
		wprt('%s 만큼 전진' % x)
		self.send_command('forward %s' % x, timeout=30, max_retry=0)
		
	def back(self, x):
		wprt('%s 만큼 후진' % x)
		self.send_command('back %s' % x, timeout=30, max_retry=0)
		
	def cw(self, x):
		wprt('%s 만큼 시계방향 회전' % x)
		self.send_command('cw %s' % x, timeout=30, max_retry=0)
		
	def ccw(self, x):
		wprt('%s 만큼 반시계방향 회전' % x)
		self.send_command('ccw %s' % x, timeout=30, max_retry=0)
		
	def flip(self, x):
		wprt('FLIP! %s' % x)
		self.send_command('flip %s' % x, timeout=30, max_retry=0)
		
	def stop(self):
		wprt('정지')
		self.force_send_command('stop')

	def go(self, x, y, z, speed):
		wprt('%s %s %s %s 만큼 이동' % (x, y, z, speed))
		self.send_command('go %s %s %s %s' % (x, y, z, speed), timeout=30, max_retry=0)
		
	def curve(self, x1, y1, z1, x2, y2, z2, speed):
		wprt('%s %s %s %s %s %s %s 만큼 커브' % (x1, y1, z1, x2, y2, z2, speed))
		self.send_command(
			'curve %s %s %s %s %s %s %s' % (x1, y1, z1, x2, y2, z2, speed),
			timeout=30, max_retry=0)

	def go_to_mid(self, x, y, z, speed, mid):
		wprt('미션패드 %s번을 기준으로 %s %s %s %s 위치로 이동' % (mid, x, y, z, speed))
		self.send_command('go %s %s %s %s m%s' % (x, y, z, speed, mid), timeout=30, max_retry=0)
		
	def curve_to_mid(self, x1, y1, z1, x2, y2, z2, speed, mid):
		wprt('%s %s %s %s %s %s %s 만큼 커브하며 미션패드 %s 감지' % (x1, y1, z1, x2, y2, z2, speed, mid))
		self.send_command(
			'curve %s %s %s %s %s %s %s m%s' % (x1, y1, z1, x2, y2, z2, speed, mid),
			timeout=30, max_retry=0)

	def jump(self, x, y, z, speed, yaw, mid1, mid2):
		wprt('mid %s 기준으로 %s, %s, %s 위치에 %s 속도로 이동하며 mid %s 감지 후 %s 만큼 회전' % (mid1, x, y, z, speed, mid2, yaw))
		self.send_command(
			'jump %s %s %s %s %s m%s m%s' % (x, y, z, speed, yaw, mid1, mid2),
			timeout=30, max_retry=0)

	def speed(self, x):
		wprt('%s 으로 속도 설정' % x)
		self.send_command('speed %s' % x, timeout=1, max_retry=3)
		
	# Roll, Pitch, Throttle, Yaw 제어
	def rc(self, r, p, t, y):
		self.send_command('rc %s %s %s %s' % (r, p, t, y), response=None, timeout=0.05, max_retry=0)

	def mission_pad_on(self):
		wprt('미션패드 인식 활성화')
		self.send_command("mon")

	def mission_pad_off(self):
		wprt('미션패드 인식 비활성화')
		self.send_command("moff")

	def mission_pad_direction(self, x):
		if x == 0:
			wprt('하단 미션패드 인식 모드')
		elif x == 1:
			wprt('전방 미션패드 인식 모드')
		elif x == 2:
			wprt('하단, 전방 두 방향 미션패드 인식 모드')

		self.send_command("mdirection %s" % x)

	def stream_on(self):
		wprt("카메라 스트리밍 활성화")
		self.send_command("streamon")

	def stream_off(self):
		wprt("카메라 스트리밍 비활성화")
		self.send_command("streamoff")

	def get_battery(self):
		result = self.get_data('battery?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result
	
	# 외부 LED 제어 함수
	# @param r : 0-255
	# @param g : 0-255
	# @param b : 0-255
	def ext_led(self, r, g, b):
		r = constrain(r, 0, 255)
		g = constrain(g, 0, 255)
		b = constrain(b, 0, 255)
		wprt("외부 LED 제어 => %d,%d,%d" % (r, g, b))
		self.send_command(
			'EXT led %d %d %d' % (r, g, b),
			timeout=30, max_retry=0)

	# 외부 LED Fade 제어 함수
	# 설정한 색으로 LED가 천천히 밝기가 변한다.(Fading)
	# @param f : 밝기 변화 주파수 0.1 ~ 2.5Hz의 범위로 입력 가능하다.
	# @param r : 0-255
	# @param g : 0-255
	# @param b : 0-255
	def ext_led_fade(self, f, r, g, b):
		f = constrain(round(f, 1), 0.1, 2.5)
		r = constrain(r, 0, 255)
		g = constrain(g, 0, 255)
		b = constrain(b, 0, 255)
		wprt("외부 LED FADING 제어 => %f,%d,%d,%d" %(f, r, g, b))
		self.send_command(
			'EXT led br %d %d %d %d' % (f, r, g, b),
			timeout=30, max_retry=0)

	# 외부 LED Blink 제어 함수
	# 설정한 두 색으로 LED가 깜빡인다
	# @param f : 깜박일 주파수 0.1 ~ 10Hz의 범위로 입력 가능하다.
	# @param r1 : 0-255
	# @param g1 : 0-255
	# @param b1 : 0-255
	# @param r2 : 0-255
	# @param g2 : 0-255
	# @param b2 : 0-255
	def ext_led_blink(self, f, r1, g1, b1, r2, g2, b2):
		f = constrain(round(f, 1), 0.1, 10)
		r1 = constrain(r1, 0, 255)
		g1 = constrain(g1, 0, 255)
		b1 = constrain(b1, 0, 255)
		r2 = constrain(r2, 0, 255)
		g2 = constrain(g2, 0, 255)
		b2 = constrain(b2, 0, 255)
		wprt("외부 LED Blink 제어 => %f,%d,%d,%d,%d,%d,%d" % (f,r1,g1,b1,r2,g2,b2))
		self.send_command(
			'EXT led br %d %d %d %d' % (f, r1, g1, b1, r2, g2, b2),
			timeout=30, max_retry=0)

	# Dot-matrix Display를 제어하는 함수
	# 픽셀이 입력되며, 1차원 리스트가 들어간다.
	# 8x8 Display이므로, 64길이 이하의 리스트가 입력된다.
	# 
	# @param pixels : 길이 64 이하의 1차원 리스트
	# 데이터 순서대로 왼쪽->오른쪽, 위->아래 순서로 정렬된다.
	# 리스트에는 0~3까지의 숫자가 입력된다.
	# 0 : 꺼짐
	# 1 : Red
	# 2 : Blue
	# 3 : Purple
	def ext_mled(self, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled g %s' % (pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# Dot-matrix Display를 제어하는 함수
	# 문자열을 출력한다.
	# @param direction 문자열이 흐르는 방향
	# 0 : 왼쪽
	# 1 : 오른쪽
	# 2 : 위쪽
	# 3 : 아래쪽
	# @param color 문자열 색상
	# 0 : Red
	# 1 : Blue
	# 2 : Purple
	# @param f 문자열 흐르는 속도(frame rate / 0.1~2.5Hz)
	# @param string 출력할 문자열 길이. 70자 제한이다.
	def ext_mled_display_string(self, direction, color, f, string):
		string = string[:70]
		
		if(direction == 0):
			movement_dir = 'l'
		elif(direction == 1):
			movement_dir = 'r'
		elif(direction == 2):
			movement_dir = 'u'
		elif(direction == 3):
			movement_dir = 'd'
		else:
			movement_dir = 'l'

		if(color == 0):
			color_code = 'r'
		elif(color == 1):
			color_code = 'b'
		elif(color == 2):
			color_code = 'p'
		else:
			color_code = 'r'
		
		f = constrain(round(f, 1), 0.1, 2.5)

		wprt("외부 Dot-matrix Display 문자열 출력 => %s" % (string))
		self.send_command(
			'EXT mled %s %s %f %s' % (movement_dir, color_code, f, string),
			timeout=30, max_retry=0)

	# 이미지를 흐르게 출력한다
	def ext_mled_image(self, direction, f, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		if(direction == 0):
			movement_dir = 'l'
		elif(direction == 1):
			movement_dir = 'r'
		elif(direction == 2):
			movement_dir = 'u'
		elif(direction == 3):
			movement_dir = 'd'
		else:
			movement_dir = 'l'

		f = constrain(round(f, 1), 0.1, 2.5)

		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled %s g %f %s' % (movement_dir, f, pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# Dot-matrix Display를 제어하는 함수
	# ASCII 한 글자를 받거나, heart를 입력받아 프리셋을 출력한다.
	def ext_mled_static_ascii(self, color, data):
		if(color == 0):
			color_code = 'r'
		elif(color == 1):
			color_code = 'b'
		elif(color == 2):
			color_code = 'p'
		else:
			color_code = 'r'
		
		wprt("외부 Dot-matrix Display Static ascii or preset => %s" % (data))
		self.send_command(
			'EXT mled s %s %s' % (color_code, data),
			timeout=30, max_retry=0)

	# 부팅 이미지를 설정한다.
	def ext_mled_set_boot_image(self, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled sg %s' % (pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# 부팅시 출력되는 이미지를 제거한다.
	def ext_mled_clear_boot_image(self):
		wprt("외부 Dot-matrix Display 부팅 시 출력 이미지 삭제")
		self.send_command(
			'EXT mled sc',
			timeout=30, max_retry=0)

	# 부팅시 출력되는 이미지를 제거한다.
	def ext_mled_set_brightness(self, brightness):
		brightness = constrain(brightness, 0, 255)
		wprt("외부 Dot-matrix Display 밝기 설정")
		self.send_command(
			'EXT mled sl %d' % (brightness),
			timeout=30, max_retry=0)

	# 외부 모듈의 TOF센서 읽기
	def ext_get_tof(self):
		result = self.get_data('EXT tof?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result

	# 외부 모듈의 버전 정보 읽기
	def ext_get_version(self):
		result = self.get_data('EXT version?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result

# 단일 드론을 사용하기 위한 클래스
class Tello(TelloComModule, TelloFlightDataReceiver):
	__version__ = __WOW_TELLO_DRONE_VERSION__
	mAddr = ('127.0.0.1', TELLO_CMD_PORT)
	is_wait_response = False # 현재 응답을 기다리는 상태일 때 True
	response_timeout = time.time() # 응답 대기 시간 체크 변수
	response_cmd = None # 대기하는 응답 커맨드
	sended_cmd = None # 전송한 커맨드
	retry_count = 0 # 재전송 카운트

	data_queue = [] # 수신된 데이터의 큐

	force_quit_wait_response = False

	is_connected_to_device = False

	flight_data = TelloFlightData()
	video_module = TelloVideoModule()

	def __init__(self, ip):
		try:
			#print("#######################################__INIT__#######################################")
			self.mAddr = (ip, TELLO_CMD_PORT)

			self.flight_data_check_time = 0 # 비행 정보 수신 상태를 표시해주는 주기
			self.video_frame = None

			self.init_socket()

			self.lock = threading.Lock()
			self.send_command_lock = threading.Lock()
			self.process_thread = threading.Thread(target=self.__process_thread)
			self.process_thread.setDaemon(True)
			self.process_thread.start()
		except Exception as e:	
			print("객체 초기화 중 에러!!\n__name__ :" + str(__name__) + "\nException :" + str(e))

	def __process_thread(self):
		keep_connect_time = 0
		while True:
			try:
				if not self.is_connected():
					if self.send_command("command", timeout=0.5) == RESP_OK:
						self.send_command("sdk?", None)
						self.send_command("sn?", None)
						self.send_command("battery?", None)
						self.connected_to_device()
				else:
					if (time.time() - keep_connect_time >= 10) and (not self.is_wait_response):
						keep_connect_time = time.time()
						ret = self.send_command("command", timeout=0.5)
						if ret == RESP_OK:
							#self.connected_to_device()
							pass
						elif ret == RESP_TIMEOUT:
							self.disconnected_to_device()
					
				time.sleep(1)
			except Exception as e:
				print(e)

	def receive_data_handler(self, addr, data):
		#print("\nresponse addr : ", addr, data)
		if self.mAddr == addr:
			self.append_queue(data)

	def tfd_receive_data_handler(self, addr, data):
		if self.mAddr[0] == addr[0]:
			self.flight_data = data
			if time.time() - self.flight_data_check_time >= 5:
				self.flight_data_check_time = time.time()
				#print("데이터 수신 상태 : 정상")

	# 연결상태를 연결 끊김으로 변경한다.
	def disconnected_to_device(self):
		self.is_connected_to_device = False

	# 연결상태를 연결됨으로 변경한다.
	def connected_to_device(self):
		self.is_connected_to_device = True

	def is_connected(self):
		return self.is_connected_to_device

	def append_queue(self, data):
		self.lock.acquire()
		self.data_queue.append(data)
		if len(self.data_queue) >= 0xFF: #만약 큐의 크기가 너무 클 경우 큐를 초기화
			self.data_queue.clear()
		self.lock.release()

	def get_queue_size(self):
		self.lock.acquire()
		ret = len(self.data_queue)
		self.lock.release()
		return ret

	# Queue 데이터 POP
	# 데이터가 없을 때 None
	def pop_queue(self):
		ret = None
		self.lock.acquire()
		if len(self.data_queue) > 0:
			ret = self.data_queue.pop(0)
		self.lock.release()

		return ret

	def clear_queue(self):
		self.lock.acquire()
		self.data_queue.clear()
		self.lock.release()

	def start_to_receive_flight_data(self):
		self.tfd_init_socket()

	def start_to_video_stream(self):
		self.video_module.init_video_socket()

	def get_frame(self):
		return self.video_module.get_frame()

	def open_video_display(self):
		self.show_video_enable = True

	def close_video_display(self):
		self.show_video_enable = False
		cv2.destroyAllWindows()

	# 명령어 전송
	# 만약 response가 None일 때 응답 대기 없이 명령어만 전송
	# 만약 response에 문자열 입력 시 해당 커맨드가 들어올 때 까지 대기, 명령 재전송
	def send_command(self, cmd, response = RESPONSE_OK, timeout = 1, max_retry = 3):
		ret = RESP_NONE
		if self.sock is not None:
			self.sended_cmd = cmd
			self.send_command_lock.acquire()
			self.force_quit_wait_response = False
			
			if not self.is_wait_response: #만약 응답 대기중이 아닐 때 응답 데이터 큐 클리어
				self.clear_queue()

			if _WOW_TELLO_DEBUG_ENABLE:
				print("명령어 전송", cmd)
			self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

			if response is not None: # 만약 응답을 받아야 할 때
				self.is_wait_response = True
				self.response_timeout = time.time()
				while not self.force_quit_wait_response:
					data = self.pop_queue()
					if data is not None: # 만약 데이터가 수신되었을 때
						if RESPONSE_ERROR in data:
							print("응답 에러 :", data)
							ret = RESP_ERROR
							break

						elif RESPONSE_UNKNOWN_COMMAND in data:
							print("알 수 없는 명령")
							ret = RESP_UNKNOWN
							break

						elif response in data: # 대기하려는 응답데이터일 때
							# print("응답 수신")
							ret = RESP_OK
							break

						else:
							print("정의되지 않은 응답 :", data)
							ret = RESP_ERROR
							break

					if time.time() - self.response_timeout >= timeout:
						self.response_timeout = time.time()
						self.retry_count += 1
						if self.retry_count > max_retry: # 재요청 횟수가 3회 초과일 때
							self.retry_count = 0
							# print("응답 시간 초과")
							ret = RESP_TIMEOUT
							break
						self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

					time.sleep(0.05) # 50ms마다 체크

				self.is_wait_response = False

			self.send_command_lock.release()

		else:
			print("소켓이 등록되어 있지 않아, 명령을 전송할 수 없습니다.")

		return ret

	# 강제 명령어 전송
	# 비상정지, 정지 등 응답 필요 없이 다른 블록 수행보다 우선되어야 하는 경우
	# 타 블록 응답과 무관하게 명령을 전송한다.
	def force_send_command(self, cmd):
		if self.sock is not None:
			self.force_quit_wait_response = True
			self.is_wait_response = False
			self.sock.sendto(cmd.encode('utf-8'), self.mAddr)

	def get_data(self, cmd, timeout = 1):
		self.send_command(cmd, None)
		timeout_time = time.time()
		while True:
			data = self.pop_queue()
			if data is not None:
				return data
			
			if time.time() - timeout_time >= timeout:
				break

			time.sleep(0.1)

		return None

	def takeoff(self):
		wprt('이륙')
		retry_count = 0
		while self.send_command('takeoff', timeout=10, max_retry=0) != RESP_OK:
			retry_count += 1
			if retry_count >= 3:
				wprt("이륙 실패")
				return
		
		wprt("이륙 성공")

	def land(self):
		wprt('착륙 시작')
		self.send_command('land', timeout=10, max_retry=0)
		wprt('착륙 완료')

	def emergency(self):
		wprt('비상정지')
		self.force_send_command('emergency')

	def up(self, x):
		wprt('%s 만큼 상승' % x)
		self.send_command('up %s' % x, timeout=30, max_retry=0)
		
	def down(self, x):
		wprt('%s 만큼 하강' % x)
		self.send_command('down %s' % x, timeout=30, max_retry=0)
		
	def left(self, x):
		wprt('%s 만큼 왼쪽으로 이동' % x)
		self.send_command('left %s' % x, timeout=30, max_retry=0)
		
	def right(self, x):
		wprt('%s 만큼 오른쪽으로 이동' % x)
		self.send_command('right %s' % x, timeout=30, max_retry=0)
		
	def forward(self, x):
		wprt('%s 만큼 전진' % x)
		self.send_command('forward %s' % x, timeout=30, max_retry=0)
		
	def back(self, x):
		wprt('%s 만큼 후진' % x)
		self.send_command('back %s' % x, timeout=30, max_retry=0)
		
	def cw(self, x):
		wprt('%s 만큼 시계방향 회전' % x)
		self.send_command('cw %s' % x, timeout=10, max_retry=0)
		
	def ccw(self, x):
		wprt('%s 만큼 반시계방향 회전' % x)
		self.send_command('ccw %s' % x, timeout=10, max_retry=0)
		
	def flip(self, x):
		wprt('FLIP! %s' % x)
		self.send_command('flip %s' % x, timeout=10, max_retry=0)
		
	def stop(self):
		wprt('정지')
		self.force_send_command('stop')

	def go(self, x, y, z, speed):
		wprt('%s %s %s %s 만큼 이동' % (x, y, z, speed))
		self.send_command('go %s %s %s %s' % (x, y, z, speed), timeout=30, max_retry=0)
		
	def curve(self, x1, y1, z1, x2, y2, z2, speed):
		wprt('%s %s %s %s %s %s %s 만큼 커브' % (x1, y1, z1, x2, y2, z2, speed))
		self.send_command(
			'curve %s %s %s %s %s %s %s' % (x1, y1, z1, x2, y2, z2, speed),
			timeout=30, max_retry=0)

	def go_to_mid(self, x, y, z, speed, mid):
		wprt('미션패드 %s번을 기준으로 %s %s %s %s 위치로 이동' % (mid, x, y, z, speed))
		self.send_command('go %s %s %s %s m%s' % (x, y, z, speed, mid), timeout=10, max_retry=0)
		
	def curve_to_mid(self, x1, y1, z1, x2, y2, z2, speed, mid):
		wprt('%s %s %s %s %s %s %s 만큼 커브하며 미션패드 %s 감지' % (x1, y1, z1, x2, y2, z2, speed, mid))
		self.send_command(
			'curve %s %s %s %s %s %s %s m%s' % (x1, y1, z1, x2, y2, z2, speed, mid),
			timeout=30, max_retry=0)

	def jump(self, x, y, z, speed, yaw, mid1, mid2):
		wprt('mid %s 기준으로 %s, %s, %s 위치에 %s 속도로 이동하며 mid %s 감지 후 %s 만큼 회전' % (mid1, x, y, z, speed, mid2, yaw))
		self.send_command(
			'jump %s %s %s %s %s m%s m%s' % (x, y, z, speed, yaw, mid1, mid2),
			timeout=30, max_retry=0)

	def speed(self, x):
		wprt('%s 으로 속도 설정' % x)
		self.send_command('speed %s' % x, timeout=1, max_retry=3)
		
	# Roll, Pitch, Throttle, Yaw 제어
	def rc(self, r, p, t, y):
		self.send_command('rc %s %s %s %s' % (r, p, t, y), timeout=0.05, max_retry=0)

	def mission_pad_on(self):
		wprt('미션패드 인식 활성화')
		self.send_command("mon")

	def mission_pad_off(self):
		wprt('미션패드 인식 비활성화')
		self.send_command("moff")

	def mission_pad_direction(self, x):
		if x == 0:
			wprt('하단 미션패드 인식 모드')
		elif x == 1:
			wprt('전방 미션패드 인식 모드')
		elif x == 2:
			wprt('하단, 전방 두 방향 미션패드 인식 모드')

		self.send_command("mdirection %s" % x)

	def stream_on(self):
		wprt("카메라 스트리밍 활성화")
		self.send_command("streamon")

	def stream_off(self):
		wprt("카메라 스트리밍 비활성화")
		self.send_command("streamoff")

	def get_battery(self):
		result = self.get_data('battery?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result

	# 외부 LED 제어 함수
	# @param r : 0-255
	# @param g : 0-255
	# @param b : 0-255
	def ext_led(self, r, g, b):
		r = constrain(r, 0, 255)
		g = constrain(g, 0, 255)
		b = constrain(b, 0, 255)
		wprt("외부 LED 제어 => %d,%d,%d" % (r, g, b))
		self.send_command(
			'EXT led %d %d %d' % (r, g, b),
			timeout=30, max_retry=0)

	# 외부 LED Fade 제어 함수
	# 설정한 색으로 LED가 천천히 밝기가 변한다.(Fading)
	# @param f : 밝기 변화 주파수 0.1 ~ 2.5Hz의 범위로 입력 가능하다.
	# @param r : 0-255
	# @param g : 0-255
	# @param b : 0-255
	def ext_led_fade(self, f, r, g, b):
		f = constrain(round(f, 1), 0.1, 2.5)
		r = constrain(r, 0, 255)
		g = constrain(g, 0, 255)
		b = constrain(b, 0, 255)
		wprt("외부 LED FADING 제어 => %f,%d,%d,%d" %(f, r, g, b))
		self.send_command(
			'EXT led br %d %d %d %d' % (f, r, g, b),
			timeout=30, max_retry=0)

	# 외부 LED Blink 제어 함수
	# 설정한 두 색으로 LED가 깜빡인다
	# @param f : 깜박일 주파수 0.1 ~ 10Hz의 범위로 입력 가능하다.
	# @param r1 : 0-255
	# @param g1 : 0-255
	# @param b1 : 0-255
	# @param r2 : 0-255
	# @param g2 : 0-255
	# @param b2 : 0-255
	def ext_led_blink(self, f, r1, g1, b1, r2, g2, b2):
		f = constrain(round(f, 1), 0.1, 10)
		r1 = constrain(r1, 0, 255)
		g1 = constrain(g1, 0, 255)
		b1 = constrain(b1, 0, 255)
		r2 = constrain(r2, 0, 255)
		g2 = constrain(g2, 0, 255)
		b2 = constrain(b2, 0, 255)
		wprt("외부 LED Blink 제어 => %f,%d,%d,%d,%d,%d,%d" % (f,r1,g1,b1,r2,g2,b2))
		self.send_command(
			'EXT led br %d %d %d %d' % (f, r1, g1, b1, r2, g2, b2),
			timeout=30, max_retry=0)

	# Dot-matrix Display를 제어하는 함수
	# 픽셀이 입력되며, 1차원 리스트가 들어간다.
	# 8x8 Display이므로, 64길이 이하의 리스트가 입력된다.
	# 
	# @param pixels : 길이 64 이하의 1차원 리스트
	# 데이터 순서대로 왼쪽->오른쪽, 위->아래 순서로 정렬된다.
	# 리스트에는 0~3까지의 숫자가 입력된다.
	# 0 : 꺼짐
	# 1 : Red
	# 2 : Blue
	# 3 : Purple
	def ext_mled(self, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled g %s' % (pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# Dot-matrix Display를 제어하는 함수
	# 문자열을 출력한다.
	# @param direction 문자열이 흐르는 방향
	# 0 : 왼쪽
	# 1 : 오른쪽
	# 2 : 위쪽
	# 3 : 아래쪽
	# @param color 문자열 색상
	# 0 : Red
	# 1 : Blue
	# 2 : Purple
	# @param f 문자열 흐르는 속도(frame rate / 0.1~2.5Hz)
	# @param string 출력할 문자열 길이. 70자 제한이다.
	def ext_mled_display_string(self, direction, color, f, string):
		string = string[:70]
		
		if(direction == 0):
			movement_dir = 'l'
		elif(direction == 1):
			movement_dir = 'r'
		elif(direction == 2):
			movement_dir = 'u'
		elif(direction == 3):
			movement_dir = 'd'
		else:
			movement_dir = 'l'

		if(color == 0):
			color_code = 'r'
		elif(color == 1):
			color_code = 'b'
		elif(color == 2):
			color_code = 'p'
		else:
			color_code = 'r'
		
		f = constrain(round(f, 1), 0.1, 2.5)

		wprt("외부 Dot-matrix Display 문자열 출력 => %s" % (string))
		self.send_command(
			'EXT mled %s %s %f %s' % (movement_dir, color_code, f, string),
			timeout=30, max_retry=0)

	# 이미지를 흐르게 출력한다
	def ext_mled_image(self, direction, f, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		if(direction == 0):
			movement_dir = 'l'
		elif(direction == 1):
			movement_dir = 'r'
		elif(direction == 2):
			movement_dir = 'u'
		elif(direction == 3):
			movement_dir = 'd'
		else:
			movement_dir = 'l'

		f = constrain(round(f, 1), 0.1, 2.5)

		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled %s g %f %s' % (movement_dir, f, pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# Dot-matrix Display를 제어하는 함수
	# ASCII 한 글자를 받거나, heart를 입력받아 프리셋을 출력한다.
	def ext_mled_static_ascii(self, color, data):
		if(color == 0):
			color_code = 'r'
		elif(color == 1):
			color_code = 'b'
		elif(color == 2):
			color_code = 'p'
		else:
			color_code = 'r'
		
		wprt("외부 Dot-matrix Display Static ascii or preset => %s" % (data))
		self.send_command(
			'EXT mled s %s %s' % (color_code, data),
			timeout=30, max_retry=0)

	# 부팅 이미지를 설정한다.
	def ext_mled_set_boot_image(self, pixels):
		if len(pixels) > 64: # 길이 체크
			return
		
		pixel_data = ''
		try:
			for pixel in pixels:
				if pixel == 1: # Red
					pixel_data += 'r'
				elif pixel == 2: # Blue
					pixel_data += 'b'
				elif pixel == 3: # Purple
					pixel_data += 'p'
				else:
					pixel_data += '0'
				
			wprt("외부 Dot-matrix Display 제어")
			for i in range(0, 8):
				if(len(pixel_data[i*8:]) >= 8):
					linestring = pixel_data[(i*8):8]
				else:
					linestring = pixel_data[(i*8):]
				wprt("%s", linestring)

			self.send_command(
				'EXT mled sg %s' % (pixel_data),
				timeout=30, max_retry=0)
		except Exception as e:
			pass

	# 부팅시 출력되는 이미지를 제거한다.
	def ext_mled_clear_boot_image(self):
		wprt("외부 Dot-matrix Display 부팅 시 출력 이미지 삭제")
		self.send_command(
			'EXT mled sc',
			timeout=30, max_retry=0)

	# 부팅시 출력되는 이미지를 제거한다.
	def ext_mled_set_brightness(self, brightness):
		brightness = constrain(brightness, 0, 255)
		wprt("외부 Dot-matrix Display 밝기 설정")
		self.send_command(
			'EXT mled sl %d' % (brightness),
			timeout=30, max_retry=0)

	# 외부 모듈의 TOF센서 읽기
	def ext_get_tof(self):
		result = self.get_data('EXT tof?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result

	# 외부 모듈의 버전 정보 읽기
	def ext_get_version(self):
		result = self.get_data('EXT version?')
		try:
			if result is not None:
				result = int(result)
			else:
				result = -1
		except:
			return -1
		return result
