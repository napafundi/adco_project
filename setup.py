from distutils.core import setup
import py2exe
import os

setup(console=[os.path.join(os.path.dirname(__file__, 'inventory.py')])
