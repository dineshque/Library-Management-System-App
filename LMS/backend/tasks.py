from celery import shared_task
from application.models import UserBook, User, Role
from email_config import send_message
from application.models import User, Role
from jinja2 import Template
from datetime import datetime
from datetime import datetime as date, timedelta


@shared_task(ignore_result=True)
def daily_reminder(subject):
     
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    
    for user in users:
        last_visited_time = user.last_visited
        current_time = datetime.now()
        time_difference = current_time - last_visited_time

        if time_difference >= timedelta(minutes=1):
            with open('templates/daily_remander.html','r') as f:
                template = Template(f.read())
                send_message(user.email, subject,template.render(username= user.username))
            
    return 'Daily Remainder Sent'

@shared_task(ignore_result=True)
def monthly_reminder(subject):
     
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    current_date_time = date.now()
    month_Before_time = current_date_time - timedelta(days=30)
    for user in users:
        user_books = UserBook.query.filter_by(user_id = user.id).all()
        issued_date = []
        book_name = []
        book_ratings = []
        for user_book in user_books:
            database_date = str(user_book.issued_date)
            issued_date_ = datetime.strptime(database_date.split()[0], "%Y-%m-%d")
            if issued_date_>= month_Before_time:
                issued_date.append(datetime.strptime(str(user_book.issued_date).split()[0], "%Y-%m-%d"))
                book_name.append(user_book.book.name)
                if user_book.book_status == 4:
                    book_ratings.append(user_book.rate)
                else:
                    book_ratings.append('')
        
        data = { 'issued_date':issued_date, 'book_name':book_name, 'book_ratings':book_ratings }                
            

                
        with open('templates/monthly_remander.html','r') as f:
            template = Template(f.read())
            send_message(user.email, subject,template.render(username= user.username, data = data))
        
    return 'Monthly Remainder Sent'