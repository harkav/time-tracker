# Task Tracker CLI app 

This is a quick and dirty CLI app that allows the user to track 
the time they've spent on a certain task. 
This app allows you to add, view, update (to some extent) and delete tasks from an SQLite database. 


## Features: 

- Add a new task: create a new task with a description, start date, end date, category, and tags. 
- View all tasks, view all tasks in the database. 
- View finished/unfinished tasks.
- Delete a task: Remove tasks by their ID
- Mark task as finished: mark a task as finished by giving it an end date


## Requirements 

This app was coded with python 3.11.
It uses the following libraries: 

- sqlite3 - for database management 
- datatime - for handling date and time 
- prettytables - for formating output tables 

## Installation 

- clone the repo 
- navigate to the project directory 
- set up a venv 
- install the dependencies 


## Usage 

### View all: 

python3 main.py "view all" 

### add:  
python3 main.py add --task "Task description" --category "Category" --start_date "YYYY-MM-DD HH:MM" --end_date "YYYY-MM-DD HH:MM" --tag "tag1" "tag2"
Only --task is required, if not provided, start_date defaults to now, and end_date defaults to None. 

### display
python3 main.py display --finished or --unfinished. Displays either the finished or unfinished tasks. Requires one of the possible flags. 

### delete
python3 main.py delete --task_id delete a task, requires task_id to delete a task. 

### finish 

python3 main.py finish --task_id, mark a task as finished. requires task_id 


## Database schema 

The app uses an sqlite database with the following schema 

tasks

    taskID (Primary Key)
    task (Text)
    start_date (Datetime)
    end_date (Datetime, nullable)
    category (Text, nullable)

tags

    tagID (Primary Key)
    tag (Text)

taskTags

    taskID (Foreign Key to tasks)
    tagID (Foreign Key to tags



## Further improvements 

- Checking consistency, some variable names might be inconsistent, taskID or task_ID and so on. 
- Adding functionality for more complicated update queries. 
- Adding functionality for more comlicated view queries 
- Adding some analytics functions, perhaps some way to create a report. 
- Adding a GUI? 
- Making it a web app 
- Cleaning up the code, adding a few comments here and there, making sure that all the comments are in English, not Norwegian. 

## Licence

MIT License, or something like that. I don't know. Do what you want to do with this. 