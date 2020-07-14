![Surprisify Logo](static/banner.png)
# Surprisify-Playlist-Generator
[Surprisify Playlist Generator](https://surprisify.me)

Playlist generator using Spotify API

Surprisify is a Spotify playlist generator that uses Spotify API and the Spotipy library. It first asks for user
authentication through Spotify, and then prompts the user to enter a "level". Levels correspond with how obscure the
playlist will be, using recursion to dive into the user's top artists' related artists. 

* Levels 1-5 should be relatively comfortable
* Levels 10 and above should be relatively unknown to the user

## The Code:

The backend script was made in Python and uses Flask as a web framework. In addition to using requests to get authorization credentials from the user, [Spotipy](https://spotipy.readthedocs.io/en/2.13.0/) was used for the algorithm and playlist generation.

### The Algorithm:
The algorithm is pretty basic and can be shown below:

```python
def get_obscure_artist(artist_id, levels, spotifyObject):

    rnd_artist = random.randint(0, 11)

    if (levels == 1):
        return artist_id

    temp_id = artist_id
    new_id = ''
    while levels >= 1:
        new_id = spotifyObject.artist_related_artists(
            temp_id)['artists'][rnd_artist]['id']
        temp_id = new_id
        levels -= 1

    return new_id
```

The method finds a related artist to one of the user's top streamed artists. Given the level input, the algorithm will randomly choose a related artist from the current artist. The higher the level the more obscure, since the algorithm will go into the related artist of the related artist (and so on) from the original top artist. This helps ensure that the artist generated from the final level will be relatively obscure but familiar to the user's music taste. If the level gets too high, however, the music might be too far from the user's comfort range.

### The Frontend

In order to enable the script to be interacted with by a user, the use of Flask as a microframework was implemented to connect the script to the frontend. Simple HTML and CSS styling with some JavaScript functions were created to make a user-friendly experience. 

### The Backend

Aside from the actual script, the only other backend code was the implementation of an SQL database using Flask SQLAlchemy, which is essentially an abstraction layer to SQL that enables the ability to interact with a databse through python. The code itself is pretty basic.

Please feel free to interact with the code and leave feedback. This is my first fully fleshed out project and I appreciate any input on how I can improve the site. 
