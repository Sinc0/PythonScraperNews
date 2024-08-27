#------ IMPORTS ------#
import requests
import re
import datetime
import json
import os
import pyclip
import kivy
import emoji
import time
import sys
import webbrowser
from threading import Thread
from functools import partial
from bs4 import BeautifulSoup
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


#------ LOAD KIVY UI ------#
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
                        id: buttonLeftSideFiller1
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: ""
                        # background_color: hex('#1DA1F2') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
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
                    
                    BoxLayout:
                        id: boxLayoutVerticalRightSide1
                        orientation: 'vertical'
                        # size_hint_y: None
                        # size_hint_x: None
                        # height: self.minimum_height
                        # width: 730
                        # spacing: 0
                        # padding: 0
                        # opacity: 0
                        disabled: False
                        
                        Button:
                            id: buttonAddToFavs1
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
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
                        Button:
                            id: buttonCopyLink1
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
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
                        id: buttonLeftSideFiller2
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: ""
                        # background_color: hex('#1DA1F2') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        valign: 'top'
                        color: "white"
                        bold: False
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
                    
                    BoxLayout:
                        id: boxLayoutVerticalRightSide2
                        orientation: 'vertical'
                        # size_hint_y: None
                        # size_hint_x: None
                        # height: self.minimum_height
                        # width: 730
                        # spacing: 0
                        # padding: 0
                        # opacity: 0
                        disabled: False
                        
                        Button:
                            id: buttonAddToFavs2
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
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
                        Button:
                            id: buttonCopyLink2
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
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
                        id: buttonLeftSideFiller3
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: ""
                        # background_color: hex('#1DA1F2') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        valign: 'top'
                        color: "white"
                        bold: False
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
                    
                    BoxLayout:
                        id: boxLayoutVerticalRightSide3
                        orientation: 'vertical'
                        # size_hint_y: None
                        # size_hint_x: None
                        # height: self.minimum_height
                        # width: 730
                        # spacing: 0
                        # padding: 0
                        # opacity: 0
                        disabled: False
                        
                        Button:
                            id: buttonAddToFavs3
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
                            text: "+"
                            background_color: hex('#0e1012') # "green" # "#292f33"
                            background_normal: "transparent" # "#292f33"
                            background_down: "transparent" # "#292f33"
                            disabled: False
                            opacity: 1 
                            on_touch_down: root.saveToFavorites(self, newsCard3Post.type) if self.collide_point(*args[1].pos) else False
                            valign: 'top'
                            color: "white"
                            bold: False
                            font_size: 19
                        Button:
                            id: buttonCopyLink3
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
                            text: "§"
                            background_color: hex('#0e1012') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                            background_normal: "transparent"
                            background_down: "transparent"
                            disabled: False
                            opacity: 1
                            on_touch_down: root.copyToClipboard(newsCard3Post.type) if self.collide_point(*args[1].pos) else False
                            valign: 'top'
                            color: "white"
                            bold: False
                            font_size: 16 

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
                        id: buttonLeftSideFiller4
                        size_hint_y: 1
                        size_hint_x: None
                        height: 100
                        width: 40
                        text: ""
                        # background_color: hex('#1DA1F2') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                        background_normal: "transparent"
                        background_down: "transparent"
                        disabled: False
                        opacity: 1
                        valign: 'top'
                        color: "white"
                        bold: False
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
                    
                    BoxLayout:
                        id: boxLayoutVerticalRightSide4
                        orientation: 'vertical'
                        # size_hint_y: None
                        # size_hint_x: None
                        # height: self.minimum_height
                        # width: 730
                        # spacing: 0
                        # padding: 0
                        # opacity: 0
                        disabled: False
                        
                        Button:
                            id: buttonAddToFavs4
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
                            text: "+"
                            background_color: hex('#0e1012') # "green" # "#292f33"
                            background_normal: "transparent" # "#292f33"
                            background_down: "transparent" # "#292f33"
                            disabled: False
                            opacity: 1 
                            on_touch_down: root.saveToFavorites(self, newsCard4Post.type) if self.collide_point(*args[1].pos) else False
                            valign: 'top'
                            color: "white"
                            bold: False
                            font_size: 19
                        Button:
                            id: buttonCopyLink4
                            size_hint_y: 1
                            size_hint_x: None
                            height: 100
                            width: 46
                            text: "§"
                            background_color: hex('#0e1012') # "white" # hex('#1DA1F2') # "darkgray" # "#292f33"
                            background_normal: "transparent"
                            background_down: "transparent"
                            disabled: False
                            opacity: 1
                            on_touch_down: root.copyToClipboard(newsCard4Post.type) if self.collide_point(*args[1].pos) else False
                            valign: 'top'
                            color: "white"
                            bold: False
                            font_size: 16 

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
            
            Button:
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                text: "Add Profile"
                background_color: 'green'
                background_normal: 'transparent'
                background_down: 'transparent'
                on_press: root.fetch_profile_inputs()
            TextInput:
                id: profileName
                size_hint_y: None
                size_hint_x: 1
                height: 40
                # width: 730
                font_size: 20
                hint_text: "profile name..."
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
                hint_text: "youtube channel name..."
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
                hint_text: "X username..."
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
                hint_text: "articles search phrase..."
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
                hint_text: "subreddit name..."
                halign: "center"
                multiline: False
                write_tab: False

<RemoveProfileScreen>:
    bl1: boxLayout1
    bl2: boxLayout2
    st1: testStackLayout1
    ti1: profileName
    btnRemoveProfile: removeProfileButton
    
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

            TextInput:
                id: profileName
                size_hint_y: None
                size_hint_x: None
                height: 0
                font_size: 0
                hint_text: "Select Profile"
                halign: "center"
                disabled: True,
                multiline: False
                write_tab: False
            Button:
                id: removeProfileButton
                size_hint_y: None
                size_hint_x: 1
                height: 40
                background_color: 'red'
                background_normal: 'transparent'
                background_down: 'transparent'
                text: "Remove Profile"
                on_press: root.DeleteProfile()

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
# Builder.load_file("ScraperNews.kv")


#------ GLOBALS ------#
global COUNTER_SAVED_X_POSTS; COUNTER_SAVED_X_POSTS = -1 # saved twitter posts
global counterSYP; counterSYP = -1 # saved youtube posts
global counterSNA; counterSNA = -1 # saved news articles
global counterSSP; counterSSP = -1 # saved subeddit posts
global counterTNS; counterTNS = 1 # total news card
global articlesLimit; articlesLimit = 10
global videosLimit; videosLimit = 10
global tweetsLimit; tweetsLimit = 10
global subredditPostsLimit; subredditPostsLimit = 10
savedTwitterPosts = []
savedYoutubePosts = []
savedNewsArticles = []
savedSubredditPosts = []
twitterDomain = "https://nitter.lucabased.xyz"
redditDomain = "https://libreddit.privacydev.net"
youtubeDomain = "https://invidious.privacydev.net"
articlesDomain = "https://search.brave.com/news"
profilePicDomain = "https://duckduckgo.com/?hps=1"


