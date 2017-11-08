from persistence.novamag_entities_v06 import Item

from persistence.parser_search_query import parse_with_and


def query_items_with_and(session, search_term):
    """
    Queries the material features of current material that contains all the atoms.

    :param session: database session
    :param search_term: text with one or several atoms
    :return: items containing ALL the atoms in the search term
    :rtype: list of Item
    """
    try:
        atoms = parse_with_and(search_term)
        #print('Lista de atoms: ', atoms)
        query = session.query(Item)
        for atom in atoms:
            query = query.filter(Item.formula.contains(atom))
        #print(query)
        return query
    finally:
        session.close()


def query_items(session, search_term):
    """
    Queries the material features of current material.

    :param session: database session
    :param search_term: search term
    :return: items containing the search term
    :rtype: list of Item
    """
    try:
        # atoms = parse_with_and()_
        return session.query(Item).filter(Item.formula.contains(search_term))
    finally:
        session.close()


def query_item_features(session, mafid):
    """
    Queries the material features of current material.

    :param session: database session
    :param mafid: id. of material
    :return: material feature
    :rtype: MaterialFeature
    """
    try:
        list_item_features = session.query(Item).filter(Item.mafid == mafid)
        return list_item_features[0]
    finally:
        session.close()


# def query_materials(session, search_term):
#     """
#     Query for materials containing certain atoms.
#
#     :param session: database session
#     :param search_term: text to find
#     :return: materiasl that contain the search term
#     :rtype: list of Material
#     """
#     # TODO optimize queries...
#     try:
#         list_material = []
#         for instance in session.query(Molecule).filter(Molecule.formula.contains(search_term)):
#             result_material = session.query(Material).filter(Material.formula == instance.formula)
#             for material in result_material:
#                 list_material.append(material)
#         return list_material
#     finally:
#         session.close()


# def query_material_feature(session, matId):
#     """
#     Queries the material features of current material.
#
#     :param session: database session
#     :param matId: id. of material
#     :return: material feature
#     :rtype: MaterialFeature
#     """
#     try:
#         list_material_feature = session.query(MaterialFeature).filter(MaterialFeature.matid == matId)
#         material_feature = list_material_feature[0]
#         return material_feature
#     finally:
#         session.close()

if __name__ == '__main__':
    print('Not yet implemented')
