import os
from moviepy.editor import *


def runConverter():
    # create song array
    mp4_list = []

    # set mp4 directory
    path = 'Songs/MP4'

    # get songs from mp4 folder and remove mp4 suffix
    getSongs(mp4_list, path)

    # convert files to mp3
    convert(mp4_list)

    # ask user if they want to delete mp4 files
    deleteOption = delete_query()

    # delete mp4
    if deleteOption == 'y':
        deleteMP4(path)

    # exit program
    elif deleteOption == 'n':
        exit()


def convert(mlist,):
    print("--- THE CONVERSION WILL NOW BEGIN ---\n\n")

    # convert songs in list
    for mp4 in range(len(mlist)):
        mp4_file = fr'Songs/MP4/{mlist[mp4]}.mp4'
        mp3_file = fr'Songs/MP3/{mlist[mp4]}.mp3'

        print(f'REMAINING CONVERSIONS: {len(mlist) - mp4}\n')

        # get mp4
        video = VideoFileClip(mp4_file)

        # convert to mp3
        audio = video.audio
        audio.write_audiofile(mp3_file)

        print('\n')
    print('--- CONVERSION DONE ---')


def deleteMP4(dir):
    for data in os.listdir(dir):
        os.remove(os.path.join(dir, data))


def delete_query():
    # acceptable responses
    options = ['y', 'n']

    # loop input until proper entry
    while True:
        query = input("Do you wish to delete all mp4 files? [y] or [n]\n:::")

        if query not in options:
            print('\nIncorrect entry. Please try again.\n')
        else:
            return query


def getSongs(mlist, path):
    # list songs in directory
    entries = os.listdir(path)

    # append songs to list
    for files in range(len(entries)):
        mlist.append(entries[files].removesuffix('.mp4'))
