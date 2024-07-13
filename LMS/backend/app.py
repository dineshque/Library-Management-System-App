from flask import Flask
from flask_security import Security
from werkzeug.security import  generate_password_hash
from application.models import db, User, Role
from application.resource import api
from application.security import datastore
from application.cache_instance import cache
from flask_cors import CORS 
from config import DevelopmentConfig
from workers import celery_init_app
from celery.schedules import crontab
from tasks import daily_reminder, monthly_reminder

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    app.security = Security(app, datastore)
    cache.init_app(app)
    CORS(app)
    with app.app_context():
        import application.views

    return app

app = create_app()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=14, minute=24, day_of_week='*'),
        daily_reminder.s('Daily Remainder'),
    )
    
    sender.add_periodic_task(
        crontab(hour=14,minute=24, day_of_month='*'),
        monthly_reminder.s('Monthly Report'),
    )
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        lib_role = Role(name='librarian', description='Librarian desc')
        db.session.add(lib_role)
        
        user_role = Role(name='user', description='User desc')
        db.session.add(user_role)
        
        try:
            db.session.commit()
            role = Role.query.filter_by(name='librarian').first()
            admin = datastore.find_user(email="librarian@gmail.com")
            if not admin:
                hashed_password = generate_password_hash('123456', method='pbkdf2:sha256')
                datastore.create_user(username="Librarian",
                                    email="librarian@gmail.com",
                                    password=hashed_password,
                                    roles=[role])
                db.session.commit()
        except Exception as e:
            print("Error while committing Role Model:", e)
    
    app.run(host="0.0.0.0", debug=True)
