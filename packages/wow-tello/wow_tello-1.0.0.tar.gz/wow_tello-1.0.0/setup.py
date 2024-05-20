from setuptools import setup, find_packages

setup(
    name='wow_tello',
    version='1.0.0', # 수정되면 꼭 version 업데이트하기
    description='Wow IoT Platform API libraries',
    author='wowsystem, nobu',
    author_email='contact@wowsystem.co.kr',
    url='https://github.com/WOWSYSTEM/',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['wowsystem', 'Drone', 'Tello', 'Tello Edu', 'Tello TT', 'DJI'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
