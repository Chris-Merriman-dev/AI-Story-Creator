'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Used to see if an image matches the description. It uses Gemini Vision.

'''

#import google.generativeai as genai
#import google.genai as genai
#from google.genai import types
from google import genai
from google.genai import types




import os
import time
import re


#GEMINI_MODEL = "gemini-1.5-flash"
#GEMINI_MODEL = "models/gemini-1.5-flash-latest"
#GEMINI_MODEL = "gemini-1.5-flash-8b"
#GEMINI_MODEL = "gemini-2.0-flash-lite"
#GEMINI_MODEL = "gemini-2.0-flash-exp-image-generation"
GEMINI_MODEL = "gemini-2.0-flash"


class Image_Description:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
    )

    #will rate image and return the number (as text) its rated from 0.0 (worse) to 1.0 (best). uses gemini vision
    def image_to_text_rating3(self, img, description):

        #prompt for seeing if image fits description
        text = f"""
        You will conduct 5 separate, independent evaluations of the following image compared to the description provided.

        For each evaluation:
        - Approach the image and text as if seeing them for the first time.
        - Compare the following text with the image: "{description}".
        - Assess how accurately the image reflects or contrasts with the text.

        Evaluate the following:
        1. Confirm the **approximate number of visible humans** matches the description. If any described human character is entirely missing, note this as an error.
        2. For **visible humans only**, check for any obvious anatomy errors (such as extra heads, missing arms, or misplaced body parts). If any such issue is detected on a human, reduce the score by **20% per instance**.
        3. Ignore anatomy for any non-human characters (such as monsters, animals, or creatures) unless explicitly stated otherwise in the description.
        4. Verify that the **overall clothing style, props, and environmental setting** generally match the description. Do not judge minor details unless glaringly wrong. Any significant mismatch should reduce the score by **10% per issue**.
        5. Assess whether the **lighting, color palette, and mood** of the scene match the tone described. Major deviations should reduce the score by **10%**.

        After completing all 5 evaluations, calculate the **average score** on a scale from 0.00 to 1.00, where 0.00 indicates no similarity and 1.00 indicates perfect similarity.

        Please return **ONLY the final average score** with no individual evaluations or explanations.
        """

        #keep trying to get response
        while True:
            try:
                system_instruction = (
                    "You are an image evaluator tasked with strictly comparing images against descriptive text prompts. "
                    "You will assess similarity, correctness of human anatomy (ensuring all body parts are present and correctly positioned), "
                    "and identify only critical discrepancies such as extra or missing limbs. "
                    "Your scoring system is quantitative only — no explanations, no extra comments. "
                    "All scores are between 0.00 (completely inaccurate) and 1.00 (perfect match). "
                    "Your evaluations must be objective, consistent, and based solely on observable facts."
                )
                response = self.client.models.generate_content(
                                model=GEMINI_MODEL,
                                contents=[text, img],
                                #config=types.GenerateContentConfig(
                                    #temperature=0.3,
                                    #system_instruction=system_instruction,
                                #),                                             
                            )
                break
            except Exception as e:
                print(e)
                time.sleep

        print(f'\n\n{response.text}')
        return response.text

    #sends in the image list and description for this list. Will find the best image out of them, that matches description and return it.
    def find_best_image2(self, images, description):
        values = []
        #"[-+]?\d*\.\d+"
        for image in images:
            #loop until we get a correct number
            while True:
                #get the rating
                str = self.image_to_text_rating3(image, description)

                #incase gemini thinks its a prohibited content image
                if str == None :
                    values.append(0.0)
                else:
                    try:
                        num = re.findall(r"[-+]?\d*\.\d+", 'NUMBERS GALOR !!! WEWEWE : ' + str)            
                        values.append(num[0])
                        #pause so we dont go over limit per minute
                        time.sleep(5)
                        break
                    except Exception as e:
                        print(e)
                        #pause so we dont go over limit per minute
                        time.sleep(5)

        #array spot, value
        best = [0,0.00]

        #find the best array spot for values
        for i in range(len(values)):
            if float(values[i]) > best[1]:
                best[0] = i
                best[1] = float(values[i])
            print(values[i] + '\n')

        print(f'\n\nArray spot : {best[0]} and value : {best[1]}\n\n')

        #return the best image to use
        return images[best[0]]
