#     Copyright (C) 2017-2018 UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056
#     http://crono.ubu.es/novamag
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056  see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.

from __future__ import division # Solving probems with Python 2.x

from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from persistence import transform_basic_tables
from persistence import parser_search_query

import config
import math

from persistence.database_access_object import query_item_features, query_items_with_and, \
    query_attached_files_of_item, query_authors_of_item, restore_image, restore_unitcell_jpg, quey_items_by_formula, \
    query_items_by_advanced_search, query_items_by_advanced_search_with_query_string, init_atoms, set_session_maker, ATOMS, \
    query_items_by_plotting_tool_search, filter_items_before_plotting_tool

from persistence.parser_search_query import contains_ampersand, replace_ampersand_by_minus, replace_minus_by_ampersand, \
    parse_form_to_query_search, parse_dict_to_query_string, has_only_one_atom

# FLASK Set up
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = config.SECRET_KEY # avoid CSRF with WTF

# DATABASE Set up
db = SQLAlchemy(app)
engine = db.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=10)
SessionMaker = db.sessionmaker(bind=engine)
set_session_maker(SessionMaker)
# Looad initially the atom list.
init_atoms()
# Load the advanced forms after loading the dynamic list
from advanced_search_form import AdvancedSearchForm
from plotting_tool_search_form import PlottingToolSearchForm

# PRESENTATION Set up
PAGE_SIZE = 10  # Size of records per page

# WEB APP Code...

# Well-Known Error Pages

