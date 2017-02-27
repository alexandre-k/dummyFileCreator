#!/usr/bin/python
import click
import os
import pandas
import re
import datetime as dt


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

@click.command()
@click.option('--source', help='手元のファイル')
@click.option('--target', help='宛先ファイル')
@click.option('--size', help='宛先ファイルのサイズ')
def main(source, target, size):
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
    data = pandas.read_csv(source)

    #
    # Start time
    #
    t1 = dt.datetime.now()
    while os.path.getsize(target) < size:
        size_in_mb = os.path.getsize(target) / 1000000
        print('宛先ファイルのサイズ: {}MB\r'.format(size_in_mb), end='')
        data.to_csv(target, mode='a', index=False)

    #
    # End time
    #
    t2 = dt.datetime.now()
    print('t1 {}'.format(t1))
    print('t2 {}'.format(t2))





if __name__ == '__main__':
    main()

