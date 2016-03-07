__author__ = 'SWEN356 Team 4'

#!flask/bin/python
from app import app

if __name__=="__main__":
    app.run(port=5000, debug=True)