from __future__ import division # Avoid problems with integer division in Python 2.7

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from persistence import transform_basic_tables

import config
import math

from persistence.database_access_object import query_items, query_item_features, query_items_with_and
from persistence.novamag_entities_v06 import Atom, Molecule

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
engine = db.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=10)
SessionMaker = db.sessionmaker(bind=engine)

PAGE_SIZE = 5  # Size of records per page

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

@app.route('/search', methods=['POST', 'GET'])
def search_result():
    if request.method == 'GET':
        app.logger.error('%s using get method', 'texto')
        return redirect(url_for('main_page'))
    else:
        app.logger.error('%s using post method', 'texto')
        search_term = request.form['query']
        # Refactoring: move code to fun query_materials
        list_item = query_items_with_and(SessionMaker(), search_term)
        total = list_item.count()
        return render_template('items.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                               current_page=1, list_item=list_item[:PAGE_SIZE])


@app.route('/search_paginate/', methods=['POST', 'GET'])
def paginate_result():
    search_term = request.args.get('search_term')
    page = request.args.get('page')
    list_item = query_items_with_and(SessionMaker(), search_term)
    total = list_item.count()
    init_record = ((int(page) - 1) * PAGE_SIZE)
    end_record = init_record + PAGE_SIZE
    return render_template('items.html', search_term=search_term, total=total, pages=int(math.ceil(total / PAGE_SIZE)),
                           current_page=page,
                           list_item=list_item[init_record:end_record])


@app.route('/show_item_features', methods=['GET'])
def show_item_features():
    mafid = request.args.get('mafid')
    # Refactoring: move code to fun query_material_features
    item_features = query_item_features(SessionMaker(), mafid)
    return render_template('itemFeatures.html', item_features=item_features, transformer=transform_basic_tables)

if __name__ == '__main__':
    #Bootstrap(app)
    #app.run(host='0.0.0.0') Acccess from other machines
    app.run() # Acccess only from local
