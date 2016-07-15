import os
import re
import codecs
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    try:
        f = codecs.open(os.path.join(here, *file_paths), 'r', 'latin1')
        version_file = f.read()
        f.close()
    except:
        raise RuntimeError("Unable to find version string.")

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


try:
    f = codecs.open('README.md', encoding='utf-8')
    long_description = f.read()
    f.close()
except:
    long_description = ''


setup(
    name='netstat-cl',
    version=find_version('GitChat.py'),
    description='ChitChat on gitchat. Discuss your projects on gitchat, without even creating chatrooms.',
    long_description=long_description,
    keywords='Ubuntu, Internet speed',
    author='Shubhodeep Mukherjee',
    author_email='shubhodeep9@gmail.com',
    url='https://github.com/shubhodeep9/python-netstat',
    license='Apache License, Version 2.0',
    install_requires=["urwid","requests"],
    py_modules=["GitChat","login","ui"],
    entry_points={
        'console_scripts': [
            'gitchat=GitChat:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)