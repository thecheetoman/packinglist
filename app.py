import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, 'checklist.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
ADMIN_PASSWORD = os.environ.get('CHECKLIST_ADMIN_PW', 'changeme')

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(200), nullable=False)
    where_to_put = db.Column(db.String(300), nullable=True)
    where_to_find = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.String(100), nullable=True)
    checked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tool': self.tool,
            'where_to_put': self.where_to_put,
            'where_to_find': self.where_to_find,
            'quantity': self.quantity,
            'checked': self.checked,
        }


def init_db():
    with app.app_context():
        db.create_all()


@app.before_request
def ensure_db():
    init_db()


@app.route('/')
def index():
    items = Item.query.order_by(Item.checked.asc(), Item.created_at.asc()).all()
    return render_template('index.html', items=items)


@app.route('/toggle/<int:item_id>', methods=['POST'])
def toggle(item_id):
    item = Item.query.get_or_404(item_id)
    item.checked = not item.checked
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if pw == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        flash('Invalid password', 'error')
    return render_template('login.html')


@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return wrapper


@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    if request.method == 'POST':
        tool = request.form.get('tool')
        where_to_put = request.form.get('where_to_put')
        where_to_find = request.form.get('where_to_find')
        quantity = request.form.get('quantity')
        if not tool:
            flash('Tool name is required', 'error')
        else:
            item = Item(tool=tool, where_to_put=where_to_put, where_to_find=where_to_find, quantity=quantity)
            db.session.add(item)
            db.session.commit()
            flash('Item added', 'success')
            return redirect(url_for('admin'))
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('admin.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
