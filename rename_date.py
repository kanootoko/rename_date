'''rename_date - this script allows to rename multiple files chosen by pattern (regular expression) to "Cam YYYY-MM-DD HH_SS_(#)"
Usage: start script in folder where your files are holded or choose the directory by --input_folder command line argument.
Possible command line arguments:
	--input_folder=<path/to/folder> [default: . ]
	--regular_expression=<regexp> [default: .*\\.([jJ][pP][gG]|[aA][vV][iI]|[tT][hH][mM]) ]
'''

import os, sys
from re import compile as re_compile, match as re_match, error as re_error
from math import log, ceil

class properties:
	def __init__(self, path: str = os.curdir, regexp: str = '.*\\.([jJ][pP][gG]|[aA][vV][iI]|[tT][hH][mM])'):
		self.path = path
		try:
			self.re = re_compile(regexp)
		except re_error:
			self.re = re_compile('.*\\.([jJ][pP][gG]|[aA][vV][iI]|[tT][hH][mM])')

def parse_args(props: properties, argv: list):
	for arg in argv[1:]:
		if arg.lower().startswith(('--input_folder=', '-if=')):
			path = os.path.normpath(arg[arg.find('=') + 1:])
			if not os.path.isdir(path):
				print('Error setting input folder: "{}" is not a folder'.format(path))
			else:
				props.path = path
		elif arg.lower().startswith(('--regular_expression=', '-re=')):
			try:
				props.re = re_compile(arg[arg.find('=') + 1:])
			except re_error:
				print('Error setting regular expression: "{}"'.format(arg[arg.find('=') + 1:]))
		elif arg.lower() in ('help', '/?', '--help', '-h', '-help'):
			print(__doc__)
			exit(0)
		else:
			print('Unknown parameter: "{}". Try "{} --help"'.format(arg, sys.argv[0]))

def main(argv):
	import time
	props = properties()
	if len(argv) > 1:
		parse_args(props, argv)
	filenames_map = {}
	for filename in filter(lambda f: os.path.isfile(props.path + os.path.sep + f) and re_match(props.re, f) is not None, os.listdir(props.path)):
		t = int(os.stat(props.path + os.sep + filename).st_mtime)
		if t in filenames_map:
			if isinstance(filenames_map[t], str):
				filenames_map[t] = [filenames_map[t], filename]
			else:
				filenames_map[t].append(filename)
		else:
			filenames_map.update({t: filename})
	for t, filenames in filenames_map.items():
		if isinstance(filenames, str):
			new_name = time.strftime('Cam %Y-%m-%d %H_%S', time.strptime(time.ctime(t))) + filename[filename.rfind('.'):]
			print('rename "{}" "{}"'.format(props.path + os.path.sep + filename, props.path + os.path.sep + new_name), file=sys.stderr)
		else:
			for i, filename in enumerate(filenames):
				new_name = time.strftime('Cam %Y-%m-%d %H_%S', time.strptime(time.ctime(t)))
				new_name += '_{0:0>{w}}{1}'.format(i + 1, filename[filename.rfind('.'):] if '.' in filename else '', w = ceil(log(len(filenames) + 1, 10)))
				print('rename "{}" "{}"'.format(props.path + os.path.sep + filename, props.path + os.path.sep + new_name), file=sys.stderr)
		
if __name__ == '__main__':
	main(sys.argv)