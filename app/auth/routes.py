from flask import redirect, url_for, flash
from flask_security import login_required, logout_user
from . import auth
from ..models import User
from .. import oauth

@auth.route('/login')
def login():
    return oauth.google.authorize_redirect(url_for('auth.callback', _external=True))

@auth.route('/login/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(email=user_info['email'], name=user_info['name'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('Logged in successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))