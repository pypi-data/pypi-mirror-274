from setuptools import setup, find_packages

setup(
    name='zfxtest',
    version='1.0.60',
    packages=find_packages(),
    # 不包含其他文件
    include_package_data=False,
    # 作者信息等
    author='zengfengxiang',
    author_email='424491679@qq.com',
    description='这是ZFX模块的测试版',
    # 项目主页
    url='',
    # 依赖列表
    install_requires=[
        'requests',
        'pyperclip',
        "pystray",
        "psutil",
        "selenium",
        "requests",
        "mysql.connector",
        "pyinstaller",
        "openpyxl",
        # 添加其他依赖库
    ],
)


