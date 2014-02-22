import sys
import io
import sort
import parse

def count_unique(sorted_file):
	f = io.open(sorted_file, 'r')
	count = 0
	prev = ''
	s = 'init'
	while s != '':
		s = f.readline()
		if s != '' and s != prev:
			count += 1
		prev = s
	return count

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage [binary] [file]'
		sys.exit()
	in_filename = sys.argv[1]
	misidn_filename = 'misidn.txt'
	word_filename = 'word.txt'
	parse.parse(in_filename, misidn_filename, word_filename)
	sort.sort(misidn_filename, misidn_filename)
	sort.sort(word_filename, word_filename)
	count1 = count_unique(misidn_filename)
	count2 = count_unique(word_filename)
	print 'number of unique misidn is', count1
	print 'number of unique words is', count2
