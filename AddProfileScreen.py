### imports ###
from kivy.uix.screenmanager import ScreenManager, Screen
from StandaloneFunctions import fetch_saved_profiles
from StandaloneFunctions import add_profile


### class ###
class AddProfileScreen(Screen):
    def __init__(self, **var_args):
        super(AddProfileScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("AddProfileScreen")

        #fetch saved profiles
        savedProfiles = fetch_saved_profiles()

        #set saved profiles count
        totalSavedProfiles = len(savedProfiles)
        
        
    def fetch_profile_inputs(self):
        #variables
        profileName = self.ti1.text
        profileYoutube = self.ti2.text
        profileTwitter = self.ti3.text
        profileArticles = self.ti4.text
        profileSubreddit = self.ti5.text

        #add profile
        add_profile(self, profileName, profileYoutube, profileTwitter, profileArticles, profileSubreddit)

        #clear text inputs
        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""
        self.ti4.text = ""
        self.ti5.text = ""