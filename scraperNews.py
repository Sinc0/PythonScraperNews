### imports general ###
import requests
import re
import twint
import time
import datetime
import json
from threading import Thread
import time
import requests
import os
import webbrowser

### imports kivy ###
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from functools import partial

#load kv file
Builder.load_file("scraperNews.kv")
# Builder.load_string("""""")

### functions ###
def displayNewsCard(self, id, buttonId, profileName, newsType, newsText):
    if id == 1: 
        self.ids.newsCard1GreenBtn.disabled = False
        self.ids.boxLayoutNewsCard1.opacity = 1
    elif id == 2: 
        self.ids.newsCard2GreenBtn.disabled = False
        self.ids.boxLayoutNewsCard2.opacity = 1
    elif id == 3: 
        self.ids.newsCard3GreenBtn.disabled = False
        self.ids.boxLayoutNewsCard3.opacity = 1

def undisplayNewsCard(self, id):
    if id == 1: self.ids.boxLayoutNewsCard1.opacity = 0
    elif id == 2: self.ids.boxLayoutNewsCard2.opacity = 0
    elif id == 3: self.ids.boxLayoutNewsCard3.opacity = 0
                    
def fetch_youtube_channel(url, self, name):
    #null check
    if url == "": print("youtube channel is null"); return
    elif 'http' not in url: print("youtube channel is null"); return

    #variables
    requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    numberOfVideosLimit = 3
    channelTitle = ""
    youtubeVideoCounter = 0

    #make request
    httpRequest = requests.get(url, headers=requestHeaders)

    #handle request result
    if httpRequest.status_code == 200:
        #variables
        requestResultText = str(httpRequest.text)

        #replace characters
        requestResultText = requestResultText.replace(".", "")

        #encode text
        requestResultText = requestResultText.encode('ascii', 'ignore')
        # requestResultText = requestResultText.decode('utf8', 'replace')

        #regex youtube channel title
        formatChannelTitle1 = re.findall(r'<title>.*YouTube</title>', str(requestResultText))
        formatChannelTitle2 = str(formatChannelTitle1[0])
        formatChannelTitle3 = formatChannelTitle2[7:]
        channelTitle = formatChannelTitle3[:-18]
        channelTitleFormated = channelTitle.replace(" ", "_").lower()
    else:
        print("youtube channel fetch failed")

    # try:
    #replace characters
    requestResultText = str(requestResultText).replace("\\u0026", "&")

    #regex youtube video data
    youtubeVideos = re.findall(r'"title":{"runs":\[{"text":"[\w*\s*\d*,*-*!*"*_*\/*:*\\*}*{*\]\'*\.\\*\-*\#*\|*\(*\)*&*+*]*ago"', requestResultText)
    # youtubeVideos = re.findall(r'"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"', requestResultText)
    
    #add videos to news feed
    for videoTitle in youtubeVideos[:numberOfVideosLimit]:
        #variables
        youtubeVideoCounter += 1

        #regex youtube video upload date
        formatFindUploadDate = re.findall(r':"[\d]*\s[^.]*ago"', videoTitle)
        if formatFindUploadDate == []:
            formatFindUploadDate = re.findall(r':"Streamed\s[\d]*\s[^.]*ago"', videoTitle)
            formatFindUploadDate = str(formatFindUploadDate).replace("Streamed ", "")
            formatFindUploadDate = str(formatFindUploadDate).lower()

        #format youtube video upload date
        formatUploadDateStep1 = str(formatFindUploadDate)[4:]
        formatUploadDateStep2 = str(formatUploadDateStep1)[:(len(formatUploadDateStep1) - 3)]
        formatedUploadDate = formatUploadDateStep2

        #regex youtube video title
        formatFindTitle = re.findall(r'"text":"[^.]*"}],"', videoTitle)

        #format youtube video title
        formatTitleStep1 = str(formatFindTitle)[10:]
        formatTitleStep2 = str(formatTitleStep1)[:(len(formatTitleStep1) - 7)]
        formatTitleStep3 = str(formatTitleStep2).replace("\\\\\"", "\"")
        formatTitleStep4 = str(formatTitleStep3).replace("\\'", "'")
        formatTitleStep5 = str(formatTitleStep4).replace("   ", " ")
        formatTitleStep6 = str(formatTitleStep5).replace("  ", " ")
        formatedTitle = formatTitleStep6

        #create news cards
        if youtubeVideoCounter <= numberOfVideosLimit:
            time.sleep(0.1)
            cardText = name + " · Youtube · " + str(formatedUploadDate) + " · " + "\n" + str(formatedTitle) + "\n"
            # print(" " + "youtube" + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))

            #update news card #1        
            if(youtubeVideoCounter == 1):
                self.ids.newsCard1Post.text = cardText #update text
                Thread(target=lambda : displayNewsCard(self, 1, 101, cardText, 'youtube', name)).start() #display card

            #update news card #2        
            elif(youtubeVideoCounter == 2):
                self.ids.newsCard2Post.text = cardText #update text
                Thread(target=lambda : displayNewsCard(self, 2, 102, cardText, 'youtube', name)).start() #display card

            #update news card #3      
            elif(youtubeVideoCounter == 3):
                self.ids.newsCard3Post.text = cardText #update text
                Thread(target=lambda : displayNewsCard(self, 3, 103, cardText, 'youtube', name)).start() #display card
        else:
            print("error: " + str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
    # except:
        # print("youtube channel does not exist")

# def fetch_twitter_profile(username, self, name):
#     #null check
#     if username == "":
#         print("twitter username is null")
#         return

#     #variables
#     numberOfTweetsLimit = 3
#     userTweets = []
#     c = twint.Config()
#     c.Username = username
#     c.Limit = 3 # buggy does not represent actual number
#     c.Hide_output = True
#     c.Store_object = True
#     c.Store_object_tweets_list = userTweets

#     #try fetch data
#     try:
#         twint.run.Search(c)
#         # print("fetched " + str(len(userTweets)) + " tweets")
#         # print(username + " latest tweets:")
#         tCounter = 0
#         for t in userTweets[:numberOfTweetsLimit]:
#             tCounter += 1
#             # print("#" + str(tCounter) + " - " + t.username + " - " + t.datestamp + " - " + t.tweet)
#             # print("#" + str(tCounter) + " - " + "twitter" + " - " + t.datestamp + " - " + t.tweet)
#             # self.ids.svLabel.text += "\n" + "twitter" + " - " + t.datestamp.replace("-", "/") + ": " + t.tweet + "\n"
#             # self.ids.svScrollBar.scroll_y = 0
            
#             #create news card
#             time.sleep(0.1)
#             print(" " + "twitter" + " - " + t.datestamp + " - " + t.tweet)
#             cardText = "Twitter" + " - " + t.datestamp.replace("-", "/") + "\n" + t.tweet
#             bl = StartingScreen.createNewsCard(self, cardText, 'twitter', name)
#             self.ids.boxLayoutPost.add_widget(bl)
        
#         # print(str(len(userTweets)))
#         # print("")
#     except:
#         print("twitter profile does not exist")
    
def year_progress():
    #variables
    JAN = 31
    FEB = 31 + 28
    MAR = 31 + 28 + 31
    APR = 31 + 28 + 31 + 30
    MAY = 31 + 28 + 31 + 30 + 31
    JUN = 31 + 28 + 31 + 30 + 31 + 30
    JUL = 31 + 28 + 31 + 30 + 31 + 30 + 31
    AUG = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
    SEP = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30
    OCT = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31
    NOV = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30
    DEC = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31
    totalDaysThisYear = 365

    #set current year
    year = datetime.datetime.now().year

    #set current month
    month = datetime.datetime.now().month

    #set current day
    day = datetime.datetime.now().day

    #check if leap year
    if year == "2024": totalDaysThisYear = 366
    
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
            
    #set percentage of year
    percentageOfYear = dayOfTheYear / totalDaysThisYear
    
    #set formatted date
    formattedDate = str(month) + " " + str(day) + " " + str(year) + " - " + str(dayOfTheYear) + "/" + str(totalDaysThisYear) + " - " + str(percentageOfYear)[2:4] + "%"
    
    return formattedDate

def add_profile(self, name, youtube = None, twitter = None):
    #variables
    profiles = []
    totalProfiles = 0
    youtubeChannel = youtube

    try: 
        #fetch profiles from profiles.json if exists
        file = open('profiles.json', "r")
        profiles = json.load(file)
        totalProfiles = len(profiles)
        
        #check if profile name is taken
        for p in profiles:
            if p['name'] == name: print("profile name already taken"); return

        #check if profile name is null
        if name == "": print("profile name empty"); return
    
    except: 
        #create profiles.json
        file = open('profiles.json', "w")
        file.close()

    #youtube url check
    if youtube == "": print("profiles youtube channel is null")
    elif 'https://www.youtube.com/' not in youtube: youtube = "https://www.youtube.com/" + youtubeChannel + "/videos"

    #fetch profile image 1
    fetchProfileImage = fetch_profile_image(youtube, name)
    
    #fetch profile image backup
    if fetchProfileImage == False:
        youtube = "https://www.youtube.com/user/" + youtubeChannel + "/videos"
        fetch_profile_image(youtube, name)

    #create profile obj
    newProfile = {"id": totalProfiles + 1, "name": name, "youtube": youtube, "twitter": twitter}

    #add profile to profiles.json
    profiles.append(newProfile)
    out_file = open("profiles.json", "w")
    json.dump(profiles, out_file, indent = 6)
    out_file.close()

def fetch_news_feed(name, self):
    #fetch profiles from profiles.json
    file = open('profiles.json', "r")
    profiles = json.load(file)
    totalProfiles = len(profiles)

    #reset news card text
    self.ids.newsCard1Post.text = ""
    self.ids.newsCard2Post.text = ""
    self.ids.newsCard3Post.text = ""

    #undisplay news card
    Thread(target=lambda : undisplayNewsCard(self, 1)).start()
    Thread(target=lambda : undisplayNewsCard(self, 2)).start()
    Thread(target=lambda : undisplayNewsCard(self, 3)).start()

    #fetch profile youtube data
    for p in profiles:
        if p['name'] == name: 
            print(p['name'])
            fetch_youtube_channel(p['youtube'], self, name)
            # fetch_twitter_profile(p['twitter'], self, name)

    #fetch profile twitter data
    # for p in profiles:
    #     if p['name'] == name: 
    #         print(p['name'])
            # fetch_twitter_profile(p['twitter'], self, name)

def fetch_saved_profiles():
    #fetch profiles from profiles.json
    file = open('profiles.json', "r")
    profiles = json.load(file)
    return profiles

def fetch_saved_favorites():
    #fetch profiles from favorites.json
    file = open('favorites.json', "r")
    favorites = json.load(file)
    return favorites

def fetch_profile_image(url, name):
    #fetch profile image from google
    if 'youtube' not in url:
        #send search query
        response = requests.get('https://www.google.com/search?q=' + name + 'k&tbm=isch&hl=en-US&cr=countryUS&tbs=isz:i')

        #handle search query results
        if response.status_code == 200:
            #regex search result images
            regexImages = re.findall(r'src="http\S*;s', response.text)
            
            #set search result images
            firstSearchHitImage = regexImages[0][5:-6]
            secondSearchHitImage = regexImages[1][5:-6]
            thirdSearchHitImage = regexImages[2][5:-6]

            #download selected search result image
            response = requests.get(secondSearchHitImage)
            
            #create image file
            file = open(os.getcwd() + '/thumbnails/' + name + '.jpg','wb')
            file.write(response.content)
            file.close()

            #fetch profile image successful
            return True

    #fetch profile image from youtube
    elif 'youtube' in url:
        #variables
        requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}

        #send search query
        httpRequest = requests.get(url, headers=requestHeaders)

        #handle search query results
        if httpRequest.status_code == 200:
            #variables
            requestResultText = str(httpRequest.text)

            #encode text
            requestResultText = requestResultText.encode('ascii', 'ignore')
            # requestResultText = requestResultText.decode('utf8', 'ignore')
            
            try:
                #regex find youtube channel image url
                findChannelImageText = re.findall(r'avatar":{"thumbnails":.*176}', str(requestResultText))
                #format channel image url
                formatChannelImage1 = findChannelImageText[0][23:]
                formatChannelImage2 = formatChannelImage1.split("},{")[2]
                formatChannelImage3 = formatChannelImage2[6:-26]
                formatChannelImage4 = formatChannelImage3[1:-1]
            except:
                #fetch profile image failed
                return False

            #download selected search result image
            response = requests.get(formatChannelImage4)

            #create image file
            file = open(os.getcwd() + '/thumbnails/' + name + '.jpg','wb')
            file.write(response.content)
            file.close()

            #fetch profile image successful
            return True

    #fetch profile image error
    else:
        print("profile image fetch failed")
        return False

