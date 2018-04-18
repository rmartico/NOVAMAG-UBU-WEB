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
        "&saturation_magnetization_min=" + str(dict["saturation_magnetization_min"]) + \
        "&saturation_magnetization_max=" + str(dict["saturation_magnetization_max"]) + \
        "&unit_cell_formation_enthalpy_min=" + str(dict["unit_cell_formation_enthalpy_min"]) + \
        "&unit_cell_formation_enthalpy_max=" + str(dict["unit_cell_formation_enthalpy_max"]) + \
        "&atomic_species=" + dict["atomic_species"]+ \
        "&species_count=" + str(dict["species_count"]) + \
        "&stechiometry_atom=" + str(dict["stechiometry_atom"]) + \
        "&stechiometry_value_min=" + str(dict["stechiometry_value_min"]) + \
        "&stechiometry_value_max=" + str(dict["stechiometry_value_max"])

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
    smd_mind = form.saturation_magnetization_min.data
    smd_maxd = form.saturation_magnetization_max.data
    ucfe_mind = form.unit_cell_formation_enthalpy_min.data
    ucfe_maxd = form.unit_cell_formation_enthalpy_max.data
    asd = form.atomic_species.data
    scd = form.species_count.data
    sad = form.stechiometry_atom.data
    sv_mind = form.stechiometry_value_min.data
    sv_maxd = form.stechiometry_value_max.data

    return "compound_space_group_min=" + str(csg_mind) + "&compound_space_group_max=" + str(csg_maxd) + "&saturation_magnetization_min=" + str(smd_mind) + "&saturation_magnetization_max=" + str(smd_maxd) +\
        "&unit_cell_formation_enthalpy_min=" + str(ucfe_mind) + "&unit_cell_formation_enthalpy_max=" + str(ucfe_maxd) + "&atomic_species=" + replace_ampersand_by_minus(clean_spaces(asd)) + "&species_count=" + str(scd) + "&stechiometry_atom=" + str(sad) + \
        "&stechiometry_value_min=" + str(sv_mind) + "&stechiometry_value_max=" + str(sv_maxd)


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