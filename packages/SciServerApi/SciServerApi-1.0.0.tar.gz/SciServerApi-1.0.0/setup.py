from setuptools import setup, find_packages

setup(name='SciServerApi',  # 包名
      version='1.0.0',  # 版本号
      description='quick access to sciserver',
      long_description=open("README.md", "r").read(),
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
      )

# python3 setup.py sdist bdist_wheel 
# twine upload dist/*