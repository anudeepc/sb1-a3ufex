from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_security import login_required, current_user
from . import receipts
from .forms import ReceiptForm
from ..models import Receipt
from .. import db, ocr
from werkzeug.utils import secure_filename
import os

# ... (existing code) ...

@receipts.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_receipt(id):
    receipt = Receipt.query.get_or_404(id)
    form = ReceiptForm(obj=receipt)
    if form.validate_on_submit():
        form.populate_obj(receipt)
        db.session.commit()
        flash('Receipt updated successfully.', 'success')
        return redirect(url_for('receipts.list_receipts'))
    return render_template('receipts/edit.html', form=form, receipt=receipt)

@receipts.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_receipt():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract information using OCR
            receipt_data = ocr.extract_receipt_info(file_path)
            
            # Save receipt to database
            new_receipt = Receipt(
                user_id=current_user.id,
                file_path=file_path,
                merchant=receipt_data['merchant'],
                date=receipt_data['date'],
                total=receipt_data['total'],
                category=receipt_data['category']
            )
            db.session.add(new_receipt)
            db.session.commit()
            
            return jsonify({'message': 'Receipt uploaded successfully'}), 200
        return jsonify({'error': 'File type not allowed'}), 400
    return render_template('receipts/upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']