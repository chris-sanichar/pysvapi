from setuptools import setup,find_packages

setup(name='pysvapi',
      version='0.1',
      description='Sandvine Python API',
      url='http://github.com/mfmarche/pysvapi',
      author='Sandvine',
      author_email='mmarchetti@sandvine.com',
      license='Apache2',
      packages=find_packages(),
      install_requires=[
          'pycurl',
          'scp',
          'paramiko',
      ],
      zip_safe=False)
