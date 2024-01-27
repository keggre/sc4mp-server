import glob
import os
import platform
import shutil
import struct
import sys
from datetime import datetime
from distutils.core import setup

import py2exe

import sc4mpserver

VERSION = sc4mpserver.SC4MP_VERSION

for item in os.listdir("dist"):
    item = os.path.join("dist", item)
    if (os.path.isfile(item)):
        os.remove(item)
    else:
        shutil.rmtree(item)

sys.argv.append('py2exe')

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

setup(
	console=[{
		"script": "sc4mpserver.py",
		"icon_resources": [(1, "resources/icon.ico")],
	}],
    zipfile=None,
	options={
		"py2exe": {
			"packages": [],
            "bundle_files": 1,
			"optimize": 2,
			"compressed": True,
            "excludes":[],
            "verbose": 4
		}
	},
	data_files=find_data_files('resources','resources',['*'])
)

print('Copying extra files to "dist"...')
shutil.copy("License.txt", "dist")
shutil.copy("Readme.html", "dist")

input("Press <Enter> to create a zip archive of the distribution...")
target = "dist"
destination = os.path.join(os.path.join("builds", "sc4mp-server-" + platform.system().lower() + "-" + str(8 * struct.calcsize("P")) + "-v" + VERSION + "." + datetime.now().strftime("%Y%m%d%H%M%S")))
print('Creating zip archive of "' + target + '" at "' + destination + '"')
shutil.make_archive(destination, "zip", target)