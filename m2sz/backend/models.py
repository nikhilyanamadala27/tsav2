from flask_sqlalchemy import SQLAlchemy
from other import dbs
from flask_security import UserMixin, RoleMixin


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


    



class Userlogin(dbs.Model, UserMixin):
    __tablename__ = "userlogin"
   
    usname1 = dbs.Column(dbs.String)
    pass1 = dbs.Column(dbs.String)
    uid = dbs.Column(dbs.Integer, autoincrement=True, primary_key=True)
    email = dbs.Column(dbs.String, nullable=False, unique=True)

    def _repr_(self):
        return f'<Userlogin {self.usname1}>'

    def set_password(self, pass1):   
        self.password_hash = generate_password_hash(pass1)

    def check_password(self, pass1):
        return check_password_hash(self.password_hash,pass1)


class Book(dbs.Model):
    __tablename__ = "book"
    no=dbs.Column(dbs.Integer)
    bid=dbs.Column(dbs.Integer,autoincrement=True,primary_key=True)
    bookings=dbs.Column(dbs.Integer)
    bb=dbs.Column(dbs.Integer)
    fuid=dbs.Column(dbs.Integer)
class Venue(dbs.Model):
    __tablename__ = "venuet"
    venue=dbs.Column(dbs.String)
    vid=dbs.Column(dbs.Integer,autoincrement=True,primary_key=True)
    loc=dbs.Column(dbs.String)
    cap=dbs.Column(dbs.Integer)
    showz= dbs.relationship('Show', backref='showt')
class Show(dbs.Model):
    __tablename__ = "showt"
    showname=dbs.Column(dbs.String)
    sid=dbs.Column(dbs.Integer,autoincrement=True,primary_key=True)

    genre=dbs.Column(dbs.String)
   
    uu = dbs.Column(dbs.Integer, dbs.ForeignKey("venuet.vid"))
    bookings=dbs.Column(dbs.Integer)
