
from setuptools import setup, find_packages

setup(
    name='dp-PDF-Crawler',
    version='0.3.0',  # Update version as needed
    description='A custom Flask package with PDF processing tools',
    packages=find_packages(),
    install_requires=[
    'fitz==0.0.1.dev2',
    'Flask==3.0.2',
    'langdetect==1.0.9',
    'nltk==3.6.7',
    'numpy==1.24.3',
    'openai==0.28.1',
    'opencv_python==4.8.1.78',
    'pandas==2.0.3',
    'pdf2image==1.16.3',
    'pdfminer.six==20221105',
    'pdfplumber==0.10.2',
    'Pillow==10.2.0',
    'pytesseract==0.3.10',
    'Requests==2.31.0',
    'scipy==1.12.0',
    'sentence_transformers==2.2.2',
    'tensorflow==2.13.1',
    'timeout_decorator==0.5.0',
    'torch==2.1.0',
    'transformers==4.35.2',
    'ultralytics==8.0.153',
    'waitress==3.0.0',
    'Werkzeug==3.0.1'
        ],
)