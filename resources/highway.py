"""
Provide access to Highway map stored in TMG file
Compatible with Python 3.7

If this code just doesn't work for you, then simply hard-code something like this:

    def highway_map():
        data_file = open(TMG_FILE, 'r')
        information = data_file.read().splitlines()
        data_file.close()
        return information
"""

_highway_data = []

def highway_map():
    """Return TMG file containing highway data."""
    
    # Try to load up...
    try:
        import importlib.resources as pkg_resources
        file = pkg_resources.read_text('resources', 'MA-region-simple.tmg')
        _highway_data.extend(file.splitlines())
        return _highway_data
    except ImportError:
        pass

    try:
        import pkg_resources

        file = pkg_resources.resource_string('resources', 'MA-region-simple.tmg').decode('utf-8')
        _highway_data.extend(file.splitlines())
        return _highway_data
    except ImportError:
        pass

    # if still cannot access, then you will have to hard-code to
    # change the following path name to the location of the
    # "words.english.txt" file
    import os
    file = open(os.path.join('resources', 'MA-region-simple.tmg'))
    for line in file.readlines():
        _highway_data.append(line[:-1])    # chomp '\n'
    return _highway_data
