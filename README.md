# MovieHub

## Full Stack Nano 

This is the final project for full stack nono deggre project


## Description:

This is flask app which will let you  search by movie name and will fetch the movie details from OMDb api and show you the result in the frontend  

## Prerequisites:
You need to obtain your personal API key from the OMDb API website in order to be able to use the website. Once you have it,   you can set it as an environment variable API_KEY through .env file.

# Authentication

### You need to register to the appliction to add movie to the list and to be admin to be able to delete movie from the list .

This project use auth0 to use this project you need to have the same setup 

## Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - User
        - can `get:movies`
        - can `post:movies`
    - Admin
        - can perform all actions


# Installing Dependencies



### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.



# Running the server

From within the root  directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:


```bash
python server.py
```

The server will run in debug mode if you need to disable this you 

need to remove  app.debug = True


## About
This project is developed by Saleh Alibrahim 
