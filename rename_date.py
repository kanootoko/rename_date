'''
rename_date - this script allows to rename multiple files chosen by regular expression to user-defined pattern

'''
version = '2.0 [2021.03.03]'

import os, sys, time
from re import Pattern as re_Pattern, compile as re_compile, match as re_match, error as re_error
from math import log, ceil
import argparse, configparser
from typing import List, Tuple, Dict, Union

class properties:
    def __init__(self, path: str = '.', regexp: str = '.*\\.([jJ][pP][gG]|[aA][vV][iI]|[tT][hH][mM])', \
                 pattern: str = 'Cam %Y-%m-%d %H_%M_%S', dry_run: bool = False, no_exif: bool = False):
        self.path = path
        self._regexp = regexp
        self.no_exif = no_exif
        try:
            self.re = re_compile(regexp)
        except re_error:
            print(f'Regular expression "{regexp}" contains error and cannot be compiled')
            raise
        self.pattern = pattern
        self.dry_run = dry_run
    def set_regexp(self, regexp: str) -> None:
        try:
            self.re = re_compile(regexp)
        except re_error:
            print(f'Regular expression "{regexp}" contains error and cannot be compiled')
            raise
        self._regexp = regexp

if __name__ == '__main__':
    props = properties()

    if os.path.isfile('rename_config.ini'):
        config = configparser.RawConfigParser()
        config.read('rename_config.ini')

        if config.has_option('default', 'input_folder'):
            props.path = config.get('default', 'input_folder')
        if config.has_option('default', 'regular_expression'):
            props.set_regexp(config.get('default', 'regular_expression'))
        if config.has_option('default', 'output_pattern'):
            props.pattern = config.get('default', 'output_pattern')
        if config.has_option('default', 'no_exif'):
            props.no_exif = config.getboolean('default', 'no_exif')

        del config

    parser = argparse.ArgumentParser(description='rename files matched by pattern to a given datetime pattern')

    parser.add_argument('--regexp', '-re', dest='regexp', action='store', type=str, help=f'regular expression to match (default: {props._regexp})')
    parser.add_argument('--output_pattern', '-op', action='store', dest='output_pattern', type=str, help=f'output pattern for the file renaming (default: {props.pattern.replace("%", "%%")})')
    parser.add_argument('--no_exif', dest='no_exif', action='store_true', help=f'use only creation/modification times, do not try to read exif')
    parser.add_argument('--dry_run', dest='dry_run', action='store_true', help=f'only print renamings, without performing them')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help=f'print all the errors')
    parser.add_argument('--save_config', dest='save_config', action='store_true', help=f'save current config to .ini file (name it "rename_config.ini" to use)')
    parser.add_argument('--version', dest='version', action='store_true', help=f'Show version and exit')
    parser.add_argument('input_folder', type=str, nargs='?', help=f'path to a folder with files to rename (default: {props.path})')

    args = parser.parse_args()

    if args.version:
        print(f'Version of the rename_date script: {version}')
        exit()

    if args.input_folder:
        props.path = args.input_folder
    if args.regexp:
        props.set_regexp(args.regexp)
    if args.output_pattern:
        props.pattern = args.output_pattern
    if args.dry_run:
        props.dry_run = True

    if args.save_config:
        config = configparser.RawConfigParser()
        config.add_section('default')
        config['default']['input_folder'] = props.path
        config['default']['regular_expression'] = props._regexp
        config['default']['output_pattern'] = props.pattern#.replace('%', '%%')
        config['default']['no_exif'] = str(props.no_exif)
        with open('rename_example_config.ini', 'w') as f:
            config.write(f)
        del config

    try:
        time.strftime(props.pattern)
    except Exception as ex:
        print(f'Error on using output pattern ({props.pattern}): {ex}')
        exit(1)

    if not args.no_exif:
        try:
            from PIL import Image
        except ModuleNotFoundError:
            print('To use exif reading you need to install PIL module (pip install Pillow). Falling back to system metadata')
            args.no_exif = True

    print(f'Current directory: {os.path.abspath(os.curdir)}')
    print(f'Input folder: {os.path.abspath(props.path)}')
    print(f'Input refular expression: {props._regexp}')
    print(f'Output pattern: {props.pattern}. Example (current time): {time.strftime(props.pattern)}')
    if args.dry_run:
        print('Dry run. No changes to files will be made')
    else:
        print('Files will be renamed in 5 seconds')
        time.sleep(5)

    filenames_map: Dict[Tuple[float, str], Union[str, List[str]]] = {}
    for filename in filter(lambda f: os.path.isfile(props.path + os.path.sep + f) and re_match(props.re, f) is not None, os.listdir(props.path)):
        stats = os.stat(props.path + os.sep + filename)
        if not args.no_exif:
            try:
                exif = Image.open(os.path.abspath(props.path + os.path.sep + filename)).getexif()
                t = time.mktime(time.strptime(exif[36867], '%Y:%m:%d %H:%M:%S'))
            except Exception as ex:
                if args.verbose:
                    print(ex)
                t = min(int(stats.st_ctime), int(stats.st_mtime)) if 'st_ctime' in dir(stats) else stats.st_mtime
        t = min(t, min(int(stats.st_ctime), int(stats.st_mtime)) if 'st_ctime' in dir(stats) else stats.st_mtime)
        time_and_extension = (
                t, \
                (filename[filename.rfind('.'):] if '.' in filename else '').lower()
        )
        if time_and_extension in filenames_map:
            if isinstance(filenames_map[time_and_extension], str):
                filenames_map[time_and_extension] = [filenames_map[t], filename] # type: ignore
            else:
                filenames_map[time_and_extension].append(filename) # type: ignore
        else:
            filenames_map[time_and_extension] = filename
    for (t, extension), filenames in filenames_map.items():
        if isinstance(filenames, str):
            new_name = time.strftime(props.pattern, time.strptime(time.ctime(t))) + extension
            if new_name == filenames:
                continue
            print('rename "{}" "{}"'.format(os.path.abspath(props.path + os.path.sep + filenames), \
                  os.path.abspath(props.path + os.path.sep + new_name)), \
                  file = sys.stdout if props.dry_run else sys.stderr)
            if not props.dry_run:
                try:
                    os.rename(props.path + os.path.sep + filenames, props.path + os.path.sep + new_name)
                except Exception as ex:
                    if args.verbose:
                        print(f'Error on renaming file: {ex}')
        else:
            for i, filename in enumerate(filenames):
                new_name = time.strftime(props.pattern, time.strptime(time.ctime(t)))
                new_name += '_{0:0>{w}}{1}'.format(i + 1, extension, w = ceil(log(len(filenames) + 1, 10)))
                if new_name == filename:
                    continue
                print('rename "{}" "{}"'.format(os.path.abspath(props.path + os.path.sep + filename), \
                      os.path.abspath(props.path + os.path.sep + new_name)), \
                      file = sys.stdout if props.dry_run else sys.stderr)
                if not props.dry_run:
                    try:
                        os.rename(props.path + os.path.sep + filename, props.path + os.path.sep + new_name)
                    except Exception as ex:
                        if args.verbose:
                            print(f'Error on renaming file: {ex}')
