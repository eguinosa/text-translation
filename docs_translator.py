# Gelin Eguinosa Rosique

import sys
import warnings
import pickle
from pprint import pprint
from os import listdir, mkdir
from os.path import isdir, isfile, join
from multi_translator import MultiTranslator
from index_creation import files_index


# Ignore warnings
warnings.filterwarnings('ignore')

# Documents locations
docs_folder = 'documents'
translation_folder = 'translations'
docs_prefix = 'document_'
translation_prefix = 'translation_'
docs_index_file = 'index_documents.pickle'
trans_index_file = 'index_translations.pickle'

# Create Spanish translator
print("Creating the Spanish translator.")
translator = MultiTranslator('es')

# Check the documents folder exist
if not isdir(docs_folder):
    # Close the program
    sys.exit()

# Check if the translation folder exists:
if not isdir(translation_folder):
    # Create the folder
    mkdir(translation_folder)

# Iterate through all the elements in the documents folder and translate them.
for file_name in listdir(docs_folder):
    # Create the path of the file
    file_path = join(docs_folder, file_name)
    # Check if we are loading the intended documents.
    if not isfile(file_path):
        continue
    if not file_name.startswith(docs_prefix):
        continue
    if not file_name.endswith('.txt'):
        continue

    # Load the content of the document
    print(f"\nLoading the content of: {file_name}")
    with open(file_path, 'r') as file:
        text = file.read()

    # Translate the content of the document
    print(f"Translating the content of: {file_name}")
    translation = translator.translation(text)

    # Save the translation
    translation_file = translation_prefix + file_name
    translation_path = join(translation_folder, translation_file)
    print(f"Saving the translation in: {translation_file}")
    with open(translation_path, 'w') as file:
        file.write(translation)

# Create the index of the documents
print("\nCreating the Index of the Documents.")
docs_index = files_index(docs_folder, docs_prefix, '.txt')

# Save the index of the documents
docs_index_path = join(docs_folder, docs_index_file)
with open(docs_index_path, 'wb') as file:
    pickle.dump(docs_index, file)

# Create the index of the translations
print("Creating the Index of the Translations.")
translation_index = files_index(translation_folder, translation_prefix + docs_prefix, '.txt')

# Save the index of the translations
translations_index_path = join(translation_folder, trans_index_file)
with open(translations_index_path, 'wb') as file:
    pickle.dump(translation_index, file)

# Load the Saved index to check if they were saved properly
with open(docs_index_path, 'rb') as file:
    new_docs_index = pickle.load(file)
with open(translations_index_path, 'rb') as file:
    new_trans_index = pickle.load(file)

# Print them in the console.
print("\nThe Documents in the Index:")
pprint(new_docs_index)
print("\nThe Translations in the Index:")
pprint(new_trans_index)
