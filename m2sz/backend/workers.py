
from datetime import datetime
from flask import current_app as app, make_response, Response, render_template,render_template_string
import pandas as pd
import json
from celery.schedules import crontab
import yagmail
from jinja2 import Template

import os

from datetime import datetime as dt

from celery import Celery
from main import app
from celery.schedules import crontab
from flask_mail import Mail, Message
from models import Userlogin, Book, Show


celery = Celery(__name__)
celery.conf.update(
    broker_url='redis://127.0.0.1:6379/0',
    result_backend='redis://127.0.0.1:6379/0',
    timezone='Asia/Kolkata',
    task_trace=False,
    worker_prefetch_multiplier=1,
)




@celery.task(name='celery.send_nemail')
def send_nemail():
    # Assuming you have a User and Ticket model or table # Import your User and Ticket models
    with app.app_context():
    
        users = Userlogin.query.all()  # Fetch all users from the database
    
        for userlogin in users:
        # Check if the user ID is in the ticket table as euserid
            book = Book.query.filter_by(fuid=userlogin.uid).first()
        
            if book:
            # User booked the tickets, send the email
                subject = 'Daily reminder'
                body='hi {}, thankyou for booking'.format(userlogin.usname1)
                
                
                yag = yagmail.SMTP(user='yanamadalasainikhil@gmail.com', password='urjcbrctgmthxwre')
                yag.send(to=userlogin.email, subject=subject, contents=body)
            else:
            # User did not book the tickets, send the email
                subject = 'Daily reminder'
                body='hi {}, new release!.'.format(userlogin.usname1)
                
                
                yag = yagmail.SMTP(user='yanamadalasainikhil@gmail.com', password='urjcbrctgmthxwre')
                yag.send(to=userlogin.email, subject=subject, contents=body)










    # Get the first and last day of the previous month
    

# Define a Celery task to send the monthly entertainment report email
@celery.task(name='celery.mnreport')
def mnreport():
    with app.app_context():
    
    
    # Fetch all users from the database
           users = Userlogin.query.all()

    # Create an HTML report for each user
           for user in users:
        # Fetch tickets booked by the user in the previous month
                tickets = Book.query.filter(Book.fuid == user.uid).all()
                if tickets:
                                total_bookings = sum(ticket.bookings for ticket in tickets)
                                template = """
                                                <html>
                                                    <body>
                                                        <h1>Monthly Report</h1>
                                                         <h4>Please find the below details of the monthly report of this month</h4><br>
                                                                <div>
                                                                    
                                                                    <h5 style="color:green">no of tickets {{data1}}</h5>
                                                                    
                                                                </div>
                                                        
                                                    </body>
                                                </html>
                                            """
                                rendered_template = render_template_string(template,  data1=total_bookings)
                                with open('report.html', 'w', encoding='utf-8') as file:
                                     file.write(rendered_template)
                                
                                subject = 'Monthly Report'
                                body='Please find the below attachment for the Monthly report'
                            
                                yag = yagmail.SMTP(user='yanamadalasainikhil@gmail.com', password='urjcbrctgmthxwre')
                                yag.send(to=user.email, subject=subject, contents=body, attachments=['report.html'])
                    
                                      



# Celery Beat schedule to run the task on the first day of each month
celery.conf.beat_schedule = {
    'send_nemail': {
        'task': 'celery.send_nemail',
        'schedule': crontab(hour=18, minute=55),  # Adjust the time as per your requirement
    },
    # 'celery.send_csv_report': {
    #     'task': 'celery.send_csv_report',
    #     'schedule': crontab(hour=17, minute=49),  # Adjust the time as per your requirement
    # },
    'mnreport': {
        'task': 'celery.mnreport',
        'schedule': crontab(day_of_month='10', hour='18', minute='57'),  # Run on the first day of each month at midnight
    },
}

