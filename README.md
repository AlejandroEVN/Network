### Project Network 

This is a social network twitter-like app.

Add, edit and like posts. Add/remove other users to your following list.

The main objective of this project was to understand how to use AJAX and JavaScript to manage data from the backend, updating the page without reloading (e.g. when liking a post) and working with Django pagination.

#### Demo
<img src="./network/demo/network-demo1.gif" width="960" height="540" />
<img src="./network/demo/network-demo2.gif" width="960" height="540" />
<img src="./network/demo/network-demo3.gif" width="960" height="540" />

#### Routes

`url: /`  
Main page. List of all the posts, ordered by date.

`url: /login` `url: /register`  
Renders corresponding HTML.

`url: /logout`  

`url: /profile/<int:user_id>`  
Renders HTML page of the user specified.

`url: /profile/<int:user_id>/following`  
Renders HTML page with the posts in the specified user's following list.

`url: /post/add`  
Adds new post to the database and redirects to index.html.

##### API

`url: /edit/<str:post_id>`  
Edits the selected post.

`url: /like/<str:post_id>`  
Toggles 'Like' post status by the user that makes the request.

`url: /profile/<str:user_id>/follow`  
Toggles 'Follow' status by the user that makes the request.


#### Installation

- Clone into your machine
- Open a terminal
- Cd into projects' folder
- Run `pip install requirements.txt` (ideally in a virtual environment)
- Run `py manage.py runserver`
- Open browser and navigate to `127.0.0.1:<your Django local port>`

#### Tech Stack
- Python
- Django
- JavaScript
- Bootstrap
- CSS
