import os;
import xlrd;
from optparse import OptionParser

def readBookMonsterTeam(book):
	worksheet = book.sheet_by_index(0);
	print worksheet;

def readXlsFile(xls_path):
	book = xlrd.open_workbook(xls_path);
	readBookMonsterTeam(book);


def main():
	parser = OptionParser();
	parser.add_option("-f", "--file", dest="file", help="xls file path", metavar="a.xls");
	parser.add_option("-o", "--output", dest="output_file", help="script file output", metavar="a.xml");

	(options, args) = parser.parse_args();

	if options.file == None:
		print '[Error] Need provide source file input.';
		return ;

	if options.output_file == None:
		options.output_file = os.path.splitext(options.file)[0] + '.xml';
	readXlsFile(options.file);

	pass;


if __name__ == '__main__':
	main()