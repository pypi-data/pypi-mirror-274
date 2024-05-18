from setuptools import setup

setup(
    name='RPICommLink',
    version='1.1.4',
    author='adixu',
    author_email='adixu7@gmail.com',
    description='A library for communication on Raspberry Pi',
    long_description="RPICommLink 是一个用于在不同设备之间建立通信连接的 Python 类。提供了一系列方法使设备能够通过 TCP/IP 协议进行数据交换。"
                     "灵活的通信设置可以轻松地在设备之间建立通信连接，无论是在局域网内部还是通过互联网。"
                     "具备完善的错误处理机制及时发现并处理连接中断、超时等异常情况，保证通信的稳定性和可靠性。"
                     "使用简单易用的接口可以方便地发送和接收数据，无需过多关注底层网络细节，让设备之间的通信变得更加简单和高效。"
                     "通过 RPICommLink 类，可以实现设备之间的数据交换，为项目提供强大的通信支持。"
                     "\n\n\n\n\n\n历代版本更新："
                     "\n\n\n\n\n\n1.0.2 -优化了函数的命名，发送模块不再进行死循环。"
                     "\n\n\n\n\n\n1.0.3 -修复了潜在bug，优化了获取IP的方式，现在可以不命名而使用默认设备名称了。添加了中文介绍。"
                     "\n\n\n\n\n\n1.0.4 -重新了上传中文介绍。"
                     "\n\n\n\n\n\n1.0.5 -修复了无法在无互联网下获取IP的报错，修复了无法同时连接两个服务器的bug。"
                     "\n\n\n\n\n\n1.0.6 -修复了潜在bug"
                     "\n\n\n\n\n\n1.0.7 -轻量化"
                     "\n\n\n\n\n\n1.1   -增加了传输摄像头帧的函数，需要自行下载opencv-python库。注意：该版本为测试版，将会有许多未发现的报错，建议在在服务器端发送摄像头帧而不是客户端。"
                     "\n\n\n\n\n\n1.1.1 -修复了几个bug。注意：该版本为测试版，将会有许多未发现的报错，建议在在服务器端发送摄像头帧而不是客户端。"
                     "\n\n\n\n\n\n1.1.2 -现在服务端与客户端都可以进行发送或接收了"
                     "\n\n\n\n\n\n1.1.3 -添加了装饰器的用法，使代码更加简介"
                     "\n\n\n\n\n\n1.1.4 -给图像接收添加了装饰器的用法；auto_frame现在可以选择不同的相机了",
    packages=['RPICommLink'],
    include_package_data=True,
    install_requires=[],
)
