from setuptools import setup,find_packages

setup(name='pysvapi',
      version='0.2',
      description='Sandvine Python API',
      url='http://github.com/chris-sanichar/pysvapi',
      author='Sandvine',
      author_email='csanichar@sandvine.com',
      license='Apache2',
      packages=find_packages(),
      install_requires=[
          'pycurl',
          'scp',
          'paramiko',
      ],
      zip_safe=False)
