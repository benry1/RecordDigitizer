# RecordDigitizer

This python project aims to make it easy to digitize your records. All you need to do is supply the recording and some basic metadata, and you will get the album output split as individual songs, ready for import into your music library.

# Project Setup

You must have a valid Discogs API key and set it in your .env file. Even basic public queries like looking up an album require a proper key.

1. Create a virtual environment like `python -m venv .venv`
2. Acvitvate the environment `source .venv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Run desired scripts with python3.

This project is too young to have a more definitive runguide, because it's going to change a lot. There's not even really a main script yet.