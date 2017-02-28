#!/usr/bin/python
import click
from colorama import Style, Fore, Back, init
import csv
import datetime as dt
import os
import platform
from pyfiglet import Figlet
import re
from sys import getsizeof, exit


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def exists(file):
    if os.path.isfile(os.path.join(DIR_PATH, file)):
        return True
    return False

def not_exists(file):
    if os.path.isfile(os.path.join(DIR_PATH, file)):
        answer = click.prompt(Fore.RED + '''「{}」既に存在します。そのファイルにデータを追加しますか。\n
              「y」や「n」で返答してください。'''.format(file))
        if str(answer) == 'y':
            return True
        else:
            print(Fore.GREEN + 'Bye' + Style.RESET_ALL)
            exit(0)
    return True

def convert_to_bytes(size):
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

def confirmation(source, target, size, encoding, delimiter):
    print(Fore.GREEN + '**************************')
    print('元のファイル：{}'.format(source))
    print('宛先ファイル：{}'.format(target))
    print('サイズ：{} bytes'.format(size))
    print('文字コード：{}'.format(encoding))
    print('区切り：{}'.format(delimiter))
    print('**************************' + Fore.RESET)

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

def welcome():
    if 'Windows' in platform.platform():
        os.system('cls')
    else:
        os.system('clear')

    fig = Figlet(font='slant')
    print(Fore.CYAN + fig.renderText('WELCOME'))


@click.command()
@click.option('--source', help='手元のファイル')
@click.option('--target', help='宛先ファイル')
@click.option('--size', help='宛先ファイルのサイズ')
@click.option('--delimiter', help='コマやタブの区切り：commaやtab')
@click.option('--encoding', help='文字コードの種類：shift_jisやutf-8')
def main(source, target, size, delimiter, encoding):
    '''
    Main function
    '''

    #
    # Change background
    #

    init()
    print(Back.WHITE)

    welcome()

    #
    # Check source file
    #
    if exists(source):
        pass
        # print('{} exists, OK'.format(source))
    else:
        raise IOError('{} does not exist.'.format(source))

    #
    # Check target file
    #
    if not_exists(target):
        print('[+] 「{}」にデータを書き込みます。'.format(target))

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
    # Delimiter
    #
    if delimiter == 'tab':
        delimiter = '\t'
    if delimiter == 'comma':
        delimiter = ','

    #
    # Confirmation
    #
    confirmation(source, target, size, encoding, delimiter)

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
        print(Fore.MAGENTA + '[+] 宛先ファイルのサイズ: {} MB\r'.format(size_in_mb, getsizeof(container)), end='')
    print('\n')

    #
    # End time
    #
    t2 = dt.datetime.now()
    print(Fore.GREEN + '開始時間 {}'.format(t1))
    print('終了時間 {}'.format(t2))
    print('実行時間 {}'.format(t2 -t1) + Style.RESET_ALL)


if __name__ == '__main__':
    main()

