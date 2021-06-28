import os
import sys
import inspect


'''
Aquest fitxer serveix per importar el directori pare
'''
path = os.path.abspath(inspect.getfile(inspect.currentframe()))
current_dir = os.path.dirname(path)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
