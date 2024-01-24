from flask import Flask,render_template,request
from other import dbs,app
from flask_restful import Resource, Api
import yagmail
from api import VAPI,SAPI,ULAPI,LoginAPI,ProtectedAPI,BAPI
from models import Userlogin,Show,Venue
import json
import os
from flask import Flask
from flask_restful import Resource, Api

import pandas as pd

from celery import Celery
from config import LocalDevelopmentConfig,Config

from flask_security import Security, SQLAlchemySessionUserDatastore

from flask_jwt_extended import JWTManager


# Replace this secret key with a strong and secure random string






from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
api = Api(app)



app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
jwt = JWTManager(app)


# Import all the controllers so they are loaded

api=None





api=Api(app)

api.add_resource(LoginAPI,"/api/loginpostv")

api.add_resource(ULAPI,"/api/uloginpost")
api.add_resource(VAPI,"/api/venueget","/api/venuepost","/api/venuedelete/<int:venuein>","/api/venueput/<int:venuein>")
api.add_resource(SAPI,"/api/showget/<int:venuein>","/api/showpost/<int:venuein>","/api/showdelete/<int:showin>","/api/showput/<int:showin>")
api.add_resource(BAPI,"/api/bookget/<int:showin>","/api/bookpost/<int:showin>/<int:uid>")

     
 

# # # Define routes
# 
 
celery = Celery(app.name,broker_url='redis://127.0.0.1:6379/0',result_backend='redis://127.0.0.1:6379/0')        

from flask import send_file

@app.route('/download_csv', methods=['GET'])
def download_csv():
    vid = request.args.get('vid', type=int)
    if vid is not None:
        task = send_csv_report.delay(vid=vid)
        result = task.get(timeout=10)
        if result:
            return send_file(result, as_attachment=True, download_name='user_details.csv')
    return "Error generating CSV file."

@celery.task(name='celery.send_csv_report')
def send_csv_report(vid):
    with app.app_context():
        venue = Venue.query.get(vid)
        vdata = {
            'vid': [venue.vid],
            'venue': [venue.venue],
            'loc': [venue.loc],
        }
        df = pd.DataFrame(vdata)

        # Convert DataFrame to a CSV string
        csv_string = df.to_csv(index=False)
        csv_file_path = 'user_details.csv'
        with open(csv_file_path, 'w', encoding='utf-8') as file:
            file.write(csv_string)
        
        return csv_file_path

            

if __name__=='__main__':
   app.run(debug=True)



# @app.route('/find',methods=['POST'])
# def find():
    
#     if request.method == 'POST':

#           loc=request.form['FIND']

          

#           venues = Venue.query.filter_by(loc=loc).all()
          

#     return render_template('venuedisp.html', venues=venues)
# @app.route('/findu',methods=['POST'])
# def findu():
    
#     if request.method == 'POST':

#           showna=request.form['FIND']

          

#           shows = Show.query.filter_by(showname=showna).all()
          

#     return render_template('showdispu.html', shows=shows)

# @app.route('/reg')
# def reg():
#     return render_template('reg.html')

# @app.route('/venue' , methods = ['GET','POST'])
# def venue():
#      if request.method == 'GET':
        
#        return render_template('venue.html')
#      elif request.method == 'POST':
          
          
#           s=Venue(venue = request.form['NAME'], loc = request.form['LOCATION'],cap =request.form['CAPACITY'])
#           dbs.session.add(s)
#           dbs.session.commit()
          
#           venues=Venue.query.all()
#           return render_template('venuedisp.html',venues=venues)
# @app.route('/venuedelete/<int:vid>', methods=['GET','POST'])
# def venuedelete(vid):
#          venued=Venue.query.filter_by(vid = vid).first()
#          dbs.session.delete(venued)
#          dbs.session.commit()
#          venues=Venue.query.all()
#          return render_template('venuedisp.html',venues=venues)
     
# @app.route('/venueedit/<int:vid>', methods=['GET','POST'])
# def venueedit(vid):
#          venuet=Venue.query.filter_by(vid = vid).first()
#          if request.method == 'GET':
#              return render_template("venuedup.html",venuet=venuet)
#          elif request.method == 'POST':
#              e=venuet.vid
         
#              dbs.session.delete(venuet)
#              s=Venue(vid = e, venue = request.form["NAME"],loc = request.form['LOCATION'],cap =request.form['CAPACITY'])
#              dbs.session.add(s)
#              dbs.session.commit()
#              venues=Venue.query.all()
#              return render_template('venuedisp.html',venues=venues)

# @app.route('/s/<int:vid>',methods = ['GET','POST'])
# def show(vid):
#      tt=vid
#      venuet=Venue.query.filter_by(vid=vid).first()
     
