from flask import render_template
from flask_security import login_required, current_user
from . import main
from ..models import Receipt
from sqlalchemy import func

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    recent_receipts = Receipt.query.filter_by(user_id=current_user.id).order_by(Receipt.date.desc()).limit(5).all()
    
    # Calculate total spending by category
    category_totals = db.session.query(
        Receipt.category, func.sum(Receipt.total)
    ).filter_by(user_id=current_user.id).group_by(Receipt.category).all()
    
    return render_template('dashboard.html', recent_receipts=recent_receipts, category_totals=category_totals)