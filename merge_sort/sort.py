import io
import sys
import os,re

TMP_FILE_PREFIX = 'tmp_range'
TMP_FILE_EXT = '.txt'

#MEM_SIZE = 1024*1024*1024 #1G
MEM_SIZE = 512

def flush_array(arr, filename):
	f = io.open(filename, 'w')
	arr.sort()
	#print arr
	for s in arr:
		f.write(s)
	f.flush()
	f.close()

def get_range_prefix(layer):
    return '_' + str(layer) + '_'

def purge(dir, pattern):
    for f in os.listdir(dir):
    	if re.search(pattern, f):
    		os.remove(os.path.join(dir, f))

def merge_file(filename1, filename2, out_filename):
	outf = io.open(out_filename, 'w')
	f1 = io.open(filename1, 'r')
	try:
    		f2 = io.open(filename2, 'r')
	except:
		s = 'init'
		while s != '':
			s = f1.readline()
			outf.write(s)
		outf.flush()
		outf.close()
		return

	s1 = 'init'
	s2 = 'init'
	moveS1 = True
	moveS2 = True
	while s1 != '' or s2 != '':
		if moveS1:
			s1 = f1.readline()
		if moveS2:
			s2 = f2.readline()
		#print 's1 is ', s1, 's2 is ', s2
		#print 'moveS1',moveS1,'moveS2',moveS2
		moveS1 = moveS2 = False
		if s2 == '' or (s1 != '' and s1 < s2):
			outf.write(s1)
			moveS1 = True
		else:
			outf.write(s2)
			moveS2 = True

	outf.flush()
	outf.close()
	f1.close()
	f2.close()

def sort(in_filename, out_filename):
	#split file by mem size and sort small groups first
	layer = 0
	f = io.open(in_filename)
	s = 'init'
	arr = []
	mem_used = sys.getsizeof(arr)
	file_counter = 0
	while s != '':
		s = f.readline()
		additional_size = sys.getsizeof(s) 
		if mem_used + additional_size < MEM_SIZE:
			arr += [s]
			mem_used += additional_size
		else:
			flush_array(arr, TMP_FILE_PREFIX + get_range_prefix(layer) + str(file_counter) + TMP_FILE_EXT)
			arr = [s]
			mem_used = sys.getsizeof(arr)
			file_counter += 1
	if arr != []:
		flush_array(arr, TMP_FILE_PREFIX + get_range_prefix(layer) + str(file_counter) + TMP_FILE_EXT)
		file_counter += 1
	f.close()

    #merge all files
	layer = 1
	while file_counter > 1:
		i = 0
		nxt_file_counter = 0
		cur_range_prefix = get_range_prefix(layer-1)
		nxt_range_prefix = get_range_prefix(layer)
		while i < file_counter:
			file1 = TMP_FILE_PREFIX + cur_range_prefix + str(i) + TMP_FILE_EXT
			if i+1 < file_counter:
				file2 = TMP_FILE_PREFIX + cur_range_prefix + str(i+1) + TMP_FILE_EXT
			else:
				file2 = ''
			outfile = TMP_FILE_PREFIX + nxt_range_prefix + str(nxt_file_counter) + TMP_FILE_EXT
			merge_file(file1, file2, outfile)
			nxt_file_counter += 1
			i += 2
		layer += 1
		file_counter = nxt_file_counter

	os.rename(TMP_FILE_PREFIX + get_range_prefix(layer-1) + '0' + TMP_FILE_EXT, out_filename) 
	purge('./', TMP_FILE_PREFIX + '*')

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'usage python sort.py [file_to_sort] [output_file]'
		sys.exit()	
	sort(sys.argv[1], sys.argv[2])
	 
