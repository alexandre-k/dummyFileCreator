#!/usr/bin/python
import click
import csv
import datetime as dt
import os
import re
from sys import getsizeof


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def exists(file):
    if os.path.isfile(os.path.join(DIR_PATH, file)):
        return True
    return False

def not_exists(file):
    if os.path.isfile(os.path.join(DIR_PATH, file)):
        raise IOError('ファイルは既に存在します')
    return True

def convert_to_bytes(size):
    print(size)
    size = re.split('(\d+)', size)
    if 'KB' in size:
        return get_size_in_bytes(size[1], '000')
    if 'MB' in size:
        return get_size_in_bytes(size[1], '000000')
    if 'GB' in size:
        return get_size_in_bytes(size[1], '000000000')
    raise ValueError('''サイズの形式は不正確です。\n
                    正確サイズは例として、1GB、8MB、79KBなどです。''')

def get_size_in_bytes(size, zeros):
    return int(str(size) + str(zeros))

def confirmation(source, target, size):
    print('**************************')
    print('元のファイル：{}'.format(source))
    print('宛先ファイル：{}'.format(target))
    print('サイズ：{} bytes'.format(size))
    print('**************************')

def reader(source, delimiter, encoding):
    with open(source, 'r', encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        rows = []
        for row in csv_reader:
            rows.append(row)
    return rows

def writer(target, delimiter, rows):
    with open(target, 'a+', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile,
                                delimiter=delimiter,
                                quoting=csv.QUOTE_NONE)
        for row in rows:
            csv_writer.writerows(row)
    return True

@click.command()
@click.option('--source', help='手元のファイル')
@click.option('--target', help='宛先ファイル')
@click.option('--size', help='宛先ファイルのサイズ')
@click.option('--delimiter', help='コマやタブの区切り：,や\t')
@click.option('--encoding', help='文字コードの種類：shift_jisやutf-8')
def main(source, target, size, delimiter, encoding):
    '''
    Main function
    '''

    #
    # Check source file
    #
    if exists(source):
        print('{} exists, OK'.format(source))
    else:
        raise IOError('{} does not exist.'.format(source))

    #
    # Check target file
    #
    if not_exists(target):
        print('{}を作成します。'.format(target))

    #
    # Check and convert size
    #
    size = convert_to_bytes(size)

    #
    # Create target file
    #
    with open(target, 'a'):
        os.utime(DIR_PATH, None)

    #
    # Confirmation
    #
    confirmation(source, target, size)

    #
    # Read file
    #
    data = reader(source, delimiter, encoding)
    container = []

    #
    # Start time
    #
    t1 = dt.datetime.now()

    #
    # Write file
    #
    while os.path.getsize(target) < size:
        if getsizeof(container) < 5000:
            container.append(data)
        else:
            writer(target, delimiter, (container))
            size_in_mb = os.path.getsize(target) / 1000000

        size_in_mb = os.path.getsize(target) / 1000000
        print('宛先ファイルのサイズ: {}MB and container: {}\r'.format(size_in_mb, getsizeof(container)), end='')
    print('\n')

    #
    # End time
    #
    t2 = dt.datetime.now()
    print('t1 {}'.format(t1))
    print('t2 {}'.format(t2))


if __name__ == '__main__':
    main()

