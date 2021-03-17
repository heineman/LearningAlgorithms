"""
Provide access to English words, stored in alphabetical order, one per line.

Compatible with Python 3.7

If this code just doesn't work for you, then simply hard-code something like this:

    def english_words():
        word_file = open(DICTIONARY_FILE, 'r')
        all_words = word_file.read().splitlines()
        word_file.close()
        return all_words
"""

_english_words = []

def english_words():
    """Return list of 321,129 English words from dictionary."""
    if _english_words:
        return _english_words

    # Try to load up...
    try:
        import importlib.resources as pkg_resources
        file = pkg_resources.read_text('resources', 'words.english.txt')
        _english_words.extend(file.splitlines())
        return _english_words
    except ImportError:
        pass

    try:
        import pkg_resources

        file = pkg_resources.resource_string('resources', 'words.english.txt').decode('utf-8')
        _english_words.extend(file.splitlines())
        return _english_words
    except ImportError:
        pass

    # if still cannot access, then you will have to hard-code to
    # change the following path name to the location of the
    # words.english.txt file
    import os
    file = open(os.path.join('resources', 'words.english.txt'))
    for line in file.readlines():
        _english_words.append(line[:-1])    # chomp '\n'
    return _english_words
