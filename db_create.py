#!/usr/bin/env python

from vote import app, db

if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://':
    raise EnvironmentError(
        'Missing SQLALCHEMY_DATABASE_URI from config file')

db.create_all()
