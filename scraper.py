import csv
import spotipy
from os import getenv
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def runScraper():
    # create spotify object
    session = load_credentials()

    # set playlist url
    PLAYLIST_LINK = link_inquiry()

    # create session
    tracks = session.playlist_tracks(PLAYLIST_LINK)

    # get playlist track items and total tracks in playlist
    items = tracks['items']
    totalTracks = tracks['total']

    # get desired file format
    fileFormat = file_inquiry()

    # text file output
    if fileFormat == 'txt':

        # name file
        txtName = filename_inquiry()
        OUTPUT_TXT_FILE = f"{txtName}.txt"

        # write data to text file
        write_txt(OUTPUT_TXT_FILE, totalTracks, items, tracks, session)

    # csv file output
    elif fileFormat == 'csv':

        # name file
        csvName = filename_inquiry()
        OUTPUT_CSV_FILE = f"{csvName}.csv"

        # write data to csv file
        write_csv(OUTPUT_CSV_FILE, totalTracks, items, tracks, session)


def file_inquiry():
    # ask user in what file format they want the data saved
    options = ['csv', 'txt']
    while True:
        userOption = input(
            "\nChoose file type where data will be saved...\nOptions:[csv] or [txt]\nType csv or txt to make a choice\n::: "
        )
        # check for proper input
        if userOption not in options:
            print('\nIncorrect entry. Please try again.\n')
        else:
            return userOption


def filename_inquiry():
    # ask user what to name the file
    return input('\nWhat will you name the file? (No extension needed)\n::: ')


def link_inquiry():
    # request playlist url from user
    return input(
        "Enter the Playlist Link (Expected format: https://open.spotify.com/playlist/...): \n"
    )


def load_credentials():
    # load client credentials from .env file
    load_dotenv()

    # get .env data
    clientID = getenv("CLIENT_ID")
    clientSecret = getenv("CLIENT_SECRET")

    # Authenticate
    auth_manager = SpotifyClientCredentials(
        client_id=clientID, client_secret=clientSecret
    )

    # return spotify object
    return spotipy.Spotify(auth_manager=auth_manager)


def write_csv(fileName, total_tracks, track_items, playlist_tracks, session_object):
    # create csv file
    with open(fileName, "w", encoding="utf-8") as file:

        # create write object
        writer = csv.writer(file)

        # write header column names
        writer.writerow([f"TRACK ({total_tracks} tracks)", "ARTIST"])

        # offset to keep index in range
        offset = 0
        for track in range(total_tracks):
            # * get_data()
            # get song name
            name = track_items[track - offset]['track']['name']

            # get artist name
            artists = ', '.join(artist['name']
                                for artist in track_items[track - offset]['track']['artists'])

            # check for first 100 rendered songs
            if (track + 1) % 100 == 0:

                # load next songs in playlist and get their items
                playlist_tracks = session_object.next(playlist_tracks)
                track_items = playlist_tracks['items']
                offset = track + 1

            # write name and artist to csv
            writer.writerow([name, artists])
    print(f"\nTEXT FILE CREATED TO {fileName}\n\n")


def write_txt(fileName, total_tracks, track_items, playlist_tracks, session_object):

    # create text file
    with open(fileName, "w", encoding="utf-8") as file:

        # write total tracks
        file.write(f"Total Tracks in Playlist: {total_tracks} \n")

        # display format for text
        file.write(
            "List Items are displayed in the following format: [Song Name by Artist]\n\n"
        )

        # offset to keep index in range
        offset = 0
        for track in range(total_tracks):
            # * get_data()
            # get song name
            name = track_items[track - offset]['track']['name']

            # get artist name
            artists = ', '.join(artist['name']
                                for artist in track_items[track - offset]['track']['artists'])

            # check for first 100 rendered songs
            if (track + 1) % 100 == 0:

                # load next songs in playlist and get their items
                playlist_tracks = session_object.next(playlist_tracks)
                track_items = playlist_tracks['items']
                offset = track + 1

            # write name and artist to txt
            file.write(f"{name} by {artists} \n")
    print(f"\nTEXT FILE CREATED TO {fileName}\n\n")
