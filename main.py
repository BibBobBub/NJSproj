from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .crawler import main_function
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/tracker_send', methods=['POST'])
@login_required
def tracker_send():
    tracker = str(request.form.get('tracker'))
    print(tracker)
    main_function(tracker, current_user.id)
    #db.session.
    print(Research_1.query.filter_by(id=1))
    return render_template('tracker.html', name=current_user.name)

@main.route('/tracker')
@login_required
def tracker():
    return render_template('tracker.html', name=current_user.name, )