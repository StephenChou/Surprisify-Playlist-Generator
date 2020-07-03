# Surprisify-Playlist-Generator
[Surprisify Playlist Generator](https://surprisify.me)

Playlist generator using Spotify API

Surprisify is a Spotify playlist generator that uses Spotify API and the Spotipy library. It first asks for user
authentication through Spotify, and then prompts the user to enter a "level". Levels correspond with how obscure the
playlist will be, using recursion to dive into the user's top artists' related artists. 

* Levels 1-5 should be relatively comfortable
* Levels 10 and above should be relatively unknown to the user

**The Code:**

The backend script was made in Python and uses Flask as a web framework.
