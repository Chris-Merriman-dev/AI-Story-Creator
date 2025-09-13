'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Creates automated AI Videos. This app was to see if I can have AI make a story video on its own. Non of the images are animated, except the opening and close video section. 
That was created with AI as well, using Wan 2.1. Everything is selected by AI and created by AI. The music was created separatly with AI and AI 
will select which music to play for each section of the story. I mainly used Google Gemini for this, but Geminis story titles were almost all the same. I ended up 
using g4f.client to create better random stories and titles. There is an option to choose either for the story. PRIMARY_STORY = True is for Gemini.

The hardest thing was getting it to create the prompts for Flux, especially with multiple characters. So I would limit how many characters it put in each scene. 
Also, I create a set number of images for each scene. I like gemini look at the description and then choose which image fits it best. This is very difficult as well. 
Gemini struggles with disformed bodies. It can't tell most of the time, when someones body is deformed. I tried many work arounds to fix this, but most just bring on 
other unforseen issues.

Conclusion on this is, it works, but not perfectly. It struggles to choose the correct images to use many times. As AI Vision gets better, this should help solve this issue.

The results of how this works can be seen on this Youtube channel : https://www.youtube.com/@AISyntheticDreams


NOTE : This has not been updated to work now. It uses outdated Gemini versions and flux creator as well. Use the YouTube channel above to see the results.

Files Needed :

audio_to_text.py
gemini_story_creator.py
gf4_image_creator.py
image_description.py
music_loader.py
video_creator.py

