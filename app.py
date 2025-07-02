from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    point_balance = db.Column(db.Integer, nullable=False, default=0)

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.Text)

class UserCharacter(db.Model):
    __tablename__ = 'user_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='심사대기')

class PatchGroup(db.Model):
    __tablename__ = 'patch_groups'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    patch_group_id = db.Column(db.Integer, db.ForeignKey('patch_groups.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=50)
    meta_data = db.Column(db.JSON)
    original_image_url = db.Column(db.String(500), nullable=False)
    web_image_url = db.Column(db.String(500), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (
        db.UniqueConstraint('package_id', 'patch_group_id', 'is_default', name='uix_default'),
    )

class UserCharacterCustomization(db.Model):
    __tablename__ = 'user_character_customizations'
    user_character_id = db.Column(db.Integer, db.ForeignKey('user_characters.id'), primary_key=True)
    patch_group_id = db.Column(db.Integer, db.ForeignKey('patch_groups.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.first():
        user = User(point_balance=1000)
        db.session.add(user)
        db.session.commit()
    import os
    os.makedirs('web_images', exist_ok=True)
    os.makedirs('pod_images', exist_ok=True)

# Routes
@app.route('/packages')
def list_packages():
    packages = Package.query.all()
    data = []
    for p in packages:
        data.append({'id': p.id, 'name': p.name, 'status': p.status, 'thumbnail': p.thumbnail_url})
    return jsonify(data)

@app.route('/purchase', methods=['POST'])
def purchase_item():
    data = request.json
    user = User.query.get(data['user_id'])
    item = Item.query.get(data['item_id'])
    if not user or not item:
        return jsonify({'error': 'Invalid user or item'}), 400
    if user.point_balance < item.price:
        return jsonify({'error': 'Not enough points'}), 400
    user.point_balance -= item.price
    db.session.commit()
    return jsonify({'message': 'purchased'})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files['image']
    uid = str(uuid.uuid4())
    import os
    os.makedirs('web_images', exist_ok=True)
    os.makedirs('pod_images', exist_ok=True)
    web_path = os.path.join('web_images', f'{uid}.webp')
    pod_path = os.path.join('pod_images', f'{uid}{file.filename[file.filename.rfind("."):]}' )
    from PIL import Image
    img = Image.open(file.stream)
    img.save(pod_path)
    img.save(web_path, format='WEBP', quality=85)
    return jsonify({'web_url': web_path, 'original_url': pod_path})

if __name__ == '__main__':
    app.run(debug=True)
