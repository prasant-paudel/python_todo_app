# SQLALCHEMY_DATABASE_URI = "sqlite:///static/todo.db"
import os
# SQLALCHEMY_DATABASE_URI = "sqlite:////home/prasant/Desktop/python/python_todo_app/static/todo.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getcwd()}/static/todo.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True