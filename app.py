import urllib.request
from createdb import home, private
from apistar import App, Route, exceptions, http
from sqlalchemy import create_engine
from passlib.hash import argon2
import jwt, json, sqlite3, time, base64
hostip = "54.177.65.193"
def htmlgen(error="")-> str:
    return f'<!DOCTYPE html> <html> <body>  {error} <br> <h2> Secure Webpage</h2>  <form action="/submit" method="POST">     Username:<br>   <input type="text" name="username">   <br>   Password:<br>   <input type="text" name="userpass">   <br>   <input type="submit" name="submit" value="login" >   <input type="submit" name="submit" value="register" > </form>  </body> </html>'
def redirect(site=f"http://{hostip}/")-> str:
    return f'<head> <!-- HTML meta refresh URL redirection --> <meta http-equiv="refresh" content="0; url={site}"> </head>' 

def postgen(body: bytes) -> dict:
    return dict(map(lambda x: x.split('='), body.decode('ascii').split('&')))


def form(body: http.Body) -> str:
    if body:
        body = postgen(body)
    else:
        return htmlgen("Oops, something went wrong.")
    if body["submit"]:
        if(not(body["username"] and body["userpass"])):
            return htmlgen("Make sure your username and password are filled")
    if body["submit"] == "login":
        eng = create_engine(f"sqlite:////{home}/apple/user.db")
        conn = eng.connect()
        try:
            h = next(conn.execute(f"select password from users where username='{body['username']}'"))[0]
            conn.close()
        except:
            conn.close()
            error = 'Your username does not exist.'
            return htmlgen(error)
            
        if(argon2.verify(body["userpass"], h)):
            token = jwt.encode({'user': body["username"], 'exp': int(time.time()) + 30*60}, private, algorithm='RS256')
            headers = {'Set-Cookie': f"Token={token.decode('utf-8')}; Max-Age=1800", 'Status': 302, 'Location': f"http://{hostip}/"}
            return http.Response(content=redirect(), headers=headers)
            
        return htmlgen('Your password is incorrect.')

    if body["submit"] == "register":
        eng = create_engine(f"sqlite:////{home}/apple/user.db")
        conn = eng.connect()
        if(next(conn.execute(f"select count(*) from users where username='{body['username']}'"))[0]):
            return htmlgen('This username is taken.')
        try:
            userpass = argon2.hash(body["userpass"])
            conn.execute(f"insert into users (username, password) values ('{body['username']}', '{userpass}')") 
            conn.close() 
            return htmlgen("Success.")
        except:
            conn.close()
    return htmlgen("Oops, something went wrong")

def welcome(Cookie: http.Header):
    if Cookie is not None:
        cookie1 = Cookie.split(";")[0].split("=")
        token = cookie1[1] if cookie1[0] == "Token" else None ##You can't actually rely on this behavior in the real world, you must search for 'Token'
        if token:
            try:
                name = urllib.request.urlopen(f"http://54.177.65.193:8080/?token={token}").read().decode('utf-8')
            except:
                return htmlgen("Oops, something went wrong")
            if(name != "Invalid."):
                return f'Hey {name}, welcome to the Internet!'
            else:
                return htmlgen("Oops, something went wrong")
    return htmlgen()
        


routes = [
    Route('/', method='GET', handler=welcome),
    Route('/submit', method='POST', handler=form),
]

app = App(routes=routes)



if __name__ == '__main__':
    app.serve('172.31.5.175', 80, debug=True)



