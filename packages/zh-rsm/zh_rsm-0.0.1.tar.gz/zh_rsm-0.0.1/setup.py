import os
import sys
import shutil
import re

path_list = ['build', 'dist', 'your_package/your_package.egg-info']
for path in path_list:
    if os.path.exists(path):
        shutil.rmtree(path)
        # os.unlink(path)
    else:
        print('no such file:%s' % path)


def main():
    from distutils.core import setup
    from setuptools import find_packages

    setup(name='zh_rsm',  # 包名
          version='0.0.1',  # 版本号
          description='',
          long_description=open('README.md').read(),
          author='yzh2002',
          author_email='2039143115@qq.com',
          url='',
          license='',
          install_requires=[],
          classifiers=[
              'Intended Audience :: Developers',
              'Programming Language :: Python :: 3.10',
          ],
          keywords='',
          packages=find_packages(),
          # 包数据，指定需要包含在包内的非 Python 文件
          package_data={},
          include_package_data=True,
          )


if __name__ == "__main__":
    main()
