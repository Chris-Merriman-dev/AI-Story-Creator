# AI Story Creator

An AI-powered application that automates the creation of narrative videos from text. This project was a research application to see if AI could autonomously create a story video on its own. It selects and creates all the images, videos, and music for the story.

## Features
* **AI-Driven Story Creation:** Creates random stories and titles.
* **AI-Generated Media:** Uses AI to select and create images and music for each section of the story.
* **Automated Video Generation:** Compiles all media into a final video.

## Technology Stack
* **Google Gemini** (used for primary story creation)
* **g4f.client** (used for better random stories and titles)
* **Wan 2.1** (used for AI-created video sections)

## Challenges & Conclusion
The hardest part was getting the AI to create consistent prompts for images, especially with multiple characters. It also struggled with selecting the correct images to match a scene's description, often choosing images with disfigured bodies. The project works, but not perfectly. As AI vision improves, these issues should be solved.

## Demonstration
The results of how this works can be seen on this YouTube channel: [AI Synthetic Dreams](https://www.youtube.com/@AISyntheticDreams)

## Files
* `audio_to_text.py`
* `gemini_story_creator.py`
* `gf4_image_creator.py`
* `image_description.py`
* `music_loader.py`
* `video_creator.py`

## Note
This project uses outdated Gemini and flux creator versions and has not been updated. The YouTube channel above shows the results of a working version.