# Step Seven: Research and Understand Login Strategy

- How is the logged in user being kept track of?
    - It is tracked by seeing if user is in session or not. Implement `session['...']` in app.py 

- What is Flask’s g object?
    - Flask's g object is global

- What is the purpose of add_user_to_g ?
    - add_user_to_g helps tracking of user logged/not logged in and make g.user as variable refer to session value. g.user checks `User.query.get(session[CURR_USER_KEY])` to retrieve user from Database.

- What does @app.before_request mean?
    - before_request is to allow execute a function before any request. @app.before_request just define g.user before running any other route.