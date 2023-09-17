import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    
    try:
        file = request.files["file_give"]
        format_file = file.filename.split('.')[-1]
        filename = f'static/file-{date_time}.{format_file}'
        file.save(filename)

        profile = request.files["profile_give"]
        format_file = profile.filename.split('.')[-1]
        profilename = f'static/profile-{date_time}.{format_file}'
        profile.save(profilename)
    except:
        filename = None;
        profilename = None;
        print('File not uploaded')

    date_time = now.strftime("%Y.%m.%d")

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': date_time
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'Diary Posted'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