def changeScreenToAdd(self):
    self.manager.current = 'add' #change to add profile screen 

def changeScreenToEdit(self):
    self.manager.current = 'edit' #change to edit profile screen 

def changeScreenToStart(self):
    self.manager.current = 'start' #change to start screen 

def changeScreenToFavorites(self):
    self.manager.current = 'favorites'  #change to favorites screen 

def changeScreenToMenu(self):
    self.manager.current = 'menu'  #change to menu screen 

def refreshScreen(self, screenName):
    self.manager.current = 'blank' #change to blank screen
    self.manager.current = screenName #change back to previous screen

# def openNewsInWebBrowser(self, searchString):
#     webbrowser.open_new('http://duckduckgo.com/?q=' + searchString)



### kivy ###
kivy.require('2.1.0')
# Config.set('graphics', 'resizable', 0)
# Config.set('graphics', 'width', '200')
# Config.set('graphics', 'height', '200')

class StartingScreen(Screen):
    def __init__(self, **var_args):
        super(StartingScreen, self).__init__(**var_args)


    def on_pre_enter(self, *args):
        print("StartingScreen")
        
        #fetch saved profiles
        savedProfiles = fetch_saved_profiles()

        #set profiles count
        totalSavedProfiles = len(savedProfiles)
        
        #variables buttons
        btnBackgroundColor = get_color_from_hex("#292f33")
        btnHeight = 40
        btnFontSize = 16

        #clear widgets
        self.bl1.clear_widgets()

        #create add button
        btnAdd = Button(
            text = "+", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', font_size = 30
        )

        #create edit button
        btnEdit = Button(
            text = "-", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = 49
        )
        #create favorite button
        btnFavorites = Button(
            text = "Saved", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = btnFontSize
        )

        #create filler button
        btnFiller = Button(
            text = "", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = btnFontSize
        )

        #bind functions to buttons
        btnAdd.bind(on_press=lambda *args: changeScreenToAdd(self))
        btnEdit.bind(on_press=lambda *args: changeScreenToEdit(self))
        btnFavorites.bind(on_press=lambda *args: changeScreenToFavorites(self))

        #add buttons to layout
        self.bl1.add_widget(btnFavorites)
        self.bl1.add_widget(btnAdd)
        self.bl1.add_widget(btnEdit)

        #add profile sidemenu buttons
        for p in savedProfiles[::-1]:
            StartingScreen.AddProfileButtons(self, p, totalSavedProfiles)
            

    def printNewsFeed(self, profile, selfObj):
        fetch_news_feed(profile['name'], selfObj)


    def startThreadPrintNewsFeed(self, *args):
        #variables
        profile = args[0]

        #start thread
        Thread(target=self.printNewsFeed, kwargs={"profile": profile, "selfObj": self}).start()


    def AddProfileButtons(self, profile, totalSavedProfiles):
        #variables
        totalMenuButtons = 4

        #set buttons count
        totalButtons = len(self.bl1.children)

        #add profile buttons
        if(totalButtons != totalSavedProfiles + totalMenuButtons):
            #create button
            newButton = Button(
                background_normal =  os.getcwd() + "/thumbnails/" + profile['name'].lower() + ".jpg",
                size_hint_y = None
            )

            #bind function buttons
            newButton.bind(on_press=lambda *args: self.startThreadPrintNewsFeed(profile))

            #add buttons to layout
            self.bl1.add_widget(newButton)


    def AddFillerButtons(self):
        #set buttons count
        totalButtons = len(self.bl2.children)

        #add filler buttons
        if(totalButtons < 6):
            #create button
            newButton = Button(
                size_hint_y = None,
                text = "",
                disabled = True
            )

            #add buttons to layout
            self.bl2.add_widget(newButton)


    def saveToFavorites(screen, self, text):
        #fetch favorites from favorites.json
        file = open('favorites.json', "r")
        favorites = json.load(file)
        totalFavorites = len(favorites)

        #create button id
        btnIdFormatting1 = text.replace(" ", "")
        btnIdFormatting2 = btnIdFormatting1.replace("_", "")
        btnIdFormatting3 = btnIdFormatting2.replace("-", "")
        btnIdFormatting4 = btnIdFormatting3.replace("\n", "")
        btnIdFormatting5 = btnIdFormatting4.replace("·", "")
        btnIdFormatting6 = btnIdFormatting5.replace("u00b7", "")
        btnIdFormatted = str(btnIdFormatting6[0:60])
        id = btnIdFormatted
        
        #variables favorite
        profile = text.split(" · ")[0]
        platform = text.split(" · ")[1]
        savedAt = str(datetime.datetime.now())
        postedAt = text.split(" · ")[2]
        text = text.split(" · ")[3].replace("\n", "")
        
        #save favorite
        newFavorite = {
            "id": id,
            "profile": profile, 
            "platform": platform, 
            "savedAt": savedAt, 
            "text": postedAt + " · " + text,
            "img": "/" + profile + ".jpg"
        }
        
        #check if favorite already saved
        for f in favorites:
            if f['id'] == id: print('news card already saved'); return
        
        #add favorite to favorites.json
        favorites.append(newFavorite)
        out_file = open("favorites.json", "w")
        json.dump(favorites, out_file, indent = 6)
        out_file.close()
        

    def removeFromFavorites(self, cardId):
        #fetch favorites from favorites.json
        file = open('favorites.json', "r")
        favorites = json.load(file)
        totalFavorites = len(favorites)
        
        #remove selected favorite
        count = 0
        for f in favorites:
            if f['id'] == cardId:
                favorites.pop(count)
                out_file = open("favorites.json", "w")
                json.dump(favorites, out_file, indent = 6)
                out_file.close()
            count += 1

        #refresh favorites screen
        if 'favorites' in str(self): refreshScreen(self, 'favorites')


    def createNewsCard(self, *args):
        #variables
        text = args[0]
        newsType = args[1]
        profile = args[2]
        baseHeight = 160
        baseWidth = 600

        #handle date
        try: savedAt = args[3]
        except: savedAt = ""

        #clean text from special characters
        cleanText1 = text.replace("\\", "")
        cleanText2 = cleanText1.replace("\\\\", "")
        cleanText3 = cleanText2.replace("//", "")
        text = cleanText3

        #calculate card text height & width
        tempTextLength = len(text)
        textHeightMultiplier = int((tempTextLength) / 107) # one line of text 107 chars
        textHeight = 37 * textHeightMultiplier # one line of text add 37 px
        textHeightMinusCorrection = (textHeightMultiplier) * 20 # if multiplier is above 2 minus 20 px
        if textHeightMultiplier > 1:totalHeight = baseHeight + textHeight - textHeightMinusCorrection
        else: totalHeight = baseHeight + textHeight
        totalWidth = baseWidth

        #create boxlayout
        bl = BoxLayout(
            orientation = "horizontal", 
            size_hint_x = None, 
            size_hint_y = None,
            height = 100,
            width = 600,
            spacing = -2,
            padding = 0
        )

        #fetch favorites from favorites.json
        file = open('favorites.json', "r")
        favorites = json.load(file)

        #create button id
        btnId = profile + newsType + text
        btnIdFormatting1 = btnId.replace(" ", "")
        btnIdFormatting2 = btnIdFormatting1.replace("_", "")
        btnIdFormatting3 = btnIdFormatting2.replace("-", "")
        btnIdFormatting4 = btnIdFormatting3.replace("\n", "")
        btnIdFormatting5 = btnIdFormatting4.replace("·", "")
        btnIdFormatting6 = btnIdFormatting5.replace("u00b7", "")
        btnId = str(btnIdFormatting6[0:60])
        
        #create profile image button
        btnProfileImg = Button(
            size_hint_x = None, 
            size_hint_y = None, 
            height = 100, 
            width = 100, 
            background_normal =  os.getcwd() + "/thumbnails/" + profile.lower() + ".jpg",
            color = 'lightgray'
        )
        btnProfileImg.id = btnId
        
        #create remove button
        if btnId in str(favorites):
            btn = Button(
                text = "-", 
                size_hint_x = None, 
                size_hint_y = None,
                height = 100,
                width = 70, 
                background_color = 'darkred', 
                background_normal = 'darkred', 
                background_down = 'darkred',
                font_size = 24,
                color = 'lightgray'
            )
            btn.id = btnId

        #create save button
        elif btnId not in str(favorites):
            btn = Button(
                text = "+", 
                size_hint_x = None, 
                size_hint_y = None,
                height = 100,
                width = 70, 
                background_color = 'green', 
                background_normal = 'green', 
                background_down = 'green',
                font_size = 24,
                color = 'lightgray'
            )
            btn.id = btnId
        
        #create button
        else:
            btn = Button(
                text = "+", 
                size_hint_x = 0.1, 
                size_hint_y = 1, 
                background_color = 'green', 
                background_normal = 'green', 
                background_down = 'green',
                color = 'lightgray'
            )
            btn.id = btnId
        
        #bind functions to buttons
        btn.bind(on_press=lambda *args: StartingScreen.removeFromFavorites(self, btn.id))

        #create news card
        btnNewsCard = Button(
                text = savedAt + " · " + newsType + " · " + text.split(" · ")[0] + "\n" + text.split(" · ")[1],
                size_hint_y = None,
                size_hint_x = None,
                padding = (60, 40), #left, top
                text_size = (600, totalHeight),
                height = 100,
                width = 499,
                multiline = True,
                disabled = False,
                halign = 'left',
                valign = 'top',
                color = 'lightgray',
                background_color = get_color_from_hex("#292f33"),
                background_normal = 'transparent',
                background_down = 'transparent'
            )

        #set background color
        # if newsType == 'twitter':
        #     b2.background_color = get_color_from_hex("#55acee")
        #     b2.background_normal = 'transparent'
        #     b2.background_down = 'transparent'
        # elif newsType == 'youtube':
        #     b2.background_color = get_color_from_hex("#e52d27")
        #     b2.background_normal = 'transparent'
        #     b2.background_down = 'transparent'

        #set search string
        # searchString = "searchString" # text.split("\n")[1]

        #add widgets to boxlayout
        bl.add_widget(btnProfileImg)
        bl.add_widget(btnNewsCard)
        bl.add_widget(btn)

        return bl


    def createTitleCard(self, *args):
        #variables
        text = args[0]
        backgroundColor = get_color_from_hex("#292f33")
        formattedText = ""
        
        #handle menu type
        try: menuType = args[1]
        except: menuType = "null"

        #create boxlayout
        bl = BoxLayout(
            orientation = "horizontal", 
            size_hint_x = 1, 
            size_hint_y = None,
            height = 100,
            width = 660
        )

        #text formatting
        text = str(text).replace(" ", "_")
        text = str(text).split("_")
        for t in text: formattedText += str(t).capitalize() + " "

        #create button 
        btn = Button(
            text = str(formattedText), 
            size_hint_x = 1, size_hint_y = 1, 
            background_color = backgroundColor, 
            background_normal = 'transparent',
            background_down = 'transparent',
            color = 'lightgray',
            font_size = 30
        )
        
        #bind functions to buttons
        if menuType == 'add': btn.bind(on_press=lambda *args: changeScreenToAdd(self))
        elif menuType == 'delete': btn.bind(on_press=lambda *args: changeScreenToEdit(self))
        elif menuType == 'favorites': btn.bind(on_press=lambda *args: changeScreenToFavorites(self))
        elif menuType == 'clear': btn.bind(on_press=lambda *args: StartingScreen.clear_news(self))

        #add button to boxlayout
        bl.add_widget(btn)

        #create title card successful
        return bl


    def clear_news(self):
        self.ids.boxLayoutPost.clear_widgets()


    def create_menu(self):
        #create title card
        titleCardAdd = StartingScreen.createTitleCard(self, 'Add', 'add')
        titleCardDelete = StartingScreen.createTitleCard(self, 'Delete', 'delete')
        titleCardFavorites = StartingScreen.createTitleCard(self, 'Saved', 'favorites')
        
        #add title card to layout
        self.ids.boxLayoutPost.add_widget(titleCardAdd)
        self.ids.boxLayoutPost.add_widget(titleCardDelete)
        self.ids.boxLayoutPost.add_widget(titleCardFavorites)



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

        #add profile
        add_profile(self, profileName, profileYoutube, profileTwitter)

        #clear text inputs
        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""



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

        #fill side panel with buttons
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
        for image in thumbnails:
            imageFile = os.getcwd() + '/thumbnails' + '/' + image
            if name in image:
                try: os.remove(imageFile)
                except: print("delete thumbnail " + name + " failed")

        #clear text inputs
        self.ti1.text = ""

        #refresh edit screen
        refreshScreen(self, 'edit')


    def FillTextInputWithData(self, profile):
        self.ti1.text = profile['name']