'''

import os
from gemini_story_creator import Gemini_Story_Creator, TYPES_OF_MUSIC
from gf4_image_creator import G4F_Image_Creator
from video_creator import Video_Creator
import random
import time
from datetime import datetime

NUMBER_OF_VIDEOS_TO_CREATE = 2

#setup our directories to use
ALL_IMAGE_DIRECTORY = 'All_Images'
IMAGE_DIRECTORY = 'Images'
ALL_TEASER_IMAGE_DIRECTORY = 'All_Teaser_Images'
TEASER_IMAGE_DIRECTORY = 'Teaser_Images'
STORY_DIRECTORY = 'Stories'

#how many images per paragraph and how many paragraphs for the story
IMAGE_AMOUNT = 5
STORY_PARAGRAPHS = 12

IMAGE_SIZE = (1080, 1920)
#IMAGE_SIZE = (1024, 1024)

#do we want to create video
CREATE_VIDEO = False

#Create story : True for using Gemini, false for other
PRIMARY_STORY = False

#use these for short intro and outros. The text ones were far too long.
SHORT_INTRO = "video_intro1.mp4"
SHORT_OUTRO = "video_outro1.mp4"

#gets our directory
def Find_Save_Directory()->str:
    count = 1

    while True:
        if os.path.isdir(os.path.join(STORY_DIRECTORY,str(count))):
            count += 1
        else:
            break

    return os.path.join(STORY_DIRECTORY,str(count)), str(count)


#saves all of our data to the directory sent in
def Save_Data(directory, story, sorted_story, intro_outro_sorted_story, story_image_descriptions, artstyle, voice, character_descriptions, music, title_intro, title_outro, teaser, teaser_image_text, item_descriptions):
    
    #save story
    with open(os.path.join(directory,'story.txt'), 'w', encoding='utf-8') as file:
        file.write(story)

    with open(os.path.join(directory,'story_artstyle.txt'), 'w', encoding='utf-8') as file:
        file.write(artstyle)

    with open(os.path.join(directory,'story_narrator_voice.txt'), 'w', encoding='utf-8') as file:
        file.write(voice)

    with open(os.path.join(directory,'title_intro.txt'), 'w', encoding='utf-8') as file:
        file.write(title_intro)
    
    with open(os.path.join(directory,'title_outro.txt'), 'w', encoding='utf-8') as file:
        file.write(title_outro)

    with open(os.path.join(directory,'teaser.txt'), 'w', encoding='utf-8') as file:
        file.write(teaser)

    with open(os.path.join(directory,'teaser_image_text.txt'), 'w', encoding='utf-8') as file:
        file.write(teaser_image_text)

    with open(os.path.join(directory,'sorted_story.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in sorted_story) 

    with open(os.path.join(directory,'intro_outro_sorted_story.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in intro_outro_sorted_story) 

    with open(os.path.join(directory,'story_image_descriptions.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in story_image_descriptions) 

    with open(os.path.join(directory,'character_descriptions.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in character_descriptions) 

    with open(os.path.join(directory,'item_descriptions.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in item_descriptions) 

    with open(os.path.join(directory,'music_types.txt'), 'w', encoding='utf-8') as file:
        file.writelines("% s\n\n" % data for data in music)

#function used to create videos. We send in a number, so if there is a certain story we want, we can just set an if statement to that number
def create_the_videos(n):
    start_time = datetime.now()
    #create our gemini story creator and then get our story
    story_creator = Gemini_Story_Creator()
    
    #story we wish to create
    if n == 435340:        
        story = f""""""    
    else:

        #default story creator (gemini)
        if PRIMARY_STORY:
            story = story_creator.create_story(STORY_PARAGRAPHS)
        #secondary story creator
        else:        
            need_story = True

            #make sure we get a story of at least the length we want
            #sometimes it bugs out and does not give us the entire story
            while need_story:
                story = story_creator.create_story_with_g4f(STORY_PARAGRAPHS)
                sorted_story = story_creator.sort_story(story)

                #checks to see if we got the length we need
                if len(sorted_story) >= STORY_PARAGRAPHS:
                    need_story = False
                else:
                    time.sleep(10)

    #get story art style to use for images    
    artstyle = story_creator.get_story_artstyle(story)

    #sort stories into paragraphs
    sorted_story = story_creator.sort_story(story)

    #select the narrators voice for this story
    voice = story_creator.select_story_voice(story, artstyle)

    #get the types of music for each paragraph scene
    music = story_creator.get_music_type(story, len(sorted_story)-1, TYPES_OF_MUSIC)

    #put a blank at start of music list, so it lines up with no music for title screen
    music.insert(0,'')

    #get our title intro and outro
    title_intro = story_creator.get_story_title_intro(sorted_story[0], story)
    title_outro = story_creator.get_story_title_outro(sorted_story[0], story)

    #create a copy of our sorted story
    intro_outro_sorted_story = sorted_story.copy()

    #now place the new intro and outro for the sorted story
    intro_outro_sorted_story[0] = title_intro

    #this sets the last pos of our list to whats in there, plus the ending statement
    intro_outro_sorted_story[len(intro_outro_sorted_story)-1] = intro_outro_sorted_story[len(intro_outro_sorted_story)-1] + " " + title_outro

    #get gemini to give us image descriptions for the story
    #story_image_descriptions = story_creator.summarize_text_for_image2(story, sorted_story)
    character_descriptions = []
    #character_descriptions = story_creator.create_character_descriptions(story)


    #This will attempt to make sure, there are no unknown variables for the characters.
    #we cap it at MAX_ATTEMPTS so it does not try forever
    MAX_ATTEMPTS = 5

    for attempt in range(MAX_ATTEMPTS):
        
        got_descriptions = False

        #loop until we get a description
        while not got_descriptions:
            character_descriptions = story_creator.create_character_descriptions(story)

            if character_descriptions is not None:
                got_descriptions = True
            else:
                time.sleep(10)

        has_unknown = any("unknown" in desc.lower() for desc in character_descriptions)
        has_gender = any("male" in desc.lower() or "female" in desc.lower() for desc in character_descriptions)

        #if it has no unknown, its okay OR it is unknown and has no male or female
        if not has_unknown or (has_unknown and not has_gender):
            break
        
        print('Character with unknown attribute. Trying again..\n')
        time.sleep(10)
    else:
        #it has failed too many times, so end this video creation
        print("Warning: Character descriptions incomplete after maximum attempts.")
        return
    
    #keep this code to use
    '''
    for attempt in range(MAX_ATTEMPTS):
        character_descriptions = story_creator.create_character_descriptions(story)
        #if it has no unknown, its okay
        if not any("unknown" in desc.lower() for desc in character_descriptions):
            break
        #we have an unknown. Now check to see if we dont have male or female. If we do not, then its okay to break too.
        elif not any("male" in desc.lower() for desc in character_descriptions) and not any("female" in desc.lower() for desc in character_descriptions):
            break
        print('Character with unknown attribute. Trying again..\n')
        time.sleep(10)
    else:
        print("Warning: Character descriptions incomplete after maximum attempts.")
        return
    '''

    got_descriptions = False

    #loop until we get item descriptions
    while not got_descriptions:
        item_descriptions = story_creator.create_item_descriptions(story)

        if item_descriptions is not None:
            got_descriptions = True
        else:
            time.sleep(10)

    
    #create our flux image prompts for the story
    story_image_descriptions = story_creator.create_image_descriptions_from_story_and_character_item_descriptions(
        story,
        sorted_story,
        character_descriptions,
        item_descriptions,
        len(sorted_story),
        artstyle,
        token_enabled=False
    )

    #get our data for our teaser video
    teaser = story_creator.get_teaser_summary(story)
    teaser_image_text = story_creator.get_teaser_summary_image4(teaser, character_descriptions, item_descriptions, artstyle)  

    #find the directories to use for this story
    directory, directory_num = Find_Save_Directory()
    directory_all_images = os.path.join(directory,ALL_IMAGE_DIRECTORY)
    directory_images = os.path.join(directory,IMAGE_DIRECTORY)
    directory_all_teaser_images = os.path.join(directory,ALL_TEASER_IMAGE_DIRECTORY)
    directory_teaser_images = os.path.join(directory,TEASER_IMAGE_DIRECTORY)

    #now create the directories for main, all images and best image to be used
    os.makedirs(directory)
    os.makedirs(directory_all_images)
    os.makedirs(directory_images)
    os.makedirs(directory_all_teaser_images)
    os.makedirs(directory_teaser_images)

    #save our story text data
    Save_Data(directory, story, sorted_story, intro_outro_sorted_story, story_image_descriptions, artstyle, voice, character_descriptions, music, title_intro, title_outro, teaser, teaser_image_text, item_descriptions)
    print('\n\n**SAVED DATA**\n\n')

    #class used to create images for video
    img_creator = G4F_Image_Creator()


    print('\n\n**Saving Image Data\n\n**')

    #Loops through and gets the images for our video
    for i in range(len(story_image_descriptions)):
        #used for our own random image seeds
        seed = random.randint(1,100)

        img_creator.Create_Images_with_Amount(story_image_descriptions[i], IMAGE_AMOUNT, directory, directory_all_images, directory_images, artstyle, IMAGE_SIZE, seed)
        #img_creator.Create_Images_with_Amount_NO_PICK(story_image_descriptions[i], IMAGE_AMOUNT, directory, directory_all_images, directory_images, artstyle, IMAGE_SIZE, seed)
        time.sleep(5)

    #if we want to create a video
    if CREATE_VIDEO:

        #gets the teaser images
        print('\n\n**Saving Teaser Image Data\n\n**')
        teaser_images_to_use = 3
        for i in range(teaser_images_to_use):
            seed = random.randint(1,100)
            img_creator.Create_Images_with_Amount(teaser_image_text, IMAGE_AMOUNT, directory, directory_all_teaser_images, directory_teaser_images, artstyle, IMAGE_SIZE, seed)
            #img_creator.Create_Images_with_Amount_NO_PICK(teaser_image_text, IMAGE_AMOUNT, directory, directory_all_teaser_images, directory_teaser_images, artstyle, IMAGE_SIZE, seed)


        print('\n\n**VIDEO CREATOR**\n\n')

        #create video class and create the video
        vid_creator = Video_Creator()
        vid_creator.Create_Full_Video(story, intro_outro_sorted_story, sorted_story[0], directory, directory_images, voice, IMAGE_SIZE, music, title_intro, title_outro, SHORT_INTRO, SHORT_OUTRO,  directory_num)

        print('\n\n**VIDEO TEASER CREATOR**\n\n')
        
        #setup the music for teaser video
        #teaser_music_file = 'Music' # os.path.join(directory, 'Music')
        teaser_music_file = os.path.join('Music', 'Sci Fi')
        teaser_music_file = os.path.join(teaser_music_file, 'scifi1.mp3')
        #teaser_music_file = os.path.join(teaser_music_file, 'Sci Fi')
        #teaser_music_file = os.path.join(teaser_music_file, 'scifi1.mp3')

        #now create our teaser video
        vid_creator.Create_Teaser_Video(teaser, sorted_story[0], directory, directory_teaser_images, 'en_uk_003', IMAGE_SIZE, teaser_music_file, teaser_images_to_use, directory_num)

        #save total time
        with open(os.path.join(directory,'total_time_vid.txt'), 'w', encoding='utf-8') as file:
            totaltime = 'Total time : {}'.format(datetime.now() - start_time)
            file.write(totaltime)
    
    else:
        #save total time
        with open(os.path.join(directory,'total_time_no_vid.txt'), 'w', encoding='utf-8') as file:
            totaltime = 'Total time : {}'.format(datetime.now() - start_time)
            file.write(totaltime)

    print('\n\n**COMPLETE**\n\n')

#main app loop. We set how many videos we wish to create and loop to do so.
for i in range(NUMBER_OF_VIDEOS_TO_CREATE):
    start_time = datetime.now()
    print(f'\nCreating Video {i}.')
    create_the_videos(i)
    end_time = datetime.now()
    print(f'\nVideo {i} Created.')
    print('\n\nDuration: {}'.format(end_time - start_time))