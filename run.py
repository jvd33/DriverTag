__author__ = 'SWEN356 Team 4'

#!flask/bin/python
from app import app
import os

if __name__=="__main__":
    os.system("seeds.py")
    app.run(host='0.0.0.0', port=5000, debug=True)