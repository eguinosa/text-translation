# Gelin Eguinosa Rosique

import sys
import warnings
from time_keeper import TimeKeeper
from multi_translator import MultiTranslator
from os import mkdir
from os.path import isdir, isfile, join


# Turn off warnings
warnings.filterwarnings('ignore')

# Record the runtime of the program
stopwatch = TimeKeeper()

if __name__ == '__main__':
    # Get the target language
    lang_dict = {'english': 'en', 'spanish': 'es'}
    print("\nBecause of internet limits, these are the available languages:")
    print(', '.join(lang_dict.keys()).title())
    stopwatch.pause()
    answer = input("\nTo which language would you like to translate? ")
    stopwatch.restart()
    answer = answer.lower().strip()
    if answer not in lang_dict:
        print("\nLanguage not supported.")
        sys.exit()
    # Save the target language
    target_lang = lang_dict[answer]

    # Check the docs folder exists, create one if it doesn't.
    if not isdir('docs'):
        mkdir('docs')

    # Load the Multi-Translator
    print("\nLoading the Multi-Translator.")
    translator = MultiTranslator(target_lang)
    print("Done.")
    print(f"[{stopwatch.run_time()}]")

    # Check if the user would like to translate a documents
    stopwatch.pause()
    answer = input("\nWould you like to translate a Document? [yes/no] ")
    stopwatch.restart()
    if answer.lower().strip() in ['yes', 'y']:
        # Ask the location of the document:
        print("\nThe document most be located inside the 'docs' folder.")
        stopwatch.pause()
        answer = input("What's the name of the file? ")
        stopwatch.restart()
        file_path = join('docs', answer)

        # Exit the program if the file doesn't exit
        if not isfile(file_path):
            print("\nFile not found.")
            sys.exit()

        # Load the file.
        print("\nLoading document.")
        with open(file_path, 'r') as file:
            file_text = file.read()

        # Translate the text
        print("Translating the Document.")
        text_translation = translator.text_translation(file_text)
        print("Done.")
        print(f"[{stopwatch.run_time()}]")

        # Saving the information in a .txt
        translation_path = join('docs', 'translation.txt')
        with open(translation_path, 'w') as file:
            file.write(text_translation)
        print("The result was saved in 'translation.txt' inside the 'docs' folder.")

        # Close the program.
        sys.exit()

    # Check if the user would like to translate something using the console:
    stopwatch.pause()
    answer = input("\nWould you like to use the console to translate? [yes/no] ")
    stopwatch.restart()
    if answer.lower().strip() not in ['yes', 'y']:
        sys.exit()

    while True:
        # Get the text the user wants to translate
        stopwatch.pause()
        answer = input("\nPlease, type what you would like to translate."
                       " (q/quit to exit)\n-> ")
        stopwatch.restart()
        if answer.lower().strip() in ['q', 'quit', 'exit']:
            break

        # Translate the text
        print("\nTranslating Text.")
        translation = translator.text_translation(answer)
        print("\nTranslation:")
        print(translation)
        print(f"[{stopwatch.run_time()}]")
