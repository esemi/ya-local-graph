# -*- coding: utf-8 -*-

from flask import render_template

from app import app


@app.route('/version.txt', methods=['GET'])
def version():
    return app.send_static_file('version.txt')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


