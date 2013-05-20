import os;
import xlrd;
from optparse import OptionParser
import MonsterTeam2Script


def collectData(workbook):
	MonsterTeam2Script.collectMonsterTeamData(workbook);

def readXlsFile(xls_path):
	workbook = xlrd.open_workbook(xls_path);
	return workbook;

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
	workbook = readXlsFile(options.file);
	collectData(workbook);

	pass;

if __name__ == '__main__':
	main()