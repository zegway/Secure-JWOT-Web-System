from app import welcome
from sqlalchemy import create_engine
from createdb import home
from passlib.hash import argon2
import sqlite3
##register test
eng = create_engine(f"sqlite:////{home}/apple/user.db")
conn = eng.connect()
testuser="test3"
testpass="test2"
welcome(submit="reg", username=testuser, userpass=testpass)
result = conn.execute(f"select * from users where username='{testuser}'")
try:
    row = next(result)
    assert row["username"] == testuser
    assert argon2.verify(testpass, row["password"])
except:
    print("Registration not adding user.")
    raise 




