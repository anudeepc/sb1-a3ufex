from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField
from wtforms.validators import DataRequired

class ReceiptForm(FlaskForm):
    merchant = StringField('Merchant', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    total = FloatField('Total', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('utilities', 'Utilities'),
        ('other', 'Other')
    ], validators=[DataRequired()])