from flask import jsonify
from flask_security import login_required, current_user
from . import drive
from ..models import Receipt
from .. import google_drive

@drive.route('/sync')
@login_required
def sync_with_drive():
    # Create a folder for the app if it doesn't exist
    folder_id = google_drive.create_or_get_folder(current_user.id)
    
    # Upload new receipts to Google Drive
    new_receipts = Receipt.query.filter_by(user_id=current_user.id, synced=False).all()
    for receipt in new_receipts:
        file_id = google_drive.upload_file(receipt.file_path, folder_id)
        receipt.drive_file_id = file_id
        receipt.synced = True
    
    db.session.commit()
    return jsonify({'message': 'Sync completed successfully'}), 200

@drive.route('/list')
@login_required
def list_drive_files():
    folder_id = google_drive.create_or_get_folder(current_user.id)
    files = google_drive.list_files(folder_id)
    return jsonify(files), 200