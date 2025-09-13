'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Stores the data on our AI created music. This will keep track of the musics directory locations and allow us to find and retrieve it.

'''

import os
import random

#directory where musics stored
DIRECTORY = "Music"

#list of lists for music [Name of music type, Directory]
MUSIC_DIRECTORIES = [
    ["Cinematic Orchestral", "Cinematic Orchestral"],
    ["Ambient", "Ambient"],
    ["Suspense/Thriller", "Suspense Thriller"],
    ["Action/Adventure", "Action Adventure"],
    ["Romantic", "Romantic"],
    ["Fantasy/Epic", "Fantasy Epic"],
    ["Mystery", "Mystery"],
    ["Happy/Upbeat", "Happy Upbeat"],
    ["Horror", "Horror"],
    ["Sad/Reflective", "Sad Reflective"],
    ["Sci-Fi", "Sci Fi"],
]

INTRO_OUTRO_DIRECTORY = [
    "Intro",
    "Outro"
]

#used to store [name of music type, [list of files]]
MUSIC_FILE_NAMES = []

class Music_Loader:

    def __init__(self):
        self.find_music_file_names()

    #finds all of our files for each music type
    def find_music_file_names(self):
        #empty our list
        #MUSIC_FILE_NAMES.clear()
        if len(MUSIC_FILE_NAMES) == 0:

            for music in MUSIC_DIRECTORIES:
                files = []
                direct = os.path.join(DIRECTORY, music[1])

                #get all the mp3 file names in this directory
                for file in os.listdir(direct):
                    if file.endswith('mp3'):
                        files.append( os.path.join(direct, file) )

                #now add them to MUSIC_FILE_NAMES
                #adds a list with the name of the music and it randomly chooses one of the files to use
                MUSIC_FILE_NAMES.append([music[0], random.choice(files) ])

    def get_all_music_file_names(self):
        return MUSIC_FILE_NAMES
    
    def get_music_file_name(self, music):
        for m in MUSIC_FILE_NAMES:
            if m[0].upper() == music.upper():
                return m[1]
        
        #if an error happens, just return first file name
        return MUSIC_FILE_NAMES[0][1]

            

