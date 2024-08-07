from flask import Flask, render_template
from application.config import Config
from application.database import db
from application.model import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if not Role.query.filter_by(name = 'admin').first():
            admin = Role(name='admin', description = 'Admin Role') 
            db.session.add(admin)
        if not Role.query.filter_by(name='Influencer').first():
            Influencer = Role(name='Influencer', description = 'Influencer Role')
            db.session.add(Influencer)
        if not Role.query.filter_by(name='Sponsor').first():
            Sponsor = Role(name='Sponsor', description = 'Sponsor Role')
            db.session.add(Sponsor)

        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='Helloworld',email='admin@gmail.com', address='Website Owner', role = [admin])
            db.session.add(admin_user)

        db.session.commit()

    return app
app = create_app()

from application.routes import *

if __name__ == "__main__":
    app.run(debug = True)