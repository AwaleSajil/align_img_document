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
