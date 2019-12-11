from flask import Flask, render_template, request, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    ads = relationship("Advertisement")


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


user_manager = UserManager(app, db, User)


@app.route('/')
def home():
    ads = Advertisement.query.order_by(Advertisement.date_created).all()
    return render_template('home.html', ads=ads)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_ad():
    if request.method == 'POST':
        ad = Advertisement()

        ad.title = request.form['title']
        ad.content = request.form['description']
        ad.price = request.form['price']
        ad.user_id = current_user.id

        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'

    return render_template('new.html')


@app.route('/ad/<ad_id>')
def profile(ad_id):
    ad = Advertisement.query.get(ad_id)
    owner = User.query.get(ad.user_id)
    return render_template('ad.html', ad=ad, owner=owner)


@login_required
@app.route('/delete/<ad_id>', methods=['POST'])
def delete(ad_id):
    ad = Advertisement.query.get(ad_id)

    if ad.user_id != current_user.id:
        return "Nie możesz usunąć tego ogłoszenia"

    try:
        db.session.delete(ad)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error'

@login_required
@app.route('/myads')
def myads():
    return render_template('myads.html')

if __name__ == '__main__':
    app.run(debug=True)
