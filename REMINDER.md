# Scratchbook to store interesting stuff

#Signin signout
https://code.tutsplus.com/tutorials/intro-to-flask-signing-in-and-out--net-29982


### Create mysql tables

CREATE TABLE users (
uid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100) NOT NULL,
lastname VARCHAR(100) NOT NULL,
email VARCHAR(120) NOT NULL UNIQUE,
pwdhash VARCHAR(100) NOT NULL
);