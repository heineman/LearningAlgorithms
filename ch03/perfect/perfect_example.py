"""
Generate the files containing the perfect hash for the words in
the English dictionary. Typically the 'perfect-hash' executable
is installed in the $PYTHON_HOME/Scripts directory as perfect-hash.

You can also directly execute this file

I executed this file with the following arguments:

    ..\\..\\resources\\words.english.txt --hft=2 -o hashFile.py

Required several minutes to execute because of the size of the
dictionary. Also I used the option (--hft=2) to create two
supplementary lists, S1 and S2, to probe into primary list, G.

Once the file is generated, you can safely delete the second
half of 'hashFile.py' which has a copy of the words in the
dictionary as a sanity check. Then I renamed the file as
generated_dictionary.py

generated_dictionary only contains the actual G, S1, S2, hash_f and
perfect_hash functions

Requires `perfect-hash` library: install using

  pip install perfect-hash

"""
from perfect_hash import main

#######################################################################
if __name__ == '__main__':
    main()
