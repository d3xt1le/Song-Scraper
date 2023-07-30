import csv
from pytube import Search, YouTube


def runDownloader():
    # create track array
    track_list = []

    # ask user what file they want to open
    openFile, extension = file_query()

    # open txt file
    if extension == 'txt':
        open_txt(track_list, openFile)

    # open csv file
    elif extension == 'csv':
        open_csv(track_list, openFile)

    # create data lists
    url_list = []
    name_list = []

    # get urls
    obtain_url(track_list, url_list, name_list)

    # download songs
    downloader(url_list, name_list)


def append_data(data, list1, list2):
    # append video title and url to respective list
    list1.append(data.results[0].watch_url)
    list2.append(data.results[0].title)


def downloader(ulist, nlist):
    print('--- STARTING SONG DOWNLOADS ---\n')
    print(f'TOTAL TO DOWNLOAD: {len(ulist)}')

    # download songs
    for url in range(len(ulist)):
        print(f'REMAINING DOWNLOADS: {len(ulist) - url}')
        link = ulist[url]
        names = nlist[url]
        download_video(link, names)

    print('---SONG DOWNLOADS COMPLETED---')


def download_video(link, name):
    # create youtube object
    youtube = YouTube(link)
    youtube = youtube.streams.get_highest_resolution()
    try:
        # download song
        print(f"--- CURRENTLY DOWNLOADING {name} ---")
        youtube.download('Songs/MP4')
    except:
        # show error for incorrect input
        print(f'---!!!AN ERROR HAS OCCURRED DOWNLOADING {name}!!!---')
    print(f'--- SUCCESSFULLY DOWNLOADED {name} ---\n')


def file_query():
    while True:
        # ask user what file to open
        userFile = input(
            'Enter name of file to get playlist from... [Only txt and csv file extensions are accepted]\n::: ')

        # check file extension csv or txt
        if not userFile.endswith(('.csv', '.txt')):
            print('\nIncorrect entry. Please try again.\n')
        else:

            # return extension and file
            extension = userFile[-3:]
            return userFile, extension


def obtain_url(tlist, ulist, nlist):
    # search for videos
    print("--- GETTING SONG URLS ---\n")

    for track in range(len(tlist)):
        print(f'URLS OBTAINED: {track + 1}/{len(tlist)}')
        query = tlist[track]
        search = Search(query)

        # append video title and url to respective list
        append_data(search, ulist, nlist)

    print('--- ALL URLS OBTAINED ---\n\n')


def open_csv(tlist, filename):
    # open file in read mode
    with open(filename, 'r') as file:
        reader = csv.reader(file)

        # add data to list
        for row in reader:
            song = row[0]
            name = row[1]

            tlist.append(f'{song} by {name}')

    # delete first index in file (not songs, just descriptive data)
    del tlist[:1]


def open_txt(clist, filename):
    # open file in read mode
    with open(filename, 'r') as file:

        # add lines to list
        for line in file:
            clist.append(line.strip())

    # delete first 3 indexes in file (not songs, just descriptive data)
    del clist[:3]
