# GDAPI
GDAPI is a simple Python Geometry Dash API module aimed at making easy access functionalities within Python. Please note that this is a beta version, so any bugs encountered should be reported on the GitHub repository.

With the support of a dedicated community, GDAPI has been able to implement hard to code features, like posting account comments, level comments, user messages, friend requests, and more.

## Features
- **Post Account Comments**: You can post comments on user accounts.
- **Post Level Comments**: Comment on specific levels within the game.
- **Post User Messages**: Send messages to other users.
- **Post Friend Requests**: Send friend requests to other users.

Many more features are planned for future updates.

## Installation
```
git clone https://github.com/Xytriza/gdapi-py.git
cd gdapi-py
pip install .
```

## Examples
### Custom Databases
If you use a GDPS you can use it here too!
```
```python
import gdapi_py

gd = gdapi_py.gdapi("username", "password", "https://gdps.location") #dont keep the / at the end!
```

### Posting Account Comments
```python
import gdapi_py

gd = gdapi_py.gdapi("username", "password")

comment = "Comment to post goes here"
success, response = gd.post_account_comment(comment)
    
if success:
    print(f"Comment posted with ID #{response}")
else:
    print(f"Failed to post comment, server response is {response}")
```

### Posting Level Comments
```python
import gdapi_py

gd = gdapi_py.gdapi("username", "password")

comment = "Comment to post goes here"
levelid = "LevelID to post comment on"
percent = "Percent gotten on level (0 for none)"
success, response = gd.post_level_comment(comment, levelid, percent)
    
if success:
    print(f"Comment posted with ID #{response}")
else:
    print(f"Failed to post comment, server response is {response}")
```

### Posting User Messages
```python
import gdapi_py

gd = gdapi_py.gdapi("username", "password")

subject = "Subject of message goes here"
body = "Body of message goes here"
accountid = "Target account id goes here"
success = gd.post_user_message(subject, body, accountid)
    
if success:
    print(f"Message posted successfully")
else:
    print(f"Failed to post message")
```

### Posting User Friend Requests
```python
import gdapi_py

gd = gdapi_py.gdapi("username", "password")

comment = "Comment of friend request goes here"
accountid = "Target account id goes here"
success = gd.post_user_friend_request(comment, accountid)
    
if success:
    print(f"Friend request posted successfully")
else:
    print(f"Failed to post friend request")
```