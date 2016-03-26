""" Install Script """
import sys, os, shutil

from meta import *


def _install():
	"""
	Runs the actual installation process.
	"""
	print "Preparing to install {} script.".format(SCRIPT_NAME)
	
	#make sure there is a place to install the script to.
	if not "SCRIPTS" in os.environ:
		print "Please set SCRIPTS environment variable."
		sys.exit(1)
	
	script_dir = os.environ["SCRIPTS"]
	
	#check to see if already installed
	if _is_already_installed(script_dir):
		print "A version of {} is already installed.".format(SCRIPT_NAME)
		print "Do you wish to overwrite it? [Y,n]"
		if raw_input() != 'Y':
			print "Cancelling installation of {}.".format(SCRIPT_NAME)
			sys.exit(0)
		else:
			print "Overwritting previously installed script {}.".format(SCRIPT_NAME)
			_uninstall()
	
	#copy python sources into script directory
	new_dir = os.path.join(script_dir, SCRIPT_NAME)
	shutil.copytree("src", new_dir)
	
	#copy executable and add permissions
	for name in EXEC_NAMES:
		os.system("sudo cp bin/{0} /bin/{0}".format(name))
		os.system("sudo chmod +x /bin/{}".format(name))
	


def _uninstall():
	"""
	Removes Python sources from the script directory and removes the executable
	from /bin/.
	"""
	if not "SCRIPTS" in os.environ:
		print "Please set SCRIPTS environment variable."
		sys.exit(1)
	
	script_dir = os.environ["SCRIPTS"]
	
	if SCRIPT_NAME in os.listdir(script_dir):
		shutil.rmtree(os.path.join(script_dir, SCRIPT_NAME))
	for name in EXEC_NAMES:
		if name in os.listdir("/bin/"):
			os.system("sudo rm -f /bin/{}".format(name))


def _is_already_installed(script_dir):
	"""Checks to see if there is a version already installed"""
	#first check the bin folder
	if SCRIPT_NAME in os.listdir(script_dir):
		return True
	for name in EXEC_NAMES:
		if name in os.listdir("/bin/"):
			return True
	
	return False



if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print "Please specify a setup command.  (e.g. 'install' or 'uninstall')"
	cmd = sys.argv[1]
	
	if cmd == 'install':
		_install()
	elif cmd == 'uninstall':
		_uninstall()
	else:
		print "Setup command '{}' not recognized.".format(cmd)
	
