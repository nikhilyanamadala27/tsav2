from flask import Flask
from flask_restful import Resource, fields, marshal_with, reqparse,marshal
from flask_security import auth_required
from models import dbs
from models import Venue,Show,Userlogin
from validation import NotFoundError, BusinessValidationError
from flask import Flask,render_template,request,make_response,jsonify
from flask import Flask, request
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with,output_json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import Userlogin, Venue, Show, dbs,Book
from validation import BusinessValidationError, NotFoundError
import bcrypt
from flask_caching import Cache
from other import app

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/1', 'CACHE_DEFAULT_TIMEOUT':100})


        

        

    
ul_fields = {
    
      'usname1' : fields.String,
    'email':fields.String,
     'pass1':fields.String,
    
}
ul_parser = reqparse.RequestParser()
ul_parser.add_argument('usname1')
ul_parser.add_argument('pass1')
ul_parser.add_argument('email')

class ULAPI(Resource):
    # @auth_required("token")
    # def get(self, email):
    #     user = Userlogin.query.filter_by(email=email).first()
    #     data = {}
    #     data['id'] = user.uid
    #     data['name'] = user.usname
     
    #     return datafrom flask import Flask, request

# Your other imports and app setup code here


    
    @marshal_with(ul_fields)
    def post(self):
        args = request.get_json()
        
        email = args.get('email', None)
        username = args.get('usname1', None)
        password = args.get('pass1', None)
        
   
        if email is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' loc is required')
       

        if username is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' Name is required')
        if password is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' loc is required')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        l = Userlogin(email=email,usname1=username,pass1=hashed_password)
        dbs.session.add(l)
        dbs.session.commit()
        return l, 201


class LoginAPI(Resource):
    def post(self):
        args = ul_parser.parse_args()
        usname1 = args.get('usname1', None)  # Updated field name
        pass1 = args.get('pass1', None)      # Updated field name
        email = args.get('email', None) 
        user = Userlogin.query.filter_by(usname1=usname1).first()

        if not user:
            return {"message": "User not found"}, 404

        if user.pass1 and bcrypt.checkpw(pass1.encode('utf-8'), user.pass1):
            # Authentication successful, create an access token
            # access_token = create_access_token(identity=user.id)
            access_token = create_access_token(identity={"uid": user.uid,"usname1": user.usname1})

            return {"message": "Login successful", "access_token": access_token}
        else:
            return {"message": "Invalid credentials"}, 401


class ProtectedAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return current_user_id
    



venue_fields = {
    'venue': fields.String,
    'vid': fields.Integer,
    'loc': fields.String,
    'cap': fields.Integer,
    'showz' : fields.String
}

v_parser = reqparse.RequestParser()
v_parser.add_argument('venue')
v_parser.add_argument('loc')
v_parser.add_argument('cap')


vu_parser = reqparse.RequestParser()
vu_parser.add_argument('venue')
vu_parser.add_argument('cap')
vu_parser.add_argument('loc')
class VAPI(Resource):
    CACHE_KEY="venues_data"
    @cache.cached(timeout=100,key_prefix=CACHE_KEY)
    @jwt_required()
    @marshal_with(venue_fields)
    def get(self):
       # venueget = dbs.session.query(Venue).filter(Venue.venue==venuein).first()
        
        all_venues = Venue.query.all()

        venues_data = [{"vid":venue.vid, "venue": venue.venue, "loc": venue.loc, "cap": venue.cap} for venue in all_venues]
        return venues_data


    @marshal_with(venue_fields)
    def post(self):
        args = v_parser.parse_args()
        venue = args.get('venue', None)
        loc = args.get('loc', None)
        cap = args.get('cap', None)
   
        

        if venue is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' Name is required')
        if loc is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' loc is required')
        if cap is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' cap is required')
       
        venuepost = dbs.session.query(Venue).filter(Venue.venue==venue).first()
        if venuepost:
            raise BusinessValidationError(status_code=400, error_code='002', error_message=' Name already exists')
        
        l = Venue(venue=venue, loc=loc,cap=cap)
        dbs.session.add(l)
        dbs.session.commit()
        cache.delete(self.CACHE_KEY)
        return l, 201
    
    def delete(self, venuein):
        l = Venue.query.get(venuein)
        print(l)
        S= Show.query.filter_by(uu=venuein).first()
        print(S)
        if l is None:
            raise NotFoundError(status_code=404)
        else:
            if S is None:
                 dbs.session.delete(l)
                 dbs.session.commit()
            else:
              dbs.session.delete(S)
              dbs.session.commit()
              dbs.session.delete(l)
              dbs.session.commit()
        cache.delete(self.CACHE_KEY) 
        return "Successfully Deleted"
            
   
        
        

    @marshal_with(venue_fields)
    def put(self, venuein):
        l = Venue.query.filter_by(vid=venuein).first()
        if not l:
            raise NotFoundError(status_code=404)
        else:
            store = l.vid
            dbs.session.delete(l)
            
            
            args = vu_parser.parse_args()
            l.vid = store
            l.venue = args.get('venue')
            l.cap = args.get('cap')
            l.loc = args.get('loc')
            dbs.session.add(l)  # Re-add the modified object to the session
            dbs.session.commit() # Commit the changes to the database
        cache.delete(self.CACHE_KEY)
        return l, 200

       



