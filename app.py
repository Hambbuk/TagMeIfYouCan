# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import threading
import uuid
from datetime import timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(BASE_DIR, 'instance')
db_path = os.path.join(db_dir, 'image_classification.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Ensure the instance directory exists
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(200), nullable=False, unique=True)
    processed = db.Column(db.Boolean, default=False)
    is_flicker = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(50), nullable=True)
    page_number = db.Column(db.Integer, nullable=True)

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    processed_images_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

# 이미지 폴더 경로 설정
IMAGE_FOLDER = 'images'
all_images = os.listdir(IMAGE_FOLDER)

# Initialize images in the database if not already present
with app.app_context():
    existing_images = {img.image_name for img in Image.query.with_entities(Image.image_name).all()}
    new_images = [img for img in all_images if img not in existing_images]
    for img in new_images:
        new_image = Image(image_name=img)
        db.session.add(new_image)
    db.session.commit()

lock = threading.Lock()
active_ips = set()

def get_unprocessed_images(limit=32):
    return Image.query.filter_by(processed=False).limit(limit).all()

def update_status():
    total_images = len(all_images)
    processed_images_count = Image.query.filter_by(processed=True).count()
    flicker_images_count = Image.query.filter_by(is_flicker=True).count()
    remaining_images = total_images - processed_images_count
    active_users = len(active_ips)
    return {
        "total_images": total_images,
        "remaining_images": remaining_images,
        "processed_images": processed_images_count,
        "flicker_images": flicker_images_count,
        "active_users": active_users
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_session', methods=['POST'])
def start_session():
    user_id = str(uuid.uuid4())
    session['user_id'] = user_id

    with lock:
        ip_address = request.remote_addr
        active_ips.add(ip_address)

    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id)
        db.session.add(user)
    db.session.commit()
    return jsonify({"status": "Session started", "user_id": user_id})

@app.route('/load_images/<int:page>', methods=['GET'])
def load_images(page):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not assigned"}), 400

    images_per_page = 32

    with lock:
        prev_images = Image.query.filter_by(user_id=user_id, page_number=page).all()
        if prev_images:
            images_to_show = [(img.image_name, img.is_flicker) for img in prev_images]
        else:
            unprocessed_images = get_unprocessed_images(images_per_page)
            images_to_show = [(img.image_name, img.is_flicker) for img in unprocessed_images]

            for image in unprocessed_images:
                image.user_id = user_id
                image.page_number = page
                image.processed = True

            db.session.commit()

        status = update_status()

    return jsonify({
        'images': [{'image_name': img, 'is_flicker': is_flicker} for img, is_flicker in images_to_show],
        'status': status
    })

@app.route('/select_image', methods=['POST'])
def select_image():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not assigned"}), 400

    data = request.get_json()
    image_name = data.get('image_name')
    is_flicker = data.get('is_flicker')

    image_entry = Image.query.filter_by(user_id=user_id, image_name=image_name).first()
    if image_entry:
        image_entry.is_flicker = is_flicker
        image_entry.processed = True
        db.session.commit()

        user = User.query.get(user_id)
        user.processed_images_count += 1
        db.session.commit()

    status = update_status()
    return jsonify({"status": "Success", "updated_status": status})

@app.route('/static/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/status')
def status():
    status = update_status()
    return jsonify(status)

@app.route('/end_session', methods=['POST'])
def end_session():
    user_id = session.get('user_id')
    if user_id:
        with lock:
            ip_address = request.remote_addr
            active_ips.discard(ip_address)
        session.pop('user_id', None)
    return jsonify({"status": "Session ended"})

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
