from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/pricing', methods=['GET'])
def get_user_page2():
    return render_template('pricing.html')

@index_views.route('/buy', methods=['GET'])
def get_user_page3():
    return render_template('buy.html')

@index_views.route('/about', methods=['GET'])
def get_user_page4():
    return render_template('about.html')


