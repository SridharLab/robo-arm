#!/usr/bin/python
"""   
desc:  Setup script for 'robo_arm' package.
notes: Install with "python setup.py install".
"""
import platform, os, shutil, glob
from setuptools import setup, find_packages, Extension

PACKAGE_METADATA = {
    'name'         : 'robo_arm',
    'version'      : 'dev',
}
    
PACKAGE_SOURCE_DIR = 'src'
MAIN_PACKAGE_DIR   = 'robo_arm'
MAIN_PACKAGE_PATH  = os.path.abspath(os.sep.join((PACKAGE_SOURCE_DIR,MAIN_PACKAGE_DIR)))

#dependencies
INSTALL_REQUIRES = [
                    'numpy >= 1.1.0',
                    'matplotlib >= 0.98',
                    'pyserial',
                    ]

#scripts and plugins
ENTRY_POINTS =  { 'gui_scripts':     [
                                      #'neurodot_control = neurodot.apps.control.main:main',
                                     ],
                  'console_scripts': [
                                      #'neurodot_shell  = neurodot.scripts.shell:main',
                                     ],
                }

#ext_data_decoder = Extension('neurodot.ext_modules.data_decoder', sources=['src/neurodot/ext_modules/data_decoder.c'])

if __name__ == "__main__":
    #complete the setup using setuptools
    setup(package_dir      = {'':PACKAGE_SOURCE_DIR},
          packages         = find_packages(PACKAGE_SOURCE_DIR),
          entry_points     = ENTRY_POINTS,
          #ext_modules      = [ext_data_decoder],
          #non-code files
          #package_data     =   {'': ['*.so']},
          **PACKAGE_METADATA
         )
