# MdChecks

## FootnoteCheck

This is a script which will read markdown files and check whether the number of inline footnotes and defined notes match. This can be used to check whether markdown files are in complete.

You can run the script by running FootnoteCheck.py -i <inputfolderpath>

The script will generate an output file with the found problems.

## Known problems

- At the moment the script marks every note at the start of a line as a defined note. This is not always the case.
- It is way too slow at the moment. Taking 2s per file.
