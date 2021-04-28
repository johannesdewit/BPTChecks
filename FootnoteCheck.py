# This script seeks to check whether multiple bptmarkdown files have any non-
# defined footnotes or footnotes that are defined but not actually appearing in
# the text.
#
# Assumptions:
#     - The files are using the regular md footnote style
#     - The footnotes are marked inline and defined on new lines at the end of
#       the document after a heading line beginning with '### Notes'

import os
from os import path
from glob import glob
from tqdm import tqdm
import sys, getopt
import datetime
import re


# Define parsing inline notes function.

# Match anything of the form: '[^123ab]'
inline_note_match = re.compile(
    r"[.\n]*?(\[\^[0-9A-Za-z]+\]).*?", re.S
)

def parse_inline_notes(md: str) -> dict:
    if not md:
        return {}

    inline_notes_list = re.findall(inline_note_match, md)

    keys = [k for k in inline_notes_list]
    if len(keys) > len(set(keys)):
        raise Exception(
            "Duplicate inline footnotes: "
            + str([key for i, key in enumerate(keys) if key in keys[:i]])
        )

    inline_notes = {}
    for i in inline_notes_list:
        inline_notes[i] = None

    return inline_notes


# Match anything of the form: `[^123ab]: some note` where
# the note may contain single (but not double) newlines
# and `[^123ab]` is at the start of a line. Columnn may
# be missing.
defined_note_match = re.compile(
    r"(?:^|\n)(\[\^[0-9A-Za-z]+\])\:? ?((?:(?!\n\n).)*)[\n{2}]?", re.S
)

def parse_defined_notes(md: str) -> dict:
    if not md:
        return {}

    defined_notes = re.findall(defined_note_match, md)

    keys = [k for k, v in defined_notes]
    if len(keys) > len(set(keys)):
        raise Exception(
            "Duplicate defined footnotes: "
            + str([key for i, key in enumerate(keys) if key in keys[:i]])
        )

    return dict(defined_notes)


# Function that compares the two dictionaries
def parse_md_files(inputpath):

    not_matching_notes = []

    for file in tqdm(glob(path.join(inputpath, '*.md')), desc=f'Parsing markdown files'):
        with open(file, 'r') as f:
            mdf = f.read()

            # Split the md file in to a 'content' and 'notes' section
            mdf = mdf.split('### Notes', 1)
            mdf_content = str(mdf[0])
            mdf_notes = str(mdf[-1])

            # Run the two parsers
            try:
                inline_notes = parse_inline_notes(mdf_content)
            except Exception as e:
                not_matching_notes.append(str(file) + ", " + str(e))
                continue
            try:
                defined_notes = parse_defined_notes(mdf_notes)
            except Exception as e:
                not_matching_notes.append(str(file) + ", " + str(e))
                continue
            f.close()

        # Compare the keys
        # Here the script should in the future show which notes are missing or undefined.
        inline_keys = [k for k in inline_notes]
        defined_keys = defined_notes.keys()
        if len(inline_keys) != len(defined_keys):
            if len(inline_keys) > len(defined_keys):
                not_matching_notes.append(str(file) + f", Missing {len(inline_keys) - len(defined_keys)} defined note(s). ")
            if len(inline_keys) < len(defined_keys):
                not_matching_notes.append(str(file) + f", Missing {len(defined_keys) - len(inline_keys)} inline note(s). ")
            continue
        else:
            continue
    return list(not_matching_notes)


# Produce output file
def write_output_file(list, header):
    output_fname = 'Output_' + str(datetime.datetime.now()) + '.txt'
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
        print('FootnoteCheck.py -i <inputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--ipath'):
            inputpath = arg
            output_list = parse_md_files(inputpath)
            write_output_file(output_list, f'Following files in {inputpath} contain problems with footnotes:')
            print('Files checked for missing footnotes')
        else:
            print('Folder not specified correctly. Try "FootnoteCheck.py -i /path/to/folder"')
            sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
