import pytesseract
from PIL import Image
import re

def extract_receipt_info(image_path):
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    
    # Parse the extracted text to find relevant information
    merchant = extract_merchant(text)
    date = extract_date(text)
    total = extract_total(text)
    category = categorize_receipt(text)
    
    return {
        'merchant': merchant,
        'date': date,
        'total': total,
        'category': category
    }

def extract_merchant(text):
    # Implement logic to extract merchant name
    # This is a simplified example and may need to be improved
    lines = text.split('\n')
    return lines[0] if lines else ''

def extract_date(text):
    # Implement logic to extract date
    # This is a simplified example and may need to be improved
    date_pattern = r'\d{1,2}/\d{1,2}/\d{2,4}'
    match = re.search(date_pattern, text)
    return match.group(0) if match else ''

def extract_total(text):
    # Implement logic to extract total amount
    # This is a simplified example and may need to be improved
    total_pattern = r'\$?\d+\.\d{2}'
    matches = re.findall(total_pattern, text)
    return max(matches, key=lambda x: float(x.replace('$', ''))) if matches else ''

def categorize_receipt(text):
    # Implement logic to categorize the receipt
    # This is a simplified example and may need to be improved
    categories = {
        'food': ['restaurant', 'cafe', 'grocery'],
        'travel': ['airline', 'hotel', 'car rental'],
        'utilities': ['electric', 'water', 'gas'],
        'other': []
    }
    
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return 'other'