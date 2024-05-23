from setuptools import setup

setup(
    name='torchcat',
    version='0.0.1',
    author='kaiyu',
    author_email='2971934557@qq.com',
    url='https://zhuanlan.zhihu.com/p/26159930',
    description='用于简化 torch 模型训练的工具',
    packages=['torchcat'],
    install_requires=['numpy', 'torchsummary'],
    # entry_points={
    #     'console_scripts': [
    #         'cat=torchcat:cat',
    #     ]
    # }
)
