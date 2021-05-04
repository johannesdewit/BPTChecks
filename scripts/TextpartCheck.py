# This script seeks to check whether multiple Brill plain test (BPT) markdown
# files have missing 'textparts'. A textpart is always marked by a header.
# At the moment missing textparts will be identified by checking the last text-
# part and comparing every other textpart mentioned. If the last textpart would
# be missing, this script will not mention it.
# Because the BPT has both 'T' and 'F' textparts. The above applies to both.
#
# Known problem: at the moment the script identifies 'F5' as missing if 'F5a' is
# present but not 'F5'.

import os
from os import path
from glob import glob
from tqdm import tqdm
import sys, getopt
import datetime
import re

def parse_md_files(inputpath):

    incorrect_textparts = []

    for file in tqdm(glob(path.join(inputpath, '*.md')), desc=f'Parsing markdown files'):
        with open(file, 'r') as f:
            mdf = f.readlines()

            tp_t_headers = []
            tp_f_headers = []

            # Add all textpart headers to list 'tp_headers'
            for line in mdf:
                if line.startswith('### textpart T') or line.startswith('### textpart F'):
                    line = line.split(':', 1)[0]
                    tp_id = line.split(' ', 2)[2]
                # If the textpart 'id' doesn't start with T or F the file should be logged as containing a fault.
                    if not tp_id.startswith('F') and not tp_id.startswith('T'):
                        incorrect_textparts.append(str(file) + ', textpart(s) not formatted correctly')
                        break
                    elif tp_id.startswith('T'):
                        tp_t_headers.append(tp_id)
                    elif tp_id.startswith('F'):
                        tp_f_headers.append(tp_id)
                else:
                    continue

            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

            # For every element of tp_headers check whether all other previous tp_id's are there
            for tp_f_id in tp_f_headers:
                tp_id = tp_f_id[1:]

                # Skip '1' and '1a', these are always correct.
                if tp_id == '1' or tp_id == '1a':
                    continue
                if tp_id.isnumeric():
                    # This only works if tp_id only consists of numbers
                    tp_id = int(tp_id)
                    while tp_id > 0:
                        if not f'F{tp_id}' in tp_f_headers:
                            incorrect_textparts.append(str(file) + f', textpart(s) F{tp_id} missing')
                        tp_id -= 1
                    continue
                else:
                    # If tp_id does not only contain digits it contains letters
                    tp_id_re = re.findall(r'(\d+)([a-z]*)', tp_id)[0]
                    tp_id_dig = tp_id_re[0]
                    tp_id_let = tp_id_re[1]

                    # If tp_id_let is a, continue
                    if tp_id_let == 'a':
                        continue
                    tp_id_let_i = alphabet.index(tp_id_let)
                    while tp_id_let_i > -1:
                        tp_id_let_alpha = alphabet[tp_id_let_i]
                        tp_full_id = 'F' + tp_id_dig + tp_id_let_alpha
                        print(tp_full_id)
                        if not tp_full_id in tp_f_headers:
                            incorrect_textparts.append(str(file) + f', textpart(s) {tp_full_id} missing')
                            break
                        tp_id_let_i -= 1
                    continue
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