@app.route('/')
@app.route('/index.html')
def main_page():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/errors/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('/errors/403.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('/errors/500.html'), 500

# Business logic

@app.route('/search', methods=['POST', 'GET'])
def search_result():
    """
    Basic search.
    """
    if request.method == 'GET':
        app.logger.error('%s using get method', 'texto')
        return redirect(url_for('main_page'))
    else:
        app.logger.error('%s using post method', 'texto')
        search_term = request.form['query']
        search_term = ''.join(search_term.split()) # remove all space, tab, etc.
        # Refactoring: move code to find query_materials
        atoms = init_atoms()
        if not contains_ampersand(search_term) or has_only_one_atom(search_term, atoms):
             # find by formula
            list_item = quey_items_by_formula(search_term)
        else:
            # find by elements
            list_item = query_items_with_and(search_term)

        total = len(list_item)
        num_pages = math.ceil(total / PAGE_SIZE)
        if total == 0:
            current_page = 0
        else:
            current_page = 1

        search_term = replace_ampersand_by_minus(search_term)
        return render_template('items.html', search_term=search_term, total=total,
                               pages=int(math.ceil(total / PAGE_SIZE)), current_page=current_page, first_page=current_page,
                               list_item=list_item[:PAGE_SIZE], parser=parser_search_query, transformer=transform_basic_tables)



@app.route('/search_paginate/', methods=['POST', 'GET'])
def paginate_result():
    """
    Basic search with pages.
    """
    search_term = request.args.get('search_term')
    search_term = replace_minus_by_ampersand(search_term)
    page = request.args.get('page')
    if (not contains_ampersand(search_term)):
        list_item = quey_items_by_formula(search_term)
    else:
        list_item = query_items_with_and(search_term)
    total = len(list_item)
    init_record = ((int(page) - 1) * PAGE_SIZE)
    end_record = init_record + PAGE_SIZE
    search_term = replace_ampersand_by_minus(search_term)

    if total == 0:
        first_page = 0
    else:
        first_page = 1

    return render_template('items.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                           current_page=page, first_page=first_page,
                           list_item=list_item[init_record:end_record], parser=parser_search_query, transformer=transform_basic_tables)



@app.route('/loadimage/<int:id>')
def show_image(id):
    #type: (int) -> image
    """
    Sending images.
    """
    logo = restore_unitcell_jpg(id)
    if logo is not None:
        return app.response_class(logo, mimetype='application/octet-stream')
    else:
        return send_file('static/images/image_not_found.png', mimetype='image/png')



@app.route('/download/<name>')
def download_image(name):
    """
    Downloads the file image from database.

    :param name: image name
    :type name: str
    :return: file image
    :rtype: blob
    """
    list = name.split('&')
    id = list[0]
    file_name = list[1]
    logo = restore_image(id, file_name)
    response = app.response_class(logo, mimetype='application/octet-stream')
    return response


# Advanced search

import traceback

@app.route('/show_item_features', methods=['GET'])
def show_item_features():
    """
    Shows item features.
    """
    try:
        mafid = request.args.get('mafid')
        # Refactoring: move code to fun query_material_features
        item_features = query_item_features(mafid)
        attached_files = query_attached_files_of_item(mafid)
        authors = query_authors_of_item(mafid)
        return render_template('itemFeatures.html', item_features=item_features, attached_files=attached_files,
                           authors=authors, transformer=transform_basic_tables)
    except:
        traceback.print_exc()
        # if the user try to find a confidential iterm by id will be redirecterd here
        return render_template('/errors/404.html'), 404


@app.route('/advanced_search')
def advanced_search():
    """
    Renders the advanced search form.
    """
    form = AdvancedSearchForm()
    return render_template('advanced_search.html', form=form)


@app.route('/advanced_search_run', methods=['POST'])
def advanced_search_run():
    """
    Collects the advanced search form.
    """
    form = AdvancedSearchForm()
    if form.validate_on_submit():

        list_item = query_items_by_advanced_search(form)
        search_query = parse_form_to_query_search(form)

        total = len(list_item)
        num_pages = math.ceil(total / PAGE_SIZE)

        if total == 0:
            current_page = 0
        else:
            current_page = 1

        return render_template('items_advanced_search.html', search_term=search_query, total=total,
                               pages=int(math.ceil(total / PAGE_SIZE)), current_page=current_page, first_page=current_page,
                               list_item=list_item[:PAGE_SIZE], parser=parser_search_query, transformer=transform_basic_tables)
    else:
        #DEBUG print("non validate on submit")
        #DEBUG print(form.is_submitted(), form.validate())
        pass

    return render_template('advanced_search.html', form=form)


@app.route('/advanced_search_paginate/', methods=['POST', 'GET'])
def advanced_search_paginate_result():
    """
    Paginates the result from the advanced search.
    """
    page = request.args.get('page')
    init_record = ((int(page) - 1) * PAGE_SIZE)
    end_record = init_record + PAGE_SIZE

    list_item = query_items_by_advanced_search_with_query_string(request.args)
    search_term = parse_dict_to_query_string(request.args)
    total = len(list_item)
    if total == 0:
        first_page = 0
    else:
        first_page = 1

    return render_template('items_advanced_search.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                           current_page=page, first_page=first_page,
                           list_item=list_item[init_record:end_record], parser=parser_search_query, transformer=transform_basic_tables)

##############################
# Plotting tool new urls
##############################
import persistence.transform_basic_tables as transformer


@app.route('/plotting_tool_search')
def plotting_tool_search():
    """
    Renders the advanced search form.
    """
    formP = PlottingToolSearchForm()
    return render_template('plotting_tool_search.html', form=formP)

@app.route('/plotting_tool_search_run', methods=['POST'])
def plotting_tool_search_run():
    print("Iniciando...")
    """
    Collects the plotting search form.
    """
    form = PlottingToolSearchForm()

    # Obtain data from database and filter null/None values
    list_items = query_items_by_plotting_tool_search(form)
    list_items = filter_items_before_plotting_tool(list_items, form.x_axis.data, form.y_axis.data)

    # Prepare data
    axis = [ form.x_axis.data, form.y_axis.data]
    elements = [form.element1.data, form.element2.data]


    # if any axis is Stoichiometry ("stechiometry" ;)) obtain new data column for the axis
    # we need to generate an "artificial calculated" new column" because this is not stored in database
    stoichiometry_axis_values = list()
    if axis[0] == 'stechiometry' or axis[1] == 'stechiometry': # if user select stoichiometry...
        stoichiometry_axis_values = transform_basic_tables.stoichiometry_calculate_axis_values(list_items, elements)
        print(stoichiometry_axis_values)


    # extract tuples with (key, descriptor +  units) for print key and text for axis
    list_choices = [(p[0], (p[1][0] + ' ' + p[1][1]).rstrip()) for p in transform_basic_tables.AXIS_CHOICES.items()]
    dict_choices = dict(list_choices) # convert to dict
    axis_print = [ dict_choices[form.x_axis.data], dict_choices[form.y_axis.data]]
    # Exception with stoichiometry
    if axis[0] == 'stechiometry':
        axis_print[0] = elements[0] + transform_basic_tables.one_minus_x_sub + elements[1] + transform_basic_tables.x_sub
    if axis[1] == 'stechiometry':
        axis_print[1] = elements[0] + transform_basic_tables.one_minus_x_sub + elements[1] + transform_basic_tables.x_sub
    # End

    # Debug
    # generate a trace with csv format for export
    print('mafid,formula, stoichiometry, x, y ')
    for item in list_items:
        if axis[0] != 'stechiometry' and axis[1] != 'stechiometry':
            print(str(item.mafid) + "," + item.formula + "," + item.molecule.stechiometry + "," + str(getattr(item, form.x_axis.data)) + "," + str(getattr(item, form.y_axis.data)))
        elif axis[0] == 'stechiometry' and axis[1] != 'stechiometry':
            print(str(item.mafid) + "," + item.formula + "," + item.molecule.stechiometry + "," + str(stoichiometry_axis_values[list_items.index(item)]) + "," + str(getattr(item, form.y_axis.data)))
        elif axis[0] != 'stechiometry' and axis[1] == 'stechiometry':
            print(str(item.mafid) + "," + item.formula + "," + item.molecule.stechiometry + "," + str(getattr(item, form.x_axis.data)) + "," + str(stoichiometry_axis_values[list_items.index(item)]))
        else:
            print(str(item.mafid) + "," + item.formula + "," + item.molecule.stechiometry + "," + str(stoichiometry_axis_values[list_items.index(item)]) + "," + str(stoichiometry_axis_values[list_items.index(item)]))

    # Render html page with data...
    return render_template('plotting_tool_chart.html', axis=axis, axis_print=axis_print, elements=elements, items=list_items,
                           total_records=len(list_items), transformer=transform_basic_tables, stoichiometry_axis_values=stoichiometry_axis_values)

####################################
# End of plotting tools new urls
####################################

if __name__ == '__main__':
    #app.run(host='0.0.0.0') Acccess from other machines
    app.run(debug=True) # Acccess only from local
