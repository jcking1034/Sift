# TODO: Add support for tags (learning types)
from flask import render_template, request, jsonify
from app import app

import pandas as pd


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')


# Example: http://127.0.0.1:5000/list?page=good&tag=visual
@app.route('/list')
def get_list():
    page = request.args.get('page', None)
    tag = request.args.get('tag', None)
    if not page:
        return 'No page given'
    if not tag:
        return 'No tag given'
    return get_list_dict(page, tag)


# Example: http://127.0.0.1:5000/update?name=aaa
@app.route('/update')
def update_popularity():
    name = request.args.get('name', None)
    if not name:
        return 'No name given'
    
    data = pd.read_csv('./data.csv')
    data.loc[data['name'] == name, ['popularity']] = data.loc[data['name'] == name, ['popularity']].apply(lambda x: x + 1) 
    data = data[['page', 'tag', 'name', 'link', 'popularity']]
    data.to_csv('./data.csv')

    return get_list_dict('biology', 'visual')


# Example: http://127.0.0.1:5000/add?page=good&tag=visual&name=abc&link=qqq
@app.route('/add')
def add_item():
    page = request.args.get('page', None)
    tag = request.args.get('tag', None)
    name = request.args.get('name', None)
    link = request.args.get('link', None)
    if not page:
        return 'No page given'
    elif not tag:
        return 'No tag given'
    elif not name:
        return 'No name given'
    elif not link:
        return 'No link given'

    new_item = pd.DataFrame({
        'page': [page.lower()], 
        'tag': [tag.lower()], 
        'name': [name.lower()], 
        'link': [link.lower()],
        'popularity': [0]
        })
    
    data = pd.read_csv('./data.csv')
    data = data.append(new_item)
    data = data.drop_duplicates(['page', 'tag', 'name', 'link'])
    data = data.reset_index()
    data = data[['page', 'tag', 'name', 'link', 'popularity']]

    data.to_csv('./data.csv')

    return get_list_dict(page, tag)


def get_list_dict(page, tag):
    ''' This function needs to get the names and links for page '''
    data = pd.read_csv('./data.csv')
    p = data[(data['page'] == page.lower()) & (data['tag'] == tag)]
    p = p.sort_values(by=['popularity'])
    names = list(p['name'])
    links = list(p['link'])

    return {
        'names': names,
        'links': links,
        }
