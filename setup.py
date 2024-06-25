import os
import platform
import shutil
import struct
from datetime import datetime

import PyInstaller.__main__ as pyinstaller
from pyinstaller_versionfile import create_versionfile

import sc4mpserver


TITLE = "SC4MP Server"
NAME = "sc4mpserver.exe"
VERSION = sc4mpserver.SC4MP_VERSION
PUBLISHER = "SimCity 4 Multiplayer Project"
DESCRIPTION = "Multiplayer gameserver for SimCity 4"
LICENSE = "MIT-0"
DIST = "dist" + str(8 * struct.calcsize("P"))


def main():

	# Make distribution directory if it does not yet exist
	print(f"Preparing distribution directory at \"{DIST}\"")
	if not os.path.exists(DIST):
		os.makedirs(DIST)

	# Purge the distribution directory
	for item in os.listdir(DIST):
		item = os.path.join(DIST, item)
		if (os.path.isfile(item)):
			os.remove(item)
		else:
			shutil.rmtree(item)

	# Create version file
	print(f"Creating version file...")
	create_versionfile(
		output_file="version.rc",
		version=VERSION,
		company_name=PUBLISHER,
		file_description=DESCRIPTION,
		internal_name=TITLE,
		legal_copyright=LICENSE,
		original_filename=NAME,
		product_name=TITLE,
	)

	# Run setup
	print("Running setup...")
	pyinstaller.run([
		f"sc4mpserver.py",
		f"--specpath",
		f"{os.path.join('temp', 'spec')}",
        f"--distpath",
		f"{DIST}",
        f"--workpath",
		f"{os.path.join('temp', 'build')}",
        f"--onefile",
		f"--noupx",
        f"--console",
        f"-i",
		f"{os.path.abspath(os.path.join('resources', 'icon.ico'))}",
		f"--version-file",
		f"{os.path.abspath('version.rc')}"
	])

	# Copy extra files to distribution directory
	print(f'Copying extra files to "{DIST}"...')
	shutil.copytree("resources", os.path.join(DIST, "resources"))
	shutil.copy("License.txt", DIST)
	shutil.copy("Readme.html", DIST)

	# CREATE A ZIP ARCHIVE OF THE DISTRIBUTION IF REQUESTED
	destination = os.path.join(os.path.join("builds", "sc4mp-server-" + platform.system().lower() + "-" + str(8 * struct.calcsize("P")) + "-v" + VERSION + "." + datetime.now().strftime("%Y%m%d%H%M%S")))
	print('Creating zip archive of "' + DIST + '" at "' + destination + '"')
	shutil.make_archive(destination, "zip", DIST)


if __name__ == "__main__":
    main()