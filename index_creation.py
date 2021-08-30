# Gelin Eguinosa Rosique

from os import listdir
from os.path import isdir, isfile, join


def files_index(folder_path, files_prefix, files_suffix):
    """
    Create an index of the files in the given folder with the given prefix and
    suffix.
    :param folder_path: The folder where the documents we want to index are.
    :param files_prefix: The prefix of the files we want to index.
    :param files_suffix: The suffix of the files we want to index.
    :return: A dictionary with the id of the files, where the id is the string
    of characters between the prefix and the suffix '<prefix><ID><suffix>'.
    """
    # Dictionary where the file names will be saved.
    index = {}

    # Check if the directory exists.
    if not isdir(folder_path):
        return index

    # Go through the files inside the folder.
    for file_name in listdir(folder_path):
        # Create the path of the file
        file_path = join(folder_path, file_name)

        # Check if we have one of the intended files
        if not isfile(file_path):
            continue
        if not file_name.startswith(files_prefix):
            continue
        if not file_name.endswith(files_suffix):
            continue

        # Create the id of the file with string between prefix and suffix.
        i = len(files_prefix)
        j = len(files_suffix)
        file_id = file_name[i:-j]
        # Check we don't have an empty value
        if not file_id:
            raise Exception("The ID of the file can't be an empty value.")

        # Save the file in the index
        index[file_id] = file_name

    # Return the created index of the files.
    return index
