import unittest
from app import create_app, db
from app.models import User, Receipt
from datetime import date

class ReceiptsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # Create a test user
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_upload_receipt(self):
        # Login the user
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)

        # Test receipt upload
        with open('tests/test_receipt.jpg', 'rb') as img:
            response = self.client.post('/receipts/upload', data={
                'file': (img, 'test_receipt.jpg')
            }, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Receipt uploaded successfully', response.data)

    def test_list_receipts(self):
        # Create a test receipt
        user = User.query.filter_by(email='test@example.com').first()
        receipt = Receipt(user_id=user.id, merchant='Test Store', date=date.today(), total=100.00, category='Other')
        db.session.add(receipt)
        db.session.commit()

        # Login the user
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)

        # Test listing receipts
        response = self.client.get('/receipts/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Store', response.data)

if __name__ == '__main__':
    unittest.main()