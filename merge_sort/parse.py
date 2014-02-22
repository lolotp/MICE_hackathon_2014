import io
import sys

def parse(filename, out_filename1, out_filename2):
	f = io.open(filename)
	outf1 = io.open(out_filename1, 'w')
	outf2 = io.open(out_filename2, 'w')
	s = 'init'
	while s != '':
		s = f.readline()
		if s != '':		
			tokens = s.split("|")
			str_misidn = tokens[2]
			str_word = "|".join(tokens[4:])
			outf1.write(str_misidn + '\n')
			outf2.write(str_word)
	outf1.flush()
	outf1.close()
	outf2.flush()
	outf2.close()

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print 'Usage python parse.py [file_to_parse] [misidn_file] [word_file]'
		sys.exit()
	parse(sys.argv[1], sys.argv[2], sys.argv[3])