#------ FUNCTIONS ------#
def year_progress():
    
    #variables
    JAN = 31
    FEB = JAN + 28
    MAR = FEB + 31
    APR = MAR + 30
    MAY = APR + 31
    JUN = MAY + 30
    JUL = JUN + 31
    AUG = JUL + 31
    SEP = AUG + 30
    OCT = SEP + 31
    NOV = OCT + 30
    DEC = NOV + 31
    totalDaysThisYear = 365

    #set current dates
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    #check if leap year
    if year == 2024: totalDaysThisYear = 366
    
    #set month name
    if month == 1: month = "Jan"; dayOfTheYear = day
    elif month == 2: month = "Feb"; dayOfTheYear = JAN + day
    elif month == 3: month = "Mar"; dayOfTheYear = FEB + day 
    elif month == 4: month = "Apr"; dayOfTheYear = MAR + day
    elif month == 5: month = "May"; dayOfTheYear = APR + day
    elif month == 6: month = "Jun"; dayOfTheYear = MAY + day
    elif month == 7: month = "Jul"; dayOfTheYear = JUN + day
    elif month == 8: month = "Aug"; dayOfTheYear = JUL + day
    elif month == 9: month = "Sep"; dayOfTheYear = AUG + day
    elif month == 10: month = "Oct"; dayOfTheYear = SEP + day
    elif month == 11: month = "Nov"; dayOfTheYear = OCT + day 
    elif month == 12: month = "Dec"; dayOfTheYear = NOV + day 
            
    #set formatted date
    formattedDate = formattedDate = str(day) + " " + str(month) + " " + str(year) + "\n" + "Day " + str(dayOfTheYear) + "/" + str(totalDaysThisYear)
    # formattedDate = formattedDate = str(day) + " " + str(month) + " " + str(year) + " · " + "Day " + str(dayOfTheYear) + "/" + str(totalDaysThisYear)
    # formattedDate = formattedDate = str(day) + " " + str(month) + " " + str(year)
    # formattedDate = str(month) + " " + str(day) + " " + str(year) + " · " + str(dayOfTheYear) + "/" + str(totalDaysThisYear)
    
    return formattedDate


def add_profile(self, name, youtube = None, twitter = None, articles = None, subreddit = None):
    
    #variables
    profiles = []
    totalProfiles = 0
    youtubeChannelName = youtube

    #load profiles.json
    try: 
        #variables
        profiles = json.load(open('profiles.json', "r"))
        totalProfiles = len(profiles)
        
        #name is taken
        for p in profiles:
            if p['name'] == name: print("profile name already taken"); return

        #name is null
        if name == "": print("profile name empty"); return
    
    #create profiles.json
    except: 
        file = open('profiles.json', "w")
        file.close()

    #youtube url check
    if youtube == "": print("profiles youtube channel is null")
    else: youtube = youtubeChannelName
    
    #fetch profile image
    # fetch_profile_image(name)

    #create profile obj
    newProfile = {
        "id": totalProfiles + 1, 
        "name": name, 
        "youtube": youtube, 
        "twitter": twitter, 
        "articles": articles, 
        "subreddit": subreddit
    }

    #add profile to profiles.json
    profiles.append(newProfile)
    out_file = open("profiles.json", "w")
    json.dump(profiles, out_file, indent = 6)
    out_file.close()


def fetch_saved_profiles():
    profiles = json.load(open('profiles.json', "r"))
    return profiles


def fetch_saved_favorites():
    favorites = json.load(open('favorites.json', "r"))
    return favorites


def fetch_profile_image(name):
    print("fetch profile image: " + name)

    # response = requests.get(profilePicDomain + "&q=joe+rogan&iax=images&ia=images&iaf=size%3AMedium")
    # requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    # "https://duckduckgo.com/i.js?l=us-en&o=json&q=joe%20rogan&vqd=4-167741814490060066453589839091229850154&f=,,,,,&p=1"
    # url = "https://duckduckgo.com/i.js"
    # PARAMS = {'l': 'us-en','o': 'json','q': 'joe%20rogan',
    # 'vqd': '3-160127109499719016074744569811997028386-179481262599639828155814625357171050706&f=,,,',
    # }
    
    try:
        response = requests.get("https://duckduckgo.com/i.js?l=us-en&o=json&q=" + name + "&vqd=4-167741814490060066453589839091229850154&f=,,,,layout:Square,&p=1", timeout=10)
        print(response.status_code)

        #handle search query results
        if response.status_code == 200:
            
            #regex search result images
            # regexImages = re.findall(r'src="http\S*;s', response.text)
            regexImages = re.findall(r',"image":"https://.[\w\d./-]*","image_token"', response.text)
            formatedUrlsArray = []

            counter = 0
            for imgUrl in regexImages:
                counter += 1
                formatedUrl = imgUrl.replace(',"image":"', "").replace('","image_token"', "")
                formatedUrlsArray.append(formatedUrl)
                print(str(counter) + ": " + formatedUrl)
            
            for item in formatedUrlsArray:
                responseSelectedImage = requests.get(item, timeout=10)
            
                #create image file
                if responseSelectedImage == 200:
                    file = open(os.getcwd() + '/thumbnails/' + name + '.jpg','wb')
                    file.write(response.content)
                    file.close()
                    return True

    #fetch profile image error
    except:
        print("error: profile image fetch failed")
        return False


def changeScreen(self, type):
    if type == "add": self.manager.current = 'add'
    elif type == "edit": self.manager.current = 'edit'
    elif type == "start": self.manager.current = 'start'
    elif type == "favorites": self.manager.current = 'favorites'
    elif type == "menu": self.manager.current = 'menu'


def refreshScreen(self, screenName):
    self.manager.current = 'blank' #change to blank screen
    self.manager.current = screenName #change back to previous screen


def newsTextCleaner(self, type, text):
    if type == "twitter":
        text = text.replace("\\u2066", "").replace("\\u2069", "")
        regexCleaning = re.findall(r'<a href=".*', text)
        if len(regexCleaning) != 0: 
            removeFromText = str(regexCleaning[0])
            text = text.replace(removeFromText, "")
            tags = re.findall(r'@[\w\d]*</a>.[^<]*', removeFromText)
            if len(tags) != 0:
                text = text + tags[0]
            links = re.findall(r'<a href="[^\"\/][\w\d\s.\/?=\-_#!:]*', removeFromText)
            if len(links) != 0:
                text = text + links[0]
            text = text.replace("www.", "")
            text = text.replace("a href=", "")
            text = text.replace("</a>", "")
            text = text.replace("<\"", "")
            text = text.replace("//", "/")
            text = text.replace("  ", " ")
            text = text.replace("https://", "")
            text = text.replace("https:/", "")
            text = text.replace("http://", "")
            text = text.replace("http:/", "")
            text = text.replace("&amp;", "")
        return text   


def fetch_news_feed(profile, self):
    
    #variables
    global counterTNS
    counterTNS = 0
    name = profile['name']
    twitter = profile['twitter']
    youtube = profile['youtube']
    youtube = str(youtube)
    youtube = youtube.replace("https://www.youtube.com/", "").replace("youtube.com", "").replace("/videos", "")
    articles = profile['articles']
    subreddit = profile['subreddit']
    file = open('profiles.json', "r")
    profiles = json.load(file)
    totalProfiles = len(profiles)

    #update UI: reset news card text
    self.ids.newsCard1Post.text = ""
    self.ids.newsCard2Post.text = ""
    self.ids.newsCard3Post.text = ""
    self.ids.newsCard4Post.text = ""

    #update UI: undisplay news card
    Thread(target=lambda : undisplayNewsCard(self, 1)).start()
    Thread(target=lambda : undisplayNewsCard(self, 2)).start()
    Thread(target=lambda : undisplayNewsCard(self, 3)).start()
    Thread(target=lambda : undisplayNewsCard(self, 4)).start()

    #fetch profile news
    for profile in profiles:
        if profile['name'] == name:

            #log 
            print("fetch profile news: " + name)

            #fetch profile news
            if profile['articles'] != "": counterTNS += 1; self.ids.category1.text = "loading Articles..."; fetch_news_articles(self, articles, profile) #ARTICLES
            if profile['youtube'] != "": counterTNS += 1; self.ids.category1.text = "Loading YouTube..."; fetch_youtube_channel(self, profile) #YOUTUBE
            if profile['twitter'] != "": counterTNS += 1; self.ids.category1.text = "Loading Twitter..."; fetch_twitter_profile(self, profile['twitter'], profile) #TWITTER
            if profile['subreddit'] != "": counterTNS += 1; self.ids.category1.text = "Loading Subreddit..."; fetch_subreddit(self, subreddit, profile) #REDDIT

            #update UI: set profile name
            self.ids.category1.text = name.upper()


