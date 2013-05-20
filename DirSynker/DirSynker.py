import os;
import shutil;
from filecmp import dircmp;
from optparse import OptionParser;

g_files_synced_left_2_right = [];
g_files_synced_right_2_left = [];

def syncContent(dir_left, dir_right, do_copy):

	if not os.path.exists(dir_left) or not os.path.exists(dir_right):
		return ;

	#print "Syncing folder %s to %s..."%(dir_left, dir_right);
	drmp = dircmp(dir_left, dir_right);

	# sync 1 -> 2
	for file in drmp.left_only:
		if do_copy:
			shutil.copy2(os.path.join(dir_left, file), dir_right);	
		g_files_synced_left_2_right.append(file);

	# sync 2 -> 1
	for file in drmp.right_only:
		if do_copy:
			shutil.copy2(os.path.join(dir_right, file), dir_left);
		g_files_synced_right_2_left.append(file);

	# replace the older file with the newer one
	for file in drmp.diff_files:
		file_left = os.path.join(dir_left, file);
		file_right = os.path.join(dir_right, file);
		fs_left = os.stat(file_left);
		fs_right = os.stat(file_right);
		if fs_left.st_mtime < fs_right.st_mtime:
			if do_copy:
				shutil.copy2(file_right, file_left);
			g_files_synced_right_2_left.append(file);
		else:
			if do_copy:
				shutil.copy2(file_left, file_right);
			g_files_synced_left_2_right.append(file);


def syncDir(options):
	print "Syncing dirs";
	drmp = dircmp(options.root_left, options.root_right);
	print "--------------------------";
	print "Dir only in left: ";
	print "--------------------------";
	for dir in drmp.left_only:
		print dir;
		path_left = os.path.join(options.root_left, dir);
		path_right = os.path.join(options.root_right, dir);
		if os.path.isdir(path_left):
			path_right = os.path.join(path_right, options.subdir_right);
			if options.do_copy:
				print "create right dir: " + path_right;
				os.makedirs(path_right);

	print "--------------------------";				
	print "Dir only in right: ";
	print "--------------------------";
	for dir in drmp.right_only:
		path_right = os.path.join(options.root_right, dir);
		path_left = os.path.join(options.root_left, dir);
		if os.path.isdir(path_right):
			path_left = os.path.join(path_left, options.subdir_left);
			if options.do_copy:
				print "create left dir: " + path_left;
				os.makedirs(path_left);

	print "--------------------------";
	print "Syncing content";
	print "--------------------------";
	dirs = os.listdir(options.root_left);
	for dir in dirs:
		dir_path = os.path.join(options.root_left, dir);
		if os.path.isdir(dir_path):			
			dir_left = os.path.join(options.root_left, dir, options.subdir_left);
			dir_right = os.path.join(options.root_right, dir, options.subdir_right);
			syncContent(dir_left, dir_right, options.do_copy);

	print "Result"
	print "--------------------------";
	print "Sync from left to right:"
	for file in g_files_synced_left_2_right:
		print file;
	print "Sync from right to left:"
	for file in g_files_synced_right_2_left:
		print file;

def main():
	parser = OptionParser();
	parser.add_option("--root_left", dest="root_left", help="Left dir to sync");
	parser.add_option("--subdir_left", dest="subdir_left", help="Sub dir structure to compare unit");
	parser.add_option("--root_right", dest="root_right", help="Right dir to sync");
	parser.add_option("--subdir_right", dest="subdir_right", help="Sub dir structure to compare unit");
	parser.add_option("-c", "--doCopy", action="store_true", dest="do_copy", help="Do copy action or not");
	(options, args) = parser.parse_args();
	print options;
	
	if options.subdir_left == None:
		options.subdir_left = "";
	if options.subdir_right == None:
		options.subdir_right = "";

	root_left = options.root_left;
	root_right = options.root_right; 
	
	syncDir(options);

if __name__ == '__main__':
	main();

