### imports ###
import requests
import re
import time
import datetime
import json
import time
import requests
import os
import webbrowser
import pyclip
from threading import Thread
from functools import partial
from bs4 import BeautifulSoup
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image, AsyncImage
from StartingScreen import StartingScreen
from AddProfileScreen import AddProfileScreen
from EditProfileScreen import EditProfileScreen
from FavoritesScreen import FavoritesScreen
from BlankScreen import BlankScreen
from StandaloneFunctions import fetch_saved_profiles
from StandaloneFunctions import fetch_saved_favorites
from StandaloneFunctions import year_progress
from StandaloneFunctions import add_profile
from StandaloneFunctions import refreshScreen



### code ###
kivy.require('2.0.0')

#load kv file or string
Builder.load_file("scraperNews.kv")
# Builder.load_string("""""")

#set kivy settings
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #removes right click display red dot
Config.set('graphics', 'resizable', '1') #changing this might break display resolution
Config.set('graphics', 'fullscreen', '0') #changing this might break display resolution
Config.write()
Window.size = (1000, 700) #width, height

#globals
global counterSTP; counterSTP = -1 # saved twitter posts
global counterSYP; counterSYP = -1 # saved youtube posts
global counterSNA; counterSNA = -1 # saved news articles
global counterSSP; counterSSP = -1 # saved subeddit posts
global counterTNS; counterTNS = 1 # total news card

#variables
savedTwitterPosts = []
savedYoutubePosts = []
savedNewsArticles = []
savedSubredditPosts = []



### class ###
class scraperNewsApp(App): #the Base Class of our Kivy App
    def build(self):
        #check if exists
        profiles_exists = os.path.exists('profiles.json')
        favorites_exists = os.path.exists('favorites.json')
        thumbnails_exists = os.path.isdir('thumbnails')

        #set window title
        self.title = "ScraperNews · " + str(year_progress())
        # self.title = "Scraper News - " + str(year_progress())

        if profiles_exists == False:
            #create profiles.json
            file = open('profiles.json', "w")
            file.write("[]")
            file.close()

        if favorites_exists == False:
            #create profiles.json
            file = open('favorites.json', "w")
            file.write("[]")
            file.close()

        if thumbnails_exists == False:
            #create thumbnails
            os.mkdir('thumbnails')
        
        #set screen manager configs
        sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(StartingScreen(name='start'))
        sm.add_widget(AddProfileScreen(name='add'))    
        sm.add_widget(EditProfileScreen(name='edit'))    
        sm.add_widget(FavoritesScreen(name='favorites'))  
        sm.add_widget(BlankScreen(name='blank'))

        return sm



### start app ###
if __name__ == '__main__':
    scraperNewsApp().run()
