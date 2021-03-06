# This script seeks to check whether multiple Brill plain test (BPT) markdown
# files have missing 'textparts'. A textpart is always marked by a header.
# At the moment missing textparts will be identified by checking the last text-
# part and comparing every other textpart mentioned. If the last textpart would
# be missing, this script will not mention it.
# Because the BPT has both 'T' and 'F' textparts. The above applies to both.
#
# Known issues:
#     - If textpart misses both a T or F the script doesn't identify it yet.
#     - Large textparts may have double letters after the textpart numbers in
#       order to identify the textpart ('aa' after 'z'). This has not been
#       resolved yet.

import os
from os import path
from glob import glob
from tqdm import tqdm
import sys, getopt
import datetime
import re

def parse_textparts(file, fail_list):

    tp_t_headers = []
    tp_f_headers = []

    for line in file:
        if line.startswith('### textpart T') or line.startswith('### textpart F'):
            line = line.split(':', 1)[0]
            tp_id = line.split(' ', 2)[2]

            # If the textpart 'id' doesn't start with T or F the file should be logged as containing a fault.
            if tp_id.startswith('T'):
                tp_t_headers.append(tp_id)
            elif tp_id.startswith('F'):
                tp_f_headers.append(tp_id)
            else:
                fail_list.append(str(file) + ', textpart(s) not formatted correctly')
                break
        else:
            continue

    return list(tp_t_headers), list(tp_f_headers), list(fail_list)

def check_textparts(tp_list, fail_list, file_name):

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for tp_id in tp_list:
        try:
            if tp_id.startswith('T'):
                tp_type = str('T')
            elif tp_id.startswith('F'):
                tp_type = str('F')
        except IndexError:
            continue
        tp_id = tp_id[1:]

        if tp_id == '1' or tp_id == '1a':
            continue
        else:
            tp_id_re = re.findall(r'(\d+)([a-z]*)', tp_id)[0]
            tp_id_dig = int(tp_id_re[0])
            tp_id_let = tp_id_re[1]
            # If tp_id_let is a, continue
            if tp_id_let == 'a':
                continue
            if not tp_id_let == '':
                tp_id_let_i = alphabet.index(tp_id_let)
                while tp_id_let_i > -1:
                    tp_id_let_alpha = alphabet[tp_id_let_i]
                    tp_full_id = tp_type + str(tp_id_dig) + tp_id_let_alpha
                    if not tp_full_id in tp_list:
                        fail_line = str(file_name) + f', textpart(s) {tp_full_id} missing'
                        if not fail_line in fail_list:
                            fail_list.append(fail_line)
                    tp_id_let_i -= 1
            else:
                while tp_id_dig > 0:
                    tp_full_id = tp_type + str(tp_id_dig)
                    elem_in_list = False
                    for elem in tp_list:
                        if elem.startswith(f'{tp_full_id}'):
                            elem_in_list = True
                        else:
                            continue
                    if not elem_in_list:
                        fail_line = str(file_name) + f', textpart(s) {tp_full_id} missing'
                        if not fail_line in fail_list:
                            fail_list.append(fail_line)
                    tp_id_dig -= 1
                continue
            continue
    return list(fail_list)

def parse_md_files(inputpath):

    incorrect_textparts = []

    for file in tqdm(glob(path.join(inputpath, '*.md')), desc=f'Parsing markdown files'):
        with open(file, 'r') as f:
            mdf = f.readlines()

            tp_t_headers, tp_f_headers, incorrect_textparts = parse_textparts(mdf, incorrect_textparts)

            incorrect_textparts.extend(check_textparts(tp_t_headers, incorrect_textparts, file))
            incorrect_textparts.extend(check_textparts(tp_f_headers, incorrect_textparts, file))

            # For some reason some lines are added multiple times. Until this problem is resolved the
            # following line is added to ensure a readable list.
            incorrect_textparts = list(set(incorrect_textparts))

            continue

    return list(incorrect_textparts)

# Produce output file
def write_output_file(list, header):
    output_fname = 'Output_textparts_' + str(datetime.datetime.now()) + '.txt'
    with open(output_fname, 'w') as f:
        f.write(str(header) + '\n')
        for line in sorted(list):
            f.write(line + '\n')
        f.close()


# Read inputpath
def main(argv):
    inputpath = ''

    # This could be improved with error messages if the folder does not exist.
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print('TextpartCheck.py -i <inputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--ipath'):
            inputpath = arg
            output_list = parse_md_files(inputpath)
            write_output_file(output_list, f'Following files in {inputpath} contain problems with textparts:')
            print('Files checked for missing textparts')
        else:
            print('Folder not specified correctly. Try "TextpartCheck.py -i /path/to/folder"')
            sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
