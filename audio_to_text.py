'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : This is for creating our subtitles on the videos. It will take an audio file, use whisper to create an srt file. We can then use this srt file to 
take our original text, that the audio was created with, to fix the words whisper got wrong. We do this so we can make our text up correctly with what is being said 
by the narrator. 

'''
import whisper
from datetime import timedelta
from moviepy import *
import re
#import torch

#import srt

#FONT_NAME = "AgeniaRegular-xR4Y0.otf"

FONT_NAME = r"C:\Windows\Fonts\Arial.ttf" #"Arial" 

#Our class for processing the audio
class Audio_to_Text:
    def __init__(self):
        pass
    
    #our format for SRT
    def format_timedelta(self, seconds):
        """Formats seconds into SRT time format: HH:MM:SS,milliseconds."""
        td = timedelta(seconds=seconds)
        minutes, seconds = divmod(td.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    #this will transcribe our audio with whisper, for our srt file
    def transcribe_whisper(self, audio_file_path, model_name="small"):
        # Load Whisper model
        model = whisper.load_model(model_name, device="cpu")

        # Transcribe audio
        result = model.transcribe(audio_file_path, language="en", temperature=0.1, word_timestamps=True)
        
        # Step 1: Get the segments from the transcription result
        segments = result.get("segments", [])
        
        # Step 2: Remove empty segments (empty strings or whitespace-only)
        filtered_segments = [seg for seg in segments if seg['text'].strip() != ""]

        # Step 3: Remove **all** duplicate segments (not just consecutive ones)
        seen_texts = set()  # A set to keep track of unique texts
        unique_segments = []

        for seg in filtered_segments:
            if seg['text'] not in seen_texts:
                unique_segments.append(seg)
                seen_texts.add(seg['text'])

        # Step 4: (Optional) If you want to return the cleaned segments as plain text
        cleaned_text = [seg['text'] for seg in unique_segments]

        print(cleaned_text)
        
        # Return the cleaned segments
        return unique_segments#, cleaned_text

    #writes the segments to the output file name choosen for srt file
    def write_srt2(self, segments, srt_output_file):
        """
        Write the corrected segments to an SRT file.
        """
        with open(srt_output_file, 'w', encoding='utf-8') as file:
            for idx, segment in enumerate(segments, 1):
                start_time = self.format_timedelta(segment['start'])
                end_time = self.format_timedelta(segment['end'])
                text = segment['text']

                #fix the text
                text = text.replace('#','')
                text = text.replace('*','')
                text = text.replace('—','-')
                text = text.replace('–','-')                
                text = text.replace('’',f"""'""")
                text = text.replace('..','')
                text = text.replace('…','.')
                text = text.replace('”','"')
                text = text.replace('“','"')

                # Strip any trailing newlines or whitespace
                text = text.rstrip()
                
                # Write each segment in SRT format
                file.write(f"{idx}\n")
                file.write(f"{start_time} --> {end_time}\n")
                file.write(f"{text}\n\n")

    #This will sort our SRT file and fix any text that does not match our original text.
    def Sort_SRT_With_Orig_Text(self, orig_text, segments):
        ###########
        #orig text in words
        orig_words = [word.lower() for word in re.findall(r"\b[a-zA-Z']+\b", orig_text)]

        #create a string of words in lower case
        orig_string = ''
        new_words = ' '.join(orig_words)
        orig_string = orig_string + new_words
        orig_string = orig_string.lstrip()

        #get the total size of words
        orig_total_size = len(orig_words)

        #############
        #get our segment words and their number of words in each segment
        segments_words = []
        segments_sizes = []
        segement_string = ''
        segment_total_size = 0

        #seperate the words with their sizes and put them into a string
        for i in range(len(segments)):
            #seperate our words
            segments_words.append([word.lower() for word in re.findall(r"\b[a-zA-Z']+\b", segments[i]['text'])])

            #get its size and add it to total size
            segments_sizes.append(len(segments_words[i]))
            segment_total_size = segment_total_size + len(segments_words[i])

            #now create these words into a string and add it to total segment string
            new_words = ' '.join(segments_words[i])
            segement_string = segement_string + ' ' + new_words

        #remove the starting space
        segement_string = segement_string.lstrip()

        print(segement_string)
        print(segments_words)
        print(segments_sizes)
        print('\n\n\n')


        print('different')

        ##############
        # SAME SIZE CASE
        #lets see if they are the same size
        if segment_total_size == orig_total_size:
            print('equal')
            orig_text_start_index = 0
            orig_text_end_index = 0
            orig_current_word = 0

            new_segments = []

            # Use a regex to match word and punctuation chunks
            tokens = list(re.finditer(r'\S+', orig_text))

            for i in range(len(segments_sizes)):
                
                #Not needed. Sometimes it will be smaller
                #if len(tokens) >= segments_sizes[i]:

                #if we are at last index, then just go to the end of the array. If we use the end index, we will go over, because segment has more words
                if i == len(segments_sizes) - 1:
                    #get the text
                    text = orig_text[orig_text_start_index:]
                else:
                    #get our new end index
                    #make sure we do not go out of bounds on our index
                    index = orig_current_word + segments_sizes[i] - 1
                    if index >= len(tokens):
                        index = len(tokens)-1
                    orig_text_end_index = tokens[index].end()  # includes punctuation
                    #get the text
                    text = orig_text[orig_text_start_index:orig_text_end_index]

                #get our new end index
                #orig_text_end_index = tokens[orig_current_word + segments_sizes[i] - 1].end()  # includes punctuation
                
                #get the text
                #text = orig_text[orig_text_start_index:orig_text_end_index]

                #set our new start index
                orig_text_start_index = orig_text_end_index
                orig_current_word = orig_current_word + segments_sizes[i]

                new_segments.append(text)


            #print('\n\nORIGINAL SEGMENTS : ')
            #print(segments)

            print('\n\nUPDATED SEGMENTS : ')
            print(new_segments)

            final_text =  ''.join(new_segments)

            if final_text == orig_text:
                print('\n\nSAME!!')

            final_text = final_text.replace('\n\n', ' ')

            print('\n\nFINAL TEXT : \n' + final_text)

        ##############
        # GREATER OR LESS SIZE CASE SEGMENT != ORIG TEXT
        #too many words, just cut off end
        else:
            print('greater')

            orig_text_start_index = 0
            orig_text_end_index = 0
            orig_current_word = 0

            segment_current_word = 0

            new_segments = []

            # Use a regex to match word and punctuation chunks
            tokens = list(re.finditer(r'\S+', orig_text))

            for i in range(len(segments_sizes)):

                #Not needed. Sometimes it will be smaller   
                #if len(tokens) >= segments_sizes[i]:                
                    
                #if we are at last index, then just go to the end of the array. If we use the end index, we will go over, because segment has more words
                if i == len(segments_sizes) - 1:
                    #get the text
                    text = orig_text[orig_text_start_index:]
                else:
                    #get our new end index
                    #make sure we do not go out of bounds on our index
                    index = orig_current_word + segments_sizes[i] - 1
                    if index >= len(tokens):
                        index = len(tokens)-1
                    orig_text_end_index = tokens[index].end()  # includes punctuation
                    #orig_text_end_index = tokens[orig_current_word + segments_sizes[i] - 1].end()  # includes punctuation
                    #get the text
                    text = orig_text[orig_text_start_index:orig_text_end_index]

                #set our new start index
                orig_text_start_index = orig_text_end_index
                orig_current_word = orig_current_word + segments_sizes[i]

                new_segments.append(text)

            #print('\n\nORIGINAL SEGMENTS : ')
            #print(segments)

            print('\n\nUPDATED SEGMENTS : ')
            print(new_segments)

            final_text =  ''.join(new_segments)

            if final_text == orig_text:
                print('\n\nSAME!!')

            final_text = final_text.replace('\n\n', ' ')

            print('\n\nFINAL TEXT : \n' + final_text)


        # Replace '\n\n' with a space in each string in the list
        new_segments = [segment.replace('\n\n', ' ').lstrip() for segment in new_segments] 
        print('\n\n')
        print(new_segments)

        return new_segments
   

    #sends in our original text we want to create srt file with, the audio file for whisper, the name for our srt file and extra_seconds (not used now)
    #this will take the audio file and use whisper to get segments for an srt file. it will take original text and make sure whisper got our text correct.
    #if not, it will fix the segments text with original. we do this, because we want the audio time stamps (with whisper), to match our subtitles and we want the subtitles to be 
    #correct. whisper is prone to making mistakes.
    def Create_SRT_With_Orig_Text(self, orig_text, audio_file, srt_output_file, extra_seconds=0):
        # Get Whisper's transcription segments
        whisper_segments = self.transcribe_whisper(audio_file, model_name="medium") # "tiny", "base", "small", "medium", or "large"

        # Adjust the end time of each segment (except the last one)
        for i in range(1, len(whisper_segments)):
            whisper_segments[i-1]['end'] = whisper_segments[i]['start']

        #sort through segments
        new_segments = self.Sort_SRT_With_Orig_Text(orig_text, whisper_segments)
        
        #it was different, so lets resort through it
        if new_segments is not None:
            #loop through and set the new text.
            for i in range(len(whisper_segments)):
                whisper_segments[i]['text'] = new_segments[i]

            #check to make sure there is text in the final segment, if not, set the end time of previous segment and remove final segment.
            #need to remove it here, because the Sort only returns a list
            if whisper_segments[len(whisper_segments)-1]['text'].strip() == '':

                #no text!, set the previous segments new end time and remove this segment
                whisper_segments[len(whisper_segments)-2]['end'] = whisper_segments[len(whisper_segments)-1]['end']
                #remove final item
                whisper_segments = whisper_segments[:-1]

        # Write the corrected segments to the SRT file
        self.write_srt2(whisper_segments, srt_output_file)
    
   