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
from NewsFeedScreen import NewsFeedScreen
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
#load kv file or string
# Builder.load_file("scraperNews.kv")
Builder.load_string("""
#:kivy 2.0.0
#:import hex kivy.utils.get_color_from_hex

<NewsFeedScreen>:
    bl1: boxLayout1

    GridLayout:
        cols: 2
        rows: 1
        spacing: 1

        ScrollView:
            id: svScrollBar2
            do_scroll_x: False
            do_scroll_y: True
            effect_cls: 'ScrollEffect'
            size_hint_x: None
            width: 100
            
            BoxLayout:
                id: boxLayout1
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: 1

        ScrollView:
            id: svScrollBar
            effect_cls: 'ScrollEffect'

            BoxLayout:
                id: boxLayoutPost
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 2
                padding: 40, 0 # left, top

                Label:
                    id: category1
                    size_hint_y: None
                    size_hint_x: None
                    height: 80
                    width: 730
                    text: ""
                    disabled: False
                    opacity: 1
                    halign: 'left'
                    color: "white"
                    bold: True,
                    opacity: 1
                    font_size: 21

                BoxLayout:
                    id: boxLayoutNewsCard1
                    orientation: 'horizontal'
                    size_hint_y: None
                    size_hint_x: None
                    height: self.minimum_height
                    width: 730
                    spacing: 0
                    padding: 0
                    opacity: 0
                    disabled: False
                    
                    Button:
                        id: buttonCopyLink1
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: "§"
                        background_color: hex('#0e1012') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        on_touch_down: root.copyToClipboard(newsCard1Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 16 
                    Button:
                        id: newsCard1Post
                        size_hint_y: None
                        size_hint_x: None
                        text: ""
                        padding: 10, 20 #left, top
                        text_size: self.width, None #width, height
                        height: self.texture_size[1]
                        width: 730
                        multiline: True
                        disabled: False
                        halign:'left'
                        valign: 'top'
                        color: 'white'
                        opacity: 1
                        font_size: 17
                        disabled: False
                        bold: True
                        on_touch_down: root.nextPost(newsCard1Post.order, newsCard1Post.type) if self.collide_point(*args[1].pos) else False
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        # height: self.texture_size[1]
                        # text_size: self.width, None
                        # size: self.texture_size
                    Button:
                        id: buttonAddToFavs1
                        size_hint_y: 1
                        size_hint_x: None
                        # height: 100
                        width: 46
                        text: "+"
                        background_color: hex('#0e1012') # "green" # "#292f33"
                        background_normal: "transparent" # "#292f33"
                        background_down: "transparent" # "#292f33"
                        disabled: False
                        opacity: 1 
                        on_touch_down: root.saveToFavorites(self, newsCard1Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 19

                Label:
                    id: category2
                    size_hint_y: None
                    size_hint_x: None
                    height: 1
                    width: 730
                    text: ""
                    disabled: False
                    opacity: 1
                    halign: 'center'
                    color: "white"
                    bold: True,
                    opacity: 0.9
                    font_size: 16

                BoxLayout:
                    id: boxLayoutNewsCard2
                    orientation: 'horizontal'
                    size_hint_y: None
                    size_hint_x: None
                    height: self.minimum_height
                    width: 730
                    spacing: 0
                    padding: 0
                    opacity: 0
                    disabled: False
                    
                    Button:
                        id: buttonCopyLink2
                        size_hint_y: 1
                        size_hint_x: None
                        height: 40
                        width: 40
                        text: "§"
                        background_color: hex('#0e1012') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        on_touch_down: root.copyToClipboard(newsCard2Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 16
                    Button:
                        id: newsCard2Post
                        size_hint_y: None
                        size_hint_x: None
                        text: ""
                        padding: 10, 20 #left, top
                        # text_size: 660, 240 #width, height
                        # height: 240
                        text_size: self.width, None #width, height
                        height: self.texture_size[1]
                        width: 730
                        multiline: True
                        disabled: False
                        halign:'left'
                        valign: 'top'
                        color: 'white'
                        opacity: 1
                        font_size: 17
                        disabled: False
                        bold: True
                        on_touch_down: root.nextPost(newsCard2Post.order, newsCard2Post.type) if self.collide_point(*args[1].pos) else False
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        # height: self.texture_size[1]
                        # size: self.texture_size
                        # text_size: self.width, None
                        # background_color: '#1DA1F2' # 292f33
                    Button:
                        id: buttonAddToFavs2
                        size_hint_y: 1
                        size_hint_x: None
                        # height: 40
                        width: 46
                        text: "+"
                        background_color: hex('#0e1012') # "green" # "#292f33"
                        background_normal: "transparent" # "#292f33"
                        background_down: "transparent" # "#292f33"
                        disabled: False
                        opacity: 1 
                        on_touch_down: root.saveToFavorites(self, newsCard2Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 19

                Label:
                    id: category3
                    size_hint_y: None
                    size_hint_x: None
                    height: 1
                    width: 730
                    text: ""
                    disabled: False
                    opacity: 1
                    halign: 'center'
                    color: "white"
                    bold: True,
                    opacity: 1
                    font_size: 16

                BoxLayout:
                    id: boxLayoutNewsCard3
                    orientation: 'horizontal'
                    size_hint_y: None
                    size_hint_x: None
                    height: self.minimum_height
                    width: 730
                    spacing: 0
                    padding: 0
                    opacity: 0
                    disabled: False
                                        
                    Button:
                        id: buttonCopyLink3
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: "§"
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        on_touch_down: root.copyToClipboard(newsCard3Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 16
                    Button:
                        id: newsCard3Post
                        size_hint_y: None
                        size_hint_x: None
                        text: ""
                        padding: 10, 20 #left, top
                        # text_size: 660, 240 #width, height
                        # height: 240
                        text_size: self.width, None #width, height
                        height: self.texture_size[1]
                        width: 730
                        multiline: True
                        disabled: False
                        halign:'left'
                        valign: 'top'
                        color: 'white'
                        opacity: 1
                        font_size: 17
                        disabled: False
                        bold: True
                        on_touch_down: root.nextPost(newsCard3Post.order, newsCard3Post.type) if self.collide_point(*args[1].pos) else False
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        # height: self.texture_size[1]
                        # size: self.texture_size
                        # text_size: self.width, None
                        # background_color: '#1DA1F2' # 292f33
                    Button:
                        id: buttonAddToFavs3
                        size_hint_y: 1
                        size_hint_x: None
                        # height: 40
                        width: 46
                        text: "+"
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1 
                        on_touch_down: root.saveToFavorites(self, newsCard3Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 19

                Label:
                    id: category4
                    size_hint_y: None
                    size_hint_x: None
                    height: 1
                    width: 730
                    text: ""
                    disabled: False
                    opacity: 1
                    halign: 'center'
                    color: "white"
                    bold: True,
                    opacity: 1
                    font_size: 16

                BoxLayout:
                    id: boxLayoutNewsCard4
                    orientation: 'horizontal'
                    size_hint_y: None
                    size_hint_x: None
                    height: self.minimum_height
                    width: 730
                    spacing: 0
                    padding: 0
                    opacity: 0
                    disabled: False

                    Button:
                        id: buttonCopyLink4
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: "§"
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        on_touch_down: root.copyToClipboard(newsCard4Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 16
                    Button:
                        id: newsCard4Post
                        size_hint_y: None
                        size_hint_x: None
                        text: ""
                        padding: 10, 20 #left, top
                        # text_size: 660, 240 #width, height
                        # height: 240
                        text_size: self.width, None #width, height
                        height: self.texture_size[1]
                        width: 730
                        multiline: True
                        disabled: False
                        halign:'left'
                        valign: 'top'
                        color: 'white'
                        opacity: 1
                        font_size: 17
                        disabled: False
                        bold: True
                        on_touch_down: root.nextPost(newsCard4Post.order, newsCard4Post.type) if self.collide_point(*args[1].pos) else False
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        # height: self.texture_size[1]
                        # size: self.texture_size
                        # text_size: self.width, None
                        # background_color: '#1DA1F2' # 292f33
                    Button:
                        id: buttonAddToFavs4
                        size_hint_y: 1
                        size_hint_x: None
                        # height: 40
                        width: 46
                        text: "+"
                        background_color: hex('#0e1012')
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1 
                        on_touch_down: root.saveToFavorites(self, newsCard4Post.type) if self.collide_point(*args[1].pos) else False
                        valign: 'top'
                        color: "white"
                        bold: False
                        font_size: 19

                Label:
                    id: category5
                    size_hint_y: None
                    size_hint_x: None
                    height: 49
                    width: 730
                    text: ""
                    disabled: True
                    opacity: 1
                    halign: 'center'
                    color: "white"
                    bold: False,
                    opacity: 1
                    font_size: 16

<AddProfileScreen>:
    bl1: boxLayout1
    ti1: profileName
    ti2: profileYoutube
    ti3: profileTwitter
    ti4: profileArticles
    ti5: profileSubreddit
    
    GridLayout:
        cols: 2
        rows: 1

        ScrollView:
            id: svScrollBar2
            do_scroll_x: False
            do_scroll_y: True
            effect_cls: 'ScrollEffect'
            size_hint_x: None
            width: 100

            BoxLayout:
                id: boxLayout1
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                
                Button:
                    size_hint_y: None
                    text: "<"
                    on_press: root.manager.current = 'start'
                    font_size: 40
                    disabled: False
                    background_color: "black"

        StackLayout:
            id: testStackLayout1
            size_hint_y: 1
            size_hint_x: 1
            
            Label:
                size_hint_y: None
                size_hint_x: 1
                height: 40
                text: "Custom Profile"
                bold: True
            TextInput:
                id: profileName
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "desired profile name"
                halign: "center"
                multiline: False
                write_tab: False
            TextInput:
                id: profileYoutube
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "youtube channel name"
                halign: "center"
                multiline: False
                write_tab: False
            TextInput:
                id: profileTwitter
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "twitter username"
                halign: "center"
                multiline: False
                write_tab: False
            TextInput:
                id: profileArticles
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "search phrase for news articles"
                halign: "center"
                multiline: False
                write_tab: False
            TextInput:
                id: profileSubreddit
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "subreddit name"
                halign: "center"
                multiline: False
                write_tab: False
            Button:
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                text: "Add"
                background_color: 'green'
                background_normal: 'transparent'
                background_down: 'transparent'
                on_press: root.fetch_profile_inputs()

<EditProfileScreen>:
    bl1: boxLayout1
    bl2: boxLayout2
    st1: testStackLayout1
    ti1: profileName
    
    GridLayout:
        cols: 2
        rows: 1

        ScrollView:
            id: svScrollBar1
            do_scroll_x: False
            do_scroll_y: True
            effect_cls: 'ScrollEffect'
            size_hint_x: None
            width: 100

            BoxLayout:
                id: boxLayout1
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

                Button:
                    size_hint_y: None
                    text: "<"
                    on_press: root.manager.current = 'start'
                    font_size: 40
                    disabled: False
                    background_color: "black"

        StackLayout:
            id: testStackLayout1
            size_hint_y: 1
            size_hint_x: 1

            Label:
                id: labelTotalSavedProfiles
                size_hint_y: None
                size_hint_x: 1
                height: 40
                text: "0 Saved Profiles"
                bold: True
            TextInput:
                id: profileName
                size_hint_y: None
                size_hint_x: 1
                height: 40
                font_size: 20
                hint_text: "select profile"
                halign: "center"
                disabled: True,
                multiline: False
                write_tab: False

            # Label:
            #     size_hint_y: None
            #     size_hint_x: 1
            #     height: 40
            #     text: "All Profiles"

            ScrollView:
                id: svScrollBar2
                do_scroll_x: False
                do_scroll_y: True
                effect_cls: 'ScrollEffect'
                size_hint_y: None
                size_hint_x: 1
                height: 580 # 440 + 80

                BoxLayout:
                    id: boxLayout2
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height

            Button:
                size_hint_y: None
                size_hint_x: 1
                height: 40
                background_color: 'red'
                background_normal: 'transparent'
                background_down: 'transparent'
                text: "Remove"
                on_press: root.DeleteProfile()

<FavoritesScreen>:
    bl1: boxLayout1
    
    GridLayout:
        cols: 2
        rows: 1

        ScrollView:
            id: svScrollBar2
            do_scroll_x: False
            do_scroll_y: True
            effect_cls: 'ScrollEffect'
            size_hint_x: None
            width: 100

            BoxLayout:
                id: boxLayout1
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                Button:
                    size_hint_y: None
                    text: "<"
                    on_press: root.manager.current = 'start'
                    font_size: 40
                    disabled: False
                    background_color: "black"
        
        ScrollView:
            id: svScrollBar
            effect_cls: 'ScrollEffect'
            
            BoxLayout:
                id: boxLayoutPost
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
                padding: 10

<BlankScreen>:
""")

#set kivy settings
kivy.require('2.0.0')
# Config.set('kivy','window_icon', 'icon.png')
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #removes right click display red dot
# Config.set('graphics', 'resizable', '1') #changing this might break display resolution
#  Config.set('graphics', 'fullscreen', '0') #changing this might break display resolution
# Config.write()
Window.set_icon("logo.ico") # Window.set_icon("icon.png")
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
        sm.add_widget(NewsFeedScreen(name='start'))
        sm.add_widget(AddProfileScreen(name='add'))    
        sm.add_widget(EditProfileScreen(name='edit'))    
        sm.add_widget(FavoritesScreen(name='favorites'))  
        sm.add_widget(BlankScreen(name='blank'))

        return sm



### start app ###
if __name__ == '__main__':
    scraperNewsApp().run()
