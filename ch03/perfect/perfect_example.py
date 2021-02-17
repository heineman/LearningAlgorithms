"""Generate the files containing the perfect hash for the
words in the English dictionary.

I executed this file with the following arguments:

    ..\\..\\words.english.txt --hft=2 -o hashFile2.py

Required several minutes of execution.

Requires `perfect-hash` library: install using

  pip install perfect-hash

"""
from perfect_hash import main

main()
