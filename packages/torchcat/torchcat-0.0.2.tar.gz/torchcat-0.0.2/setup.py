from setuptools import setup

setup(
    name='torchcat',
    version='0.0.2',
    author='kaiyu',
    author_email='2971934557@qq.com',
    url='https://zhuanlan.zhihu.com/p/26159930',
    description='用于简化 torch 模型训练的工具',
    packages=['torchcat'],
    install_requires=['numpy', 'torchsummary'],
)

'''
python -m build

python -m twine upload --repository pypi dist/*
'''
