#!/bin/sh

rm -rf db.sqlite3 faiss_index.idx
python manage.py migrate
