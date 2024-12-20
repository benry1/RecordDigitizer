import os
import json
import discogs_client
from dotenv import load_dotenv
load_dotenv()

DISCOGS_API_KEY = os.getenv('DISCOGS_API_KEY')

def GetAlbumFromDiscogs(album_name):
    client = discogs_client.Client('ExampleApplication/0.1', user_token=DISCOGS_API_KEY)
    results = (client.search(album_name, type='master'))
    result = results.page(1)[0]

    release = client.master(result.data['id'])
    # print("Data:", json.dumps(release.data, indent=2))
    # print("Tracklist:", release.tracklist)
    for track in release.tracklist:
        print(track.data['position'], track.data['title'], track.data['duration'])


    cleaned = {
        'artist': release.main_release.artists[0].name,
        'title': release.title,
        'year': release.year,
        'cover_image': release.images[0]['uri'],
        'tracks': []
    }

    for index, track in enumerate(release.tracklist):
        cleaned['tracks'].append({
            'position_raw': track.data['position'],
            'position': index+1,
            'title': track.data['title'],
            'duration': track.data['duration']
        })

    # print(json.dumps(cleaned, indent=2))
    return cleaned

