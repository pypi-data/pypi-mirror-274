# from distutils.core import setup
# setup(形参1=值,形参2=值)
import sys

# 建议使用
from setuptools import setup


def readme():
      with open('README.rst', encoding="UTF-8") as f:
            return f.read()

setup(name="pkgtestlib", version="1.0.1", description="", packages=["pkgtestlib"]
      , py_modules=["Tool"]
      , author="bjlhx15", author_email="bjlhx15@163.com"
      , long_description=readme()
      # , install_requires=["requests>2.18"]
      , python_requires=">=3.5"
      , url="https://github.com/bjlhx15"
      , license="MIT")