#      if request.method == 'GET':
       
#        return render_template('show.html', venuet=venuet)
#      elif request.method == 'POST':
          
          
#           st=Show(uu=tt ,bookings=request.form['B'],showname = request.form['NAME'], rating = request.form['RATING'],genre =request.form['TYPE'],runtime=request.form['RT'])
#           dbs.session.add(st)
#           dbs.session.commit()
          
#           shows=venuet.showz
#           print (shows,venuet)
#           return render_template('showdisp.html', venuet=venuet, shows=shows)


# @app.route('/show/<int:vid>',methods = ['GET','POST'])
# def show4(vid):
#      tt=vid
#      venuet=Venue.query.filter_by(vid=vid).first()
     
#      if request.method == 'GET':
#        shows=venuet.showz
#        return render_template('showdisp.html', venuet=venuet, shows=shows)
     
# @app.route('/showdelete/<int:sid>/<int:vid>', methods=['GET','POST'])
# def showdelete(sid,vid):
            
#             showt=Show.query.filter_by(sid=sid).first()
        
#             venuet=Venue.query.filter_by(vid=vid).first()
#             dbs.session.delete(showt)
            
            
#             dbs.session.commit()
#             shows=venuet.showz
            
#             return render_template('showdisp.html',showt=showt,venuet=venuet,shows=shows)
     
     
# @app.route('/showedit/<int:sid>/<int:vid>', methods=['GET','POST'])
# def showedit(sid,vid):
         
#          venuet=Venue.query.filter_by(vid=vid).first()
#          showt=Show.query.filter_by(sid = sid).first()
#          if request.method == 'GET':
#              return render_template("showdup.html",venuet=venuet,showt=showt)
#          elif request.method == 'POST':
#              e=showt.sid
#              b=showt.bookings
#              #showt.rating=request.form['RATING']
#             #  showt.genre=request.form['TYPE']
#             #  showt.showname=request.form['NAME']
#             #  showt.
#              dbs.session.delete(showt)
#              sc=Show(sid = e,bookings=b,showname=request.form['NAME'] ,rating = request.form['RATING'],genre =request.form['TYPE'],runtime =request.form['RT'])
#              dbs.session.add(sc)
#              dbs.session.commit()
#              shows=venuet.showz
            
#              return render_template('showdisp.html',showt=showt,venuet=venuet,shows=shows)

# @app.route('/user',methods=['GET','POST'])
# def user():
#     if request.method == 'GET':
        
#        return render_template('user.html')
#     elif request.method == 'POST':
#         user_name = request.form['NAME']
#         hashed_password =  request.form['PASSWORD']
#         user = Userlogin.query.filter_by(usname1=user_name).first()

#         if user==None:
            
          
          
#             x=Userlogin(usname1 = request.form['NAME'], pass1 =hashed_password,email = request.form['email'])
#             dbs.session.add(x)
#             dbs.session.commit()
         
          
          
          
#             venues=Venue.query.all()
#             return render_template('userdisp.html',venues=venues)
#         else:
#             venues=Venue.query.all()
#             return render_template('userdisp.html',venues=venues)

# @app.route('/user/<int:vid>',methods=['GET','POST'])
# def user1(vid):
#     venue=Venue.query.filter_by(vid=vid).first()
#     shows=venue.showz
#     if request.method == 'GET':
        
#        return render_template('showdispu.html',shows=shows)   

    

# @app.route('/booking/<int:sid>',methods=['GET','POST'])
# def book(sid):
#     show=Show.query.filter_by(sid=sid).first()
   
#     if request.method == 'GET':
#        print(show.bookings)  
#        return render_template('booking.html',show=show)
    
#     else:
#         available=show.bookings
        
        
#         if available < int(request.form['TICKETS']):
#             return render_template('booking.html',show=show,message="enter valid number")
           
#         else:
#             show.bookings-=int(request.form['TICKETS'])
#             dbs.session.commit()
#             return render_template('booking.html',show=show,message="booking sucessful")
# @app.route('/feed',methods=['GET','POST'])
# def feed():
#     if request.method == 'GET':
#        return render_template('feed.html')
#     elif request.method == 'POST':
          
          
#           f=Feedback(feedback = request.form['F'])
#           dbs.session.add(f)
#           dbs.session.commit()
#           venues=Venue.query.all()
          
          
#           return render_template('userdisp.html',venues=venues)


# @app.route('/sum')
# def sum():
       
#         sh = Show.query.all()
#         (labels, bookings) = ([], [])
#         for l in sh:
#             labels.append(l.showname)
#             bookings.append(l.bookings)
            
            
       
       
#         return render_template('sum.html',labels = json.dumps(labels), bookings= json.dumps(bookings)   )
   
     
      

