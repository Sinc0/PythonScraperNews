import json
import os

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

# from StandaloneFunctions import fetch_news_feed
from StandaloneFunctions import fetch_saved_profiles
# from StandaloneFunctions import fetch_saved_favorites
# from StandaloneFunctions import fetch_profile_image
# from StandaloneFunctions import fetch_twitter_profile
# from StandaloneFunctions import fetch_news_articles
# from StandaloneFunctions import fetch_youtube_channel
# from StandaloneFunctions import fetch_subreddit
# from StandaloneFunctions import displayNewsCard
# from StandaloneFunctions import undisplayNewsCard
# from StandaloneFunctions import nitterFilterPost
# from StandaloneFunctions import year_progress
# from StandaloneFunctions import add_profile
# from StandaloneFunctions import changeScreen
from StandaloneFunctions import refreshScreen

class EditProfileScreen(Screen):
    def __init__(self, **var_args):
        super(EditProfileScreen, self).__init__(**var_args)
        

    def on_pre_enter(self, *args):
        print("EditProfileScreen")

        #clear saved profile list
        self.ids.testBoxLayout2.clear_widgets()
        
        #fetch saved profiles
        savedProfiles = fetch_saved_profiles()

        #set saved profiles count
        totalSavedProfiles = len(savedProfiles)

        #set layout buttons count
        totalButtons = len(self.ids.testBoxLayout2.children)

        #add saved profiles buttons
        if totalButtons != totalSavedProfiles:
            #clear widgets
            self.ids.testBoxLayout2.clear_widgets()

            #add buttons
            for x in range(totalSavedProfiles):
                reverseListCount = (totalSavedProfiles - 1) - x # reverse list to make latest added on top
                EditProfileScreen.AddProfileButtons(self, savedProfiles[reverseListCount])

            #set total saved profiles
            self.ids.labelTotalSavedProfiles.text = str(totalSavedProfiles) + " Saved Profiles"
        
        #fill side panel with filler buttons
        # for x in range(6):
        #     StartingScreen.AddFillerButtons(self)


    def AddProfileButtons(self, profile):
        #create button
        newButton = Button(
            size_hint_y = None,
            height = 40,
            text = profile['name']
        )

        #add functions to buttons
        newButton.bind(on_press=lambda *args: EditProfileScreen.FillTextInputWithData(self, profile))

        #add button layout
        self.ids.testBoxLayout2.add_widget(newButton)


    def DeleteProfile(self):
        #variables
        name = self.ti1.text
        
        #fetch saved profiles
        profiles = fetch_saved_profiles()

        #remove saved profile from list
        count = 0
        for p in profiles:
            if p['name'] == name: profiles.pop(count)
            count += 1

        #remove profile from profiles.json
        out_file = open("profiles.json", "w")
        json.dump(profiles, out_file, indent = 6)
        out_file.close()

        #fetch saved profiles thumbnails
        thumbnails = os.listdir(os.getcwd() + '/thumbnails')

        #remove saved profile thumbnail file
        # for image in thumbnails:
        #     imageFile = os.getcwd() + '/thumbnails' + '/' + image
        #     if name in image:
        #         try: os.remove(imageFile)
        #         except: print("delete thumbnail " + name + " failed")

        #clear text inputs
        self.ti1.text = ""

        #refresh edit screen
        refreshScreen(self, 'edit')


    def FillTextInputWithData(self, profile):
        self.ti1.text = profile['name']