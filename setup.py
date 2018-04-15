from setuptools import setup

setup(name='evermutt',
      version='0.1',
      description='A ncurses based Evernote client',
      url='http://github.com/scootersmk/evermutt',
      author='Scott Koch',
      author_email='scottkoch@gmail.com',
      license='MIT',
      packages=['evermutt'],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Console :: Curses",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7",],
      zip_safe=False)
