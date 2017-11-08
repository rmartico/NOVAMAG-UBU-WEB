import re

def parse_with_and(text):
    """
    Parses the text query search givin the list between & character.
    :param test: text with search query
    :return: atom list
    :rtype: list of strings
    """
    # firt convert to lower and then capitalize
    text = correct_captitalized_letters(text)
    return re.findall('&*([A-Za-z]+)', text)


def correct_captitalized_letters(text):
    """
    Corrects capital letters at the beginning of the atom.

    :param text: text with search query
    :return: text with capitalized atoms
    :rtype: string
    """
    return text.lower().title()