show_fields = {
    'sid': fields.Integer,
    'genre': fields.String,
    'showname': fields.String,
    'booking': fields.Integer,
    
}

s_parser = reqparse.RequestParser()

s_parser.add_argument('showname')

s_parser.add_argument('genre')
s_parser.add_argument('sid')
s_parser.add_argument('bookings')


su_parser = reqparse.RequestParser()
su_parser.add_argument('showname')
su_parser.add_argument('genre')
su_parser.add_argument('bookings')
class SAPI(Resource):
    @marshal_with(show_fields)
    def get(self, venuein):
        showget1 = Show.query.filter_by(uu=venuein).all()

        showget = [{"sid":show.sid, "showname": show.showname, "genre": show.genre, "bookings": show.bookings} for show in showget1]
        return showget
    @marshal_with(show_fields)
    def post(self,venuein):
        args = s_parser.parse_args()
        showname = args.get('showname', None)
        bookings=args.get('bookings',None)
        genre = args.get('genre', None)
        
        if showname is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' Name is required')
        
        if genre is None:
            raise BusinessValidationError(status_code=400, error_code='001', error_message=' genre is required')
       
        showpost = dbs.session.query(Show).filter(Show.showname==showname).first()
        if showpost:
            raise BusinessValidationError(status_code=400, error_code='002', error_message=' Name already exists')
        
        l = Show(showname=showname, genre=genre,bookings=bookings,uu=venuein)
        dbs.session.add(l)
        dbs.session.commit()
        return "", 201

    def delete(self, showin):
        l = Show.query.get(showin)
        
        if not l:
            raise NotFoundError(status_code=404)
        else:
            
            dbs.session.delete(l)
           
             # Re-add the modified object to the session
            dbs.session.commit()  # Commit the changes to the database
        return l, 200

    @marshal_with(show_fields)
    def put(self, showin):
        l = Show.query.get(showin)
        
        if l is None:
            raise NotFoundError(status_code=404)
        store = l.sid
        dbs.session.delete(l)
        args = su_parser.parse_args()
        l.sid = store
        l.showname = args.get('showname')
        l.genre = args.get('genre')
        
        l.bookings = args.get('bookings')
        dbs.session.add(l)
        dbs.session.commit()
        return l,200

b_fields = {
    'bid': fields.Integer,
    'no': fields.String,
    'bookings': fields.Integer,    
}       
b_parser = reqparse.RequestParser()



b_parser.add_argument('no')

b_parser.add_argument('bookings')

class BAPI(Resource):
   
    
    def get(self,showin):
        showget8 = Show.query.filter_by(sid=showin).first()
        available=showget8.bookings
        print(available)
        
        return {"available": available}
    
    def post(self,showin,uid):
        args = b_parser.parse_args()
        
        bookings=args.get('bookings')
        no = args.get('no', None)
        
        print(uid)
       
        showget6 = Show.query.filter_by(sid=showin).first()
        print(showget6)
        print(showget6.bookings)
        print(bookings)
        available=showget6.bookings
        if available < int(bookings):
            
            return {"mid": "entre correct number" ,"available": available}
       
        else:
             showget6.bookings-=int(bookings)
             available = showget6.bookings
             if showget6.bookings == 0:
                 dbs.session.commit()
                 l = Book(bookings=bookings, no=no,bb=showin,fuid=uid)
                 dbs.session.add(l)
                 dbs.session.commit()
                 return {"mid": "housefull","available": available} 
             else:
                   
                    l = Book(bookings=bookings, no=no,bb=showin,fuid=uid)
                    dbs.session.add(l)
                    dbs.session.commit()
                    return {"available": available}
             
     
