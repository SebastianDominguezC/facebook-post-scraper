import os
import json
from datetime import datetime
from facebook_scraper import get_posts
import requests

posts = []

user = ''
password = ''

user_to_scrape = ''

try:
    for post in get_posts(user_to_scrape, pages=50, credentials=(user, password)):
        # Post id and create dir for media
        id = post['post_id']
        os.mkdir(f'./media/{id}', 0o777)

        # Dictionary for data references
        time = datetime.timestamp(post['time'])
        p_dict = {
            "id": id,
            "text": post['text'],
            "images": [],
            "video": "",
            "time": time,
        }

        # Loop images
        i = 0
        for image in post['images']:
            r = requests.get(image, allow_redirects=True)
            file = f'./media/{id}/{i}.jpg'
            open(file, 'wb').write(r.content)
            i += 1
            p_dict['images'].append(file)

        # Video
        if post['video'] != None:
            r = requests.get(post['video'], allow_redirects=True)
            file = f'./media/{id}/vid.mp4'
            open(file, 'wb').write(r.content)
            p_dict['video'] = file

        # Add dictionary to array
        posts.append(p_dict)
except:
    print('oops, error ocurred')

# Convert array to json and write to file
posts_json = json.dumps(posts, indent=4)
json_file = 'data.json'
open(json_file, 'w').write(posts_json)
