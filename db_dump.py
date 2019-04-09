#!/usr/bin/python -u

import pymongo
import sys
sys.path.append("/opt/topspot/web_service/src")
from constants import *
sys.path.append(TRAFFIC_CONFIG_PATH)
from traffic_config import *
import os
import subprocess
from datetime import datetime, timedelta
import time
import datetime
import time
import shutil

output_directory = "/home/qet/test_dump_loc"
channel_name = CHANNEL_ID_LIST[0]
print "channel_name", channel_name
days_delete = 7
# set username and password to "None" if there is no un and pass for mongo
username = None
password = None
db = "qet"

def backup(output_dir, channel_name, days_to_delete):
	try:
		today = datetime.datetime.now().strftime("%Y_%b_%d")
		output_file = str(channel_name) + "_" + today
		#output = os.path.join(output_dir, output_file)
		print "--- Taking the dump ---"
		if username and password:
			backup_output = subprocess.check_output(
				[
					"mongodump",
					"-d", '%s' % db,
					"-u", '%s' % username,
					"-p", '%s' % password,
					"-o", '%s' % output_file
				])
		else:
			backup_output = subprocess.check_output(
				[
					"mongodump",
					"-d", '%s' % db,
					"-o", '%s' % output_file
				])

		print "--- Dump taken successfully ---"
		print "--- Compressing the dump ---"
		convert_tar = subprocess.check_output(
			[
				"tar",
				"-zcvf",
				"{}.tar.gz".format(output_file),
				"{}".format(output_file)
			])
		# move the compressed file to output folder
		move_file = subprocess.check_output(
			[
				"mv",
				"{}.tar.gz".format(output_file),
				"{}".format(output_dir)
			])

		print "--- Compression done ---"
		print "--- Removing dump file older than {} days ---".format(int(days_to_delete))
		#code to remove the old files and the folder after dump is taken
		visited = False
		for root, dirs, files in os.walk(output_dir):
			#print root, dirs, files
			if visited:
				break
			visited = True
			# for each_dir in dirs:
			# 	dir_to_remove = os.path.join(root, each_dir)
			# 	shutil.rmtree(dir_to_remove) # directory removed after compressing
			for each_file in files:
				if each_file.startswith("vrl"):
					now = time.time()
					full_path = os.path.join(root, each_file)
					# print "full_path", full_path
					# print "now", now - 7 * 86400
					# here 7 * 86400 = 7 days
					if os.stat(full_path).st_mtime <= now - int(days_to_delete) * 86400:
						if os.path.isfile(full_path):
							os.remove(full_path)
				else:
					pass

		dirs = os.listdir(".")
		for each_dir in dirs:
			if each_dir == output_file:
				shutil.rmtree(each_dir) # directory removed after compressing
			else:
				pass
		print "--- Done ---"
	except Exception, ex:
		print "Exception in db_dump script while taking db dump", ex

if __name__ == "__main__":
	print "--- mongodump initialized ---"
	print "--- Please do not escape or quit ---"
	backup(output_directory, channel_name, days_delete)
	print "--- Exiting ---"
