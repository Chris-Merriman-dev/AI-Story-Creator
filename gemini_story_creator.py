'''
Created By : Christian Merriman

Date : 2/20/25

Purpose : Used to create our AI stories. The Gemini_Story_Creator class has many functions available for creating and settings up the rest of our story settings 
for our AI created video. 

'''

#refer to for limits per minute and day : https://ai.google.dev/gemini-api/docs/rate-limits#free-tier
#refer to for different models : https://ai.google.dev/gemini-api/docs/models/gemini#model-variations

import os
#from langchain_google_genai import ChatGoogleGenerativeAI
import random
from random import shuffle
import time
from token_count import Token_Count

from google import genai
from google.genai import types

from g4f.client import Client
from g4f.Provider.Blackbox import Blackbox
from g4f.Provider.PollinationsAI import PollinationsAI
from g4f import get_model_and_provider

#GEMINI_MODEL = "gemini-1.5-flash"
#GEMINI_MODEL = "gemini-1.5-flash-8b"
#GEMINI_MODEL = "gemini-2.0-flash-lite"
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_MODEL2 = "gemini-2.5-flash-preview-04-17"

#narrator voice options with their descriptions for AI to pick
VOICE_OPTIONS = [
    ('A woman narrator used for calm voice.', 'en_female_emotional'),
    #('An old man narrator used for calm voice.', 'en_male_narration'),
    ('Wacky man narrator used for excited voice.', 'en_male_funny'),
    ('An english UK man used for a normal voice.', 'en_uk_003'),
    ('An english US woman used for excited voice.', 'en_us_001'),
    ('An english US woman used for excited voice. Is popular voice for tiktok videos.','en_us_002'),
    ('An okay english US man used for a plain sounding voice.','en_us_009')   
]

#types of music and their descriptions for AI to pick
TYPES_OF_MUSIC = ["**Cinematic Orchestral** Epic, emotional music, perfect for dramatic moments or big events in a story.",

"**Ambient** Calm, atmospheric soundscapes ideal for establishing settings or providing a soothing background.",

"**Suspense/Thriller** Tense, edgy music that builds anticipation and keeps the audience on the edge of their seat.",

"**Action/Adventure** Upbeat, fast-paced music with dynamic rhythms, suitable for action-packed scenes.",

"**Romantic** Soft, emotional melodies to enhance romantic or heartwarming moments.",

"**Fantasy/Epic** Magical or mystical music that complements fantasy themes, bringing a sense of wonder.",

"**Mystery** Dark, moody tracks with a sense of intrigue, fitting for uncovering secrets or detective-type stories.",

"**Happy/Upbeat** Bright and energetic music, perfect for uplifting moments, comedic scenes, or feel-good stories.",

"**Horror** Dissonant, eerie music to create an unsettling atmosphere for spooky or horror-themed videos.",

"**Sad/Reflective** Melancholic tunes to evoke feelings of loss, contemplation, or sorrow.",

"**Sci-Fi** Futuristic, electronic music with synthesizers and atmospheric soundscapes, perfect for depicting advanced technology, space exploration, or dystopian themes. The music should evoke a sense of wonder, mystery, or tension, complementing a futuristic or sci-fi setting.",
]

