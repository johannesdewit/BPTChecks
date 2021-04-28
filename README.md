# BPTChecks

A package with different scripts that check whether Brill plain text (BPT) markdown files are formatted correctly.

## FootnoteCheck

Requirements:
- tqdm 4.60.x

This is a script which will read bpt-markdown files and check whether the number of inline footnotes and defined notes match. This can be used to check whether markdown files are in complete.

You can run the script by running:

    FootnoteCheck.py -i <inputfolderpath>

The script will generate an .txt output file with the found problems.
