# align_document_image
Small flask / computer vision project that takes a scanned image of document and returns the aligned image in base64 encoding and saves the aligned image to results directory. 

## Setup

1. Clone the repo
```bash
git clone https://github.com/AwaleSajil/align_img_document
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Update the absolute path of the two directories (uploads and results) in config.py file
```bash
upload_dir = r"C:\.......\align_img_document\uploads"
result_dir = r"C:\.......\align_img_document\results"
```

## Problem 1: Endpoint to take image and return the aligned image in base64 encoding

1. Run the Flask app
```bash
python app.py
```
2. Browse http://127.0.0.1:5000/
3. Upload image(s) and Sumbit

![alt text](https://github.com/AwaleSajil/align_img_document/blob/main/read_me_img/upload_img.png?raw=true)

