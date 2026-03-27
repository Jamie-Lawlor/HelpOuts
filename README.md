# What is HelpOuts?

HelpOuts is an application that connects the community with volunteers to get jobs done. Communities can store their projects and advertise jobs they need volunteers for to complete their project. A helper can request to join a community and once accepted, they can offer their help for any job requested by the community.

<img src="static/images/templogo6.png">

## Before starting

You will need to install:

- [Python](https://github.com/logos)
- [XAMPP](https://www.apachefriends.org/download.html)

## Creating the database
- Once XAMPP is installed, select apache and sql to turn them on
- Once both options are running, on [localhost](http://localhost), select phpmyadmin.
- You are then brought to create database, call the database helpoutsdevdb01.
- Create a .env file and include these fields:

    - DB_USER= YOUR_USERNAME_HERE
    - DB_HOST=localhost
    - DB_NAME=helpoutsdevdb01
    - DB_PORT=3306
    - DB_URL=mysql+pymysql://YOUR_USERNAME_HERE:@localhost:3306/helpoutsdevdb01
    
- Finally in the SQL section in your helpoutsdevdb database, copy and paste all of the data from the seed.sql file located here: db/local-setup/seed.sql

## Running HelpOuts
To run HelpOuts there are a few things to setup. 
Open up a new terminal and run the command
```
python -m venv venv
```
This command creates a virtual environment for HelpOuts.

To activate the venv on Windows run:
```
venv\Scripts\activate
```
You should now see "(venv)" beside your directory path in the terminal.

To install the libraries required to use HelpOuts, run this command once your virtual environment is activated:

```
pip install -r requirements.txt
```

## Enjoy HelpOuts

Press play on the app.py file and you can now successfully run HelpOuts on your local machine!