[![Build Status](https://travis-ci.org/jvd33/DriverTag.svg?branch=master)](https://travis-ci.org/jvd33/DriverTag)
#DriverTag Setup
**SYSTEM DEPENDENCIES:**
Python 3.x
PostgreSQL 9.4 or higher
Linux operating system (Works on Windows but not supported in this readme)

**Instructions for Linux:**


1. **pip install python3-venv** if not already installed
2. Navigate to the root project directory */DriverTag/ and create the virtual environment with **pyvenv venv**
3. **source venv/bin/activate** to switch to the virtual environment
4. **pip install -r requirements.txt** to install the required Python libraries
5. (Optional) **python seeds.py** to seed the database with test data
5. **python run.py**
6. Navigate to localhost:5000


To exit the virtual environment, type deactivate in the virtual environment command line
