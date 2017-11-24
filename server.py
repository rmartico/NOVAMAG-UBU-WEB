from __future__ import division # Solving probems with Python 2.x

from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from persistence import transform_basic_tables
from persistence import parser_search_query

import config
import math

from persistence.database_access_object import query_items, query_item_features, query_items_with_and, \
    query_attached_files_of_item, query_authors_of_item, restore_image, restore_unitcell_jpg, quey_items_by_formula, \
    query_items_by_advanced_search, query_items_by_advanced_search_with_query_string, init_atoms, set_session_maker, ATOMS

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
# Load the advanced form after loading the dynamic list
from advanced_search_form import AdvancedSearchForm

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
            print("Searching by formula")
            list_item = quey_items_by_formula(search_term)
        else:
            # find by elements
            print("Searching by items")
            list_item = query_items_with_and(search_term)

        print(type(list_item))
        total = len(list_item)
        print('Total items', type(total))
        print(type(PAGE_SIZE))
        print(total)
        num_pages = math.ceil(total / PAGE_SIZE)
        print(type(num_pages))
        print(math.ceil(total / PAGE_SIZE))
        search_term = replace_ampersand_by_minus(search_term)
        return render_template('items.html', search_term=search_term, total=total,
                               pages=int(math.ceil(total / PAGE_SIZE)), current_page=1,
                               list_item=list_item[:PAGE_SIZE], parser=parser_search_query)


@app.route('/search_paginate/', methods=['POST', 'GET'])
def paginate_result():
    """
    Basic search with pages.
    """
    search_term = request.args.get('search_term')
    print('Search term paginating', search_term)
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
    return render_template('items.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                           current_page=page,
                           list_item=list_item[init_record:end_record], parser=parser_search_query)

"""
Sending images
"""


@app.route('/loadimage/<int:id>')
def show_image(id):
    logo = restore_unitcell_jpg(id)
    if logo is not None:
        return app.response_class(logo, mimetype='application/octet-stream')
    else:
        return send_file('static/images/image_not_found.png', mimetype='image/png')



@app.route('/download/<name>')
def download_image(name):
    id = request.args.get('mafid')
    file_name = request.args.get('file_name')
    logo = restore_image(id, file_name)
    response = app.response_class(logo, mimetype='application/octet-stream')
    return response

""""
Advanced searc
"""
import traceback

@app.route('/show_item_features', methods=['GET'])
def show_item_features():
    """
    Shows item features.
    """
    try:
        mafid = request.args.get('mafid')
        # Refactoring: move code to fun query_material_features
        print("Mafid "+  mafid)
        item_features = query_item_features(mafid)
        print("1")
        attached_files = query_attached_files_of_item(mafid)
        print("2")
        authors = query_authors_of_item(mafid)
        print("3")
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
    print(form.errors)
    if form.validate_on_submit():

        list_item = query_items_by_advanced_search(form)
        search_query = parse_form_to_query_search(form)

        print(type(list_item))
        total = len(list_item)
        print('Total items', type(total))
        print(type(PAGE_SIZE))
        print(total)
        num_pages = math.ceil(total / PAGE_SIZE)
        print(type(num_pages))
        print(math.ceil(total / PAGE_SIZE))

        return render_template('items_advanced_search.html', search_term=search_query, total=total,
                               pages=int(math.ceil(total / PAGE_SIZE)), current_page=1,
                               list_item=list_item[:PAGE_SIZE], parser=parser_search_query)
    else:
        print("non validate on submit")
        print(form.is_submitted(), form.validate())

    return render_template('advanced_search.html', form=form)


@app.route('/advanced_search_paginate/', methods=['POST', 'GET'])
def advanced_search_paginate_result():
    """
    Paginates the result from the advanced search.
    """
    page = request.args.get('page')
    list_item = query_items_by_advanced_search_with_query_string(request.args)
    search_term = parse_dict_to_query_string(request.args)
    total = len(list_item)
    init_record = ((int(page) - 1) * PAGE_SIZE)
    end_record = init_record + PAGE_SIZE
    return render_template('items_advanced_search.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                           current_page=page,
                           list_item=list_item[init_record:end_record], parser=parser_search_query)

if __name__ == '__main__':
    #Bootstrap(app)
    #app.run(host='0.0.0.0') Acccess from other machines
    app.run() # Acccess only from local
