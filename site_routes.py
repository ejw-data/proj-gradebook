from flask import Blueprint, render_template, jsonify
from query import feedback_most_recent

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return render_template('index.html')

@site.route('/unit')
def unit():
    feedback = feedback_most_recent()
    return render_template('unit.html', feedback= feedback)

@site.route('/session')
def session():
    return render_template('session.html')

@site.route('/class')
def classes():
    return render_template('class.html')

@site.route('/student')
def student():
    return render_template('student.html')