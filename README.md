# BPTChecks

An expanding package with different scripts that check whether Brill plain text (BPT) markdown files are formatted correctly.

Requirements:
- tqdm 4.60.x

## FootnoteCheck.py

This is a script which will read BPT-markdown files and check whether the number of inline footnotes and defined notes match. This can be used to check whether markdown files are in complete.

You can run the script by running:

    FootnoteCheck.py -i <inputfolderpath>

The script will generate an Output_footnotes_<datetime>.txt output file with the found problems.

## TextpartCheck.py

This is a script which will read BPT-markdown files and check whether the number of textparts included is correct. At the moment this is done by looking at the last textpart included and check whether all the preceding numbers are there as expected.

You can run the script by running:

    TextpartCheck.py -i <inputfolderpath>

The script will generate an Output_textparts_<datetime>.txt output file with the found problems.
