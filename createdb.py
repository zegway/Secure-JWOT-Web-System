from sqlalchemy import create_engine
import sqlite3

home="home/navarrus" #This is the name of the base directory that you have permissions for

private = open("private.pem", "rb").read()
public = open("public.pem", "rb").read()

if __name__ == '__main__':

#Creates a user-database in the home folder
    eng = create_engine(f"sqlite:////{home}/apple/user.db")
    conn = eng.connect()

    conn.execute("create table users (username varchar(64) PRIMARY KEY, password varchar(73))")

    conn.close()
