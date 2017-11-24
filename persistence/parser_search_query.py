import re

def parse_dict_to_query_string(dict):
    """
    Parses dict with query string to string

    :param dict: dictionary
    :type: dict
    :return: params as quey string
    :rtype: string
    """
    return \
        "compound_space_group_min=" + str(dict["compound_space_group_min"]) + \
        "&compound_space_group_max=" + str(dict["compound_space_group_max"]) + \
        "&saturation_magnetization=" + str(dict["saturation_magnetization"]) + \
        "&unit_cell_formation_enthalpy=" + str(dict["unit_cell_formation_enthalpy"]) + \
        "&atomic_species=" + dict["atomic_species"]+ \
        "&species_count=" + str(dict["species_count"]) + \
        "&stechiometry_atom=" + str(dict["stechiometry_atom"]) + \
        "&stechiometry_value=" + str(dict["stechiometry_value"])

def parse_form_to_query_search(form):
    # type: (AdvancedSearchForm) -> str
    """
    Parses the text query search giving the list with ampersand characters betweeen parameters.

    :param form: form with advanced search
    :type: AdvancedSearchForm
    :return: params as quey string
    :rtype: list of strings
    """
    csg_mind = form.compound_space_group_min.data
    csg_maxd = form.compound_space_group_max.data
    smd = form.saturation_magnetization.data
    ucfed = form.unit_cell_formation_enthalpy.data
    asd = form.atomic_species.data
    scd = form.species_count.data
    sad = form.stechiometry_atom.data
    svd = form.stechiometry_value.data

    return "compound_space_group_min=" + str(csg_mind) + "&compound_space_group_max=" + str(csg_maxd) + "&saturation_magnetization=" + str(smd) + \
        "&unit_cell_formation_enthalpy=" + str(ucfed) + "&atomic_species=" + replace_ampersand_by_minus(clean_spaces(asd)) + "&species_count=" + str(scd) + "&stechiometry_atom=" + str(sad) + \
        "&stechiometry_value=" + str(svd)


def parse_with_and(text):
    # type: (str) -> List
    """
    Parses the text query search giving the list between & character.

    :param text: text with search query
    :return: atom list
    :rtype: list of strings
    """
    # first convert to lower and then capitalize
    text = correct_captitalized_letters(text)
    text = clean_spaces(text)
    text = text + "&"
    return re.findall('([A-Za-z]+)&', text)


def correct_captitalized_letters(text):
    # type: (str) -> str
    """
    Corrects capital letters at the beginning of the atom.

    :param text: text with search query
    :return: text with capitalized atoms
    :rtype: string
    """
    return text.lower().title()


def contains_ampersand(text):
    # type: (str) -> str
    """
    Searchs for an ampersand.

    :param text: text with search query
    :return: True if contains any ampersand
    :rtype: bool
    """
    return '&' in text


def replace_ampersand_by_minus(text):
    # type: (str) -> str
    """
    Replaces ampersand symbol by minus symbol in the query string.
    Note: problems parsing the query string, we need to replace the symbol inside a parameter.

    :param text: query search
    :return: query search
    """
    return text.replace('&', '-')

def replace_minus_by_ampersand(text):
    # type: (str) -> str
    """
    Replaces minus symbol by ampersand symbol.
    Note: recover the original text.

    :param text: text
    :return: text
    """
    return text.replace('-', '&')


def clean_spaces(text):
    # type: (str) -> str
    """
    Clean the white symbols in the string.

    :param text: text
    :return: text without white symbols
    """
    return text.replace(' ','')


def has_only_one_atom(search_term, ATOMS_LIST):
    # type: (str, List) -> bool
    """
    Checks if current search term contains only one atom.

    :param search_term: text with search query
    :param ATOM_LIST: constant list of atoms
    :return: True if contains only one atom
    :rtype: bool
    """
    return search_term in ATOMS_LIST