class FavoritesScreen(Screen):
    def __init__(self, **var_args):
        super(FavoritesScreen, self).__init__(**var_args)

    def on_pre_enter(self, *args):
        print("FavoritesScreen")

        #clear card widgets
        self.ids.boxLayoutPost.clear_widgets()

        #fetch saved profiles
        savedProfiles = fetch_saved_profiles()

        #set saved profiles count
        totalSavedProfiles = len(savedProfiles)

        #set total layout buttons
        totalButtons = len(self.ids.boxLayoutPost.children)

        #fetch saved favorites
        favorites = fetch_saved_favorites()

        #set saved favorites count
        totalFavorites = len(favorites)

        #fill side panel with buttons
        # for x in range(6):
        #     StartingScreen.AddFillerButtons(self)

        #add saved favorites news cards
        for f in favorites[::-1]:
            if totalButtons < totalFavorites:
                savedAt =  "saved " + str(f['savedAt'][:-16]) + "\n" + f['profile']
                bl = StartingScreen.createNewsCard(self, f['text'], f['platform'], f['profile'], savedAt)
                self.ids.boxLayoutPost.add_widget(bl)

class BlankScreen(Screen):
    def __init__(self, **var_args):
        super(BlankScreen, self).__init__(**var_args)
    
    def on_pre_enter(self, *args):
        print("BlankScreen")

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

#start app
if __name__ == '__main__':
    scraperNewsApp().run()