def fetch_news_articles(self, name, profile):
    
    try:
        #variables
        global counterSNA
        global savedNewsArticles
        global articlesLimit
        counterSNA = -1
        totalNewsArticles = 0
        totalNewsLinks = 0
        savedNewsArticles = []
        newsArticleObjects = []
        
        #request news articles
        httpRequest = requests.get(articlesDomain + "?q=" + name, timeout=10)
        print(httpRequest.status_code)
        # print(httpRequest.content)
        
        #regex articles data
        regexNewsTitles = re.findall(r'line-clamp-2  heading-serpresult">[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”|]*</span></a>', httpRequest.text)
        regexNewsLinks = re.findall(r'<a href="[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”|]*<span class="snippet-title', httpRequest.text)
        regexNewsDate = re.findall(r' <span class="attr">[\w\d\s]*</span> </cite>', httpRequest.text)
        regexNewsPublisher = re.findall(r'>[\w\d\s.]*</span></div> <span class="attr', httpRequest.text)
        totalNewsArticles = len(regexNewsTitles)
        totalNewsLinks = len(regexNewsLinks)
        
        #debugging
        print("totalNewsArticles: " + str(totalNewsArticles))
        print("regexNewsLinks: " + str(totalNewsLinks))

        #add news articles objects
        counter = 0
        for item in regexNewsTitles:
            counter += 1
            title = item.replace('line-clamp-2  heading-serpresult">', "").replace("</span>" , "").replace("</a>", "").replace("&amp;", "&")
            link = regexNewsLinks[counter - 1].split("class=\"")[0].replace('<a href="', "").replace("\"", "")
            date = regexNewsDate[counter - 1].replace(' <span class="attr">', "").replace("</span> </cite>", "")
            publisher = regexNewsPublisher[counter - 1].replace("</span></div> <span class=\"attr", "").replace(">", "")
            newsArticleObjects.append({"id": str(counter), "date": date, "publisher": publisher, "title": str(title), "link": link})

        #debugging
        # for item in newsArticleObjects[0:10]:
        #     print(item)

        #articles null check
        if totalNewsArticles == 0:
            print("0 articles found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, "articles", "null")).start()
            return
        
        #articles exists
        elif totalNewsArticles > 0:
            
            if totalNewsArticles < 10: articlesLimit = totalNewsArticles

            #add post obj
            for article in newsArticleObjects[0:articlesLimit]:
                post = {
                    "id": article['id'],
                    "title": article['title'],
                    "link": article['link'],
                    "date": article['date'],
                    "publisher": article['publisher'],
                    "type": "article",
                    "profile": profile['name']
                }
                savedNewsArticles.append(post)

            #increment counter
            counterSNA = -1

            #update UI  
            Thread(target=lambda : displayNewsCard(self, counterTNS, "article", None)).start()

    except Exception as e:
        print(e); print("fetch news articles failed")
        Thread(target=lambda : displayNewsCard(self, counterTNS, "articles", "null")).start()
        return


def fetch_youtube_channel(self, profile):
    
    try:
        #variables
        global savedYoutubePosts
        global counterSYP
        global counterTNS
        global videosLimit
        savedYoutubePosts = []
        channelVideoObjects = []
        counterSYP = -1
        totalYoutubeVideos = 0
        name = profile['name']
        youtubeName = profile['youtube']

        #fetch channel id/videos
        httpRequest1 = requests.get(youtubeDomain + "/search?q=" + youtubeName + "&type=channel", timeout=10)
        regexChannelName = re.findall(r'<a href="/channel/[\w\d._-]*">', httpRequest1.text)
        youtubeChannelId = regexChannelName[0].replace('<a href=\"/channel/', "").replace('">', "")

        #fetch channel videos
        httpRequest2 = requests.get(youtubeDomain + "/channel/" + youtubeChannelId)
        regexChannelVideos = re.findall(r'<a href="/watch\?v=[\w\d_-]*"><p dir="auto">[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\']*</p></a>', str(httpRequest2.content))
        regexChannelVideoUploadDates = re.findall(r'<p class="video-data" dir="auto">Shared[\w\d\s]*</p>', str(httpRequest2.content))
        regexChannelVideoDurations = re.findall(r'<p class="length">[\d:]*</p>', str(httpRequest2.content))
        
        #regex channel video data
        counter = 0
        for v in regexChannelVideos:
            counter += 1
            vid = str(counter)
            vlink = v.split("><p")[0].replace('<a href="', "").replace('"', "")
            vtitle = v.split("><p")[1].replace(' dir="auto">', "").replace("</p></a>", "").replace("&#39;", "'").replace('&quot;', "\"")
            vuploadDate = regexChannelVideoUploadDates[counter - 1].replace('<p class="video-data" dir="auto">Shared ', "").replace("</p>", "")
            vduration = regexChannelVideoDurations[counter - 1].replace('<p class="length">', "").replace("</p>", "")
            channelVideoObjects.append({"id": vid, "date": vuploadDate, "duration": vduration, "title": vtitle, "link": "https://www.youtube.com" + vlink})
            
        #set total videos
        totalYoutubeVideos = len(channelVideoObjects)
        print("totalYoutubeVideos: " + str(totalYoutubeVideos))
        
        #youtube videos null check
        if totalYoutubeVideos == 0:
            print("0 youtube posts found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, "youtube", "null")).start()
            return
        
        #youtube videos exists
        elif totalYoutubeVideos > 0:
            
            #set total cards
            if totalYoutubeVideos < 10: 
                videosLimit = totalYoutubeVideos

            #debugging
            # for item in channelVideoObjects[0:videosLimit]:
            #     print(item)

            #create post objects
            for video in channelVideoObjects[0: videosLimit]:
                post = {
                    "id": video['id'],
                    "title": video['title'],
                    "date": video['date'],
                    "link": video['link'],
                    "duration": video['duration'],
                    "type": "youtube",
                    "profile": name
                }
                savedYoutubePosts.append(post)

            #update UI       
            counterSYP = -1
            Thread(target=lambda : displayNewsCard(self, counterTNS, "youtube", savedYoutubePosts[0])).start()
    
    except Exception as e:
        print(e); print("youtube channel fetch failed")
        Thread(target=lambda : displayNewsCard(self, counterTNS, "youtube", "null")).start()
        return


def fetch_twitter_profile(self, username, profile):
    
    try:
        #variables
        global savedTwitterPosts
        global COUNTER_SAVED_X_POSTS
        global tweetsLimit
        savedTwitterPosts = []
        COUNTER_SAVED_X_POSTS = -1
        name = profile['name']

        #fetch twitter profile
        httpRequest = requests.get(twitterDomain + "/" + username, timeout=10)
        # print(httpRequest.status_code)
        # print(httpRequest.text)

        #parse html
        className = "timeline-item"
        soup = BeautifulSoup(httpRequest.text, 'html.parser')
        tweets = soup.find_all('div', class_=className)
        # print(className + ": " + str(len(tweets)))
        # print(tweets)
        
        #handle tweets
        count = 0
        for obj in tweets:

            #filter post text
            obj = str(obj)
            text = nitterFilterPost("text", obj, None)
            link = nitterFilterPost("link", obj, False)
            date = nitterFilterPost("date", obj, link)
            pinned = nitterFilterPost("pinned", obj, link)
            retweet = nitterFilterPost("retweet", obj, link)
            youtube = nitterFilterPost("youtube", obj, link)
            poll = nitterFilterPost("poll", obj, link)
            images = nitterFilterPost("images", obj, text)
            videos = nitterFilterPost("videos", obj, link)

            #might use later
            # comments = nitterFilterPost("comments", obj, link); print("comments: " + comments)
            # retweets = nitterFilterPost("retweets", obj, link); print("retweets: " + retweets)
            # qoutes = nitterFilterPost("qoutes", obj, link); print("qoutes: " + qoutes)
            # likes = nitterFilterPost("likes", obj, link); print("likes: " + likes)

            #check if tweet is pinned or a retweet
            #     count = count + 1
            if pinned != "True" and retweet != "True":
            # if pinned != "True":
                count = count + 1

                # post = { "id": str(count), "text": obj }
                post = {
                    "id": str(count),
                    "username": username,
                    "link": link,
                    "date": date,
                    "pinned": pinned,
                    "retweet": retweet,
                    "text": text,
                    "youtube": youtube,
                    "poll": poll,
                    "images": images,
                    "videos": videos,
                    "type": "twitter",
                    "profile": profile['name']
                }
                savedTwitterPosts.append(post)

        #debugging
        print("totalTwitterPosts: " + str(len(savedTwitterPosts)))
        # print("twitter posts:")
            # for tweet in savedTwitterPosts[:tweetsLimit]:
            #     print(tweet)

        #twitter posts null check
        if len(savedTwitterPosts) == 0:
            print("0 twitter posts found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, "twitter", "null")).start()
            return

        #twitter posts exists
        elif len(savedTwitterPosts) > 0:
            COUNTER_SAVED_X_POSTS = -1
            savedTwitterPosts = savedTwitterPosts[0:tweetsLimit]
            Thread(target=lambda : displayNewsCard(self, counterTNS, "twitter", savedTwitterPosts[0])).start()
                
    except Exception as e:
        print(e); print("twitter profile fetch failed")
        Thread(target=lambda : displayNewsCard(self, counterTNS, "twitter", "null")).start()
        return


def fetch_subreddit(self, name, profile):

    try:    
        #variables
        global savedSubredditPosts
        global counterSSP
        global subredditPostsLimit
        savedSubredditPosts = []
        totalStickied = 0
        totalSubredditPosts = 0
        count = 0
        counterSSP = -1
        profileName = profile['name']
        profileSubreddit = profile['subreddit']

        #fetch subreddit posts
        httpRequest = requests.get(redditDomain + "/r/" + name + "/hot", timeout=10)
        
        #regex subreddit data
        regexTitle = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', httpRequest.text)
        regexLink = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', httpRequest.text)
        regexDate = re.findall(r'<span class="created" title=".*', httpRequest.text)
        regexStickied = re.findall(r'<div class="post stickied".*', httpRequest.text)
        totalStickied = len(regexStickied)
        totalSubredditPosts = len(regexTitle)
        regexTitle = regexTitle[totalStickied:subredditPostsLimit + totalStickied]
        regexLink = regexLink[totalStickied:subredditPostsLimit + totalStickied]
        regexDate = regexDate[totalStickied:subredditPostsLimit + totalStickied]

        #subreddit posts null check
        if totalSubredditPosts == 0:
            print("0 subreddit posts found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, "subreddit", "null")).start()
            return
        
        #subreddit posts exists
        elif totalSubredditPosts > 0:
            
            #set total posts
            if totalSubredditPosts < 10: 
                subredditPostsLimit = totalSubredditPosts
           
            for item in regexTitle:
                title = str(item)
                title = title.split(">")[1]
                title = title.replace("&quot;", "").replace("&#x27;", "").replace(".</a", "").replace("</a", "")
                title = title.replace("â", "a").replace("¦", "").replace("Isit", "Is it").replace("isit", "is it")
                title = title.replace("a\x80", "").replace("\x80", "").replace("\x9c", "")
                title = title.replace("\x9f", "").replace("\x8e", "").replace("\x9d", "")
                title = title.replace("\x99", "").replace("ð ", "").replace("ð", "")
                title = title.replace("¶", " ").replace("&amp;", "&")

                link = regexLink[count]
                link = str(link)
                link = link.replace("<a href=\"", "")
                link = link.split("/\">")[0]
                link = "https://reddit.com/r/" + profileSubreddit + "/comments/" + link.split("comments/")[1].split("/")[0]

                date = regexDate[count]
                date = str(date)
                date = date.split(",")[0]
                date = date.replace("<span class=\"created\" title=\"", "")
                
                #create obj post
                post = {
                    "id": str(count + 1),
                    "title": title,
                    "link": link,
                    "date": date,
                    "type": "subreddit",
                    "subreddit": "/r/" + profileSubreddit,
                    "profile": profileName
                }
                savedSubredditPosts.append(post)

                #increment
                count += 1

            #debugging
            print("totalSubredditPosts: " + str(totalSubredditPosts))
            # print("subreddit posts:")
            # for p in savedSubredditPosts:
            #     print(p['id'] + " - " + p['title'])
                # print(p)

            #update UI    
            counterSSP = -1
            Thread(target=lambda : displayNewsCard(self, counterTNS, "subreddit", None)).start()
             
    except Exception as e:
        print(e); print("subreddit fetch failed")
        Thread(target=lambda : displayNewsCard(self, counterTNS, "subreddit", "null")).start()
        return


def nitterFilterPost(type, obj, link):
    
    if type == "text":

        #format text
        obj = emoji.demojize(obj) #handle emojis
        obj = obj.replace('<a href="/', '').replace("</a>", "").replace('">@', '@').replace('" title="', ' ').replace("\n\n", "\n").replace("\n", ":newline:")
        obj = re.findall(r'dir="auto">[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”]*', obj)
        obj = str(obj).replace("['dir=\"auto\">", "").replace("<\']", "").replace("&amp;", "&").replace("\\", "").replace("'dir=\"auto\">", "")
        obj = obj.replace("<',", "").replace(".", ". ").replace(":newline:", "\n").replace("search?q=%23", "").replace("::", ",").replace("\">", "")
        obj = obj.replace("  ", " ").replace("']", "").replace(".  ", ". ")
        obj = obj.split("',")[0]

        objTags = re.findall(r'@[\w\d]*', obj)
        for tag in objTags:
            obj = obj.replace(tag, "")
        
        objTags = re.findall(r'[\w\d]*#', obj)
        for tag in objTags:
            obj = obj.replace(tag, "#")

        return obj

    elif type == "retweet":
        #regex
        retweet = re.findall(r'<div class="retweet-header">.*</span>', obj)
        
        #tweet is retweet
        if(len(retweet) > 0): return "True"

        #tweet is original
        elif(len(retweet) == 0): return "False"

    elif type == "pinned":
        #regex
        pinned = re.findall(r'<div class="pinned">', obj)
        
        #tweet is pinned
        if(len(pinned) > 0): return "True"

        #tweet is not pinned
        elif(len(pinned) == 0): return "False"
            
    elif type == "date":
        #regex
        date = re.findall(r'title=".*</a></span>', obj); date = date[0]
        
        #format date
        if(len(date) > 0):
            date = str(date)
            date = date.split("\">")[0]
            date = date.replace('title="', "")
            date = date[0:-14]
            date = date.replace(",", "")
            return date
            
        #null check
        elif(len(link) == 0): return "False"

    elif type == "link":
        #regex
        link = re.findall(r'<a class="tweet-link" href="/.*</a>', obj)
        
        #format link
        if(len(link) > 0):
            link = str(link)
            link = link.replace("['<a class=\"tweet-link\" href=\"/", "")
            link = link.replace("\"></a>']", "")
            link = link.replace("#m", "")
            link = "https://x.com/" + link # link = twitterDomain + link
            return link

        #null check
        elif(len(link) == 0): return "False"

    elif type == "likes":
        #regex
        likes = re.findall(r'icon-heart" title=""></span>.*', obj)

        #format likes
        if(len(likes) > 0):
            likes = str(likes)
            likes = likes.replace("['icon-heart\" title=\"\"></span> ", "")
            likes = likes.replace("</div></span>']", "")
            likes = likes.replace(",", ".")
            if likes == "": likes = "0"
            return likes

        #null check
        elif(len(likes) == 0): return "False"
            
    elif type == "qoutes":
        #regex
        qoutes = re.findall(r'icon-quote" title=""></span>.*', obj)

        #format qoutes
        if(len(qoutes) > 0):
            qoutes = str(qoutes)
            qoutes = qoutes.replace("['icon-quote\" title=\"\"></span>", "")
            qoutes = qoutes.replace("['icon-quote\" title=\"\"></span> ", "")
            qoutes = qoutes.replace("</div></span>']", "")
            qoutes = qoutes.replace(",", ".")
            qoutes = qoutes.replace(" ", "")
            if qoutes == "": qoutes = "0"
            return qoutes

        #null check
        elif(len(qoutes) == 0): return "False"

    elif type == "retweets":
        #regex
        retweets = re.findall(r'icon-retweet" title=""></span>.*', obj)

        #format retweets count
        if(len(retweets) > 0):
            retweets = str(retweets)
            retweets = retweets.replace("[\'icon-retweet\" title=\"\"></span> ", "")
            retweets = retweets.replace("</div></span>']", "")
            retweets = retweets.replace(",", ".")
            retweets = retweets.replace("Marques Brownlee retweeted</div></span></div>'. 'icon-retweet\" title=\"\"></span> ", "")
            if retweets == "": retweets = "0"
            return retweets

        #null check
        elif(len(retweets) == 0): return "False"

    elif type == "comments":
        #regex
        comments = re.findall(r'icon-comment" title=""></span>.*', obj)

        #format comments count
        if(len(comments) > 0):
            comments = str(comments)
            comments = comments.replace("[\'icon-comment\" title=\"\"></span> ", "")
            comments = comments.replace("</div></span>']", "")
            comments = comments.replace(",", ".")
            if comments == "": comments = "0"
            return comments
        elif(len(comments) == 0): return "False"

    elif type == "videos":
        #variables
        videosArray = []

        #regex
        videos = re.findall(r'class="gallery-video"><div class="attachment video-container">\n<img src=".*', obj)

        #format video thumbnail url
        if(len(videos) > 0):
            for vid in videos:
                vid = vid.replace("\n", "")
                vid = vid.replace("class=\"gallery-video\"><div class=\"attachment video-container\">", "")
                vid = vid.replace("<img src=\"/", "")
                vid = vid.replace("\"/>", "")
                vid = twitterDomain + vid
                videosArray.append(vid)
            return videosArray

        #null check
        elif(len(videos) == 0): return "False"
            
    elif type == "images":
        #variables
        imagesArray = []

        #regex
        images = re.findall(r'target="_blank"><img alt="" src="/pic.*/>', obj)

        #handle images
        if(len(images) > 0):
            #variables
            count = 0

            #handle img urls
            for img in images:
                count = count + 1

                #format img url
                img = img.replace("target=\"_blank\"><img alt=\"\" src=\"/", "")
                img = img.replace("\"/>", "")
                
                #add to array
                imagesArray.append(img)

                #download img
                # img = img.replace("%3Fname%3Dsmall", "")
                # img = twitterDomain + img
                # img_data = requests.get(img, timeout=10).content
                # with open(os.getcwd() + "/temp/" + str(link) + "-" + str(count) + ".jpg", 'wb') as handler: handler.write(img_data)
                
            return imagesArray
            
        #null check
        elif(len(images) == 0): return "False"

    elif type == "poll":
        #regex
        poll = re.findall(r'<div class="poll-meter leader">\n.*</span>\n.*</span>\n.*</span>\n.*</div>', obj)
        pollLeader = re.findall(r'<div class="poll-meter leader">\n.*</span>\n.*</span>\n.*</span>\n.*</div>', obj)
        pollLeader = str(pollLeader)
        pollLeader = pollLeader.split('<span class="poll-choice-option">')
        pollItems = re.findall(r'<div class="poll-meter">\n.*</span>\n.*</span>\n.*</span>\n.*</div>', obj)
        pollVotes = re.findall(r'<span class="poll-info">.*</span>', obj)

        #handle poll text
        if(len(pollLeader) == 2):
            #format poll leader
            pollLeaderPercentage = str(pollLeader[0].split("%")[0].replace("['<div class=\"poll-meter leader\">\\n<span class=\"poll-choice-bar\" style=\"width: ", ""))
            pollLeaderText = str(pollLeader[1].split("%")[0]).replace("</span>\\n</div>']", "")
            obj = pollLeaderPercentage + "%" + " · " + pollLeaderText

            #format poll items
            pollItems = str(pollItems).replace("['", "").replace("']", "")
            pollItems = pollItems.split('\'<div class="poll-meter">')
            for i in pollItems:
                i = i.replace('<div class=\"poll-meter\">\\n<span class=\"poll-choice-bar\" style=\"width: ', "")
                i = i.replace('\\n<span class=\"poll-choice-bar\" style=\"width:  ', "")
                i = i.replace('</span>\\n<span class=\"poll-choice-option\">', " · ")
                i = i.replace('</span>\\n</div>', "")
                i = i.replace('; ', " · ")
                i = i.replace("'", "")
                i = i.replace(", ", "")
                i = i.split(" · ")[0] + " · " + i.split(" · ")[2]
                obj = obj + "\n" + i

            #format poll votes
            pollVotes = str(pollVotes)
            pollVotes = pollVotes.replace("['<span class=\"poll-info\">", "")
            pollVotes = pollVotes.replace("</span>']", "")
            pollVotes = pollVotes.replace(",", ".")
            pollVotes = pollVotes.replace(" votes • Final results", "")
            pollVotes = "Total Votes: " + pollVotes
            obj = obj + "\n" + pollVotes

            return obj

        #null check
        elif(len(pollLeader) == 1): return "False"
            
    elif type == "youtube":
        #regex
        obj = re.findall(r'https://piped.kavin.rocks/.*</div>', obj)

        #format youtube url
        if(len(obj) > 0): 
            obj = str(obj)
            obj = obj.replace("piped.kavin.rocks/", "youtube.com/watch?v=")
            obj = obj.replace("['", "")
            obj = obj.replace("']", "")
            obj = obj = obj.split('">')[0]
            return obj

        #null check
        elif(len(obj) == 0): return "False"


def displayNewsCard(self, id, platform, profileData):
    
    #variables
    card1 = self.ids.newsCard1Post
    card2 = self.ids.newsCard2Post
    card3 = self.ids.newsCard3Post
    card4 = self.ids.newsCard4Post
    blayout1 = self.ids.boxLayoutNewsCard1
    blayout2 = self.ids.boxLayoutNewsCard2
    blayout3 = self.ids.boxLayoutNewsCard3
    blayout4 = self.ids.boxLayoutNewsCard4

    #check card id
    if id == 1: cardObj = card1; boxlayoutObj = blayout1; cardObj.order = id
    if id == 2: cardObj = card2; boxlayoutObj = blayout2; cardObj.order = id
    if id == 3: cardObj = card3; boxlayoutObj = blayout3; cardObj.order = id
    if id == 4: cardObj = card4; boxlayoutObj = blayout4; cardObj.order = id
    self.changeButtonColor(id, platform)

    #check platform
    if platform == "twitter": cardObj.type = "twitter"; cardObj.text = "X · No posts found..."
    elif platform == "youtube": cardObj.type = "youtube"; cardObj.text = "YouTube · No posts found..."
    elif platform == "article": cardObj.type = "article"; cardObj.text = "Articles · No posts found..."
    elif platform == "subreddit": cardObj.type = "subreddit"; cardObj.text = "Subreddit · No posts found..."


    #check profile data
    if profileData != "null" and platform == "twitter": cardObj.text = "X · Click to Read..."
    elif profileData != "null" and platform == "youtube": cardObj.text = "YouTube · Click to Read..."
    elif profileData != "null" and platform == "article": cardObj.text = "Articles · Click to Read..."
    elif profileData != "null" and platform == "subreddit": cardObj.text = "Subreddit · Click to Read..."
    
    #update UI: display card    
    try: boxlayoutObj.opacity = 1; cardObj.opacity = 1
    except: print("Kivy UI Error")


def undisplayNewsCard(self, id):
    try:
        if id == 1: self.ids.boxLayoutNewsCard1.opacity = 0
        elif id == 2: self.ids.boxLayoutNewsCard2.opacity = 0
        elif id == 3: self.ids.boxLayoutNewsCard3.opacity = 0
        elif id == 4: self.ids.boxLayoutNewsCard4.opacity = 0
    
    except: 
        print("Kivy UI Error")


#------ SCREEN 1: Posts ------#
class NewsFeedScreen(Screen):
    
    def __init__(self, **var_args):
        super(NewsFeedScreen, self).__init__(**var_args)
        self.ids.category1.text = str(year_progress())


    def on_pre_enter(self, *args):

        #log
        print("Screen: News Feed") 
        
        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        btnBackgroundColor = get_color_from_hex("#292f33")
        btnHeight = 40
        btnFontSize = 16

        #update UI: clear widgets
        self.bl1.clear_widgets()

        #create buttons
        btnAdd = Button(text = "+", size_hint_y = None, height = btnHeight, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = btnFontSize, bold = True)
        btnEdit = Button(text = "-", size_hint_y = None, height = btnHeight, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = btnFontSize, bold = True)
        btnFavorites = Button(text = "Saved", size_hint_y = None, height = btnHeight, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = btnFontSize, bold = True)
        # btnFiller = Button(text = "", size_hint_y = None, height = btnHeight, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = btnFontSize)

        #bind functions to buttons
        btnAdd.bind(on_press=lambda *args: changeScreen(self, 'add'))
        btnEdit.bind(on_press=lambda *args: changeScreen(self, 'edit'))
        btnFavorites.bind(on_press=lambda *args: changeScreen(self, 'favorites'))

        #update UI: add buttons
        self.bl1.add_widget(btnFavorites) #favorite button
        self.bl1.add_widget(btnAdd) #add button
        self.bl1.add_widget(btnEdit) #edit button
        for p in savedProfiles[::-1]: #sidemenu buttons
            NewsFeedScreen.AddProfileButtons(self, p, totalSavedProfiles)
            

    def printNewsFeed(self, profile, selfObj):
        fetch_news_feed(profile, selfObj)


    def startThreadPrintNewsFeed(self, *args):
        
        #variables
        profile = args[0]

        #start thread
        Thread(target=self.printNewsFeed, kwargs={"profile": profile, "selfObj": self}).start()


    def AddProfileButtons(self, profile, totalSavedProfiles):
        
        #variables
        totalMenuButtons = 4
        totalButtons = len(self.bl1.children)

        #check total profile buttons
        if(totalButtons != totalSavedProfiles + totalMenuButtons):
            
            profilePicDefault = os.getcwd() + "/images/fallbackProfilePic.png"
            profilePicCustom = ""

            #create button
            # newButton = Button(background_normal = os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg", background_down = os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg", size_hint_y = None, opacity = 0.9)
            newButton = Button(background_normal = profilePicDefault, background_down = profilePicDefault, size_hint_y = None, opacity = 0.9)
            newButton.bind(on_press=lambda *args: self.startThreadPrintNewsFeed(profile)) #bind function buttons

            #update UI: add button
            self.bl1.add_widget(newButton)


    def saveToFavorites(screen, self, type):

        #debugging
        # print(savedTwitterPosts[COUNTER_SAVED_X_POSTS])
        # print(savedYoutubePosts[counterSYP])

        #variables
        totalTwitterPosts = len(savedTwitterPosts)
        totalYoutubePosts = len(savedYoutubePosts)
        totalNewsArticles = len(savedNewsArticles)
        totalSubredditPosts = len(savedSubredditPosts)
        
        try:
            #check post platform
            if type == "twitter" and totalTwitterPosts > 0: post = savedTwitterPosts[COUNTER_SAVED_X_POSTS] #TWITTER
            elif type == "youtube" and totalYoutubePosts > 0: post = savedYoutubePosts[counterSYP] #YOUTUBE
            elif type == "article" and totalNewsArticles > 0: post = savedNewsArticles[counterSNA] #ARTICLE
            elif type == "subreddit" and totalSubredditPosts > 0: post = savedSubredditPosts[counterSSP] #SUBREDDIT
            else: return

            #handle favorite obj
            newFavorite = {
                "id": (post['username'] + post['text'] + post['date']).replace(" ", "").replace("_", "").replace("-", "").replace("\n", "").replace("·", "").replace("u00b7", ""),
                "profile": post['profile'],
                "date": post['date'], 
                "platform": type, 
                "savedAt": str(datetime.datetime.now())[0:10], 
                "text": post['title'],
                "img": "/thumbnails/" + post['profile'] + ".jpg",
                "link": post['link']
            }
            favorites.append(newFavorite)

            #load favorites.json
            favorites = json.load(open('favorites.json', "r"))

            #check if card already saved
            for f in favorites:
                if f['id'] == id: print('news card already saved'); return
            
            #update favorites.json
            out_file = open("favorites.json", "w"); json.dump(favorites, out_file, indent = 6); out_file.close()

        except:
            print("error: save"  + type + " card failed")
        

    def removeFromFavorites(self, cardId):
        
        #debugging
        print("removeFromFavorites")

        #variables
        favorites = json.load(open('favorites.json', "r"))
        
        #remove selected favorite
        count = 0
        for f in favorites:
            if f['id'] == cardId:
                favorites.pop(count)
                out_file = open("favorites.json", "w")
                json.dump(favorites, out_file, indent = 6)
                out_file.close()
            count += 1

        #Update UI: refresh favorites screen
        if 'favorites' in str(self): refreshScreen(self, 'favorites')


    def createFavoritesCard(self, *args):
        
        #variables
        obj = args[0]
        print(str(obj))
        id = obj['id']
        profile = obj['profile']
        platform = obj['platform']
        savedAt = obj['savedAt']
        text = obj['text']
        img = obj['img']
        date = obj['date']
        link = obj['link']
        colorTwitter = get_color_from_hex('#1DA1F2')
        colorYoutube = get_color_from_hex('#FF0000')
        colorArticle = get_color_from_hex('#0e1012')
        colorSubreddit = get_color_from_hex('#ff4500')
        bl = BoxLayout(orientation = "horizontal", size_hint_x = None, size_hint_y = None, height = 240, width = 600) #, spacing = (40, 40), padding = (40, 40)
        favorites = json.load(open('favorites.json', "r"))
        imgSrc = os.getcwd() + "/thumbnails/" + str(profile) + ".jpg"

        #clean card text
        if platform == "twitter": text = newsTextCleaner(self, platform, text)

        #check platform
        if platform == "twitter": platform = "Twitter"
        elif platform == "youtube": platform = "Youtube"
        elif platform == "article": platform = "Article"
        elif platform == "subreddit": platform = "Subreddit"

        #create widgets 
        btnProfileImg = Button(size_hint_x = None, size_hint_y = None, height = 220, width = 220, background_normal =  imgSrc,background_down =  imgSrc,color = 'lightgray') #profile button
        btn1 = Button(text = "-", size_hint_y = 0.5,size_hint_x = None, width = 70, background_color = get_color_from_hex('#0e1012'), background_normal = 'transparent', background_down = 'transparent', font_size = 30, color = 'lightgray', opacity = 0.9) #remove button
        btn2 = Button(text = "§", size_hint_y = 0.5,size_hint_x = None, width = 70, background_color = get_color_from_hex('#0e1012'), background_normal = 'transparent',background_down = 'transparent',font_size = 19,color = 'lightgray',opacity = 0.9)
        sl = StackLayout(orientation = "tb-lr", size_hint_y = 0.917,size_hint_x = None) #stacklayout # height = 300, width = 600, spacing = (0, 20), padding = (0, 20)
        btnNewsCard = Button(
            text = "Saved " + savedAt + ": " + "\n\n" + platform + " · " + profile + " · " + date + "\n" + text,
            size_hint_y = None,
            size_hint_x = None,
            padding = (40, 40), #left, top
            text_size = (560, 240),
            height = 220,
            width = 560,
            # multiline = True,
            disabled = False,
            halign = 'left',
            valign = 'top',
            color = 'white',
            background_color = "black", # #292f33
            background_normal = 'transparent',
            background_down = 'transparent',
            bold = True,
            font_size = 16,
            opacity = 0.9
        )

        #bind functions to buttons
        btn1.bind(on_press=lambda *args: NewsFeedScreen.removeFromFavorites(self, id))
        btn2.bind(on_press=lambda *args: NewsFeedScreen.copyToClipboard(self, link))

        #set widget platform colors
        if platform == "Twitter": btnNewsCard.background_color = colorTwitter; btn1.background_color = colorTwitter; btn2.background_color = colorTwitter
        elif platform == "Youtube": btnNewsCard.background_color = colorYoutube; btn1.background_color = colorYoutube; btn2.background_color = colorYoutube
        elif platform == "Article": btnNewsCard.background_color = colorArticle; btn1.background_color = colorArticle; btn2.background_color = colorArticle
        elif platform == "Subreddit": btnNewsCard.background_color = colorSubreddit; btn1.background_color = colorSubreddit; btn2.background_color = colorSubreddit

        #update UI: add widgets to layouts
        bl.add_widget(btnProfileImg)
        bl.add_widget(btnNewsCard)
        sl.add_widget(btn2)
        sl.add_widget(btn1)
        bl.add_widget(sl)
        return bl


    def clear_news(self):
        self.ids.boxLayoutPost.clear_widgets()

    
    def twitterNextPost(self, order):
        
        #variables
        global COUNTER_SAVED_X_POSTS
        totalTwitterPosts = len(savedTwitterPosts)

        #twitter posts null check
        if totalTwitterPosts == 0: return

        #twitter posts exists
        elif totalTwitterPosts > 0:
            
            #increment counter
            if COUNTER_SAVED_X_POSTS == (len(savedTwitterPosts) - 1): COUNTER_SAVED_X_POSTS = -1
            COUNTER_SAVED_X_POSTS = COUNTER_SAVED_X_POSTS + 1; 

            #set card text
            id = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["date"])
            text = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["text"])
            text = newsTextCleaner(self, 'twitter', text)
            # username = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["username"])
            # images = savedTwitterPosts[COUNTER_SAVED_X_POSTS]["images"]
            # videos = savedTwitterPosts[COUNTER_SAVED_X_POSTS]["videos"]
            # youtube = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["youtube"])
            # retweet = str(savedTwitterPosts[COUNTER_SAVED_X_POSTS]["retweet"])
            cardText = "\n" + "X" + " · " + id + " · " + date + "\n\n" + "(Self-Post)" + "\n" + text + "\n"
            
            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #update UI card text
            card.text = cardText


    def youtubeNextPost(self, order):
        
        #variables
        global counterSYP
        totalYoutubeVideos = len(savedYoutubePosts)

        #youtube posts null check
        if totalYoutubeVideos == 0: return
        
        #youtube posts exists
        elif totalYoutubeVideos > 0:
            
            #increment counter
            if counterSYP == (len(savedYoutubePosts) - 1): counterSYP = -1 #check if last card
            counterSYP = counterSYP + 1 

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #set card text
            videoId = savedYoutubePosts[counterSYP]['id'] + "/" + str(totalYoutubeVideos)
            videoUploadDate = savedYoutubePosts[counterSYP]['date']
            videoDuration = savedYoutubePosts[counterSYP]['duration']
            videoTitle = savedYoutubePosts[counterSYP]['title']
            cardText = "YouTube" + " · " + videoId + " · " + videoUploadDate + "\n\n" + videoTitle + " (" + videoDuration + ")"

            #update UI card text
            card.text = cardText


    def articleNextPost(self, order):
        
        #variables
        global counterSNA
        totalArticles = len(savedNewsArticles)

        #articles null check
        if totalArticles == 0: return

        #articles exists
        elif totalArticles > 0:
            
            #increment counter
            if counterSNA == (totalArticles - 1): counterSNA = -1
            counterSNA = counterSNA + 1

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #set card text
            articleId = savedNewsArticles[counterSNA]['id'] + "/" + str(totalArticles)
            articleDate = savedNewsArticles[counterSNA]['date']
            articleTitle = savedNewsArticles[counterSNA]['title']
            articlePublisher =  "(" + savedNewsArticles[counterSNA]['publisher'].split(".")[0].upper() + ")"
            articleLink = savedNewsArticles[counterSNA]['link']
            cardText = "Article" + " · " + articleId + " · " + articleDate + "\n\n" + articlePublisher + "\n" + articleTitle

            #update UI text
            card.text = cardText


    def subredditNextPost(self, order):
        
        #variables
        global counterSSP
        totalSubredditPosts = len(savedSubredditPosts)

        #subreddit posts null check
        if totalSubredditPosts == 0: return

        #subreddit posts exists
        elif totalSubredditPosts > 0:
            
            #increment counter
            if counterSSP == (len(savedSubredditPosts) - 1): counterSSP = -1
            counterSSP = counterSSP + 1

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post
            
            #set card text
            cardId = savedSubredditPosts[counterSSP]['id'] + "/" + str(totalSubredditPosts)
            cardDate = savedSubredditPosts[counterSSP]['date']
            cardTitle = savedSubredditPosts[counterSSP]['title']
            cardSubreddit = savedSubredditPosts[counterSSP]['subreddit']
            cardText = "Subreddit" + " · " + cardId + " · " + cardDate + "\n\n" + cardTitle
            
            #update UI card text
            card.text = cardText


    def copyToClipboard(self, type):

        #check platform
        if type == "twitter" and len(savedTwitterPosts) != 0: pyclip.copy(savedTwitterPosts[COUNTER_SAVED_X_POSTS]['link'])
        elif type == "youtube" and len(savedYoutubePosts) != 0: pyclip.copy(savedYoutubePosts[counterSYP]['link'])
        elif type == "article" and len(savedNewsArticles) != 0: pyclip.copy(savedNewsArticles[counterSNA]['link'])
        elif type == "subreddit" and len(savedSubredditPosts) != 0: pyclip.copy(savedSubredditPosts[counterSSP]['link'])
        else: pyclip.copy(type) # favorites screen
       
        #debugging
        clipboardText = pyclip.paste(text=True); print("copyToClipboard: " + clipboardText) 


    def nextPost(self, order, type):
        if type == "youtube": self.youtubeNextPost(order)
        elif type == "twitter": self.twitterNextPost(order)
        elif type == "article": self.articleNextPost(order)
        elif type == "subreddit": self.subredditNextPost(order)


    def changeButtonColor(self, order, type):
        
        #variables
        colorTwitter = get_color_from_hex('#1DA1F2')
        colorYoutube = get_color_from_hex('#FF0000')
        colorArticle = get_color_from_hex('#0e1012')
        colorSubreddit = get_color_from_hex('#ff4500')
        card = ""
        buttonFavorites = ""
        buttonLink = ""
        buttonLeftSideFiller = ""

        #check card order
        if order == 1: 
            card = self.ids.newsCard1Post; 
            buttonFavorites = self.ids.buttonAddToFavs1; 
            buttonLink = self.ids.buttonCopyLink1 
            buttonLeftSideFiller = self.ids.buttonLeftSideFiller1 
        elif order == 2: 
            card = self.ids.newsCard2Post; 
            buttonFavorites = self.ids.buttonAddToFavs2; 
            buttonLink = self.ids.buttonCopyLink2
            buttonLeftSideFiller = self.ids.buttonLeftSideFiller2
        elif order == 3: 
            card = self.ids.newsCard3Post; 
            buttonFavorites = self.ids.buttonAddToFavs3; 
            buttonLink = self.ids.buttonCopyLink3
            buttonLeftSideFiller = self.ids.buttonLeftSideFiller3
        elif order == 4: 
            card = self.ids.newsCard4Post; 
            buttonFavorites = self.ids.buttonAddToFavs4; 
            buttonLink = self.ids.buttonCopyLink4 
            buttonLeftSideFiller = self.ids.buttonLeftSideFiller4

        #set card platform color
        if type == "twitter": 
            card.background_color = colorTwitter; 
            buttonFavorites.background_color = colorTwitter; 
            buttonLink.background_color = colorTwitter
            buttonLeftSideFiller.background_color = colorTwitter
        elif type == "youtube": 
            card.background_color = colorYoutube; 
            buttonFavorites.background_color = colorYoutube; 
            buttonLink.background_color = colorYoutube
            buttonLeftSideFiller.background_color = colorYoutube
        elif type == "article": 
            card.background_color = colorArticle; 
            buttonFavorites.background_color = colorArticle; 
            buttonLink.background_color = colorArticle
            buttonLeftSideFiller.background_color = colorArticle
        elif type == "subreddit": 
            card.background_color = colorSubreddit; 
            buttonFavorites.background_color = colorSubreddit; 
            buttonLink.background_color = colorSubreddit
            buttonLeftSideFiller.background_color = colorSubreddit


#------ SCREEN 2: Saved ------#
class FavoritesScreen(Screen):
    
    def __init__(self, **var_args):
        super(FavoritesScreen, self).__init__(**var_args)


    def on_pre_enter(self, *args):
        print("Screen: Favorites")

        #clear card widgets
        self.ids.boxLayoutPost.clear_widgets()

        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        totalButtons = len(self.ids.boxLayoutPost.children)
        favorites = fetch_saved_favorites()
        totalFavorites = len(favorites)
        lbl1 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")
        lbl2 = Label(size_hint_y = 1, size_hint_x = 1, text = str(len(favorites)) + " Saved Posts", bold = True)
        lbl3 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")

        #update UI: fill side panel with buttons
        # for x in range(6):
            # NewsFeedScreen.AddFillerButtons(self)

        #update UI widgets
        self.ids.boxLayoutPost.add_widget(lbl1)
        self.ids.boxLayoutPost.add_widget(lbl2)
        for fav in favorites[::-1]:
            if totalButtons < totalFavorites:
                bl = NewsFeedScreen.createFavoritesCard(self, fav)
                self.ids.boxLayoutPost.add_widget(bl)
        self.ids.boxLayoutPost.add_widget(lbl3)


#------ SCREEN 3: Profile Add ------#
class AddProfileScreen(Screen):
    
    def __init__(self, **var_args):
        super(AddProfileScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("Screen: Add Profile") #log

        #variables
        savedProfiles = fetch_saved_profiles()
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

        #update UI: clear text inputs
        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""
        self.ti4.text = ""
        self.ti5.text = ""


#------ SCREEN 4: Profile Remove ------#
class RemoveProfileScreen(Screen):
    
    def __init__(self, **var_args):
        super(RemoveProfileScreen, self).__init__(**var_args)
        

    def on_pre_enter(self, *args):
        print("Screen: Remove Profile") #log

        #variables
        self.ids.boxLayout2.clear_widgets()
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        totalButtons = len(self.ids.boxLayout2.children)

        #update UI: add saved profiles buttons
        if totalButtons != totalSavedProfiles:
            
            #clear widgets
            self.ids.boxLayout2.clear_widgets()

            #add buttons
            for x in range(totalSavedProfiles):
                reverseListCount = (totalSavedProfiles - 1) - x # reverse list to make latest added on top
                RemoveProfileScreen.AddProfileButtons(self, savedProfiles[reverseListCount])

            #set total saved profiles
            # self.ids.labelTotalSavedProfiles.text = str(totalSavedProfiles) + " Saved Profiles"
        
        #update UI: fill side panel with filler buttons
        # for x in range(6):
            # NewsFeedScreen.AddFillerButtons(self)

        self.btnRemoveProfile.text = "Remove Profile"


    def AddProfileButtons(self, profile):
        
        #create button widget
        newButton = Button(size_hint_y = None, height = 40, text = profile['name'].upper(), background_color = get_color_from_hex("#292f33"))
        newButton.bind(on_press=lambda *args: RemoveProfileScreen.FillTextInputWithData(self, profile)) #add functions to buttons

        #update UI: add button layout
        self.ids.boxLayout2.add_widget(newButton)


    def DeleteProfile(self):
        
        #variables
        name = self.ti1.text
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

        
        #update UI
        self.ti1.text = "" #clear text inputs
        refreshScreen(self, 'edit') #refresh edit screen


    def FillTextInputWithData(self, profile):
        self.ti1.text = profile['name']
        self.btnRemoveProfile.text = "Remove " + profile['name'].upper()

 
#------ SCREEN 5: Blank ------#
class BlankScreen(Screen):

    def __init__(self, **var_args):
        super(BlankScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("Screen: Blank") #log


#------ Base Class ------#
class ScraperNewsApp(App):
    
    def build(self):
        
        #update UI: set window title
        self.title = "Scraper News" #"Scraper News · " + str(year_progress())

        #create json files
        if os.path.exists('profiles.json') == False: file = open('profiles.json', "w"); file.write("[]"); file.close()
        if os.path.exists('favorites.json') == False: file = open('favorites.json', "w"); file.write("[]"); file.close()

        #create thumbnail directory
        if os.path.isdir('thumbnails') == False: os.mkdir('thumbnails')
        
        #screen manager configs
        sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(NewsFeedScreen(name='start'))
        sm.add_widget(AddProfileScreen(name='add'))    
        sm.add_widget(RemoveProfileScreen(name='edit'))    
        sm.add_widget(FavoritesScreen(name='favorites'))  
        sm.add_widget(BlankScreen(name='blank'))
        return sm


#------ KIVY SETTINGS ------#
kivy.require('2.0.0')
Window.set_icon("logo.ico") # Window.set_icon("icon.png")
Window.size = (1000, 700) #width, height
# Config.set('kivy','window_icon', 'icon.png')
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #removes right click display red dot
# Config.set('graphics', 'resizable', '1') #changing this might break display resolution
# Config.set('graphics', 'fullscreen', '0') #changing this might break display resolution
# Config.write()


#------ START APP ------#
if __name__ == '__main__': ScraperNewsApp().run()