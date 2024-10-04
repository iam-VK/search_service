#!/bin/bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm