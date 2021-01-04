# TDLOG-agenda
a project to realize an automatized planning system with ankidroid learning features

# Feature ideas
Cookies + Personal Statistics \
Finished task + get ahead \
Anki features \
Mail inscription


# Backend
## Main Technologies
- flask
- sqlalchemy

## Architecture
All the backend stuff is in *backend*. Is contains *src, tests and a Dockerfile*.  
*src* contains all the code that is used for the backend and *tests* contains pytest files to test *src*.  
*src* is subdivided in 4 different categories.  
 - *algorithm* is about the optimization part for the calendar.
 - *anki* is about the anki functions and features.
 - *entities* contains the classes for SQLalchemy to function properly.
 - at the root, there are 2 files, *init_db*, that deploys and mocks a database, and *main*, that starts the app.

## How to start it independently
Simply use "python main.py", or use the Dockerfile corresponding to the backend via :  
"docker build -t backend ." and "docker run backend"


# Frontend
## Main Technology
- Angular

## Architecture
A regular angular app, with a Dockerfile at the root.
src contains the code, which contains the main files.  
app contains main files for the app and routing, components (related to views),  
models to use json easily to communicate with backend,  
service contains an api and another one to restrict access while not logged in.

## How to start it independently
Use "ng serve" in frontend or start the related Dockerfile via :  
"docker build -t frontend ." and "docker run frontend"

# How to start everything locally
Use "docker-compose build", then "docker-compose up", then head to http://localhost:4200/