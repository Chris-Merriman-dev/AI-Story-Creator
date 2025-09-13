'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Used to create our AI Videos. Video_Creator class will accept data and make our AI created videos and trailers.
Please refer to function description for details.
Functions to start with :
Create_Full_Video
Create_Teaser_Video

'''
from tiktokvoice import *
from mutagen.mp3 import MP3
from music_loader import Music_Loader
import time
import cv2
import numpy as np
import os
from moviepy import *
from moviepy.video.tools.subtitles import SubtitlesClip
from audio_to_text import Audio_to_Text
import subprocess

FONT_NAME = "AgeniaRegular-xR4Y0.otf"
INTRO_OUTRO_VIDEOFILE = "IntroOutro1.mp4"

#class for creating videos
class Video_Creator:
    def __init__(self):
        pass
    
    def Convert_MP3_to_WAV(self, mp3file, wavfile):
        # convert mp3 to wav file 
        subprocess.call(['ffmpeg', '-y', '-i', mp3file, 
                        wavfile])

    #sends in our text (description), directory location and the voice we wish to use and creates the voice audio to save
    def Creat_Audio(self, description, directory, voice):
        tts(description, voice, os.path.join(directory,"temp.mp3"), False)
        return os.path.join(directory,"temp.mp3")

    #create our SRT file for subtitles
    def Create_SRT(self, directory, audiofile, i, story_part, extra_seconds, filenametouse = ''):

        #create our srt
        aud_to_txt = Audio_to_Text()
        if filenametouse == '':
            aud_to_txt.Create_SRT_With_Orig_Text(story_part, audiofile, os.path.join( directory, f'srt{i}.srt'), extra_seconds )
        else:
            aud_to_txt.Create_SRT_With_Orig_Text(story_part, audiofile, os.path.join( directory, filenametouse), extra_seconds )

    #function that creates and writes the teaser video file
    def Create_Teaser_Video_With_Audio2(self, audiofilename, extra_seconds, directory, directory_images, story_part, story_title, image_size, images_to_use, music, directory_num):
        FRAMES_PER_SECOND = 20
        
        audio = MP3(audiofilename)
        print('\n*******************\n\n')
        print(audio.info.length)
        
        seconds = np.ceil(audio.info.length)

        frameSize = (image_size[0], image_size[1])
        #*'mp4v'
        #*'DIVX'
        out = cv2.VideoWriter(os.path.join(directory,f'teaservideo.mp4'),cv2.VideoWriter_fourcc(*'mp4v'), FRAMES_PER_SECOND, frameSize)

        #60 frames per second. add extra seconds
        total_frames = int((seconds + extra_seconds) * FRAMES_PER_SECOND)
        

        images = []

        for i in range(images_to_use):
            #Create and resize the image to match the frame size if necessary
            image = cv2.imread(os.path.join(directory_images, f'Image{i}.png'))            
            image = cv2.resize(image, (frameSize[0], frameSize[1]))  # Resize to (width, height)
            images.append(image)

        #get image section frames
        section_frames = int(total_frames / images_to_use)
        mod_frames = int(total_frames % images_to_use)  #this will be added to the final frame to use

        sections = []

        #creates when to stop for each section (really dont need last, but have it just incase)
        for i in range(images_to_use):
            if i == images_to_use - 1:
                sections.append(section_frames + mod_frames)
            else:
                sections.append(section_frames)

        current_section = 0


        for i in range(len(sections)):

            #write the current sections image
            for j in range(sections[current_section]):
                out.write(images[current_section])

            #inc to next section
            current_section = current_section + 1

        out.release()

        #now put them together
        videoclip = VideoFileClip(os.path.join(directory,f'teaservideo.mp4'))
        
        #############
        #show title
        duration = videoclip.duration

        x1 = videoclip.subclipped(0,1)
        x2 = videoclip.subclipped(1, duration-1)
        x3 = videoclip.subclipped(-1)
        

        # Generate a text clip  
        newFrame = (int( frameSize[0] - (frameSize[0] * 0.1) ), int(frameSize[1]/8) )
        txt_clip = TextClip(font=FONT_NAME,text = story_title, font_size = 75, size=newFrame, method='caption', color = '#FFFFFF', stroke_color='#000000', stroke_width = 3, margin = (0,100), duration = duration - 2.0, text_align ='center')
        txt_clip = txt_clip.with_position(('center', 'top'))
        txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])
        
        # Overlay the text clip on the first video clip  
        x2 = CompositeVideoClip([x2, txt_clip])  

        #concat videos into one
        videos = [x1,x2,x3]
        videoclip = concatenate_videoclips(videos)
        
        #get our audio file and add it to the video
        audioclip = AudioFileClip(audiofilename)

        new_audioclip = CompositeAudioClip([audioclip])
        p1 = videoclip.subclipped(0,int(extra_seconds/2))#.with_effects([vfx.CrossFadeIn(1.0)])
        p2 = videoclip.subclipped(int(extra_seconds/2), videoclip.duration - int(extra_seconds/2))
        p3 = videoclip.subclipped(videoclip.duration - (extra_seconds/2), videoclip.duration)
        p2.audio = new_audioclip

        videos = [p1,p2,p3]
        finalVideo = concatenate_videoclips(videos).with_effects([vfx.FadeIn(1.0, 0.0), vfx.FadeOut(1.0, 0.0)])

        #create the srt file needed for this
        #get the audio
        wavfilename = os.path.join(directory, f'teaser.wav' )
        self.create_audio_file(finalVideo, wavfilename)

        #now create our srt
        self.Create_SRT(directory, wavfilename, 0, story_part, 0, 'teaser.srt')

        #get the subtitles
        srtfile = os.path.join(directory, f'teaser.srt')
        subtitles = SubtitlesClip(subtitles=srtfile, make_textclip=self.make_textclip2, encoding="windows-1252")#.with_effects([vfx.FadeIn(0.5, 0.0), vfx.FadeOut(0.5, 0.0)])

        #print(subtitles.size)
        faded_subtitles = []

        total = len(subtitles.subtitles)
        num = 0
        for sub in subtitles.subtitles:  # Iterate through the subtitle events
            #start_time, end_time, text = sub
            start_time = sub[0][0]
            end_time = sub[0][1]
            text = sub[1]
            duration = end_time - start_time

            textclip = self.make_textclip2(text)
            textclip.start = start_time

            textclip.duration = duration

            #set end time and add effects
            textclip.end = end_time
            textclip = textclip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])
            faded_subtitles.append(textclip)

            num = num + 1

        print('ok')

        #if we have subtitles
        if len(faded_subtitles) > 0 :         
            
            #concat our subtitles and join with finalvideo
            faded_vids = concatenate_videoclips(faded_subtitles)#, method='compose')

            # Create a silent clip of 1-second duration
            silent_clip = ColorClip(size=(1, 1), color=(0, 0, 0), duration=int(extra_seconds/2) )
            silent_clip = silent_clip.with_opacity(0) #.set_opacity(0) # Make it transparent

            # Concatenate the silent clip with the subtitles to introduce the 1-second delay
            delayed_subtitles = concatenate_videoclips([silent_clip, faded_vids])

            # Overlay the delayed subtitles on the video
            finalVideo = CompositeVideoClip([finalVideo, delayed_subtitles])

        #adds our music to the teaser video
        finalVideo = self.Add_Music_To_Teaser_Video(finalVideo, music)

        #save the video
        finalVideo.write_videofile(os.path.join(directory,f'FINAL_TEASER_VIDEO{str(directory_num)}.mp4'), audio_codec='aac')

        #UNCOMMENT FOR SMALLER VIDEO
        #resize to half its size and save it to small name
        ###finalVideo.with_effects([vfx.Resize(0.3)]).write_videofile(os.path.join(directory,f'FINAL_TEASER_VIDEO_SMALL.mp4'), audio_codec='aac', fps = FRAMES_PER_SECOND)


        #now clean up files not needed
        videoclip.close()
        #if os.path.exists(os.path.join(directory,f'teaservideo.mp4')):
        #    os.remove(os.path.join(directory,f'teaservideo.mp4'))

        #close and delete the file
        audioclip.close()
        #if os.path.exists(audiofilename):
        #    os.remove(audiofilename)

        #delete wav file for srt
        #if os.path.exists(os.path.join(directory, f'teaser.wav' )):
        #    os.remove(os.path.join(directory, f'teaser.wav' ))

        #delete srt file
        #subtitles.close()
        #if os.path.exists(os.path.join(directory, f'teaser.srt')):
        #    os.remove(os.path.join(directory, f'teaser.srt'))

    #creates our text clip
    def make_textclip2(self, txt):
        frameSize = (1080, 1920)
        txt_clip = TextClip(font=FONT_NAME,text = txt, font_size = 60, size=frameSize, method='caption', color = '#FFFFFF', stroke_color='#000000', stroke_width = 3, 
                        text_align="center",
                        horizontal_align="center",
                        vertical_align="bottom",)
        return txt_clip
    
    #Takes a videos audio and writes it to a wav file
    def create_audio_file(self, videofile, audiofile, openvideo=False, closevideo = False):
        # Load the video file
        if openvideo:
            video = VideoFileClip(videofile)
        else:
            video = videofile

        # Extract the audio from the video
        audio = video.audio

        # Write the audio to a WAV file
        if os.path.exists(audiofile):
            os.remove(audiofile)
            time.sleep(.5)

        audio.write_audiofile(audiofile)

        # Close the video file
        if closevideo:
            video.close()
        audio.close()

    # Used for creating video with a longer title intro and outro
    def Create_Video_With_Audio5(self, audiofilename, extra_seconds, directory, directory_images, title_intro, title_outro, count, story_part, image_size):
        FRAMES_PER_SECOND = 20
        
        audio = MP3(audiofilename)
        print('\n*******************\n\n')
        print(audio.info.length)
        
        seconds = np.ceil(audio.info.length)

        frameSize = (image_size[0], image_size[1])
        #*'mp4v'
        #*'DIVX'
        out = cv2.VideoWriter(os.path.join(directory,f'video{count}.mp4'),cv2.VideoWriter_fourcc(*'mp4v'), FRAMES_PER_SECOND, frameSize)

        #60 frames per second. add extra seconds
        total_frames = int((seconds + extra_seconds) * FRAMES_PER_SECOND)
        
        image = cv2.imread(os.path.join(directory_images, f'Image{count}.png'))

        # Resize the image to match the frame size if necessary

        image = cv2.resize(image, (frameSize[0], frameSize[1]))  # Resize to (width, height)

        #image = cv2.resize(image, (512,512))
        for i in range(total_frames):
            #img = cv2.imread(os.path.join(directory_images, f'Image{count}.png'))
            out.write(image)

        out.release()

        #now put them together
        videoclip = VideoFileClip(os.path.join(directory,f'video{count}.mp4'))
                
        #show title
        if count == 0:
            duration = videoclip.duration

            x1 = videoclip.subclipped(0,1)
            x2 = videoclip.subclipped(1, duration-1)
            x3 = videoclip.subclipped(-1)
            

            # Generate a text clip  
            newFrame = (int( frameSize[0] - (frameSize[0] * 0.1) ), int(frameSize[1]/8) )
            txt_clip = TextClip(font=FONT_NAME,text = story_part, font_size = 75, size=newFrame, method='caption', color = '#FFFFFF', stroke_color='#000000', stroke_width = 3, margin = (0,100), duration = duration - 2.0, text_align ='center')

            #txt_clip = txt_clip.with_position(('top'))
            txt_clip = txt_clip.with_position(('center', 'top'))

            txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])
            
            # Overlay the text clip on the first video clip  
            x2 = CompositeVideoClip([x2, txt_clip])  

            x2.write_videofile(os.path.join(directory,f'x2{count}.mp4'))
            videos = [x1,x2,x3]
            videoclip = concatenate_videoclips(videos)#.with_effects([vfx.FadeIn(1.0, 0.0), vfx.FadeOut(1.0, 0.0)])

        #get audio clip and add to video
        audioclip = AudioFileClip(audiofilename)

        new_audioclip = CompositeAudioClip([audioclip])
        p1 = videoclip.subclipped(0,int(extra_seconds/2))#.with_effects([vfx.CrossFadeIn(1.0)])
        p2 = videoclip.subclipped(int(extra_seconds/2), videoclip.duration - int(extra_seconds/2))
        p3 = videoclip.subclipped(videoclip.duration - (extra_seconds/2), videoclip.duration)
        p2.audio = new_audioclip

        videos = [p1,p2,p3]
        finalVideo = concatenate_videoclips(videos).with_effects([vfx.FadeIn(1.0, 0.0), vfx.FadeOut(1.0, 0.0)])

        #create for our subtitles
        faded_subtitles = []

        #add subtitles to video
        if count > 0:
            
            #get the audio
            wavfilename = os.path.join(directory, f'wav{count}.wav' )
            self.create_audio_file(finalVideo, wavfilename)

            #now create our srt
            self.Create_SRT(directory, wavfilename, count, story_part, 0)

            #get the subtitles
            srtfile = os.path.join(directory, f'srt{count}.srt')
            subtitles = SubtitlesClip(subtitles=srtfile, make_textclip=self.make_textclip2, encoding="windows-1252")

            total = len(subtitles.subtitles)
            num = 0
            for sub in subtitles.subtitles:  # Iterate through the subtitle events
                #start_time, end_time, text = sub
                start_time = sub[0][0]
                end_time = sub[0][1]
                text = sub[1]
                duration = end_time - start_time

                textclip = self.make_textclip2(text)
                textclip.start = start_time
                textclip.duration = duration
                textclip.end = end_time
                textclip = textclip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])
                

                faded_subtitles.append(textclip)

                num = num + 1

            print('ok')

        #if we have subtitles
        if len(faded_subtitles) > 0 :         
            
            #concat our subtitles and join with finalvideo
            faded_vids = concatenate_videoclips(faded_subtitles)#, method='compose')

            # Create a silent clip of 1-second duration
            silent_clip = ColorClip(size=(1, 1), color=(0, 0, 0), duration=int(extra_seconds/2) )
            silent_clip = silent_clip.with_opacity(0) #.set_opacity(0) # Make it transparent

            # Concatenate the silent clip with the subtitles to introduce the 1-second delay
            delayed_subtitles = concatenate_videoclips([silent_clip, faded_vids])

            # Overlay the delayed subtitles on the video
            finalVideo = CompositeVideoClip([finalVideo, delayed_subtitles])

        finalVideo.write_videofile(os.path.join(directory,f'video_audio{count}.mp4'))

        #now clean up files not needed
        videoclip.close()
        if os.path.exists(os.path.join(directory,f'video{count}.mp4')):
            os.remove(os.path.join(directory,f'video{count}.mp4'))

        #delete audio file
        #audioclip.close()
        #if os.path.exists(audiofilename):
        #    os.remove(audiofilename)

        #delete wav file for srt
        if os.path.exists(os.path.join(directory, f'wav{count}.wav' )):
            os.remove(os.path.join(directory, f'wav{count}.wav' ))

        #delete srt file
        if os.path.exists(os.path.join(directory, f'srt{count}.srt')):
            os.remove(os.path.join(directory, f'srt{count}.srt'))

    #used for creating video with short intro and outros
    def Create_Video_With_Audio6(self, audiofilename, extra_seconds, directory, directory_images, count, story_part, main_title, image_size):
        FRAMES_PER_SECOND = 20
        
        audio = MP3(audiofilename)
        print('\n*******************\n\n')
        print(audio.info.length)
        
        seconds = np.ceil(audio.info.length)

        frameSize = (image_size[0], image_size[1])
        #*'mp4v'
        #*'DIVX'
        out = cv2.VideoWriter(os.path.join(directory,f'video{count}.mp4'),cv2.VideoWriter_fourcc(*'mp4v'), FRAMES_PER_SECOND, frameSize)

        #60 frames per second. add extra seconds
        total_frames = int((seconds + extra_seconds) * FRAMES_PER_SECOND)
        
        #get our image
        image = cv2.imread(os.path.join(directory_images, f'Image{count}.png'))

        # Resize the image to match the frame size if necessary
        image = cv2.resize(image, (frameSize[0], frameSize[1]))  # Resize to (width, height)

        #now write the image for total frames needed
        for i in range(total_frames):
            out.write(image)

        out.release()

        #now put them together
        videoclip = VideoFileClip(os.path.join(directory,f'video{count}.mp4'))
        
        #show title
        if count == 0:
            duration = videoclip.duration

            #seperate the video into 3 clips. Middle is for text
            x1 = videoclip.subclipped(0,1)
            x2 = videoclip.subclipped(1, duration-1)
            x3 = videoclip.subclipped(-1)            

            # Generate a text clip  
            newFrame = (int( frameSize[0] - (frameSize[0] * 0.1) ), int(frameSize[1]/8) )
            txt_clip = TextClip(font=FONT_NAME,text = main_title, font_size = 75, size=newFrame, method='caption', color = '#FFFFFF', stroke_color='#000000', stroke_width = 3, margin = (0,100), duration = duration - 2.0, text_align ='center')
            txt_clip = txt_clip.with_position(('center', 'top'))
            txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])
            
            # Overlay the text clip on the first video clip  
            x2 = CompositeVideoClip([x2, txt_clip])  

            #write it and then concat them
            x2.write_videofile(os.path.join(directory,f'x2{count}.mp4'))
            videos = [x1,x2,x3]
            videoclip = concatenate_videoclips(videos)

        #load our audio clip and then add it to our video
        audioclip = AudioFileClip(audiofilename)
        new_audioclip = CompositeAudioClip([audioclip])
        p1 = videoclip.subclipped(0,int(extra_seconds/2))#.with_effects([vfx.CrossFadeIn(1.0)])
        p2 = videoclip.subclipped(int(extra_seconds/2), videoclip.duration - int(extra_seconds/2))
        p3 = videoclip.subclipped(videoclip.duration - (extra_seconds/2), videoclip.duration)
        p2.audio = new_audioclip

        #concat video to use
        videos = [p1,p2,p3]
        finalVideo = concatenate_videoclips(videos).with_effects([vfx.FadeIn(1.0, 0.0), vfx.FadeOut(1.0, 0.0)])

        #create for our subtitles
        faded_subtitles = []

        #add subtitles to video
        if count > 0:
            
            #get the audio
            wavfilename = os.path.join(directory, f'wav{count}.wav' )
            self.create_audio_file(finalVideo, wavfilename)

            #now create our srt
            self.Create_SRT(directory, wavfilename, count, story_part, 0)

            #get the subtitles
            srtfile = os.path.join(directory, f'srt{count}.srt')
            subtitles = SubtitlesClip(subtitles=srtfile, make_textclip=self.make_textclip2, encoding="windows-1252")#.with_effects([vfx.FadeIn(0.5, 0.0), vfx.FadeOut(0.5, 0.0)])
    
            total = len(subtitles.subtitles)
            num = 0
            for sub in subtitles.subtitles:  # Iterate through the subtitle events
                #start_time, end_time, text = sub
                start_time = sub[0][0]
                end_time = sub[0][1]
                text = sub[1]
                duration = end_time - start_time

                textclip = self.make_textclip2(text)
                textclip.start = start_time
                textclip.duration = duration

                #set our textclip end and then effects to it
                textclip.end = end_time
                textclip = textclip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])              
                faded_subtitles.append(textclip)

                num = num + 1

            print('ok')

        #if we have subtitles
        if len(faded_subtitles) > 0 :         
            
            #concat our subtitles and join with finalvideo
            faded_vids = concatenate_videoclips(faded_subtitles)#, method='compose')

            # Create a silent clip of 1-second duration
            silent_clip = ColorClip(size=(1, 1), color=(0, 0, 0), duration=int(extra_seconds/2) )
            silent_clip = silent_clip.with_opacity(0) #.set_opacity(0) # Make it transparent

            # Concatenate the silent clip with the subtitles to introduce the 1-second delay
            delayed_subtitles = concatenate_videoclips([silent_clip, faded_vids])

            # Overlay the delayed subtitles on the video
            finalVideo = CompositeVideoClip([finalVideo, delayed_subtitles])

        finalVideo.write_videofile(os.path.join(directory,f'video_audio{count}.mp4'))

        #now clean up files not needed
        videoclip.close()
        if os.path.exists(os.path.join(directory,f'video{count}.mp4')):
            os.remove(os.path.join(directory,f'video{count}.mp4'))

        #delete audio file
        #audioclip.close()
        #if os.path.exists(audiofilename):
        #    os.remove(audiofilename)

        #delete wav file for srt
        if os.path.exists(os.path.join(directory, f'wav{count}.wav' )):
            os.remove(os.path.join(directory, f'wav{count}.wav' ))

        #delete srt file
        if os.path.exists(os.path.join(directory, f'srt{count}.srt')):
            os.remove(os.path.join(directory, f'srt{count}.srt'))
    
    #used for the new intro and outro 5/1/25
    def Create_Final_Video5(self, directory, count, music, intro_file, outro_file, directory_num):
        all_videos = []

        #we want to create individual lists for each type of music in a row. Ex: Type A A, B B B, C, A ... etc
            
        for i in range(count):
            all_videos.append(VideoFileClip(os.path.join(directory,f'video_audio{i}.mp4')))

        videos_music_files = self.Get_Videos_Music_File(all_videos, music)

        #now add music to video section and return the concat music for each part
        final_videos = []
        num = 0
        for videos in videos_music_files:

            #our first spot in the array is our intro and it has no music
            if num == 0:
                final_videos.append( videos[0] )
            #if its our last video, send in true for earlier fade out
            elif num == len(videos_music_files) - 1:
                final_videos.append( self.Add_Music_To_Videos(videos, True) )
            #send in videos to add music with normal fade out
            else:
                final_videos.append(  self.Add_Music_To_Videos(videos, False) )
            
            num = num + 1

        finalVideo = concatenate_videoclips(final_videos)#.with_effects([vfx.FadeOut(1.0, 0.0)])


        #open the files
        intro_video = VideoFileClip(intro_file)
        outro_video = VideoFileClip(outro_file)

        #intro_video = self.Create_Intro_Video(directory, intro, 4)
        #outro_video = self.Create_Outro_Video(directory, outro, 4)

        #now join them all together
        finalVideo = concatenate_videoclips([intro_video, finalVideo, outro_video])

        #finalVideo = CompositeVideoClip([finalVideo]).with_effects([vfx.CrossFadeOut(1.0)])
        finalVideo.write_videofile(os.path.join(directory,f'FINAL_VIDEO_TITLE_INTRO_{str(directory_num)}.mp4'), audio_codec='aac')

        #UNCOMMENT FOR SMALLER VIDEO
        #resize to half its size and save it to small name
        ######finalVideo.with_effects([vfx.Resize(0.1)]).write_videofile(os.path.join(directory,f'FINAL_VIDEO_SMALL.mp4'), audio_codec='aac')

        #close videos and delete them
        try :
            for vid in all_videos:
                vid.close()

            #now delete videos
            for i in range(count):
                if os.path.exists(os.path.join(directory,f'video_audio{i}.mp4')):
                    os.remove(os.path.join(directory,f'video_audio{i}.mp4'))
        except:
            pass

        #close videos
        intro_video.close()
        outro_video.close()

    #Used for creating a longer version of our intro video (no longer used)
    def Create_Intro_Video(self, directory, intro, extra_seconds):
        intro = intro.replace('#','')
        intro = intro.replace('*','')
        intro = intro.replace('—','-')
        intro = intro.replace('’','')
        intro = intro.replace('–','-') 
        intro = intro.replace('..','')
        intro = intro.replace('…','.')
        intro = intro.replace('”','"')
        intro = intro.replace('“','"')
        #intro = intro.lstrip()  
        #get our audio
        #return audio file name
        audiofilename = self.Creat_Audio(intro, directory, 'en_uk_003')

        audio = MP3(audiofilename)
        print('\n*******************\n\n')
        print(audio.info.length)
        
        seconds = np.ceil(audio.info.length)

        #open video to use :
        #Read the video
        cap =cv2.VideoCapture(INTRO_OUTRO_VIDEOFILE)

        #Work with the frames
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)            

        #Work with the frames
        fps = cap.get(cv2.CAP_PROP_FPS)       

        #Extract the height and width
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)            

        #Extract the height and width
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            

        #Initiate the output writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        print('\nCreating intro without audio...\n\n')

        out = cv2.VideoWriter(os.path.join(directory,f'intro_videoX.mp4'),cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width), int(height)))

        #frames per second. add extra seconds
        total_frames = int((seconds + extra_seconds) * fps)

        #lets us know get frames going in forward direction. If false, get going in reverse
        forward = True
        frame_index = 0
        for i in range(total_frames):
            if(cap.isOpened()):
                if forward and frame_index < frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                    ret, frame = cap.read()
                    frame = cv2.resize(frame,(int(width), int(height)))
                    #frame = cv2.resize(frame,(int(1080), int(1920)))
                    out.write(frame)
                    frame_index = frame_index+1

                    #check to see if we need to go reverse now
                    if frame_index >= frames:
                        forward = False
                        frame_index = frames - 1

                elif not forward and frame_index >= 0:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                    ret, frame = cap.read()
                    frame = cv2.resize(frame,(int(width), int(height)))
                    #frame = cv2.resize(frame,(int(1080), int(1920)))
                    out.write(frame)
                    frame_index = frame_index-1

                    #check to see if we need to go forward now
                    if frame_index < 0:
                        forward = True
                        frame_index = 0
        #end of for

        out.release()
        cap.release()

        print('\nCreating intro with audio...\n\n')

        #now put them together
        videoclip = VideoFileClip(os.path.join(directory,f'intro_videoX.mp4'))

        #now create voice audio
        audioclip = AudioFileClip(audiofilename)

        new_audioclip = CompositeAudioClip([audioclip])
        p1 = videoclip.subclipped(0,int(extra_seconds/2))#.with_effects([vfx.CrossFadeIn(1.0)])
        p2 = videoclip.subclipped(int(extra_seconds/2), videoclip.duration - int(extra_seconds/2))
        p3 = videoclip.subclipped(videoclip.duration - (extra_seconds/2), videoclip.duration)
        p2.audio = new_audioclip

        videos = [p1,p2,p3]
        finalVideo = concatenate_videoclips(videos).with_effects([vfx.FadeIn(2.0, 0.0), vfx.FadeOut(2.0, 0.0)])

        #create the srt file needed for this

        #get the audio
        wavfilename = os.path.join(directory, f'intro.wav' )
        self.create_audio_file(finalVideo, wavfilename)

        #now create our srt
        self.Create_SRT(directory, wavfilename, 0, intro, 0, 'intro.srt')

        #get the subtitles
        srtfile = os.path.join(directory, f'intro.srt')
        subtitles = SubtitlesClip(subtitles=srtfile, make_textclip=self.make_textclip2, encoding="windows-1252")#.with_effects([vfx.FadeIn(0.5, 0.0), vfx.FadeOut(0.5, 0.0)])

        #print(subtitles.size)
        faded_subtitles = []

        total = len(subtitles.subtitles)
        num = 0
        for sub in subtitles.subtitles:  # Iterate through the subtitle events
            #start_time, end_time, text = sub
            start_time = sub[0][0]
            end_time = sub[0][1]
            text = sub[1]
            duration = end_time - start_time

            textclip = self.make_textclip2(text)
            textclip.start = start_time            
            textclip.duration = duration
            textclip.end = end_time

            textclip = textclip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])

            faded_subtitles.append(textclip)

            num = num + 1

        print('ok')

        #if we have subtitles
        if len(faded_subtitles) > 0 :         
            
            #concat our subtitles and join with finalvideo
            faded_vids = concatenate_videoclips(faded_subtitles)#, method='compose')

            # Create a silent clip of 1-second duration
            silent_clip = ColorClip(size=(1, 1), color=(0, 0, 0), duration=int(extra_seconds/2) )
            silent_clip = silent_clip.with_opacity(0) #.set_opacity(0) # Make it transparent

            # Concatenate the silent clip with the subtitles to introduce the 1-second delay
            delayed_subtitles = concatenate_videoclips([silent_clip, faded_vids])

            # Overlay the delayed subtitles on the video
            finalVideo = CompositeVideoClip([finalVideo, delayed_subtitles])

        #now create the music audio
        #load music
        path = os.path.join('Music', 'Intro')
        audioclip = AudioFileClip(os.path.join(path,'TheIntroMusic.mp3') )
        new_audioclip = CompositeAudioClip([audioclip])

        fade_out = "00:00:02"

        #set the audio effects
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeIn("00:00:02")]).with_effects([afx.AudioFadeOut(fade_out)]).with_effects([afx.AudioLoop(duration=finalVideo.duration)]).with_effects([afx.MultiplyVolume(0.20)])
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeOut(fade_out)])

        #join our video audio and our music audio together
        total_audios = CompositeAudioClip([new_audioclip, finalVideo.audio])

        #now set out videos audio to the composite audio
        finalVideo.audio = total_audios


        finalVideo.write_videofile(os.path.join(directory,f'intro_videoX2.mp4'))

        print('\nFinished creating intro with audio!\n\n')
        videoclip.close()
        if os.path.exists(os.path.join(directory,f'intro_videoX.mp4')):
            os.remove(os.path.join(directory,f'intro_videoX.mp4'))

        #delete wav file for srt
        if os.path.exists(os.path.join(directory, f'intro.wav' )):
            os.remove(os.path.join(directory, f'intro.wav' ))

        #delete srt file
        #subtitles.close()
        #if os.path.exists(os.path.join(directory, f'intro.srt')):
        #    os.remove(os.path.join(directory, f'intro.srt'))

        #return finalVideo
        return os.path.join(directory,f'intro_videoX2.mp4')

    #User for creating a longer version of outro video (no longer used)
    def Create_Outro_Video(self, directory, outro, extra_seconds):
        outro = outro.replace('#','')
        outro = outro.replace('*','')
        outro = outro.replace('—','-')
        outro = outro.replace('’','')
        outro = outro.replace('–','-') 
        outro = outro.replace('..','')
        outro = outro.replace('…','.')
        outro = outro.replace('”','"')
        outro = outro.replace('“','"')
        #outro = outro.lstrip()  
        #get our audio
        #return audio file name
        audiofilename = self.Creat_Audio(outro, directory, 'en_uk_003')

        audio = MP3(audiofilename)
        print('\n*******************\n\n')
        print(audio.info.length)
        
        seconds = np.ceil(audio.info.length)

        #open video to use :
        #Read the video
        cap =cv2.VideoCapture(INTRO_OUTRO_VIDEOFILE)

        #Work with the frames
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)            

        #Work with the frames
        fps = cap.get(cv2.CAP_PROP_FPS)       

        #Extract the height and width
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)            

        #Extract the height and width
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            

        #Initiate the output writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        print('\nCreating outro without audio...\n\n')

        out = cv2.VideoWriter(os.path.join(directory,f'outro_videoX.mp4'),cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width), int(height)))

        #frames per second. add extra seconds
        total_frames = int((seconds + extra_seconds) * fps)

        #lets us know get frames going in forward direction. If false, get going in reverse
        forward = True
        frame_index = 0
        for i in range(total_frames):
            if(cap.isOpened()):
                if forward and frame_index < frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                    ret, frame = cap.read()
                    frame = cv2.resize(frame,(int(width), int(height)))
                    #frame = cv2.resize(frame,(int(1080), int(1920)))
                    out.write(frame)
                    frame_index = frame_index+1

                    #check to see if we need to go reverse now
                    if frame_index >= frames:
                        forward = False
                        frame_index = frames - 1

                elif not forward and frame_index >= 0:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                    ret, frame = cap.read()
                    frame = cv2.resize(frame,(int(width), int(height)))
                    #frame = cv2.resize(frame,(int(1080), int(1920)))
                    out.write(frame)
                    frame_index = frame_index-1

                    #check to see if we need to go forward now
                    if frame_index < 0:
                        forward = True
                        frame_index = 0
        #end of for

        out.release()
        cap.release()

        print('\nCreating outro with audio...\n\n')

        #now put them together
        videoclip = VideoFileClip(os.path.join(directory,f'outro_videoX.mp4'))

        #now create voice audio
        audioclip = AudioFileClip(audiofilename)

        new_audioclip = CompositeAudioClip([audioclip])
        p1 = videoclip.subclipped(0,int(extra_seconds/2))#.with_effects([vfx.CrossFadeIn(1.0)])
        p2 = videoclip.subclipped(int(extra_seconds/2), videoclip.duration - int(extra_seconds/2))
        p3 = videoclip.subclipped(videoclip.duration - (extra_seconds/2), videoclip.duration)
        p2.audio = new_audioclip

        videos = [p1,p2,p3]
        finalVideo = concatenate_videoclips(videos).with_effects([vfx.FadeIn(2.0, 0.0), vfx.FadeOut(2.0, 0.0)])

        #create the srt file needed for this
        #get the audio
        wavfilename = os.path.join(directory, f'outro.wav' )
        self.create_audio_file(finalVideo, wavfilename)

        #now create our srt
        self.Create_SRT(directory, wavfilename, 0, outro, 0, 'outro.srt')

        #get the subtitles
        srtfile = os.path.join(directory, f'outro.srt')
        subtitles = SubtitlesClip(subtitles=srtfile, make_textclip=self.make_textclip2, encoding="windows-1252")#.with_effects([vfx.FadeIn(0.5, 0.0), vfx.FadeOut(0.5, 0.0)])

        #print(subtitles.size)
        faded_subtitles = []
        
        #extra_seconds = 2
        #fade_duration = int(extra_seconds / 2)

        total = len(subtitles.subtitles)
        num = 0
        for sub in subtitles.subtitles:  # Iterate through the subtitle events
            #start_time, end_time, text = sub
            start_time = sub[0][0]
            end_time = sub[0][1]
            text = sub[1]
            duration = end_time - start_time

            textclip = self.make_textclip2(text)
            textclip.start = start_time
            
            # Calculate the intended end time of the textclip within faded_vids
            #intended_end_time = end_time

            textclip.duration = duration

            textclip.end = end_time

            textclip = textclip.with_effects([vfx.CrossFadeIn(0.25), vfx.CrossFadeOut(0.25)])

            faded_subtitles.append(textclip)

            num = num + 1

        print('ok')

        #if we have subtitles
        if len(faded_subtitles) > 0 :         
            
            #concat our subtitles and join with finalvideo
            faded_vids = concatenate_videoclips(faded_subtitles)#, method='compose')

            # Create a silent clip of 1-second duration
            silent_clip = ColorClip(size=(1, 1), color=(0, 0, 0), duration=int(extra_seconds/2) )
            silent_clip = silent_clip.with_opacity(0) #.set_opacity(0) # Make it transparent

            # Concatenate the silent clip with the subtitles to introduce the 1-second delay
            delayed_subtitles = concatenate_videoclips([silent_clip, faded_vids])

            # Overlay the delayed subtitles on the video
            finalVideo = CompositeVideoClip([finalVideo, delayed_subtitles])

        #now create the music audio
        #load music
        path = os.path.join('Music', 'Outro')
        audioclip = AudioFileClip(os.path.join(path,'TheOutroMusic.mp3') )
        new_audioclip = CompositeAudioClip([audioclip])

        fade_out = "00:00:02"

        #set the audio effects
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeIn("00:00:02")]).with_effects([afx.AudioFadeOut(fade_out)]).with_effects([afx.AudioLoop(duration=finalVideo.duration)]).with_effects([afx.MultiplyVolume(0.20)])
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeOut(fade_out)])

        #join our video audio and our music audio together
        total_audios = CompositeAudioClip([new_audioclip, finalVideo.audio])

        #now set out videos audio to the composite audio
        finalVideo.audio = total_audios


        finalVideo.write_videofile(os.path.join(directory,f'outro_videoX2.mp4'))

        print('\nFinished creating outro with audio!\n\n')
        videoclip.close()
        if os.path.exists(os.path.join(directory,f'outro_videoX.mp4')):
            os.remove(os.path.join(directory,f'outro_videoX.mp4'))

        #delete wav file for srt
        if os.path.exists(os.path.join(directory, f'outro.wav' )):
            os.remove(os.path.join(directory, f'outro.wav' ))

        #delete srt file
        #subtitles.close()
        #if os.path.exists(os.path.join(directory, f'outro.srt')):
        #    os.remove(os.path.join(directory, f'outro.srt'))


        #return finalVideo
        return os.path.join(directory,f'outro_videoX2.mp4')

    #take out videos and match them up with music files
    def Get_Videos_Music_File(self, all_videos, music):
        music_load = Music_Loader()
        
        concat_vids = []

        #title intro has no music
        concat_vids.append( (all_videos[0], '') )

        #Used to match up video files, with our types of music
        i = 1
        while i < len(all_videos):
            vids = []
            #vids.append( (all_videos[i], music[i]) )
            vids.append( (all_videos[i], music_load.get_music_file_name(music[i]) ) )

            if i + 1 >= len(all_videos):
                concat_vids.append(vids)
                break
            
            concat = False
            for j in range(i + 1,len(all_videos)):
                if music[i] == music[j]:
                    vids.append( (all_videos[j], music_load.get_music_file_name(music[j]) ) )
                else:
                    concat_vids.append(vids)
                    i = j
                    concat = True
                    break
            
            #this checks to see if its the final end of while loop for last music types
            if not concat:
                concat_vids.append(vids)
                concat = True
                break

        return concat_vids
    
    #used to add the music to our teaser video
    def Add_Music_To_Teaser_Video(self, video, music_file):
        
        #load music file
        audioclip = AudioFileClip(music_file)
        new_audioclip = CompositeAudioClip([audioclip])

        fade = "00:00:02"

        #set the audio effects
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeIn(fade)]).with_effects([afx.AudioFadeOut(fade)]).with_effects([afx.AudioLoop(duration=video.duration)]).with_effects([afx.MultiplyVolume(0.20)])
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeOut(fade)])

        #join our video audio and our music audio together
        total_audios = CompositeAudioClip([new_audioclip, video.audio])

        #now set out videos audio to the composite audio
        video.audio = total_audios

        return video
    
    #this will add the music to the video list sent in. videos[0] is the video and video[0][1] is the music
    def Add_Music_To_Videos(self, videos, last_videos):
        concat1 = []

        #put all videos in a list to be concatinated
        for video in videos:
            concat1.append(video[0])

        #now join them all together
        video_for_music = concatenate_videoclips(concat1)
        
        #now add the music to the video
        #load music
        audioclip = AudioFileClip(videos[0][1])
        new_audioclip = CompositeAudioClip([audioclip])

        #if this is our last video of the story, fade out earlier
        if last_videos:
            fade_out = "00:00:06"
        else:
            fade_out = "00:00:02"

        #set the audio effects
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeIn("00:00:02")]).with_effects([afx.AudioFadeOut(fade_out)]).with_effects([afx.AudioLoop(duration=video_for_music.duration)]).with_effects([afx.MultiplyVolume(0.20)])
        new_audioclip = new_audioclip.with_effects([afx.AudioFadeOut(fade_out)])

        #join our video audio and our music audio together
        total_audios = CompositeAudioClip([new_audioclip, video_for_music.audio])

        #now set out videos audio to the composite audio
        video_for_music.audio = total_audios

        return video_for_music

    #create the teaser video with data sent in
    def Create_Teaser_Video(self, teaser, story_title, directory, directory_images, voice, image_size, music, images_to_use, directory_num):
        #set buffer seconds
        extra_seconds = 2

        #make sure these characters are not in string or it will error out text to audio
        teaser = teaser.replace('#','')
        teaser = teaser.replace('*','')
        teaser = teaser.replace('—','-')
        teaser = teaser.replace('’','')
        teaser = teaser.replace('..','')
        teaser = teaser.replace('–','-')
        teaser = teaser.replace('…','.')
        teaser = teaser.replace('”','"')
        teaser = teaser.replace('“','"')
        #sorted_story[i] = sorted_story[i].replace('"','')
        teaser = teaser.lstrip()

        story_title = story_title.replace('#','')
        story_title = story_title.replace('*','')
        story_title = story_title.replace('—','-')
        story_title = story_title.replace('’','')
        story_title = story_title.replace('..','')
        story_title = story_title.replace('–','-')
        story_title = story_title.replace('…','.')
        story_title = story_title.replace('”','"')
        story_title = story_title.replace('“','"')
        #sorted_story[i] = sorted_story[i].replace('"','')
        story_title = story_title.lstrip()  

        #return audio file name
        audiofilename = self.Creat_Audio(teaser, directory, voice)

        #now create and write the video file
        self.Create_Teaser_Video_With_Audio2(audiofilename, extra_seconds, directory, directory_images, teaser, story_title, image_size, images_to_use, music, directory_num)

    #this will create the video with the data sent in.
    def Create_Full_Video(self, story, sorted_story, title, directory, directory_images, voice, image_size, music, title_intro, title_outro, intro_file, outro_file, directory_num):
        
        main_title = title

        #go through all descriptions and images
        for i in range(0,len(sorted_story)):  

            #if title screen, add 6 extra seconds. else just 2
            #we also need to check our text for certain characters that can error out our text to audio
            if i == 0:
                extra_seconds = 6
                sorted_story[i] = sorted_story[i].replace('#','')
                sorted_story[i] = sorted_story[i].replace('*','')
                sorted_story[i] = sorted_story[i].replace('—','-')
                sorted_story[i] = sorted_story[i].replace('’',f"""'""")
                sorted_story[i] = sorted_story[i].replace(':','')
                sorted_story[i] = sorted_story[i].replace('..','')
                sorted_story[i]  = sorted_story[i].replace('–','-')
                sorted_story[i]  = sorted_story[i].replace('…','.')
                sorted_story[i] = sorted_story[i].replace('“','"')
                sorted_story[i] = sorted_story[i].replace('”','"')     
                #sorted_story[i] = sorted_story[i].replace('"','')
                sorted_story[i] = sorted_story[i].lstrip()

                main_title = main_title.replace('#','')
                main_title = main_title.replace('*','')
                main_title = main_title.replace('—','-')
                main_title = main_title.replace('’',f"""'""")
                main_title = main_title.replace(':','')
                main_title = main_title.replace('..','')
                main_title  = main_title.replace('–','-')
                main_title  = main_title.replace('…','.')
                main_title = main_title.replace('“','"')
                main_title = main_title.replace('”','"')     
                main_title = main_title.lstrip()

            else:
                extra_seconds = 2
                sorted_story[i] = sorted_story[i].replace('#','')
                sorted_story[i] = sorted_story[i].replace('*','')
                sorted_story[i] = sorted_story[i].replace('—','-')
                sorted_story[i] = sorted_story[i].replace('’',f"""'""")
                sorted_story[i] = sorted_story[i].replace('..','')
                sorted_story[i]  = sorted_story[i].replace('–','-')
                sorted_story[i]  = sorted_story[i].replace('…','.')
                sorted_story[i] = sorted_story[i].replace('”','"')
                sorted_story[i] = sorted_story[i].replace('“','"')
                #sorted_story[i] = sorted_story[i].replace('"','')
                #sorted_story[i] = sorted_story[i].lstrip()    
                
            #return audio file name
            audiofilename = self.Creat_Audio(sorted_story[i], directory, voice)

            #create the video with our newly created audio file and the rest of our data sent in
            self.Create_Video_With_Audio6(audiofilename, extra_seconds, directory, directory_images, i, sorted_story[i], main_title, image_size)

        #now put them all together
        self.Create_Final_Video5(directory, len(sorted_story), music, intro_file, outro_file, directory_num)