#class for creating and formatting the story, for the video
class Gemini_Story_Creator:
    def __init__(self):
        self.google_api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.google_api_key)

        #model, provider = get_model_and_provider("gpt-3.5-turbo", None, stream=False)
        #self.model, self.provider = get_model_and_provider("blackboxai", None, stream=False)

        self.g4f_client = Client( provider = PollinationsAI)

    #used for creating a story with g4f ai client
    def testg4f(self, role, prompt):
        chat_completion = self.g4f_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": role + prompt}],
        )

        print(chat_completion.choices[0].message.content or "")

        return chat_completion.choices[0].message.content 

    #large function that will create a prompt to send to the AI for a story. These options were all created by AI.
    #i just copied and pasted these options here, since this was used for testing
    def get_random_prompt(self, size):
        # Settings
        settings = [
            'a haunted mansion on a cliff', 'a futuristic space station orbiting a dying star', 
            'a magical forest in the heart of an ancient kingdom', 'a small, sleepy town by the sea', 
            'a bustling cyberpunk city with neon lights', 'a forgotten underground laboratory', 
            'a medieval castle surrounded by a thick fog', 'a secluded island lost in the Bermuda Triangle', 
            'a desolate wasteland after an apocalypse', 'an enchanted library hidden in a mountain cave', 
            'a sprawling metropolis with towering skyscrapers', 'a hidden village deep in a jungle', 
            'a vast desert with only the remnants of ancient civilizations', 'an abandoned amusement park', 
            'a creepy old lighthouse by a stormy sea', 'a frozen tundra with an ancient buried city', 
            'a bustling bazaar on a distant planet', 'a post-apocalyptic city covered in overgrowth', 
            'a time-warped town stuck in the 1960s', 'a cursed pirate ship floating on a foggy sea', 
            'a vast and ancient library lost to time', 'a secret base hidden inside a mountain range', 
            'an old mansion built on the side of a volcano', 'a thriving space colony on Mars', 
            'a moonlit temple in a jungle, untouched by time', 'a forgotten city buried beneath the ocean', 
            'a giant treehouse village in a forest canopy', 'an abandoned military base in a remote desert', 
            'an interdimensional portal in a quiet suburban home', 'a magical tower suspended in the clouds', 
            'a remote fishing village plagued by mysterious disappearances', 'a vast, overgrown garden of alien plants', 
            'a labyrinth beneath a city filled with dark secrets', 'a dusty saloon in a Wild West ghost town', 
            'a hidden shrine atop a mountain, far from civilization', 'a massive underground cave system full of crystals', 
            'a ruined city overtaken by nature', 'a crumbling space station orbiting a black hole', 
            'a cozy cabin in the snowy woods', 'a strange alternate reality full of strange beings', 
            'a forgotten temple in the heart of a jungle', 'a towering lighthouse overlooking a dark ocean', 
            'an eerie island surrounded by a blood-red sea', 'a futuristic city built on top of an ancient ruin', 
            'a military base on an isolated island', 'a bustling port city with a pirate past', 
            'a hidden desert oasis with a powerful secret', 'an isolated mansion on a snowy mountain peak',

            'a sprawling underground city illuminated by bioluminescent plants',

            'a mysterious fog-covered moor with ancient stone circles',

            'a high-tech research facility on the edge of a black hole',

            'a vibrant alien marketplace on a distant planet',

            'a cursed village where time stands still',

            'a sunken city filled with treasures and dangers',

            'a remote observatory on a mountaintop, watching the stars',

            'a dilapidated train station haunted by the spirits of lost travelers',

            'a vast, shimmering ocean with floating islands',

            'a hidden cave with glowing crystals and ancient inscriptions',

            'a futuristic city where technology and nature coexist harmoniously',

            'a dark, twisted carnival filled with sinister attractions',

            'a secret garden that blooms only at night',

            'a crumbling castle perched on a stormy cliff',

            'a bustling spaceport filled with travelers from across the galaxy',

            'a forgotten battlefield where the echoes of war linger',

            'a serene lake surrounded by mountains, hiding dark secrets beneath its surface',

            'a massive tree with a village built within its branches',

            'a desolate moon with ancient ruins and strange creatures',

            'a hidden sanctuary for mythical creatures in a remote valley',

            'a futuristic underwater city thriving beneath the ocean waves',

            'a mysterious island that appears and disappears with the tides',

            'a sprawling junkyard filled with remnants of a lost civilization',

            'a haunted battlefield where the past refuses to stay buried',

            'a vibrant city built entirely of glass and light',

            'a secret laboratory hidden in the Arctic tundra',

            'a mystical waterfall that grants wishes to those who dare to approach',

            'a vast, empty plain where time seems to stand still',

            'a hidden alcove in a bustling city, filled with ancient artifacts',

            'a crumbling library filled with forbidden knowledge',

            'a futuristic amusement park with rides that defy gravity',

            'a remote monastery perched on a cliff, overlooking a raging sea',

            'a dark alleyway in a city where shadows come to life',

            'a sprawling vineyard with a dark history of betrayal',

            'a hidden cave system that leads to an underground world',

            'a futuristic city where the sky is filled with flying cars',

            'a mysterious forest where the trees whisper secrets',

            'a vast, abandoned factory filled with forgotten machinery',

            'a secret societys headquarters hidden beneath a bustling city',

            'a floating city above the clouds, accessible only by airship',

            'a haunted hotel where guests never check out',

            'a remote island with a volcano that holds ancient secrets',

            'a hidden temple guarded by mythical creatures',

            'a futuristic battlefield where soldiers fight with advanced technology',

            'a sprawling metropolis with a dark underbelly of crime',

            'a serene beach with bioluminescent waves at night',

            'a mysterious cave that leads to a parallel universe',

            'a forgotten castle in the middle of a vast desert',

            'a hidden oasis in a barren wasteland, rumored to grant immortality',

            'a dark, enchanted forest where nothing is as it seems',

            'a futuristic city where dreams can be bought and sold',

            'a secretive government facility conducting experiments on time travel',

            'a vast, ancient ruin that holds the key to a lost civilization',

            'a sprawling space colony on a distant planet',

            'a high-tech laboratory on the edge of a black hole',

            'a futuristic city with flying cars and towering skyscrapers',

            'an alien landscape filled with bioluminescent flora and fauna',

            'a derelict spaceship drifting through the void of space',

            'a virtual reality world where anything is possible',

            'a post-apocalyptic city overrun by mutated creatures',

            'a secret research facility hidden beneath the surface of Mars',

            'a massive space station serving as a hub for intergalactic trade',

            'a time-warped dimension where the laws of physics don’t apply',

            'a cybernetic metropolis where humans and machines coexist',

            'a mysterious asteroid with ancient alien technology buried within',

            'a futuristic underwater city thriving beneath the ocean waves',

            'a desolate moon with remnants of an ancient civilization',

            'a hidden base on a remote planet, home to a rebel faction',

            'a colossal spaceship designed for interstellar travel',

            'a dystopian world ruled by a totalitarian regime',

            'a floating city above the clouds, powered by advanced technology',

            'a dark, abandoned space station haunted by the ghosts of its crew',

            'a vast alien desert with shifting sands and hidden dangers',

            'a futuristic arena where gladiators battle for survival',

            'a secret laboratory experimenting with genetic engineering',

            'a time-traveling train that journeys through different eras',

            'a cyberpunk city where neon lights illuminate the night',

            'a mysterious portal leading to alternate dimensions',

            'a massive alien spacecraft hovering over a major city',

            'a hidden colony of humans living on a distant planet',

            'a futuristic prison floating in the atmosphere of a gas giant',

            'a virtual reality game that becomes a fight for survival',

            'a remote outpost on the edge of the galaxy, teeming with secrets',

            'a sprawling junkyard on a distant planet, filled with forgotten technology',

            'a sentient spaceship with its own consciousness and motives',

            'a futuristic marketplace where alien species trade exotic goods',

            'a dark forest on an alien planet, filled with strange creatures',

            'a massive underground city built to escape a dying Earth',

            'a high-tech observatory monitoring cosmic anomalies',

            'a colony on a terraformed planet, struggling with its new environment',

            'a mysterious energy field surrounding a distant star',

            'a futuristic hospital using advanced technology to heal the sick',

            'a hidden alien base disguised as a natural formation',

            'a time-warped city where past and future collide',

            'a vast ocean on an alien world, home to intelligent marine life',

            'a cybernetic enhancement clinic offering illegal modifications',

            'a futuristic train system connecting distant planets',

            'a secret society operating in the shadows of a technologically advanced city',

            'a massive alien artifact buried beneath the surface of a planet',

            'a high-tech farm using advanced genetics to grow food in space',

            'a virtual reality simulation used for training elite soldiers',

            'a mysterious signal coming from a distant galaxy',

            'a futuristic library containing the knowledge of countless civilizations',

            'a hidden sanctuary for rogue AI seeking freedom',

            'a colossal space elevator connecting Earth to orbit',

            'a dark web of espionage and intrigue in a high-tech society',

            'a remote research station studying the effects of time travel',

            'a futuristic amusement park with rides that defy gravity',

            'a crumbling skyscraper during a citywide evacuation',

            'a high-speed chase through the narrow streets of a bustling metropolis',

            'an abandoned warehouse filled with hidden traps and treasures',

            'a remote jungle where mercenaries clash with local rebels',

            'a military base under siege from an unknown enemy',

            'a futuristic arena where gladiators battle for glory',

            'a secret laboratory where experiments have gone horribly wrong',

            'a pirate ship sailing through treacherous waters in pursuit of a legendary treasure',

            'a dark alleyway where rival gangs face off in a turf war',

            'a high-stakes poker game in a luxurious casino with dangerous players',

            'a snow-covered mountain where a secret mission unfolds',

            'a bustling airport where a bomb threat puts everyone on edge',

            'a deserted island where survivors must fight for resources',

            'a crowded subway station during a terrorist attack',

            'a high-tech heist in a secure vault filled with priceless artifacts',

            'a remote outpost on the edge of a hostile alien planet',

            'a futuristic city where a rebellion is brewing against a corrupt government',

            'a secret bunker where a group of heroes plans their next move',

            'a dangerous race through a post-apocalyptic wasteland',

            'a hidden temple filled with ancient traps and treasures',

            'a high-speed train hurtling through the countryside with a deadly secret',

            'a dark forest where hunters become the hunted',

            'a bustling marketplace where a thief must evade capture',

            'a rooftop chase across the skyline of a sprawling city',

            'a military convoy ambushed in a war-torn country',

            'a secret society meeting in an underground lair',

            'a futuristic cityscape where drones patrol the skies',

            'a remote research facility overrun by hostile creatures',

            'a high-stakes auction for a stolen artifact with dangerous bidders',

            'a crowded beach where a sudden storm brings chaos',

            'a hidden cave where a treasure map leads to danger',

            'a luxury yacht under attack by pirates on the high seas',

            'a bustling train station where a mysterious figure is being pursued',

            'a secretive government facility where experiments on super-soldiers take place',

            'a dark, abandoned amusement park where secrets are buried',

            'a high-tech lab where a rogue AI threatens humanity',

            'a remote village where ancient warriors protect a powerful secret',

            'a futuristic city where a hacker must infiltrate a corporate stronghold',

            'a dangerous jungle filled with traps and mercenaries',

            'a high-stakes escape from a maximum-security prison',

            'a secret base hidden in the mountains, home to a rebel faction',

            'a crowded nightclub where a deadly game of cat and mouse unfolds',

            'a vast desert where a convoy must navigate through enemy territory',

            'a high-tech spaceship on a mission to save a dying planet',

            'a dark alley where a detective confronts a notorious crime lord',

            'a remote island where a deadly game of survival takes place',

            'a futuristic city where a vigilante fights against corruption',

            'a secret laboratory where a scientist races against time to stop a disaster',

            'a bustling port city where smugglers operate in the shadows',

            'a high-speed motorcycle chase through winding mountain roads',

            'a hidden fortress where a final showdown between heroes and villains occurs',

            'a crowded stadium where a deadly competition takes place',

            'a dark, labyrinthine catacomb filled with ancient secrets',

            'a futuristic battlefield where soldiers fight with advanced technology',

            'a secretive auction house where dangerous items are sold to the highest bidder',

            'a remote outpost on a frozen planet where survival is uncertain'

        ]
        
        #  Characters descriptions
        characters = [
            'a disgraced knight seeking redemption', 'a brilliant but eccentric scientist', 
            'a wandering sorceress on a quest', 'a young detective solving a series of mysterious murders', 
            'a retired space captain with a dark past', 'a rogue AI who gains self-awareness', 
            'a ghost who can interact with the living world', 'a time-traveling historian', 
            'a shape-shifting thief with a heart of gold', 'an ancient warrior resurrected to stop an impending war', 
            'a young witch trying to control her powers', 'a forgotten king who returns to claim his throne', 
            'a street-smart hacker with a secret', 'a retired assassin trying to live a peaceful life', 
            'a mysterious traveler with a hidden agenda', 'a cursed immortal searching for a way to die', 
            'a princess who disguises herself as a commoner', 'a reformed villain trying to do good', 
            'a reluctant hero who is forced to save the world', 'a dragon-shifter torn between two worlds', 
            'a stranded astronaut trying to survive', 'a cursed pirate captain', 'a rebellious student defying a corrupt government', 
            'a bounty hunter tracking down dangerous criminals', 'an exiled sorcerer seeking revenge', 
            'a werewolf struggling with their curse', 'an oracle who sees visions of a dark future', 
            'a talking animal guiding a lost traveler', 'a secret agent working undercover', 'a fallen angel trying to regain their wings', 
            'a hacker who stumbles upon a world-changing secret', 'a mad scientist with questionable morals', 
            'a ghostly apparition seeking closure', 'an unlikely hero from a faraway land', 'a time-displaced warrior from the future', 
            'a noble knight turned mercenary', 'a cursed artist whose paintings come to life', 
            'a curious child who discovers a magical artifact', 'a sorcerer struggling with forbidden magic', 
            'a half-human, half-alien hybrid', 'a shape-shifting bounty hunter from another dimension', 
            'a detective with a supernatural gift', 'a royal bodyguard with a tragic past', 
            'a mystic who can communicate with the dead', 'a stranded survivor in a post-apocalyptic world', 
            'a merchant with knowledge of forbidden knowledge', 'a shape-shifting prince hiding his identity', 
            'an alien diplomat navigating human politics',
            'a fallen star who has lost their cosmic powers and seeks redemption', 
            'a blind seer who can read minds but struggles to decipher her own future',
            'a former assassin who now protects the very people they once targeted',
            'a cursed noblewoman whose touch turns everything she loves to stone',
            'a renegade priestess banished for practicing forbidden rites of the old gods',
            'a genetically modified soldier with enhanced abilities but fading humanity',
            'a cybernetic ghost trapped between the digital and physical worlds',
            'a con artist who has fallen in love with one of their marks',
            'a former witchhunter now cursed by the magic they once despised',
            'a jaded journalist who uncovers a conspiracy but risks their life to expose the truth',
            'a runaway clone fighting to find their own identity',
            'a fallen angel who questions their own morality and desires redemption',
            'an enigmatic hacker who manipulates reality itself through code',
            'a time-bending rogue who alters history for personal gain',
            'a mute healer who communicates through emotions, not words',
            'a troubled artist who paints visions of the future that come true',
            'a vengeful spirit seeking to destroy the family that wronged them',
            'a shapeshifting criminal who assumes different identities to infiltrate governments',
            'a former cult leader now hunted by their own followers',
            'a powerful empath who can read others’ emotions but is overwhelmed by them',
            'a haunted war veteran who sees the ghosts of their past on the battlefield',
            'a genetically engineered child who has the wisdom of an ancient sage',
            'a cursed gladiator who can never die but longs for peace',
            'an ageless vampire who falls in love with a mortal, knowing it will end tragically',
            'a charming spy who struggles with the blurred lines between loyalty and betrayal',
            'a royal outcast who holds the key to a long-lost treasure of immense power',
            'a ruthless bounty hunter who develops an unexpected bond with their prey',
            'a mad scientist whose inventions threaten to unravel the fabric of reality',
            'a rogue witch with the ability to control time, but at a great personal cost',
            'an immortal detective who has solved every mystery but still seeks purpose',
            'a double agent playing both sides of a war they want no part in',
            'a disgraced noble who becomes a mercenary in an attempt to redeem their family name',
            'a failed experiment who retains the memories of their former life',
            'a pirate captain cursed to sail the seas forever, never able to dock again',
            'a disgruntled angel who falls to Earth seeking vengeance on their former superiors',
            'a time traveler who accidentally disrupts a timeline they must now fix',
            'an outlaw who challenges the very laws of reality with their forbidden magic',
            'a once-loyal soldier now seeking justice for war crimes committed by their nation',
            'a clairvoyant who knows the fate of every soul except their own',
            'a monstrous creature who seeks the cure to their own cursed form',
            'a warrior who bears the cursed mark of a fallen god and seeks to destroy it',
            'an assassin who takes jobs to erase memories, not just lives',
            'a mysterious wanderer who leaves a trail of vanished towns and broken hearts',
            'a former villain who now runs an orphanage but struggles with their dark past',
            'a time-traveling thief who steals from the past to change the future',

            'a genetically engineered super-soldier questioning their purpose in a war-torn galaxy',

            'a rogue scientist who creates sentient life in a quest for immortality',

            'a cybernetic bounty hunter with a hidden agenda and a heart of gold',

            'a telepathic alien ambassador trying to broker peace between warring factions',

            'a space pirate captain searching for a legendary treasure hidden in a black hole',

            'a virtual reality game designer who becomes trapped in their own creation',

            'a sentient spaceship with a personality and a mission to protect its crew',

            'a time-displaced historian who must navigate a future they don’t understand',

            'a genetically modified child with the ability to manipulate time',

            'a rogue AI seeking to understand human emotions through a series of experiments',

            'a cyborg detective solving crimes in a neon-lit dystopian city',

            'a scientist who accidentally opens a portal to a parallel universe',

            'a space explorer haunted by the ghosts of their fallen crew',

            'a hacker who discovers a conspiracy involving alien technology',

            'a former astronaut who becomes a cult leader after a near-death experience in space',

            'a psychic medium who communicates with extraterrestrial beings',

            'a soldier from a future war who is sent back in time to prevent its occurrence',

            'a genetically engineered assassin with a conscience that fights against their programming',

            'a time-traveling journalist uncovering the truth behind historical events',

            'a rogue scientist who creates a device that allows people to relive their memories',

            'a space station janitor who uncovers a plot to sabotage the station',

            'a clone who rebels against their creators and seeks to forge their own destiny',

            'a telekinetic child who must hide their powers from a government agency',

            'a bioengineered creature seeking acceptance in a world that fears them',

            'a time-traveling librarian who protects the timeline from rogue time travelers',

            'a space diplomat trying to unite different alien species against a common threat',

            'a scientist who invents a device that allows people to communicate with their future selves',

            'a rogue android seeking to understand what it means to be human',

            'a space archaeologist uncovering the secrets of an ancient alien civilization',

            'a former villain turned hero who must confront their past to save the future',

            'a psychic detective who solves crimes by entering the minds of the guilty',

            'a time-traveling musician who influences history through their songs',

            'a genetically modified human with the ability to control technology with their mind',

            'a space explorer who discovers a planet inhabited by sentient plants',

            'a rogue timekeeper who manipulates time for personal gain',

            'a scientist who creates a serum that grants temporary superpowers',

            'a former government agent turned vigilante fighting against a corrupt regime',

            'a space mechanic who repairs ships while uncovering intergalactic conspiracies',

            'a time-traveling historian who must prevent a catastrophic event from occurring',

            'a sentient hologram seeking to understand the nature of existence',

            'a genetically engineered soldier who rebels against their creators',

            'a space diplomat who must navigate the complexities of intergalactic politics',

            'a rogue scientist who creates a device that allows people to swap bodies',

            'a time-displaced warrior who must adapt to a world they no longer recognize',

            'a cybernetic hacker who can manipulate digital realities',

            'a former space pirate seeking redemption by helping those in need',

            'a time-traveling botanist who seeks to save endangered species from extinction',

            'a mysterious traveler who appears in different timelines, leaving behind clues for others to follow',

            'a fearless mercenary with a reputation for taking impossible jobs',

            'a skilled martial artist seeking revenge for a fallen mentor',

            'a former special forces operative turned vigilante',

            'a street racer with a knack for high-stakes heists',

            'a rogue spy who uncovers a conspiracy within their own agency',

            'a bounty hunter with a personal vendetta against a notorious criminal',

            'a retired assassin pulled back into the game for one last job',

            'a tech-savvy hacker who uses their skills to fight against corruption',

            'a soldier with a mysterious past who must confront their demons',

            'a master thief planning the ultimate heist in a high-security facility',

            'a fearless firefighter who risks everything to save lives',

            'a former gang member trying to escape their violent past',

            'a skilled archer fighting to protect their homeland from invaders',

            'a rogue cop who takes justice into their own hands',

            'a survivalist navigating a post-apocalyptic wasteland',

            'a young prodigy who becomes a hero in a world of supervillains',

            'a former athlete turned bodyguard for a high-profile client',

            'a skilled pilot who must navigate treacherous skies in a war-torn world',

            'a master swordsman seeking to reclaim their familys honor',

            'a secret agent with a license to kill and a taste for danger',

            'a relentless journalist uncovering the truth behind a powerful corporation',

            'a former soldier turned mercenary who fights for the highest bidder',

            'a street-smart detective solving crimes in a gritty urban landscape',

            'a skilled escape artist who must break free from a high-security prison',

            'a lone wolf tracker hunting down a dangerous fugitive',

            'a charismatic leader rallying a group of rebels against an oppressive regime',

            'a sharpshooter with a mysterious past and a deadly aim',

            'a former spy who must go undercover to infiltrate a criminal organization',

            'a fearless explorer searching for lost treasures in uncharted territories',

            'a skilled mechanic who builds custom vehicles for high-speed chases',

            'a young hacker who uses their skills to expose government secrets',

            'a former assassin who now protects the innocent from their former allies',

            'a master of disguise who infiltrates enemy ranks to gather intelligence',

            'a relentless bounty hunter tracking down a dangerous fugitive across the galaxy',

            'a skilled combat medic who saves lives on the battlefield',

            'a former criminal mastermind seeking redemption through heroic deeds',

            'a street fighter who rises through the ranks of an underground fighting ring',

            'a survival expert leading a group through a dangerous wilderness',

            'a skilled sniper who must protect a high-value target from assassins',

            'a former soldier with a haunted past who seeks to make amends',

            'a daring pilot who must navigate a treacherous airspace during a war',

            'a master tactician leading a rebellion against a tyrannical government',

            'a skilled martial artist who must defend their dojo from a rival gang',

            'a former spy who must confront their old enemies to protect their family',

            'a fearless adventurer exploring ancient ruins filled with traps and treasures',

            'a skilled negotiator who must defuse a hostage situation',

            'a former athlete turned vigilante using their skills to fight crime',

            'a rogue scientist who uses their inventions to battle against evil forces',

            'a charismatic con artist who uses their charm to outsmart dangerous foes',

            'a skilled driver who participates in illegal street races to pay off debts',

            'a former soldier turned bodyguard who must protect a target from assassins',

            'a master of parkour who uses their agility to escape danger',

            'a relentless detective who will stop at nothing to solve a case',

            'a skilled swordswoman fighting to reclaim her familys legacy',

            'a former criminal who becomes a hero after a life-changing event',

            'a daring thief who pulls off heists in the most secure locations',

            'a survivalist who thrives in a world where society has collapsed',


        ]

        #first names
        first_names = [
            'Aaron', 'Abigail', 'Adam', 'Adeline', 'Alex', 'Alexa', 'Alice', 'Alicia', 'Amelia', 'Anna', 'Anthony', 'Ashley',
            'Benjamin', 'Blake', 'Brandon', 'Caden', 'Caleb', 'Cameron', 'Caroline', 'Charlotte', 'Chloe', 'Christopher',
            'Daniel', 'David', 'Delilah', 'Diana', 'Dominic', 'Eden', 'Ella', 'Elijah', 'Emily', 'Emma', 'Ethan', 'Evan',
            'Faith', 'Finn', 'Gabriel', 'Gage', 'Grace', 'Hannah', 'Harper', 'Hayden', 'Henry', 'Isaac', 'Isabella', 'Ivy',
            'Jack', 'Jackson', 'Jacob', 'James', 'Jasmine', 'Jayden', 'Jenna', 'Jeremiah', 'Jessica', 'John', 'Jonathan',
            'Jordan', 'Joseph', 'Joshua', 'Julia', 'Justin', 'Kaitlyn', 'Katherine', 'Kayla', 'Kevin', 'Kylie', 'Liam', 'Lily',
            'Logan', 'Lucas', 'Lucy', 'Mackenzie', 'Madeline', 'Mason', 'Matthew', 'Maya', 'Megan', 'Melanie', 'Michael', 'Miley',
            'Molly', 'Nina', 'Noah', 'Oliver', 'Olivia', 'Oscar', 'Parker', 'Patrick', 'Rachel', 'Rebecca', 'Riley', 'Robert',
            'Ryan', 'Sadie', 'Samuel', 'Savannah', 'Scarlett', 'Sierra', 'Sophia', 'Spencer', 'Stella', 'Stephen', 'Sophie', 'Tessa',
            'Thomas', 'Tina', 'Victoria', 'Violet', 'Vivian', 'William', 'Wyatt', 'Zoe', 'Zachary', 'Zara', 'Aiden', 'Addison',
            'Alexander', 'Alexa', 'Allison', 'Amos', 'Anna', 'April', 'Ava', 'Beatrice', 'Bella', 'Blair', 'Brady', 'Brianna',
            'Bryce', 'Calvin', 'Camila', 'Chase', 'Clara', 'Cora', 'Dakota', 'Daniela', 'Daphne', 'Diana', 'Diego', 'Dylan',
            'Eden', 'Ellie', 'Emily', 'Eva', 'Gavin', 'Gianna', 'Graham', 'Grant', 'Gwen', 'Hayley', 'Heather', 'Holly', 'Hudson',
            'Hunter', 'Indigo', 'Irene', 'Isabelle', 'Isaiah', 'Jace', 'Jaime', 'Jasper', 'Jean', 'Jenna', 'Jocelyn', 'Johnny',
            'Jordan', 'Josephine', 'Josiah', 'Jude', 'Kaden', 'Kelsey', 'Kennedy', 'Kiana', 'Kimberly', 'Landon', 'Lauren', 'Leah',
            'Leo', 'Liana', 'Lydia', 'Maddie', 'Madison', 'Mara', 'Mark', 'Martha', 'Mary', 'Mason', 'Matthew', 'Melody', 'Mia',
            'Micah', 'Mindy', 'Misty', 'Nina', 'Noelle', 'Olga', 'Peyton', 'Quinn', 'Rae', 'Rachel', 'Reagan', 'Riley', 'Ronan',
            'Ruby', 'Sabrina', 'Samantha', 'Sandy', 'Savanna', 'Scarlett', 'Selena', 'Shane', 'Shannon', 'Sierra', 'Sofia', 'Tessa',
            'Tristan', 'Valerie', 'Vanessa', 'Vera', 'Violet', 'Willa', 'Willow', 'Zoe', 'Zane', 'Zachary',
            'Aaron', 'Ava', 'Alistair', 'Azalea', 'Beau', 'Bennett', 'Briar', 'Callum', 'Cecilia', 'Clio', 'Dax', 'Daria', 'Devon', 'Elliot', 
            'Ezekiel', 'Fern', 'Fiona', 'Freya', 'Gabrielle', 'Gareth', 'Giovanni', 'Hendrix', 'Imogen', 'Ivy', 'Iris', 'Juno', 'Kendall', 'Kenzo', 
            'Lola', 'Lucian', 'Lysandra', 'Milo', 'Miriam', 'Nash', 'Nova', 'Odessa', 'Orlando', 'Poppy', 'Priscilla', 'Quentin', 'Quinn', 'Rhea', 
            'Rocco', 'Sable', 'Soren', 'Tamsin', 'Thaddeus', 'Thea', 'Ulric', 'Veda', 'Viggo', 'Wren', 'Xander', 'Xenia', 'Yara', 'Zara', 'Zelda',
            'Aurelia', 'Balthazar', 'Blaise', 'Cadenza', 'Cassius', 'Clarity', 'Dante', 'Dahlia', 'Dorian', 'Edith', 'Ezekiel', 'Esme', 
            'Flora', 'Gael', 'Gideon', 'Hera', 'Indigo', 'Isidore', 'Jasper', 'Juniper', 'Kieran', 'Kendrick', 'Leif', 'Leona', 'Lucinda', 
            'Magnolia', 'Maverick', 'Nicolette', 'Oriana', 'Percival', 'Petra', 'Raven', 'Renata', 'Rocco', 'Solene', 'Seraphina', 'Soren', 
            'Tabitha', 'Theodore', 'Uriah', 'Vespera', 'Wilder', 'Xerxes', 'Yasmine', 'Zelda', 'Zayden', 'Zinnia', 'Archer', 'Benedict', 
            'Cressida', 'Daxter', 'Eloise', 'Elowen', 'Fletcher', 'Gwyneth', 'Hawke', 'Icarus', 'Juno', 'Kaius', 'Larkin', 'Leona', 'Marigold', 
            'Nikolai', 'Ophelia', 'Rhea', 'Sable', 'Thorne', 'Valerian', 'Vega', 'Zephyr'
        ]

        #last names
        last_names = [
            'Adams', 'Allen', 'Anderson', 'Baker', 'Ball', 'Banks', 'Barnes', 'Barnett', 'Bauer', 'Becker', 'Bell', 'Bennett', 
            'Blake', 'Blanchard', 'Bradley', 'Brown', 'Bryant', 'Burns', 'Butler', 'Campbell', 'Carlson', 'Chapman', 'Chen', 'Chavez',
            'Clark', 'Cole', 'Collins', 'Cook', 'Craig', 'Davis', 'Dawson', 'Day', 'Dean', 'Diaz', 'Dickson', 'Dixon', 'Donovan', 'Douglas',
            'Edwards', 'Ellis', 'Evans', 'Ferguson', 'Fisher', 'Fleming', 'Ford', 'Fowler', 'Francis', 'Gaines', 'Garcia', 'Gardner', 'Gibson',
            'Graham', 'Green', 'Griffith', 'Hall', 'Hamilton', 'Hansen', 'Harris', 'Harrison', 'Hart', 'Hayes', 'Henderson', 'Hernandez', 'Hill',
            'Hodges', 'Holland', 'Holmes', 'Howard', 'Hudson', 'Hughes', 'Hunter', 'Jackson', 'James', 'Jenkins', 'Johnson', 'Jones', 'Jordan',
            'Joseph', 'Kelly', 'Kennedy', 'King', 'Knight', 'Lambert', 'Lawrence', 'Lee', 'Lewis', 'Liu', 'Long', 'Lopez', 'Lucas', 'Manning',
            'Martin', 'Martinez', 'Mason', 'Matthews', 'McCarthy', 'McDonald', 'Miller', 'Mitchell', 'Moore', 'Morgan', 'Morris', 'Murphy',
            'Nelson', 'Nguyen', 'Nichols', 'Norman', 'O’Brien', 'O’Connor', 'Olson', 'Parker', 'Parsons', 'Patel', 'Peck', 'Perkins', 'Peterson',
            'Pittman', 'Price', 'Ramos', 'Reed', 'Reynolds', 'Richardson', 'Roberts', 'Robinson', 'Rodriguez', 'Rose', 'Russell', 'Sanchez', 'Scott',
            'Shaw', 'Simpson', 'Smith', 'Stewart', 'Stone', 'Sullivan', 'Taylor', 'Thomas', 'Thompson', 'Tucker', 'Turner', 'Wallace', 'Ward',
            'Watson', 'Webb', 'White', 'Williams', 'Wilson', 'Woods', 'Wright', 'Yang', 'Young', 'Zimmerman', 'Abbott', 'Alexander', 'Avery',
            'Baldwin', 'Barber', 'Beasley', 'Black', 'Bliss', 'Bowen', 'Bradshaw', 'Browning', 'Buckley', 'Burnett', 'Byers', 'Calderon', 'Carlson',
            'Christian', 'Cameron', 'Clarke', 'Clayton', 'Crawford', 'Curtis', 'Dalton', 'Davis', 'Deleon', 'Denson', 'Douglas', 'Elliott', 'Ellington',
            'Fields', 'Finley', 'Franklin', 'Gage', 'Garrett', 'Garrison', 'Gates', 'Granger', 'Greenwood', 'Grover', 'Harper', 'Hartman', 'Hawkins',
            'Hayward', 'Hendrix', 'Hoffman', 'Hudson', 'Hughes', 'Irwin', 'Jensen', 'Kennedy', 'Kim', 'Larkin', 'Leach', 'Lester', 'Levine', 'Lindsey',
            'Maddox', 'Mason', 'Mercer', 'Miller', 'Moore', 'Moran', 'Moreno', 'Olsen', 'Patterson', 'Peters', 'Phipps', 'Pierce', 'Quinn', 'Reed',
            'Rice', 'Robinson', 'Rose', 'Sanders', 'Schmidt', 'Scott', 'Shannon', 'Sims', 'Sloan', 'Smith', 'Snyder', 'Spencer', 'Stokes', 'Sullivan',
            'Tanner', 'Vaughn', 'Watkins', 'White', 'Williams', 'Wilkerson', 'Wilson', 'Yates',
            'Abbott', 'Ashford', 'Banks', 'Barrett', 'Benton', 'Blackwood', 'Blakeley', 'Briggs', 'Buckingham', 'Caldwell', 'Chamberlain', 'Chapman',
            'Chavez', 'Clayton', 'Crawford', 'Cross', 'Dalton', 'Dawes', 'Delgado', 'Dillard', 'Elliott', 'Everett', 'Farrell', 'Fitzgerald',
            'Foster', 'Fowler', 'Freeman', 'Galloway', 'Gibbs', 'Gorman', 'Harrison', 'Henderson', 'Holloway', 'Horton', 'Hughes', 'Jackson',
            'Kendall', 'Knightley', 'Landry', 'Leclerc', 'Lindsey', 'Manning', 'Montgomery', 'O’Neill', 'O’Reilly', 'Parker', 'Pendleton', 'Pierce',
            'Preston', 'Quinn', 'Raleigh', 'Randolph', 'Reed', 'Richards', 'Rollins', 'Rosemond', 'Schneider', 'Spencer', 'Taylor', 'Travis', 'Vance',
            'Vaughn', 'Wells', 'Whitaker', 'Wilkins', 'Williamson', 'Winters', 'Wolfe', 'Wyatt', 'Yates', 'Youngblood', 'Zane',
            'Abernathy', 'Ainsley', 'Albright', 'Bainbridge', 'Barclay', 'Bastian', 'Bennett', 'Blackwell', 'Bliss', 'Bradford', 'Branford', 
            'Bridges', 'Caldwell', 'Calhoun', 'Carrington', 'Chapman', 'Clifton', 'Coleman', 'Covington', 'Crawford', 'Davenport', 'Devlin',
            'Dickinson', 'Donahue', 'Ellison', 'Farnsworth', 'Fletcher', 'Garrison', 'Gilbert', 'Grafton', 'Harrington', 'Hendrickson', 'Hollis',
            'Huntley', 'Kerrigan', 'Kingsley', 'Langford', 'Lester', 'Lockwood', 'Maddox', 'Marston', 'Mason', 'McAllister', 'Merrick', 
            'Middlesex', 'Montague', 'Morrison', 'Nash', 'Newman', 'Pendleton', 'Quincy', 'Raleigh', 'Remington', 'Sampson', 'Sinclair', 
            'Sullivan', 'Tennyson', 'Vanderbilt', 'Vaughn', 'Westbrook', 'Wexler', 'Willoughby', 'Winston', 'Woodson', 'York', 'Ziegler'
        ]
        
        #  Events  descriptions
        events = [
            'discovers an ancient artifact with unimaginable power', 
            'unravels a conspiracy that could destroy the world', 'must stop a cataclysmic event that threatens their home', 
            'is tasked with finding the last known survivor of a vanished civilization', 'gets caught in a time loop and must find a way to break free', 
            'becomes involved in a deadly game of survival in a dystopian society', 'accidentally releases a powerful curse and must find a way to undo it', 
            'is forced to make an impossible choice that could change the course of history', 'is betrayed by someone they trusted and must escape a deadly trap', 
            'learns a terrible truth about their origins that changes everything', 'must protect an ancient relic from being stolen', 
            'becomes the leader of an uprising against an oppressive regime', 'is cursed to relive the worst day of their life', 
            'finds themselves in the middle of an intergalactic war', 'witnesses the destruction of their hometown and vows revenge', 
            'discovers they have powers they can’t control', 'gets pulled into a mystery involving their own family', 
            'discovers a long-lost sibling with a dark secret', 'must solve a murder to clear their name', 'is transported to a parallel universe', 
            'accidentally unleashes a creature from another world', 'is haunted by a shadowy figure from their past', 
            'stumbles upon a long-forgotten treasure map', 'must retrieve a magical object to save the world', 'discovers a dark secret buried in their town’s history', 
            'finds themselves trapped in a dimension with no escape', 'gets caught in a battle between gods', 'accidentally triggers a chain of events that causes a global disaster', 
            'must stop a time-traveling villain from changing history', 'joins a group of rebels to fight a corrupt government', 'uncovers a hidden society controlling the world from the shadows', 
            'must protect a prophecy that could determine the fate of the universe', 'becomes a target of a mysterious and powerful organization', 
            'gets caught up in an ancient war between good and evil', 'has to navigate a deadly game of survival for a grand prize', 
            'inherits a mansion with a dark past that haunts them', 'meets a mythical creature who offers them a dangerous bargain', 
            'becomes a pawn in a high-stakes political game', 'must stop a rogue AI from taking over humanity', 
            'discovers their soulmate across time and space', 'uncovers the truth about their ancestry', 'is thrust into a conflict with an evil version of themselves', 
            'is tasked with breaking a magical curse that affects their entire family', 'must escape a deadly virtual reality world', 'joins forces with an unexpected ally to defeat a common enemy', 
            'discovers an alien invasion in the making and must stop it', 'finds themselves stuck in a never-ending battle against time',
            'uncovers an ancient prophecy that could save or destroy the world', 
            
            'finds themselves being hunted by an unstoppable force', 
            'is chosen by a mysterious entity to protect a sacred realm', 
            'discovers a hidden underground city with a forgotten history', 
            'must stop a mad scientist from unleashing a world-changing invention', 
            'becomes the unwilling leader of a faction in a brutal war', 
            'uncovers a long-forgotten cult that controls the fate of humanity', 
            'must protect a child who holds the key to humanity’s survival', 
            'discovers a deadly secret about their best friend', 
            'gets tangled in a web of lies that could unravel everything they know', 
            'is forced to confront their greatest fear in a life-or-death situation', 
            'uncovers a long-lost civilization beneath the ocean', 
            'must choose between love and duty in a deadly situation', 
            'stumbles upon a sentient being with the power to reshape reality', 
            'is betrayed by a family member and forced to flee for their life', 
            'discovers an ancient technology capable of altering the course of history', 
            'is trapped in a dream world where nothing is as it seems', 
            'finds themselves at the center of a revolution that could change everything', 
            'uncovers a forbidden love affair with disastrous consequences', 
            'finds an artifact that can bring the dead back to life—but at a cost', 
            'is forced to betray their friends to save the world', 
            'discovers a vast conspiracy to control the world’s economy', 
            'meets an immortal being who has been alive for centuries', 
            'is forced to make an alliance with a powerful enemy', 
            'discovers they are the heir to a powerful but dangerous legacy', 
            'is pulled into a conflict between the living and the dead', 
            'discovers the truth about an alternate reality where they never existed', 
            'must break a curse that prevents them from ever leaving a certain city', 
            'unravel a mystery about their past that could shatter their identity', 
            'finds themselves inside a world where technology has merged with magic', 
            'becomes part of a rebellion to overthrow a ruthless ruler', 
            'is transported to a world where everyone is a different version of themselves', 
            'uncovers the secrets of an ancient order that governs the multiverse', 
            'discovers that a long-dead ancestor has been watching over them', 
            'is forced to fight a powerful entity that feeds on their fears', 
            'meets a time traveler who warns them about an apocalyptic event', 
            'becomes a guardian of an ancient relic with the power to reshape time', 
            'must stop a powerful sorcerer from opening a portal to another dimension', 
            'uncovers a dark secret about a seemingly perfect society', 
            'is betrayed by someone they love, leading to a path of revenge', 
            'stumbles upon an ancient weapon that could destroy the world', 
            'is chosen as the champion in a deadly arena that decides the fate of the universe', 
            'uncovers the existence of parallel worlds, each with its own version of them', 
            'must stop a shadowy group from assassinating a political leader', 
            'discovers the existence of creatures from another world hidden on Earth', 
            'finds themselves trapped in a virtual reality game where every decision is life or death', 
            'joins a team of rebels to stop an oppressive regime that controls the skies', 
            'discovers an ancient curse that has been passed down through generations', 
            'finds a portal to a mystical land, but at the cost of their humanity', 
            'is chosen as the last hope for an entire race of beings facing extinction', 
            'unravel the mystery behind an ancient alien artifact that could alter the galaxy', 
            'is forced to confront their dark past and the choices that led them to where they are', 
            'is tasked with finding a missing person who holds the key to stopping an impending war',

            "Stumbles upon a hidden underground fighting ring and is drawn into the competition.",

            "Accidentally activates a long-dormant security system that leads to a thrilling escape.",

            "Is recruited by a secret organization to stop a global threat.",

            "Finds themselves in the middle of a high-speed chase through the city.",

            "Discovers a hidden stash of weapons and must decide whether to use them.",

            "Is caught in a sudden storm while sailing and must navigate to safety.",

            "Uncovers a plot to steal a valuable artifact and must race against time to stop it.",

            "Is thrust into a survival situation after a plane crash in a remote area.",

            "Joins a team of adventurers on a quest to find a legendary treasure.",

            "Is challenged to a dangerous game of cat and mouse with a skilled adversary.",

            "Finds a mysterious map that leads to a series of thrilling challenges.",

            "Is trapped in a collapsing building and must find a way out before it's too late.",

            "Accidentally witnesses a crime and becomes a target for the criminals.",

            "Is forced to participate in a high-stakes heist to save a loved one.",

            "Discovers a hidden passage in an ancient ruin that leads to unexpected dangers.",

            "Is caught in a political coup and must navigate the chaos to survive.",

            "Finds themselves in a deadly race against time to defuse a bomb.",

            "Is recruited to join a team of elite operatives on a covert mission.",

            "Stumbles upon a secret laboratory conducting dangerous experiments.",

            "Is challenged to a duel by a rival seeking revenge.",

            "Finds a powerful artifact that attracts the attention of dangerous foes.",

            "Is swept into a rebellion against an oppressive regime.",

            "Accidentally triggers a series of events that lead to a thrilling chase.",

            "Is forced to confront their fears while navigating a treacherous landscape.",

            "Discovers a hidden base of operations for a criminal organization.",

            "Is caught in a natural disaster and must find a way to safety.",

            "Is thrust into a world of espionage when they uncover a spy ring.",

            "Finds themselves in a deadly game of survival on a deserted island.",

            "Is challenged to a race against time to save a kidnapped friend.",

            "Accidentally activates a time machine and must navigate different eras.",

            "Is drawn into a conspiracy that leads to a thrilling investigation.",

            "Finds a mysterious device that grants them extraordinary abilities.",

            "Is forced to make a daring escape from a high-security facility.",

            "Discovers a hidden world of magical creatures and must protect it from danger.",

            "Is caught in a battle between rival factions vying for control.",

            "Is tasked with retrieving a stolen item from a heavily guarded location.",

            "Finds themselves in a thrilling chase across rooftops in a bustling city.",

            "Is recruited to join a team of explorers on a dangerous expedition.",

            "Accidentally uncovers a plot to unleash chaos and must stop it.",

            "Is thrust into a deadly competition where only one can survive.",

            "Finds a hidden treasure map that leads to a series of perilous challenges.",

            "Is caught in a web of intrigue involving powerful figures.",

            "Is forced to confront a dangerous creature that threatens their home.",

            "Discovers a hidden talent for combat that helps them in a crisis.",

            "Is swept into a whirlwind of action during a city-wide festival.",

            "Finds themselves in a race against time to prevent a disaster.",

            "Is challenged to a high-stakes game that tests their skills and wits.",

            "Accidentally stumbles upon a secret meeting of powerful individuals.",

            "Is drawn into a thrilling adventure when they find a lost artifact.",

            "Must navigate a treacherous landscape filled with traps and obstacles.",

            "Is forced to team up with an unlikely ally to face a common enemy.",

            "Finds themselves in a thrilling showdown with a notorious villain."

        
        ]
        
        # Genres
        genres = [
            'mystery', 'sci-fi', 'fantasy', 'horror', 'romance', 'thriller', 'adventure', 
            'historical fiction', 'dystopian', 'magical realism', 'psychological drama', 
            'crime fiction', 'urban fantasy', 'steampunk', 'space opera', 'high fantasy', 
            'conspiracy thriller', 'post-apocalyptic', 'superhero', 'slice of life', 'noir', 
            'alternate history', 'dark fantasy', 'bildungsroman', 'zombie apocalypse', 'fairy tale', 
            'paranormal', 'historical fantasy', 'weird fiction', 'time travel', 'action-packed', 
            'supernatural thriller', 'fable', 'epic fantasy', 'satire', 'political thriller', 
            'romantic comedy', 'religious allegory', 'satirical dystopian', 'psychological horror', 
            'coming-of-age', 'space western', 'detective fiction', 'magical adventure', 
            'philosophical fiction', 'buddy cop', 'futuristic dystopia', 'survival fiction', 
            'mythic fiction', 'vampire fiction', 'urban horror', 'dark comedy', 'biographical fiction',

            'action', 'adventure romance', 'alien invasion', 'anthology', 'apocalyptic', 

            'art heist', 'biopunk', 'body horror', 'children’s literature', 'chick lit', 

            'climate fiction', 'cozy mystery', 'cyberpunk', 'dark romance', 'detective thriller', 

            'dystopian romance', 'epistolary', 'erotic fiction', 'family saga', 'feminist fiction', 

            'futuristic romance', 'ghost story', 'grimdark fantasy', 'historical romance', 

            'horror comedy', 'intergalactic adventure', 'literary fiction', 'magical realism romance', 

            'medieval fantasy', 'metafiction', 'military science fiction', 'murder mystery', 

            'mythology', 'new adult', 'non-linear narrative', 'occult fiction', 'parody', 

            'postmodern fiction', 'psychological thriller', 'quest fantasy', 'realistic fiction', 

            'religious fiction', 'romantic fantasy', 'romantic suspense', 'sci-fi romance', 

            'short stories', 'slipstream', 'space exploration', 'spiritual fiction', 

            'steampunk romance', 'supernatural romance', 'surrealism', 'techno-thriller', 

            'teen fiction', 'thriller romance', 'time slip', 'urban fantasy romance', 

            'vintage fiction', 'war fiction', 'weird western', 'whodunit', 'women’s fiction', 

            'young adult', 'zany comedy', 'zombie romance', 'historical mystery', 

            'magical realism horror', 'futuristic thriller', 'time travel romance', 

            'action-adventure', 'historical adventure', 'romantic drama', 'sword and sorcery', 

            'mythical adventure', 'caper', 'fable fantasy', 'sci-fi thriller', 

            'romantic fantasy comedy', 'historical horror', 'adventure fantasy', 

            'mystery thriller', 'superhero romance', 'dark fantasy romance', 

            'magical realism mystery', 'urban fantasy thriller', 'historical drama', 

            'romantic suspense thriller', 'epic adventure', 'fantasy romance', 

            'sci-fi adventure', 'mystery comedy', 'action thriller', 'historical fiction romance'
        ]
        
        #  Themes
        themes = [
            'betrayal and redemption', 'the consequences of ambition', 'love in a world torn apart by war', 
            'the clash of ancient traditions and futuristic technology', 'identity and self-discovery', 
            'sacrifice for the greater good', 'the blurred lines between right and wrong', 'the fight against an oppressive regime', 
            'the power of friendship in times of adversity', 'survival against all odds', 'revenge and forgiveness', 
            'the search for meaning in a chaotic world', 'moral ambiguity', 'the fragility of peace', 'the strength of the human spirit', 
            'the pursuit of knowledge at any cost', 'greed and corruption', 'the battle between good and evil', 
            'technology and its impact on society', 'destiny and free will', 'overcoming fear', 'the dangers of unchecked power', 
            'hope in the face of darkness', 'the consequences of playing god', 'the quest for immortality', 
            'individual versus society', 'the power of art to change the world', 'memory and its distortions', 
            'self-sacrifice for the greater good', 'the destructiveness of vengeance', 'the search for true love', 
            'deception and truth', 'the struggle for freedom', 'the duality of human nature', 'acceptance and tolerance', 
            'the journey to find home', 'the idea of fate versus choice', 'the exploration of the unknown', 
            'the fragility of life', 'the illusion of control', 'the beauty of the mundane', 
            'the consequences of hubris', 'human nature versus artificial intelligence', 
            'the loss of innocence', 'the journey of personal growth', 'the isolation of the individual', 
            'dealing with guilt', 'family versus personal ambition', 'a world without rules',

            'the thrill of the chase', 'betrayal in the heat of battle', 'the fight for survival in a hostile world', 

            'the quest for a legendary artifact', 'the rise of an unlikely hero', 'the consequences of a reckless decision', 

            'the battle against time to save a loved one', 'the struggle for power in a corrupt regime', 

            'the clash of rival factions', 'the journey to uncover hidden truths', 

            'the impact of war on the human spirit', 'the pursuit of justice in a lawless land', 

            'the fight against an ancient evil', 'the quest for vengeance', 

            'the struggle to protect a secret that could change everything', 'the race against a ticking clock', 

            'the power of teamwork in overcoming obstacles', 'the consequences of a dangerous alliance', 

            'the thrill of espionage and deception', 'the fight for freedom against oppression', 

            'the journey through uncharted territories', 'the impact of betrayal on friendships', 

            'the struggle to maintain humanity in a brutal world', 'the quest to stop a catastrophic event', 

            'the power of sacrifice in the face of danger', 'the thrill of a high-stakes heist', 

            'the battle against a powerful adversary', 'the journey to reclaim a lost legacy', 

            'the consequences of a forbidden romance in a time of war', 'the fight for survival in a post-apocalyptic world', 

            'the quest to unlock ancient secrets', 'the struggle against a relentless enemy', 

            'the impact of technology on warfare', 'the thrill of a deadly game', 

            'the journey to unite divided factions', 'the consequences of a tragic past', 

            'the fight against a corrupt system', 'the power of hope in desperate times', 

            'the thrill of a secret mission', 'the struggle to protect the innocent', 

            'the quest for redemption in a world of chaos', 'the impact of loyalty in times of conflict', 

            'the battle for control of a powerful resource', 'the journey to discover one’s true potential', 

            'the consequences of a life-altering choice', 'the fight against a supernatural force', 

            'the thrill of a race against rivals', 'the struggle to overcome personal demons', 

            'the quest to save a dying world', 'the impact of friendship in the face of danger', 

            'the battle against a ticking time bomb', 'the journey to uncover a conspiracy', 

            'the consequences of a reckless adventure', 'the fight for justice in a corrupt society', 

            'the thrill of a treasure hunt', 'the struggle to survive in a hostile environment', 

            'the quest to break free from captivity', 'the impact of sacrifice on a mission', 

            'the battle against a powerful villain', 'the journey to find a lost civilization', 

            'the consequences of a secret war', 'the fight for survival in a deadly competition', 

            'the thrill of a daring escape', 'the struggle to protect a fragile alliance', 

            'the quest to harness a forbidden power', 'the impact of betrayal on a mission', 

            'the battle for the future of humanity', 'the journey to confront a dark past', 

            'the consequences of a dangerous obsession', 'the fight against a relentless pursuit', 

            'the thrill of a high-stakes negotiation', 'the struggle to maintain hope in despair', 

            'the quest to uncover hidden talents', 'the impact of a mentor on a hero’s journey', 

            'the battle against a powerful corporation', 'the journey to reclaim a stolen identity', 

            'the consequences of a fateful encounter', 'the fight for a better tomorrow', 

            'the thrill of a secret society', 'the struggle to balance duty and desire', 

            'the quest to protect a sacred place', 'the impact of a prophecy on a hero’s journey', 

            'the battle against a ticking clock', 'the journey to find inner strength', 

            'the consequences of a life-changing decision', 'the fight against a powerful curse', 

            'the thrill of a daring rescue', 'the struggle to overcome societal expectations', 

            'the quest to unite warring factions', 'the impact of a tragic loss on a hero’s journey'
        ]
        
        # Tones
        tones = [
            'dark and brooding', 'light-hearted and humorous', 'melancholic and reflective', 'tense and suspenseful', 
            'epic and heroic', 'romantic and emotional', 'optimistic and hopeful', 'sinister and eerie', 
            'mysterious and thought-provoking', 'gritty and realistic', 'uplifting and inspirational', 
            'graceful and poetic', 'tragic and sorrowful', 'adventurous and bold', 'whimsical and playful', 
            'hopeful and heartwarming', 'somber and tragic', 'cynical and jaded', 'reflective and philosophical', 
            'raw and unfiltered', 'tender and emotional', 'surreal and strange', 'mournful and regretful', 
            'charming and quirky', 'ambiguous and uncertain', 'dreamlike and fantastical', 'depressing and bleak', 
            'exciting and fast-paced', 'romantic and nostalgic', 'confusing and disorienting', 'heroic and triumphant', 
            'introspective and deep', 'bittersweet and conflicted', 'chilling and horrifying', 'playful and carefree', 
            'melodramatic and exaggerated', 'somber and philosophical', 'light and breezy', 'hopeful and defiant', 
            'suspenseful and nerve-wracking', 'disillusioned and jaded', 'relentless and unyielding', 
            'vivid and rich', 'fast-paced and thrilling', 'subdued and gentle', 'graceful and uplifting', 
            'epic and sweeping', 'heartfelt and sincere', 'energetic and fiery', 'calm and soothing',

            'intense and gripping', 'dynamic and explosive', 'adrenaline-fueled and thrilling', 

            'fierce and unrelenting', 'bold and daring', 'fast-paced and exhilarating', 

            'raw and visceral', 'tenacious and relentless', 'fiery and passionate', 

            'chaotic and unpredictable', 'vibrant and electrifying', 'urgent and compelling', 

            'suspenseful and heart-pounding', 'heroic and valiant', 'dramatic and impactful', 

            'gritty and hard-hitting', 'ferocious and wild', 'unstoppable and fierce', 

            'intrepid and adventurous', 'explosive and dramatic', 'thrilling and suspenseful', 

            'intense and emotional', 'brave and courageous', 'frenzied and chaotic', 

            'unstoppable and powerful', 'adventurous and daring', 'intense and action-packed', 

            'fiery and intense', 'relentless and fierce', 'dynamic and fast-paced', 

            'gripping and suspenseful', 'thrilling and captivating', 'bold and adventurous', 

            'high-octane and exhilarating', 'tense and electrifying', 'fast-paced and gripping', 

            'adventurous and daring', 'intense and heart-racing', 'explosive and thrilling', 

            'fierce and passionate', 'dynamic and engaging', 'urgent and suspenseful', 

            'adrenaline-pumping and exciting', 'intense and captivating', 'dramatic and thrilling', 

            'fast-paced and action-packed', 'vivid and intense', 'explosive and dynamic', 

            'tense and gripping', 'fierce and relentless', 'adventurous and bold', 

            'high-energy and thrilling', 'intense and powerful', 'dynamic and fast-paced', 

            'urgent and heart-pounding', 'explosive and captivating', 'intense and gripping', 

            'fierce and action-oriented', 'dynamic and thrilling', 'adventurous and exciting', 

            'high-stakes and suspenseful', 'intense and dramatic', 'fast-paced and exhilarating', 

            'gritty and intense', 'bold and daring', 'tense and suspenseful', 

            'adrenaline-fueled and gripping', 'dynamic and action-packed', 'urgent and thrilling', 

            'explosive and heart-pounding', 'intense and electrifying', 'fierce and powerful', 

            'dramatic and engaging', 'high-energy and captivating', 'tense and action-oriented', 

            'adventurous and thrilling', 'dynamic and gripping', 'urgent and compelling', 

            'explosive and intense', 'intense and fast-paced', 'fierce and relentless', 

            'dramatic and heart-stopping', 'high-octane and thrilling', 'tense and gripping', 

            'adventurous and daring', 'dynamic and engaging', 'urgent and suspenseful', 

            'explosive and captivating', 'intense and powerful', 'fierce and action-packed', 

            'dramatic and thrilling', 'high-energy and exhilarating', 'tense and heart-pounding', 

            'adrenaline-fueled and gripping', 'dynamic and fast-paced', 'urgent and thrilling', 

            'explosive and intense', 'intense and captivating', 'fierce and relentless', 

            'dramatic and engaging', 'high-stakes and suspenseful', 'tense and action-oriented', 

            'adventurous and bold', 'dynamic and thrilling', 'urgent and compelling', 

            'explosive and heart-pounding', 'intense and gripping', 'fierce and powerful', 

            'dramatic and captivating', 'high-energy and thrilling', 'tense and suspenseful', 

            'adrenaline-pumping and exciting', 'dynamic and action-packed', 'urgent and gripping', 

            'explosive and dramatic', 'intense and emotional', 'fierce and passionate', 

            'dramatic and impactful', 'high-octane and exhilarating', 'tense and electrifying', 

            'adventurous and daring', 'dynamic and fast-paced', 'urgent and heart-stopping', 

            'explosive and captivating', 'intense and powerful', 'fierce and relentless', 

            'dramatic and thrilling', 'high-energy and engaging', 'tense and gripping', 

            'adrenaline-fueled and thrilling', 'dynamic and action-oriented', 'urgent and compelling'
        ]
        
        #shuffle our names
        shuffle(first_names)
        shuffle(last_names)

        # Randomly select one from each category
        setting = random.choice(settings)
        character = random.choice(characters)
        name = f'named {random.choice(first_names)} {random.choice(last_names)}'  # Use random first and last name
        event = random.choice(events)
        genre = random.choice(genres)
        theme = random.choice(themes)
        tone = random.choice(tones)

        #names = f' For the character names used in the story, choose from these first names {first_names} and these last names {last_names}.'
        #names = f' For the character names used in the story, choose randomly from these first names {first_names} and these last names {last_names}.'
        
        #names = f"For the character names used in the story, choose randomly from these first names: {', '.join(first_names[:100])} and these last names: {', '.join(last_names[:100])}."

        #we do this so our AI can create unique names. Gemini and other AIs like to reuse same names a lot. We are trying to vary them best as possible
        names = f"For the character names used in the story, choose randomly from these first names: {', '.join(first_names[:100])} and these last names: {', '.join(last_names[:100])}. Ensure the names are fresh, diverse, and not overused in typical stories. Aim for names that suit the genre and feel fitting for the setting and tone of the narrative."


        #this will see if we let the ai create its own name
        if random.random() > 0.98:
            name = ""
            names = ""
        name = ""
        # Combine to form a random story prompt
        #many different prompts to test out story creation

        #prompt = (f"Write a {genre} story with a {tone} tone about {character}{name} "
        #          f"who {event} in {setting}.{names} The theme of the story should be "
        #          f"'{theme}'. Come up with a title name and place it at the start. Place after the title, all character names in the story. Label them both. When creating character names, be very random.")
        prompt = (f"Write a {genre} story with a {tone} tone about {character}{name} "
                f"who {event} in {setting}.{names} The theme of the story should be "
                f"'{theme}'. Come up with a title name and place it at the start. Limit the size to no more than {size} paragraphs.")
        
        prompt = (f"Compose a {genre} narrative, imbued with a {tone} tone, centered around {character}{name} "
          f"who experiences {event} within a distinct locale referred to as {setting}. The names of any supporting individuals are {names}. "
          f"The underlying exploration should revolve around the concept of '{theme}'. "
          f"Begin the composition with an original title that captures the essence of the story, avoiding commonplace or predictable naming conventions for both the title and the setting. Limit the narrative to a maximum of {size} paragraphs.")

        #fall back one with names fix
        prompt = (f"Compose a {genre} narrative, imbued with a {tone} tone, centered around {character}{name} "
          f"who experiences {event} within a distinct locale referred to as {setting}. {names}. "
          f"The underlying exploration should revolve around the concept of '{theme}'. "
          f"Begin the composition with an original title that captures the essence of the story, avoiding commonplace or predictable naming conventions for both the title and the setting. Limit the narrative to a maximum of {size} paragraphs.")

        #chat gpt update
        prompt = (
            f"Compose a {genre} narrative, imbued with a {tone} tone, centered around {character}{name} "
            f"who experiences {event} in a world with an entirely unique and inventive setting. "
            f"Create fresh, imaginative names for the cities and characters, avoiding any conventional or predictable names. "
            f"Ensure that the setting feels original, with locations that have never been seen before. {names} "
            f"The underlying exploration should revolve around the concept of '{theme}'. "
            f"Begin the composition with an original title that captures the essence of the story. "
            f"Limit the narrative to a maximum of {size} paragraphs."
        )

        prompt = (f"Compose a {genre} narrative, imbued with a {tone} tone, centered around {character}{name} "
          f"who experiences {event} within a distinct locale referred to as {setting}. {names} "
          f"Use a mix of fresh, diverse, and fitting names that suit the characters and setting, avoiding overused or predictable names. "
          f"The underlying exploration should revolve around the concept of '{theme}'. "
          f"Begin the composition with an original title that captures the essence of the story, avoiding commonplace or predictable naming conventions for both the title and the setting. "
          f"Limit the narrative to a maximum of {size} paragraphs.")
        
        prompt = (f"Compose a {genre} narrative, imbued with a {tone} tone, centered around a character who experiences {event} within a distinct locale referred to as {setting}. "
          f"{names} The character names should be diverse, unique, and creative, ensuring that no names feel overly familiar or reused. "
          f"The underlying exploration should revolve around the concept of '{theme}'. "
          f"Begin the composition with an original title that captures the essence of the story, avoiding predictable naming conventions for both the title and the setting. "
          f"Limit the narrative to a maximum of {size} paragraphs.")


        #print('\n\n COUNT: : ' + str(Token_Count.count_tokens(prompt)) )

        return prompt
    
    #creates a story based on random prompt and returns the string of it
    #send in size to limit to so many paragraphs
    def create_story_with_g4f(self, size)->str:        
        
        while True:
            try:
                result = self.testg4f("You are an expert story teller. ", 
                                      self.get_random_prompt(size) + " Give a title but no labels!")
                break
            except Exception as e:
                    print(e)
                    time.sleep(10)

        while True:
            try:
                result = self.testg4f(
                    "You are an expert proofreader and story editor.",
                    f"""You will receive a story below. Proofread it for grammar, spelling, and flow. 
                    If the story appears unfinished, abrupt, or incomplete, continue the story naturally, preserving the existing tone, pacing, and narrative style until it reaches a satisfying conclusion. 
                    Do not explain your changes. Return only the revised, completed story with the title at the start. 

                    Story: {result}"""
                        )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        return result
    
    #creates a story based on random prompt and returns the string of it
    #send in size to limit to so many paragraphs
    def create_story(self, size)->str:        
        
        while True:
            try:
                #create a random story
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=self.get_random_prompt(size),
                    config=types.GenerateContentConfig(
                        temperature=1.1,
                        system_instruction='You are an expert story teller.',
                    ),
                )
                break
            except Exception as e:
                    print(e)
                    time.sleep(10)

        while True:
            try:
                #proof read and then return
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=f"Proof read this story and make changes needed. Make sure to put the title of the story at the start. Do not tell me about changes you have done. : {result.text}",
                    config=types.GenerateContentConfig(
                        system_instruction='You are an expert proof reader.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        return result.text
    
    #this will take the data we received on item descriptions and format them for Flux.
    def format_item_description(self, desc):
        # Split by commas and strip whitespace
        parts = [p.strip() for p in desc.split(",")]

        # If the list size is 7 (missing one part due to "and"), split the last element
        if len(parts) == 7 and 'and' in parts[-1]:
            last_part = parts[-1].split("and")
            # Strip extra spaces and add the two parts as separate entries
            parts[-1] = last_part[0].strip()
            parts.append(last_part[1].strip())

        # Check if we now have 8 parts
        if len(parts) != 8:
            #raise ValueError(f"Item description does not have 8 attributes: {desc}")
            return None

        # Extract attributes
        name, item_type, material, color, size, design_style, notable_features, condition = parts

        # Create the formatted prompt
        prompt = (
            f"A {item_type.lower()} called {name}, made of {material.lower()} with a {color.lower()} color. "
            f"It is {size.lower()} in size, designed in a {design_style.lower()} style, "
            f"featuring {notable_features.lower()}. The item is currently {condition.lower()}."
        )

        if not prompt.endswith("."):
            prompt += "."

        return prompt


    def create_item_descriptions(self, story):
        descriptions = []

        itemtext = f"""
        Read the following story and identify important physical objects, artifacts, or items that play a significant or narrative-relevant role in the story. For each item, extract or invent a detailed physical description using the 8 attributes below, separated by commas — and no commas allowed within any attribute value. If a trait is unspecified or not mentioned, you MUST create a plausible one yourself. Do not leave any attribute as 'unknown', 'undefined', 'unspecified', or blank.
        There must always be 8 attributes.

        Only include items that are crucial to the story's events, setting, or character motivations — avoid ordinary or background objects.

        The 8 attributes, in order, are:

        1. Item Name  
        2. Item Type  
        3. Material/Composition  
        4. Primary Color  
        5. Size/Dimensions (use format 'size: small/medium/large' or 'size: height x width x length')  
        6. Design Style  
        7. Notable Features  
        8. Current Condition  

        Example format:
        The Obsidian Heart, Artifact, crystalline stone, deep black, size: small, eldritch, glowing crimson veins, pristine

        **Do not add any extra text, labels, or explanations. Only return the final list of item descriptions in this exact format, one per line, with each description separated by two newlines (\n\n).**

        Here is the story:
        {story}
        """

        itemtext = f"""
        Read the following story and identify all important physical objects, artifacts, or items that play a significant or narrative-relevant role in the story. For each item, extract or plausibly invent a complete, detailed physical description containing **exactly 8 attributes**, separated by commas. **Do not include commas within any attribute value**.

        **You must always provide 8 attributes for every item.**  
        If a trait is unspecified or missing in the story, you MUST create a fitting, plausible one consistent with the story’s world and context. Never leave any attribute empty, undefined, unknown, or marked as 'unspecified'.

        The required 8 attributes, in strict order, are:

        1. Item Name  
        2. Item Type  
        3. Material/Composition  
        4. Primary Color  
        5. Size/Dimensions (format: 'size: small/medium/large' or 'size: height x width x length')  
        6. Design Style  
        7. Notable Features  
        8. Current Condition  

        **Example format:**
        The Obsidian Heart, Artifact, crystalline stone, deep black, size: small, eldritch, glowing crimson veins, pristine

        **Rules:**
        - Only include items that are crucial to the story’s events, setting, or character motivations — skip ordinary, unimportant, or background objects.
        - Every item description must have **exactly 8 comma-separated attributes** in the correct order.
        - Ensure no attribute contains commas.
        - If no items are present, return an empty string.

        **Important: Double-check that every item description has exactly 8 attributes, separated by commas, before returning the final output.**

        **Do not add any extra text, labels, numbers, or explanations. Only return the final list of item descriptions in this exact format, one per line, with each description separated by two newlines (\n\n).**

        Here is the story:
        {story}
        """

        itemtext = f"""
        Read the following story and identify all important physical objects, artifacts, or items that play a significant or narrative-relevant role in the story. For each identified item, extract or invent a complete, detailed physical description containing **exactly 8 attributes**, separated by commas.  
        **Do not include commas within any attribute value** under any circumstance.

        **You must always provide exactly 8 attributes for every item.**  
        If any attribute is missing or unspecified in the story, you MUST invent a plausible, context-appropriate value consistent with the story’s world, ensuring the total number of attributes remains exactly 8.  
        **Never leave any attribute blank, undefined, unknown, or marked as 'unspecified'.**

        The required 8 attributes, in this exact strict order, are:

        1. Item Name  
        2. Item Type  
        3. Material/Composition  
        4. Primary Color  
        5. Size/Dimensions (use 'size: small', 'size: medium', 'size: large', or 'size: height x width x length')  
        6. Design Style  
        7. Notable Features  
        8. Current Condition  

        **Example format (one line, 8 comma-separated attributes, no commas inside attribute values):**  
        The Obsidian Heart, Artifact, crystalline stone, deep black, size: small, eldritch, glowing crimson veins, pristine

        **Formatting and Rules:**
        - Only include items that are crucial to the story’s events, setting, or character motivations. Ignore ordinary, irrelevant, or background objects.
        - Every item description must have **exactly 8 attributes, separated by commas, in the precise order listed above.**
        - Ensure no attribute contains commas or extra punctuation.
        - If no items are present in the story, return an empty string.

        **Important: Before returning your final output, double-check and validate that every item description has exactly 8 attributes, separated by commas, no more and no less. Do not add any extra text, labels, numbers, bullet points, or explanations.**

        **Return only the final list of item descriptions, one per line, separated by two newlines (\\n\\n).**

        Here is the story:
        {story}
        """


        while True:
            try:
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=itemtext,
                    config=types.GenerateContentConfig(
                        temperature=0.9,
                        #system_instruction='You are an expert proof reader.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)
        
        #result = llm.invoke(text)

        #print(result.content)

        descriptions = result.text.split('\n\n')

        if descriptions and descriptions[-1] == "":
            descriptions.pop()

        print(descriptions)

        # Convert to a list of character descriptions
        formatted_item_descriptions = [self.format_item_description(desc) for desc in descriptions]

        #if we had an error, just return None
        if None in formatted_item_descriptions:
            return None

        print('\n\n\n')
        print(formatted_item_descriptions)

        return formatted_item_descriptions
        #return descriptions

    #takes data of story character descriptions and formats it for Flux
    def format_character_description(self, desc):
        # Split by commas and strip whitespace
        parts = [p.strip() for p in desc.split(",")]

        # If the list size is 12 (missing one part due to "and"), split the last element
        if len(parts) == 12 and 'and' in parts[-1]:
            last_part = parts[-1].split("and")
            # Strip extra spaces and add the two parts as separate entries
            parts[-1] = last_part[0].strip()  # First part before "and"
            parts.append(last_part[1].strip())  # Second part after "and"

        # Check if we now have 13 parts
        if len(parts) != 13:
            #raise ValueError(f"Character description does not have 13 attributes: {desc}")
            return None

        # Extract attributes from the list
        name, gender, race, age, skin_color, hairstyle, hair_color, haircut, eye_color, height, build, attire, notable_traits = parts

        # Adjusting the height description to remove "height:" for clarity
        height = height.replace("height:", "").strip()

        # Create the formatted prompt
        prompt = (
            f"{name} is a {age}-year-old {race.lower()} {gender.lower()} with {skin_color.lower()} skin, "
            f"{hairstyle.lower()} {hair_color.lower()} hair styled in a {haircut.lower()}, and {eye_color.lower()} eyes. "
            f"They are {height} tall with a {build.lower()} build. "
            f"They wear {attire.lower()} and are noted for {notable_traits.lower()}."
        )

        if not prompt.endswith("."):
            prompt += "."

        return prompt
    
    #sends a prompt to Gemini to create detailed descriptions of how each story character looks. This is to try and keep them looking the same through out.
    def create_character_descriptions(self, story)->list:
        descriptions = []

        #chatgpt created prompt 4/22
        besttext = f"""
            Read the following story and extract or invent detailed physical descriptions for each character mentioned. Each description must be formatted as a single line string with the following 13 attributes, separated by commas — and no commas allowed within any attribute value. If a trait is unspecified or not mentioned, you MUST create a plausible one yourself. Do not leave any attribute as 'unknown', 'undefined', 'unspecified', or blank. For characters without hair, write 'bald' for hairstyle, 'none' for hair color, and 'none' for haircut. Ensure that each description contains a fully completed set of attributes.

            The 13 attributes, in order, are:

            1. Name  
            2. Gender  
            3. Race  
            4. Age  
            5. Skin color  
            6. Hairstyle  
            7. Hair color  
            8. Haircut  
            9. Eye color  
            10. Height (use format 'height: feet inches')  
            11. Build  
            12. Attire  
            13. Notable traits  

            Example format:
            Zane Caldwell, Male, White, 35, pale, long, black, layered, blue, height: 6 feet 1 inches, lean, black leather jacket and cargo pants, sharp wit and tactical genius

            **Do not add any extra text, labels, or explanations. Only return the final list of character descriptions in this exact format, one per line, with each character description separated by two newlines (\n\n).**

            Here is the story:
            {story}
            """
 
        while True:
            try:
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=besttext,
                    config=types.GenerateContentConfig(
                        temperature=0.9,
                        #system_instruction='You are an expert proof reader.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)
        
        #result = llm.invoke(text)

        #print(result.content)

        descriptions = result.text.split('\n\n')

        if descriptions and descriptions[-1] == "":
            descriptions.pop()

        print(descriptions)

        # Convert to a list of character descriptions
        formatted_character_descriptions = [self.format_character_description(desc) for desc in descriptions]

        #if we had an error, just return None
        if None in formatted_character_descriptions:
            return None

        print('\n\n\n')
        print(formatted_character_descriptions)

        return formatted_character_descriptions


    def sort_story(self, story)->list:
        #returns story sorted into list
        return story.split('\n\n')
    
    #select the narrators voice for this story
    def select_story_voice(self, story, artstyle):
               
        #create list of voices
        voices = []
        for voice in VOICE_OPTIONS:
            voices.append(voice[0])

        #get results
        text = f'Ill give you a story, art style and you are to pick a narrator for it from an option list. Return the exact descriptiong given. Story : {story}, art style : {artstyle}, option list : {voices}'
        
        while True:
            try:
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=text,
                    config=types.GenerateContentConfig(
                        temperature=0.9,
                        #system_instruction='You are an expert proof reader.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        print(result.text)

        #sometimes it errors out, so if it doesnt select a voice, choose the first for default
        try:
            index = voices.index(result.text.replace('\n',''))
            voice_type = VOICE_OPTIONS[index][1]
            return voice_type
        except ValueError:
            print("Voice not found!")
            return VOICE_OPTIONS[0][1]
    
    #This is a prompt creator for our Flux image creation. Very challenging to get this to always work correctly. Much trial and error put into this.
    def create_image_descriptions_from_story_and_character_item_descriptions(self, story, story_image_descriptions, character_descriptions, item_descriptions, image_number, art_style, token_enabled = True)->list:
        descriptions = []

        if not art_style:
            art_style = "Photorealistic"  # or your default fallback

        #creates flux image prompt for title screen
        prompt_test1 = f"""
        You are an expert prompt engineer for Flux, specializing in generating highly structured, photorealistic image prompts in the **{art_style}** art style.

        Your task is to generate a Flux image prompt summarizing the following story visually. Follow these exact formatting rules:

        **Flux Prompt Structure:**

        1. Start with:  
        **Art Style: {art_style}**

        2. Write a **single continuous paragraph** describing the visual scene. Integrate the following details naturally within the narrative:

        - Select up to **2 characters maximum** from the 'character_descriptions' list by full name.
        - Describe each character’s appearance, pose, action, and exact position in the scene.
        - Paste their **entire multi-sentence description block exactly as written** into the paragraph when introducing them.
        - If a character is holding, interacting with, or wearing any item(s) from 'item_descriptions', integrate those **full item description blocks naturally into their appearance or actions.**
        - Do **not paraphrase or alter** any character or item descriptions. Use them exactly as provided.
        - Ensure the paragraph clearly conveys who is where in the scene, what they’re doing, what they’re wearing or carrying, and how they interact with objects or other characters.
        - Remove each used item from the remaining item list as it’s integrated.

        3. After describing characters and items fully, conclude the paragraph with a vivid but concise **layered background description** that includes:
        - A wide spatial setting, with clear foreground, midground, and background details such as a distant cityscape, skyline, streets, or natural environment to create depth and avoid a zoomed-in or overly tight framing.
        - Atmospheric details like lighting, weather, ambient sounds, scents, and the emotional tone that frame the characters naturally and cohesively.

        **Strict Additional Rules:**

        - Do not use spatial position labels like "(Left Foreground)" — instead, describe positions narratively in the paragraph.
        - Avoid listing or repeating actions and poses separately.
        - Do not include a 'Camera Angle & Mood' section.
        - Do not paraphrase or modify any character or item description blocks.
        - Do not list remaining unused items separately — only include them if naturally present in the scene.

        **Output Example Format:**

        Art Style: {art_style}

        A continuous paragraph describing the characters, their actions, appearance, items, and the environment in rich detail, with layered spatial description ensuring a wide, immersive setting.

        **Here is the input data:**

        Story: {story}

        Character List: {character_descriptions}

        Item List: {item_descriptions}
        """

        while True:
            try:
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    #contents=besttext,
                    contents=prompt_test1,
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        system_instruction='You are an expert at creating text for text to image with FLUX.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        descriptions.append(result.text)

        #will loop through and create all the Flux image prompts for the rest of our story
        for i in range(1,image_number):
            
            # race, age, skin color, hairstyle and color, hair cut, eye color, height (say height : feet inches), build, attire, physical features, and any notable traits

            ## paragraph
            prompt_test1 = f"""
            You are an expert at crafting detailed, structured text-to-image prompts for Flux.

            Your task is to generate a Flux image prompt that visually represents the scene described in the provided paragraph.

            You may reference the full story for broader context regarding setting and character names, but the image prompt must strictly depict what is described within the provided paragraph.
            Follow these exact rules:

            - The image must be created in the **{art_style}** art style.
            - Ensure all visual descriptions — from character design to setting, lighting, and atmosphere — are appropriate to this style.
            - **Your final Flux prompt must begin with `Art Style: {art_style}` before listing any other details.**

            **Flux Prompt Structure:**

            1. Start with:  
            **Art Style: {art_style}**

            2. Write a **single continuous paragraph** describing the visual scene. Integrate the following details naturally within the narrative:

            - Select up to **2 characters maximum** from the 'character_descriptions' list by full name.
            - Describe each character’s appearance, pose, action, and exact position in the scene.
            - Paste their **entire multi-sentence description block exactly as written** into the paragraph when introducing them.
            - If a character is holding, interacting with, or wearing any item(s) from 'item_descriptions', integrate those **full item description blocks naturally into their appearance or actions.**
            - Do **not paraphrase or alter** any character or item descriptions. Use them exactly as provided.
            - Ensure the paragraph clearly conveys who is where in the scene, what they’re doing, what they’re wearing or carrying, and how they interact with objects or other characters.
            - Remove each used item from the remaining item list as it’s integrated.

            3. After describing characters and items fully, conclude the paragraph with a vivid but concise **layered background description** that includes:
            - A wide spatial setting, with clear foreground, midground, and background details such as a distant cityscape, skyline, streets, or natural environment to create depth and avoid a zoomed-in or overly tight framing.
            - Atmospheric details like lighting, weather, ambient sounds, scents, and the emotional tone that frame the characters naturally and cohesively.

            **Strict Additional Rules:**

            - Do not use spatial position labels like "(Left Foreground)" — instead, describe positions narratively in the paragraph.
            - Avoid listing or repeating actions and poses separately.
            - Do not include a 'Camera Angle & Mood' section.
            - Do not paraphrase or modify any character or item description blocks.
            - Do not list remaining unused items separately — only include them if naturally present in the scene.

            **Output Example Format:**

            Art Style: {art_style}

            A continuous paragraph describing the characters, their actions, appearance, items, and the environment in rich detail, with layered spatial description ensuring a wide, immersive setting.

            Here is the input data:

            Story: {story}

            Character Descriptions: {character_descriptions}

            Item Descriptions: {item_descriptions}

            Scene Description (paragraph): {story_image_descriptions[i]}
            """
            

            while True:
                try:
                    result = self.client.models.generate_content(
                        model=GEMINI_MODEL,
                        #contents=besttext,
                        contents=prompt_test1,
                        config=types.GenerateContentConfig(
                            temperature=0.5,
                            system_instruction='You are an expert at creating text for text to image with FLUX.',
                        ),
                    )
                    break
                except Exception as e:
                    print(e)
                    time.sleep(10)


            descriptions.append(result.text)

            #i put sleep in, so we do not go over google geminis limit
            time.sleep(10)

        return descriptions

    #get story art style to use for images  
    def get_story_artstyle(self, story):

        #types of art styles (created by AI)
        art_styles = [
            "Photorealistic, Highly detailed, lifelike images",
            "Digital Painting, Simulates traditional painting techniques using digital tools",
            "3D Render, Creates images with three-dimensional depth and realism",
            "Pencil Sketch, Mimics hand-drawn pencil sketches",
            "Watercolor, Emulates the soft, flowing characteristics of watercolor paintings",
            "Oil Painting, Replicates the rich textures and colors of oil paintings",
            "Pastel Drawing, Captures the soft, vibrant hues typical of pastel artwork",
            "Anime/Manga, Generates images in the style of Japanese animation and comics",
            "Cyberpunk, Features futuristic, neon-lit urban environments",
            "Steampunk, Combines Victorian-era aesthetics with steam-powered machinery",
            "Surrealism, Creates dream-like, fantastical imagery",
            "Fantasy, Depicts mythical creatures and magical settings",
            "Vaporwave, Incorporates retro-futuristic and glitch art elements",
            "Pop Art, Uses bold colors and popular culture references",
            "Minimalist, Focuses on simplicity and clean design",
            "Abstract, Emphasizes shapes, colors, and forms over realistic representation",
            "style of TOK, Flux Half Illustration: Blends photorealism with illustration",
            "r3dcma, Red Cinema: Applies cinematic color grading",
            "GHIBSKY style, Ghibsky: Creates Ghibli-inspired landscapes",
            "style of 80s cyberpunk, 80s Cyberpunk: Generates retro-futuristic scenes",
            "sftsrv style illustration, Softserve Anime: Produces soft, pastel anime visuals"
        ]

        
        #prompt for pick the art style
        text = f"""You are selecting the most visually appropriate art style for illustrating the following story, based on mood, setting, and atmosphere.

        Use the following list of available art styles to choose from:

        {art_styles}

        **Important Rules:**
        - Only choose an art style label from the list provided above.
        - Return **only the style name exactly as it appears before the first comma** in the list.
        - Do not include descriptions, extra words, or explanations.
        - Your response should be a single string containing only the selected art style label.

        **Example:** If selecting "GHIBSKY style, Ghibsky: Creates Ghibli-inspired landscapes", respond only with `GHIBSKY style`.

        **Story:** {story}
        """


        while True:
            try:

                result = self.client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=text,
                        config=types.GenerateContentConfig(
                            temperature=0.9,
                            #system_instruction='You are an expert proof reader.',
                        ),
                    )
                break
            except Exception as e:
                print(e)
                time.sleep(10)
            
        print(result.text)
        return result.text
        
    #selects the types of music for each paragraph. Tries to at least do 2 in a row, so it does not keep switching.
    def get_music_type(self, story, paragraph_amount, music_types):
        text = f'Read the following story : {story} , and list of music types, with their descriptions : {music_types} \n\nI want you to put a type of music that best describes each of the {paragraph_amount} paragraphs. But review them and makes sure that each paragraph type does not switch until the type has stayed for at least 2 consecutive types. Remember to make them consecutive! Only return the list of music types, for each paragraph. Do not number and do not give any other information but the title name of the music type.'
        
        while True:
            try:
                #get results
                result = self.client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=text,
                            config=types.GenerateContentConfig(
                                temperature=0.9,
                                #system_instruction='You are an expert proof reader.',
                            ),
                        )
                break
            except Exception as e:
                print(e)
                time.sleep(10)
        
        #create array of types and remove final one, if its blank
        result_types = result.text.split('\n')

        if result_types[len(result_types)-1] == '':
            result_types.pop()

        #now fix music types
        for m in result_types:
            m = m.replace('*','')
            m = m.replace('#','')
            m = m.replace('”','"')
            m = m.replace('“','"')
            m = m.lstrip()
            m = m.rstrip()

        return result_types
    
    #has AI create text for our video stories introduction
    def get_story_title_intro(self, title_in, story):
        
        #format our title correctly
        title = title_in
        title = title.replace('#','')
        title = title.replace('*','')
        title = title.replace('—','-')
        title = title.replace('’','')
        title = title.replace('–','-')
        title = title.replace('..','')
        title = title.replace('…','.')        
        title = title.replace('”','"')
        title = title.replace('“','"')
        title = title.lstrip()
        title = title.rstrip()

        prompt = f"""You will be provided with a story title and the full story text.

        Write a one-sentence opening line to introduce the story. It must clearly state this is an AI-generated story, include the title, and optionally hint at the tone, genre, or mood of the story — but keep it brief and natural.

        Examples:
        - "Now we present the AI-generated story of {{title}}."
        - "Prepare for the AI-generated sci-fi adventure, {{title}}."
        - "This is the AI-crafted tale of {{title}}, a story of betrayal and courage."

        Guidelines:
        - It must be one sentence.
        - It can hint at the story’s mood, genre, or stakes, but stay under 20 words.
        - Return only the final sentence.
        - No extra explanations, comments, or text before or after.
        - No breaking the one-sentence rule.

        Story title: {title}

        Story text:
        {story}"""



        system_instruction = (
            "You are an expert narrator specializing in creating concise, engaging story introductions. "
            "Always return only the full text of a one-sentence opening line that introduces the provided story title. "
            "Select wording that matches the tone and genre of the story based on its text."
        )

        while True:
            try:
                #get results
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        system_instruction=system_instruction,
                    ),
                )

                break
            except Exception as e:
                print(e)
                time.sleep(10)
    
        text = result.text

        text = text.replace('#','')
        text = text.replace('*','')
        text = text.replace('—','-')
        text = text.replace('’','')
        text = text.replace('–','-')
        text = text.replace('..','')
        text = text.replace('…','.')        
        text = text.replace('”','"')
        text = text.replace('“','"')
        text = text.lstrip()

        return text
    
    #has AI create text for our video stories ending
    def get_story_title_outro(self, title_in, story):
        #format our title correctly
        title = title_in
        title = title.replace('#','')
        title = title.replace('*','')
        title = title.replace('—','-')
        title = title.replace('’','')
        title = title.replace('–','-')
        title = title.replace('..','')
        title = title.replace('…','.')        
        title = title.replace('”','"')
        title = title.replace('“','"')
        title = title.lstrip()
        title = title.rstrip()

        prompt = f"""You will be provided with a story title and the full story text. Write a short, simple closing line to end the story. It should acknowledge the conclusion of the story by name, and remind the viewer to subscribe. Examples include lines like "And that concludes our story of {{title}}. Don't forget to subscribe and tune in again." or "Thanks for joining us for {{title}}. Be sure to hit subscribe for more stories."

        Choose wording that matches the tone and genre of the story based on its text. Keep it casual and friendly. Return only the full text of the closing line, with the title name inserted where appropriate. Do not include any explanations, comments, or additional text.

        Story title: {title}

        Story text:
        {story}"""

        system_instruction = (
            "You are an expert narrator specializing in creating concise, engaging story introductions and conclusions. "
            "Always return only the full text of a one or two-sentence closing line that concludes the story and reminds the viewer to subscribe."
        )


        while True:
            try:
                #get results
                result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        system_instruction=system_instruction,
                    ),
                )

                break
            except Exception as e:
                print(e)
                time.sleep(10)
    
        text = result.text

        text = text.replace('#','')
        text = text.replace('*','')
        text = text.replace('—','-')
        text = text.replace('’','')
        text = text.replace('–','-')
        text = text.replace('..','')
        text = text.replace('…','.')        
        text = text.replace('”','"')
        text = text.replace('“','"')
        text = text.lstrip()

        return text


    #creates the text for our teaser video
    def get_teaser_summary(self, story):
        text = f"""Take this story : {story} ; and create a quick teaser, without spoiling the story, to be used for text to audio. If you put a character in the teaser, you should use their name. End it by creativly telling the viewer, in your own words, the name of the story and to clink the link below to watch the full video to find out. Do not label this and ONLY return the summary."""

        while True:
            try:
                #proof read and then return
                result = self.client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=text,
                            config=types.GenerateContentConfig(
                                system_instruction='You are an expert writer.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        return result.text

    #create flux image prompts for our teaser video
    def get_teaser_summary_image4(self, teaser, character_descriptions, item_descriptions, art_style):
        
        #prompt for teaser image
        besttext = f"""
        You are an expert at crafting text-to-image prompts for Flux.

        First, generate a Flux image prompt that visually represents the provided teaser trailer concept in the following art style: **{art_style}**. The image must vividly reflect the scene’s tone, environment, characters, and any significant items as described, capturing the precise visual mood and narrative moment in this style.
        **Your final Flux prompt should begin with `Art Style: {art_style}` before listing characters, items, and scene details.**

        You may reference the character descriptions from the 'character_descriptions' list to ensure that the characters involved are accurately depicted. Only include characters actively appearing in this specific teaser scene.

        For each included character:
        - Fully describe them using the **entire text description exactly as written in the 'character_descriptions' list**. This includes all sentences and details — do not paraphrase, summarize, or truncate these descriptions in any way.
        - Clearly state the character’s pose, body language, facial expression, action, and any interactions they have within the scene, ensuring these match the mood and role they play in the teaser concept.
        - Ensure that if a character is positioned in a particular way (e.g., standing, sitting, lying down), this is clearly reflected in the description, avoiding any contradictions between height, build, and physical position.
        - If a character is behind another or in any non-standard position (e.g., lying down, hiding), explicitly describe their exact placement relative to the other characters to prevent ambiguity.

        Include any relevant items or props from the 'item_descriptions' list that appear in the teaser scene.  
        - Each included item must be presented using the **entire text description exactly as written in the 'item_descriptions' list**.  
        - Do not paraphrase, summarize, or modify these descriptions in any way.  
        - Place each relevant item description immediately after the character descriptions and before describing character actions and poses.

        Incorporate visual elements from the environment described in the teaser, including architecture, props, lighting, atmosphere, and mood-specific details to create a vivid, contextually appropriate backdrop that enhances the narrative tension or emotion.

        If the teaser concept involves characters who are in distant or contrasting locations (e.g., one in a dark forest, another in a distant castle, or separated by vast landscapes), arrange them in a **left-right split-screen** format. This means:
        - On the left side, depict one character in their relevant position.
        - On the right side, depict the second character in their relevant position.
        - Ensure the two characters are visually separated but maintain a sense of connection through the environment, lighting, or visual effects.

        If the characters are close together in the teaser scene or their positions do not warrant separation, use a **unified layout** where they are in the same frame.

        Once you have generated the image prompt, immediately review it for clarity. Ensure that:
        - The prompt begins with `Art Style: {art_style}`
        - Each character’s description is presented using the **entire text description from the 'character_descriptions' list**, before any actions they perform.
        - Each item’s description is presented using the **entire text description from the 'item_descriptions' list**, before being incorporated into the scene’s visual description.
        - Actions, poses, and positions (e.g., standing, sitting, lying down) are clearly attributed to the correct character, logically matching their physical traits, height, and role within the teaser scene.
        - The scene flows naturally, with no conflicting or awkward visual elements (such as extra limbs, misplaced actions, or ambiguous relationships between characters, items, and their surroundings).
        - The setting, lighting, color palette, and visual tone fully reflect the teaser’s intended mood and narrative.
        - The composition and perspective are logically consistent, enhancing the storytelling impact of the image.

        If any phrasing or structure issues would cause visual confusion, adjust them immediately to improve clarity and sequencing. Do not explain or label your changes — simply return the final, revised Flux image prompt string.

        Here is the input data:

        Teaser Concept: {teaser}

        Character Descriptions: {character_descriptions}

        Item Descriptions: {item_descriptions}
        """


        while True:
            try:
                #proof read and then return
                result = self.client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=besttext,
                            config=types.GenerateContentConfig(
                                temperature=0.5,
                                system_instruction='You are an expert at creating text for text to image with FLUX.',
                    ),
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        return result.text
 
        
        
        text = f"""Take this teaser summary of this story : {teaser} ; and also this list of character descriptions {character_descriptions} ; 
                Now research how Flux text to image works and use the teaser summary and character descriptions, to create a text for text to image on FLUX. 
                Make sure to describe only the character in the teaser summary, in detail of the following : race, gender, age, skin color, hairstyle and color, 
                haircut, eye color, height, build, attire, physical features, and any notable traits and the actions they are taking in this scene. 
                To find their descriptions, search the character descriptions and cross-reference the list using both first and last names. 
                If the character in the character description is not in the teaser summary, then do not put them in the resulting text. 
                You are also to describe the scenes setting of where it is and what is happening there. 
                Only do whats needed to describe the image for text to image for FLUX. 
                Do not tell a story or anything that is not needed for an image. ONLY what is needed for describing a text to image for FLUX. 
                Do not label the results or describe what you are doing. ONLY return the result text!"""
        #proof read and then return
        result = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=text,
                    config=types.GenerateContentConfig(
                        system_instruction='You are an expert at creating text for text to image with FLUX.',
            ),
        )

        return result.text