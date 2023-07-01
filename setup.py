from setuptools import setup

setup(name='clean_folder',
      version='1',
      description='Sort your messy folders',
      url='https://github.com/zhenyamisyuryow/clean_folder',
      author='Zhenyamisyuryow',
      author_email='johndoe@example.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts':['clean-folder = clean_folder.clean:main']})