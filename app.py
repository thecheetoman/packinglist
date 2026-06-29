import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(app.instance_path, 'checklist.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
ADMIN_PASSWORD = os.environ.get('CHECKLIST_ADMIN_PW', 'changeme')

# IMPORTANT
LOCATIONS = ['Drawer 1', 'Drawer 2', 'Drawer 3', 'Shelf A', 'Shelf B', 'Cabinet', 'Closet', 'Under Bed', 'Other']

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    where_to_put = db.Column(db.String(300), nullable=True)
    where_to_find = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.String(100), nullable=True)
    checked = db.Column(db.Boolean, default=False)
    checked_by = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    where_to_put = db.Column(db.String(300), nullable=True)
    where_to_find = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.String(100), nullable=True)
    checked = db.Column(db.Boolean, default=False)
    checked_by = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


_db_initialized = False


def init_db():
    global _db_initialized
    if _db_initialized:
        return
    db.create_all()
    _db_initialized = True


@app.before_request
def ensure_db():
    init_db()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('join'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Username is required', 'error')
            return render_template('join.html')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['username'] = username
        if not session.get('admin'):
            session['admin'] = False
        return redirect(url_for('index'))
    return render_template('join.html')


@app.route('/logout')
def user_logout():
    session.pop('username', None)
    return redirect(url_for('join'))


@app.route('/mode', methods=['POST'])
@login_required
def set_mode():
    mode = request.form.get('mode', 'tools')
    if mode in ('tools', 'parts'):
        session['mode'] = mode
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    mode = session.get('mode', 'tools')
    if mode == 'parts':
        items = Part.query.order_by(Part.checked.asc(), Part.created_at.asc()).all()
    else:
        items = Item.query.order_by(Item.checked.asc(), Item.created_at.asc()).all()
    return render_template('index.html', items=items, mode=mode)


@app.route('/item/<int:item_id>')
@login_required
def item_detail(item_id):
    mode = session.get('mode', 'tools')
    if mode == 'parts':
        item = Part.query.get_or_404(item_id)
    else:
        item = Item.query.get_or_404(item_id)
    location_image = None
    if item.location:
        for ext in ('png', 'jpg', 'jpeg', 'webp', 'gif'):
            path = os.path.join(app.static_folder, 'images', 'locations', f'{item.location}.{ext}')
            if os.path.exists(path):
                location_image = f'images/locations/{item.location}.{ext}'
                break
    return render_template('item_detail.html', item=item, locations=LOCATIONS, mode=mode, location_image=location_image)


@app.route('/toggle/<int:item_id>', methods=['POST'])
@login_required
def toggle(item_id):
    mode = session.get('mode', 'tools')
    if mode == 'parts':
        item = Part.query.get_or_404(item_id)
    else:
        item = Item.query.get_or_404(item_id)
    item.checked = not item.checked
    item.checked_by = session.get('username') if item.checked else None
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/leads/login', methods=['GET', 'POST'])
def leads_login():
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if pw == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('leads'))
        flash('Invalid password', 'error')
    return render_template('leads_login.html')


@app.route('/leads/logout')
def leads_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('leads_login'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/leads', methods=['GET', 'POST'])
@admin_required
def leads():
    if request.method == 'POST':
        kind = request.form.get('kind', 'tool')
        tool = request.form.get('tool')
        location = request.form.get('location')
        where_to_find = request.form.get('where_to_find')
        quantity = request.form.get('quantity')
        if not tool:
            flash('Name is required', 'error')
        else:
            Model = Part if kind == 'part' else Item
            item = Model(tool=tool, location=location, where_to_find=where_to_find, quantity=quantity)
            db.session.add(item)
            db.session.commit()
            flash('Item added', 'success')
            return redirect(url_for('leads'))
    items = Item.query.order_by(Item.created_at.desc()).all()
    parts = Part.query.order_by(Part.created_at.desc()).all()
    return render_template('leads.html', items=items, parts=parts, locations=LOCATIONS)


@app.route('/leads/reset', methods=['POST'])
@admin_required
def leads_reset():
    Item.query.delete()
    Part.query.delete()
    db.session.commit()
    flash('All tools and parts cleared. Usernames preserved.', 'success')
    return redirect(url_for('leads'))


if __name__ == '__main__':
    app.run(debug=True)
