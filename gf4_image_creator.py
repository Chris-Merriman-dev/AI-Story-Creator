'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Used to create our Flux images from an online version of Flux. It will send the prompt for creating the image and then download it.
It will also use image_description to use gemini vision to find the best image for the scene.

'''

from g4f.client import Client
#from g4f.Provider 
import requests
from PIL import Image
from io import StringIO
import time
import os
from image_description import Image_Description
import random

IMAGE_SEED = 1

#class for creating images. handles connecting, sending informatin and retrieving the images
class G4F_Image_Creator:
    def __init__(self):
        pass

    def Save_Image_to_Directory(self, image, directory):
        #loop until we have free file name to save
        file_name = 'Image'
        file_type = '.png'
        count = 0

        while True:
            path = os.path.join(directory, file_name + str(count) + file_type)
            
            if not os.path.exists(path):
                image.save(path)
                print('Saved : ' + path)
                break
            else:
                count +=1

    #gets our flux image
    def Create_Image_With_Seed(self, prompt, image_size, seed):
        client = Client()

        #this will loop and make sure the image downloads fully.
        #we use a try to open and if it works, we break loop
        while True:
            #set loop count to 0
            loop_count = 0

            #this will keep trying to create an image, incase we get an error
            while True:
                try:
                    #generate our image
                    response = client.images.generate(
                        model="flux",
                        prompt=prompt,
                        response_format="url",
                        width=image_size[0],
                        height=image_size[1],
                        strength=0.8,
                        enhance=True,
                        #seed = seed,
                        private=True
                    )
                    break
                except Exception as e:
                    print(e)

            print(f"Generated image URL: {response.data[0].url}")

            #loop until we download our image, or if we fail too many times trying to
            while True:                
                #get the data
                r = requests.get(response.data[0].url, stream=True)

                #success, so break loop
                if r.status_code == 200:
                    break
                #looped too many times, so redownload
                elif loop_count > 30:
                    print('loop_count > 15')
                    break
                #keep trying to download it
                else:
                    print('not 200')
                    loop_count = loop_count + 1

            #only attempt the download if we know we have something.
            if loop_count <= 15 :
                #if we can open image, we break loop. Else redownload it
                try:
                    image = Image.open(r.raw)
                    break
                except:
                    print('\nERROR LOADING DOWNLOADED IMAGE.\nRETRYING NEW IMAGE\n')

        return image

    #gets our flux image
    def Create_Image(self, prompt, image_size):
        client = Client()

        #this will loop and make sure the image downloads fully.
        #we use a try to open and if it works, we break loop
        while True:
            #set loop count to 0
            loop_count = 0

            #this will keep trying to create an image, incase we get an error
            while True:
                try:
                    #generate our image
                    response = client.images.generate(
                        model="flux",
                        prompt=prompt,
                        response_format="url",
                        width=image_size[0],
                        height=image_size[1],
                        strength=0,
                        enhance=True,
                    )
                    break
                except:
                    pass

            print(f"Generated image URL: {response.data[0].url}")

            #loop until we download our image, or if we fail too many times trying to
            while True:                
                #get the data
                r = requests.get(response.data[0].url, stream=True)

                #success, so break loop
                if r.status_code == 200:
                    break
                #looped too many times, so redownload
                elif loop_count > 30:
                    print('loop_count > 15')
                    break
                #keep trying to download it
                else:
                    print('not 200')
                    loop_count = loop_count + 1

            #only attempt the download if we know we have something.
            if loop_count <= 15 :
                #if we can open image, we break loop. Else redownload it
                try:
                    image = Image.open(r.raw)
                    break
                except:
                    print('\nERROR LOADING DOWNLOADED IMAGE.\nRETRYING NEW IMAGE\n')

        return image

    #creates amount number of images and then saves to directory. It will use gemini vision to pick best one
    def Create_Images_with_Amount(self, prompt, amount, directory, directory_all_images, directory_images, artstyle, image_size, seed):
        #amount of images created stored here
        images = []
        art = ''#f'Create an image with the following description with art style {artstyle} : '
        
        #create our images and save them
        for i in range(amount):
            #img = self.pipeline(prompt=prompt).images[0]
            #img = self.Create_Image(art + prompt, image_size)
            img = self.Create_Image_With_Seed(art + prompt, image_size, seed)
            seed = seed + random.randint(1,100)
            images.append(img)
            self.Save_Image_to_Directory(img, directory_all_images)

        #now find the image that works best
        img_des = Image_Description()
        image = img_des.find_best_image2(images, prompt)

        #now save it to our main image directory
        self.Save_Image_to_Directory(image, directory_images)

    #creates images and then saves to directory. It doesnt use Gemini vision to pick best image
    def Create_Images_with_Amount_NO_PICK(self, prompt, amount, directory, directory_all_images, directory_images, artstyle, image_size, seed):
        #amount of images created stored here
        images = []
        art = ''#f'Create an image with the following description with art style {artstyle} : '
        
        #create our images and save them
        for i in range(amount):
            #img = self.pipeline(prompt=prompt).images[0]
            #img = self.Create_Image(art + prompt, image_size)
            img = self.Create_Image_With_Seed(art + prompt, image_size, seed)
            seed = seed + random.randint(1,100)
            images.append(img)
            self.Save_Image_to_Directory(img, directory_all_images)
            time.sleep(6)

        #now find the image that works best
        #img_des = Image_Description()
        #image = img_des.find_best_image2(images, prompt)

        #now save it to our main image directory
        #self.Save_Image_to_Directory(image, directory_images)

    
