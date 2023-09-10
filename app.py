from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient
from datetime import datetime

connect_mongo = 'mongodb+srv://xander:Aa13245768@cluster0.hgsq4xy.mongodb.net/'
client = MongoClient(connect_mongo)
db = client.dbxander


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

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'Diary Posted'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
