# Secure-JWOT-Web-System
Description of the Secure Apple System:


The user is first told to register/login in the front page, where it only interacts with the minimal Python webservice APIstar. Upon successful login, you are given a token, stored in your Cache with an age of 30 minutes. However, not only is the token signed, it is to be verified by a seperate service, which the browser does not interact with, using a Diffie-Hellman key signature scheme between the python web-service and a minimal C RESTFUL API made with the HTTP packet parser, Kore.io. 

The C API recieves a token and quickly determines if the author holds the private key corresponding to its public key, and then if valid, checks the expiration in epoch miliseconds to determine whether the token is expired. If the token is deemed valid, the user is served a personalized greeting page by the Python service.


Both the C API and Python services have comprehensive checks throughout the code to prevent any security risks. Additionally, included is a test.py in the main directory, and several test.c files in the libjwt include folder.  

The Python service stores user data in an SQLite database.

To set up, the following dependencies are required:

libJWT

Kore.io

APIStar

pyJWT

SQLalchemy

Then make sure to replace the provided private and public PEM-formatted RSA 2048 keys.
Finally, run createdb.py, after editing the paths at the top of the file
Edit app.py and apple/src/apple.c to the ip address/ports you wish to bind to
and run app.py

Then in the apple directory, use "kodev build && kodev run" to complete the network. 
