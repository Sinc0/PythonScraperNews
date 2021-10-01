### imports ###
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

### imports kivy ###
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
# from kivy.graphics import Rectangle, Color
# from kivy.utils import rgba
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button

### request settings ###
#api key = AIzaSyCHDajHZ7clx29MBJQ2omXfEprzsRw5n6Y
#cookie settings = 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'

### regex history ###
#"title":{"runs":[{"text":"
#"width":336,"height":188}]},"title":{"runs":[{"text":"
#"width":336,"height":188}]},"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago
#"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"
#"text":"[^.]*"}],"

### notes ###
#https://www.youtube.com/channel/UCkw4JCwteGrDHIsyIIKo4tQ
#https://www.googleapis.com/youtube/v3/search?key=AIzaSyCHDajHZ7clx29MBJQ2omXfEprzsRw5n6Y&channelId=UCkw4JCwteGrDHIsyIIKo4tQ&part=snippet,id&order=date&maxResults=20

### global variables ###
youtubeVideos = []
youtubeVideoCounter = 0

### global functions ###
def fetch_youtube_channel(url, self, name):
    #null check
    if url == "":
        print("youtube channel is null")
        return

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
        requestResultText = requestResultText.encode('utf8', 'ignore')
        # requestResultText = requestResultText.decode('utf8', 'ignore')

        #prints
        # print("youtube channel fetch succesful")
        # print(requestResultText)

        #create text file
        with open('test.txt', 'w') as f:
            f.write(str(requestResultText))

        #regex youtube channel title
        formatChannelTitle1 = re.findall(r'<title>.*YouTube</title>', str(requestResultText))
        formatChannelTitle2 = str(formatChannelTitle1[0])
        formatChannelTitle3 = formatChannelTitle2[7:]
        channelTitle = formatChannelTitle3[:-18]
        channelTitleFormated = channelTitle.replace(" ", "_").lower()
    else:
        print("youtube channel fetch failed")

    try:
        #regex youtube video data
        requestResultText = str(requestResultText).replace("\\u0026", "&")
        regexYoutubeVideos = re.findall(r'"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"', requestResultText)

        #create title card
        bl = StartingScreen.createTitleCard(self, name, 'youtube')
        self.ids.boxLayoutPost.add_widget(bl)

        for videoTitle in regexYoutubeVideos[:numberOfVideosLimit]:
            youtubeVideoCounter += 1

            #format youtube video upload date
            formatFindUploadDate = re.findall(r':"[\d]*\s[^.]*ago"', videoTitle)
            if formatFindUploadDate == []:
                formatFindUploadDate = re.findall(r':"Streamed\s[\d]*\s[^.]*ago"', videoTitle)
                formatFindUploadDate = str(formatFindUploadDate).replace("Streamed ", "")
                formatFindUploadDate = str(formatFindUploadDate).lower()
            formatUploadDateStep1 = str(formatFindUploadDate)[4:]
            formatUploadDateStep2 = str(formatUploadDateStep1)[:(len(formatUploadDateStep1) - 3)]
            formatedUploadDate = formatUploadDateStep2

            #format youtube video title
            formatFindTitle = re.findall(r'"text":"[^.]*"}],"', videoTitle)
            formatTitleStep1 = str(formatFindTitle)[10:]
            formatTitleStep2 = str(formatTitleStep1)[:(len(formatTitleStep1) - 7)]
            formatTitleStep3 = str(formatTitleStep2).replace("\\\\\"", "\"")
            formatTitleStep4 = str(formatTitleStep3).replace("\\'", "'")
            formatTitleStep5 = str(formatTitleStep4).replace("   ", " ")
            formatTitleStep6 = str(formatTitleStep5).replace("  ", " ")
            formatedTitle = formatTitleStep6

            #print youtube data to console
            if youtubeVideoCounter <= numberOfVideosLimit:
                # print(" " + str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
                # print("#" + str(youtubeVideoCounter) + " - " + "youtube" + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))
                # self.ids.svLabel.text += "\n" + "youtube" + " - " + str(formatedUploadDate) + ": " + str(formatedTitle) + "\n"
                # self.ids.svScrollBar.scroll_y = 0
                
                #create news card
                time.sleep(0.1)
                print(" " + "youtube" + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))
                cardText = "Youtube" + " - " + str(formatedUploadDate) + "\n" + str(formatedTitle)
                bl = StartingScreen.createNewsCard(self, cardText, 'youtube', name)
                self.ids.boxLayoutPost.add_widget(bl)
            # else:
            #     print(str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
    except:
        print("youtube channel does not exist")

def fetch_twitter_profile(username, self, name):
    #null check
    if username == "":
        print("twitter username is null")
        return

    #variables
    numberOfTweetsLimit = 3
    userTweets = []
    c = twint.Config()
    c.Username = username
    c.Limit = 3 # buggy does not represent actual number
    c.Hide_output = True
    c.Store_object = True
    c.Store_object_tweets_list = userTweets

    #try fetch data
    try:
        twint.run.Search(c)
        # print("fetched " + str(len(userTweets)) + " tweets")
        # print(username + " latest tweets:")
        tCounter = 0
        for t in userTweets[:numberOfTweetsLimit]:
            tCounter += 1
            # print("#" + str(tCounter) + " - " + t.username + " - " + t.datestamp + " - " + t.tweet)
            # print("#" + str(tCounter) + " - " + "twitter" + " - " + t.datestamp + " - " + t.tweet)
            # self.ids.svLabel.text += "\n" + "twitter" + " - " + t.datestamp.replace("-", "/") + ": " + t.tweet + "\n"
            # self.ids.svScrollBar.scroll_y = 0
            
            #create news card
            time.sleep(0.1)
            print(" " + "twitter" + " - " + t.datestamp + " - " + t.tweet)
            cardText = "Twitter" + " - " + t.datestamp.replace("-", "/") + "\n" + t.tweet
            bl = StartingScreen.createNewsCard(self, cardText, 'twitter', name)
            self.ids.boxLayoutPost.add_widget(bl)
        
        # print(str(len(userTweets)))
        # print("")
    except:
        print("twitter profile does not exist")
    
def year_progress():
    #variables
    JAN = 31
    FEB = 31 + 28
    MAR = 31 + 28 + 31
    APR = 31 + 28 + 31+ 30
    MAY = 31 + 28 + 31+ 30 + 31
    JUN = 31 + 28 + 31+ 30 + 31 + 30
    JUL = 31 + 28 + 31+ 30 + 31 + 30 + 31
    AUG = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
    SEP = 31 + 28 + 31+ 30 + 31 + 30 + 31 + 31 + 30
    OCT = 31 + 28 + 31+ 30 + 31 + 30 + 31 + 31 + 30 + 31
    NOV = 31 + 28 + 31+ 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30
    DEC = 31 + 28 + 31+ 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31
    year = datetime.datetime.now().year
    totalDaysThisYear = 365
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    #check if leap year
    if year == "2024": 
        totalDaysThisYear = 366
    
    #check month name
    if month == 1: 
        dayOfTheYear = JAN + day
        month = "JAN"
    if month == 2: 
        dayOfTheYear = FEB + day
        month = "FEB"
    if month == 3:
        dayOfTheYear = MAR + day 
        month = "MAR"
    if month == 4:
        dayOfTheYear = APR + day
        month = "APR"
    if month == 5:
        dayOfTheYear = MAY + day
        month = "MAY"
    if month == 6:
        dayOfTheYear = JUN + day
        month = "JUN"
    if month == 7:
        dayOfTheYear = JUL + day
        month = "JUL"
    if month == 8:
        dayOfTheYear = AUG + day
        month = "AUG"
    if month == 9:
        dayOfTheYear = SEP + day
        month = "SEP"
    if month == 10:
        dayOfTheYear = OCT + day
        month = "OCT"
    if month == 11:
        dayOfTheYear = NOV + day 
        month = "NOV"
    if month == 12:
        dayOfTheYear = DEC + day 
        month = "DEC"
            
    #check percentage of year
    percentageOfYear = dayOfTheYear / totalDaysThisYear
    
    print(str(day) + " " + str(month) + " " + str(year) + " - " + str(dayOfTheYear) + "/" + str(totalDaysThisYear) + " - " + str(percentageOfYear)[2:4] + "%")
    return str(day) + " " + str(month) + " " + str(year) + " - " + str(dayOfTheYear) + "/" + str(totalDaysThisYear) + " - " + str(percentageOfYear)[2:4] + "%"

def add_profile(self, name, youtube = None, twitter = None):
    #variables
    profiles = []
    totalProfiles = 0

    try: 
        #fetch all saved profiles from profiles.json if exists
        file = open('profiles.json', "r")
        profiles = json.load(file)
        totalProfiles = len(profiles)
        
        #check if profile name is available
        for p in profiles:
            if p['name'] == name:
                print("profile name already taken")
                return

        #check naming errors
        if name == "":
            print("profile name empty")
            return
    
    except: 
        #create profiles.json if does not exists
        file = open('profiles.json', "w")
        file.close()

    #new profile obj
    newProfile = {
        "id": totalProfiles + 1,
        "name": name, 
        "youtube": youtube, 
        "twitter": twitter 
    }

    #add new profile to json file
    profiles.append(newProfile)
    out_file = open("profiles.json", "w")
    json.dump(profiles, out_file, indent = 6)
    out_file.close()

    #try get profile image
    fetch_profile_image(youtube)

def remove_profile(name):
    #variables
    profiles = []
    totalProfiles = 0
    totalProfilesUpdated = 0
    
    try:
        #fetch all saved profiles from json file
        file = open('profiles.json', "r")
        profiles = json.load(file)
        totalProfiles = len(profiles)

        #remove profile
        for p in profiles:
            if p['name'] == name:
                profiles.pop(p['id'] - 1)
        
        #print error message if profile does not exist
        totalProfilesUpdated = len(profiles)
        if totalProfiles == totalProfilesUpdated:
            print("profile " + name + " does not exist")
            return
        
        #update profiles.json
        out_file = open("profiles.json", "w")
        json.dump(profiles, out_file, indent = 6)
        out_file.close()
    except:
        print("error something went wrong removing profile")

def fetch_news_feed(name, self):
    #fetch all saved profiles from profiles.json if exists
    file = open('profiles.json', "r")
    profiles = json.load(file)
    totalProfiles = len(profiles)

    #clear all news card widgets
    self.ids.boxLayoutPost.clear_widgets()

    #fetch profile data
    for p in profiles:
        if p['name'] == name:
            print(p['name'])
            # self.ids.svLabel.text = ""
            # self.ids.svLabel.text = p['name']
            # self.ids.svScrollBar.scroll_y = 0
            
            fetch_youtube_channel(p['youtube'], self, name)
            fetch_twitter_profile(p['twitter'], self, name)

    print("")

def fetch_saved_profiles():
    #fetch all saved profiles from profiles.json if exists
    file = open('profiles.json', "r")
    profiles = json.load(file)
    return profiles

def fetch_profile_image(url):
    #null check
    if url == "":
        print("youtube channel is null")
        return

    #variables
    requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    httpRequest = requests.get(url, headers=requestHeaders)

    #successful request
    if httpRequest.status_code == 200:
        #variables
        requestResultText = str(httpRequest.text)
        requestResultText = requestResultText.encode('utf8', 'ignore')
        # requestResultText = requestResultText.decode('utf8', 'ignore')

        #save html to text file
        with open('test.txt', 'w') as f:
            f.write(str(requestResultText))

        #regex find channel title
        formatChannelTitle1 = re.findall(r'<title>.*YouTube</title>', str(requestResultText))
        formatChannelTitle2 = str(formatChannelTitle1[0])
        formatChannelTitle3 = formatChannelTitle2[7:]
        channelTitle = formatChannelTitle3[:-18]
        channelTitleFormated = channelTitle.replace(" ", "_").lower()
        
        #regex find channel image url
        formatChannelImage1 = re.findall(r'avatar":{"thumbnails":.*176}', str(requestResultText))
        formatChannelImage2 = formatChannelImage1[0][23:]
        formatChannelImage3 = formatChannelImage2.split("},{")[2]
        formatChannelImage4 = formatChannelImage3[6:-26]
        formatedChannelImage = formatChannelImage4[1:-1]

        #download channel image
        response = requests.get(formatedChannelImage)
        f = open(os.getcwd() + '/thumbnails/' + channelTitleFormated + '.jpg','wb')
        f.write(response.content)
        f.close()
        return True

    #failed request
    else:
        # print("profile image fetch failed")
        return False

def changeScreenToAdd(self):
    self.manager.current = 'add'

def changeScreenToEdit(self):
    self.manager.current = 'edit'

def changeScreenToStart(self):
    self.manager.current = 'start'

### tests ###
# year_progress()
# fetch_youtube_channel('https://www.youtube.com/c/animalplanet/videos')
# fetch_youtube_channel('https://www.youtube.com/c/KimerLorens/videos')
# fetch_twitter_profile("animalplanet")
# fetch_twitter_profile("elonmusk")
# fetch_twitter_profile("spacex")
# fetch_twitter_profile("tesla")
# add_profile("testName", "youtube.com/c/testChannel", "testUsername")
# remove_profile("test")
# fetch_news_feed("animalplanet")
# fetch_news_feed("elonmusk")
# fetch_profile_image('https://www.youtube.com/c/KimerLorens/videos')

### kivy ###
kivy.require('2.0.0')

#settings
Config.set('graphics', 'resizable', 0)
#Config.set('graphics', 'width', '200')
#Config.set('graphics', 'height', '200')

#classes
class StartingScreen(Screen):
    def __init__(self, **var_args):
        super(StartingScreen, self).__init__(**var_args) # that has been overwritten in a class object. to inherited methods from a parent or sibling class super function can be used to gain access

    def on_pre_enter(self, *args):
        print("StartingScreen")
        
        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        # print("total saved profiles: " + str(len(savedProfiles)))

        #clear widgets
        self.bl1.clear_widgets()

        #create add and edit buttons
        btnBackgroundColor = get_color_from_hex("#292f33")
        btnAdd = Button(text = "+", size_hint_y = None, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = 30)
        btnAdd.bind(on_press=lambda *args: changeScreenToAdd(self))
        btnEdit = Button(text = "-", size_hint_y = None, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = 49)
        btnEdit.bind(on_press=lambda *args: changeScreenToEdit(self))

        #add create and edit buttons
        self.bl1.add_widget(btnAdd)
        self.bl1.add_widget(btnEdit)

        #add saved profile buttons
        for p in savedProfiles[::-1]:
            # print(str(p))
            StartingScreen.AddProfileButtons(self, p, totalSavedProfiles)

        #test remove widgets
        # totalChildrens = len(self.bl1.children)
        # self.bl1.remove_widget(self.bl1.children[totalChildrens - 1])
        # self.bl1.remove_widget(self.bl1.children[totalChildrens - 2])        

    def printNewsFeed(self, profile, selfObj):
        #prints
        # print(profile)
        # print(selfObj)

        #fetch news feed
        fetch_news_feed(profile['name'], selfObj)

    def startThreadPrintNewsFeed(self, *args):
        #variables
        profile = args[0]

        #prints
        # print(profile['name'])

        #start thread
        Thread(target=self.printNewsFeed, kwargs={"profile": profile, "selfObj": self}).start()

    def AddProfileButtons(self, profile, totalSavedProfiles):
        #variables
        totalButtons = len(self.bl1.children)

        #prints
        # print("total buttons: " + str(totalButtons))
        # print(self.bl1.children)

        #add profile buttons
        if(totalButtons != totalSavedProfiles + 2):
            #create button
            newButton = Button()
            newButton.background_normal =  os.getcwd() + "/thumbnails/" + profile['name'].lower() + ".jpg"
            newButton.size_hint_y = None
            newButton.bind(on_press=lambda *args: self.startThreadPrintNewsFeed(profile))
            # newButton.text = "#" + str(totalButtons - 1)
            # newButton.bind(on_press = self.startThreadPrintNewsFeed)

            #add button
            self.bl1.add_widget(newButton)

    def AddFillerButtons(self):
        #variables
        totalButtons = len(self.bl2.children)

        #prints
        # print("total buttons: " + str(totalButtons))
        
        #add filler buttons
        if(totalButtons < 6):
            #create button
            newButton = Button()
            newButton.size_hint_y = None
            newButton.text = ""
            newButton.disabled = True

            #add button
            self.bl2.add_widget(newButton)

    def saveToFavorites(self, cardId, profile, platform, cardText):
        #find boxlayout widget
        for c in self.ids.boxLayoutPost.children:
            #find button widget
            for s in c.children:
                try:
                    if s.id == cardId:
                        if s.text == '+':
                            #change button style
                            s.background_color = "darkred"
                            s.background_normal = "darkred"
                            s.text = '-'

                            try: 
                                #fetch all saved favorites from favorites.json if exists
                                file = open('favorites.json', "r")
                                favorites = json.load(file)
                                totalFavorites = len(favorites)
                                # print("total favorites: " + str(totalFavorites))
                                # print(favorites)
                            except: 
                                #create favorites.json if does not exists
                                file = open('favorites.json', "w")
                                file.close()

                            #save new favorite
                            newFavorite = {
                                "id": str(cardId),
                                "profile": profile, 
                                "platform": platform, 
                                "savedAt": str(datetime.datetime.now()), 
                                "text": cardText
                            }
                            
                            #check if already saved
                            for f in favorites:
                                if f['id'] == cardId:
                                    print('news card already saved')
                                    return
                            
                            #add new favorite
                            favorites.append(newFavorite)
                            out_file = open("favorites.json", "w")
                            json.dump(favorites, out_file, indent = 6)
                            out_file.close()

                        elif s.text == '-':
                            #change button style
                            s.text = '+'
                            s.background_color = "green"
                            s.background_normal = "green"
                            
                            #fetch all saved favorites from favorites.json if exists
                            file = open('favorites.json', "r")
                            favorites = json.load(file)
                            totalFavorites = len(favorites)
                            # print("total favorites: " + str(totalFavorites))
                            
                            count = 0
                            for f in favorites:
                                #remove selected favorite
                                if f['id'] == cardId:
                                    favorites.pop(count)
                                    out_file = open("favorites.json", "w")
                                    json.dump(favorites, out_file, indent = 6)
                                    out_file.close()
                                count += 1
                except:
                    None
            # print("")

    def createNewsCard(self, text, newsType, profile):
        #variables
        baseHeight = 120
        baseWidth = 660

        #calculate card text height
        tempTextLength = len(text)
        textHeightMultiplier = int((tempTextLength) / 107) # one line of text 107 chars
        textHeight = 37 * textHeightMultiplier # one line of text add 37 px
        textHeightMinusCorrection = (textHeightMultiplier) * 20 # if multiplier is above 2 minus 20 px

        #prints
        # print("tempText count: " + str(tempTextLength))
        # print("textHeightMultiplier: " + str(textHeightMultiplier))
        # print("textHeightMinusCorrection: " + str(textHeightMinusCorrection))

        #set total height
        if textHeightMultiplier > 1:
            totalHeight = baseHeight + textHeight - textHeightMinusCorrection
        else:
            totalHeight = baseHeight + textHeight
        
        #set total width
        totalWidth = baseWidth

        #boxlayout
        bl = BoxLayout(orientation = "horizontal", size_hint_x = 1, size_hint_y = None)
        bl.height = totalHeight - 40
        bl.width = 660
        bl.spacing = -2
        bl.padding = 0

        #fetch all saved favorites from favorites.json if exists
        file = open('favorites.json', "r")
        favorites = json.load(file)
        totalFavorites = len(favorites)

        #format text to id
        btnIdFormatting1 = text.replace(" ", "")
        btnIdFormatting2 = btnIdFormatting1.replace("_", "")
        btnIdFormatting3 = btnIdFormatting2.replace("-", "")
        btnIdFormatting4 = btnIdFormatting3.replace("\n", "")
        btnIdFormatted = str(btnIdFormatting4[0:40])
        
        #check if id is already in favorites
        if btnIdFormatted in str(favorites):
            #create remove button
            btn = Button(text = "-", size_hint_x = 0.1, size_hint_y = 1, background_color = 'darkred', background_normal = 'darkred', background_down = 'darkred')
        elif btnIdFormatted not in str(favorites):
            #create save button
            btn = Button(text = "+", size_hint_x = 0.1, size_hint_y = 1, background_color = 'green', background_normal = 'green', background_down = 'green')
        
        #set additional save/remove button variables
        btn.id = btnIdFormatted
        btn.color = 'lightgray'
        btn.bind(on_press=lambda *args: StartingScreen.saveToFavorites(self, btn.id, profile, newsType, text))

        #news card text
        b2 = Button(text = text)
        b2.size_hint_y = None
        b2.size_hint_x = 1
        b2.padding = (20, 40)
        b2.text_size = (610, totalHeight)
        b2.height = totalHeight - 40
        b2.multiline = True
        b2.disabled = False
        b2.halign = 'left'
        b2.valign = 'top'
        b2.color = 'lightgray'
        b2.background_color = get_color_from_hex("#292f33")
        b2.background_normal = 'transparent'
        b2.background_down = 'transparent'
        # if newsType == 'twitter':
        #     b2.background_color = get_color_from_hex("#55acee")
        #     b2.background_normal = 'transparent'
        #     b2.background_down = 'transparent'
        # elif newsType == 'youtube':
        #     b2.background_color = get_color_from_hex("#e52d27")
        #     b2.background_normal = 'transparent'
        #     b2.background_down = 'transparent'

        #add widgets to boxlayout
        # bl.add_widget(lbl)
        bl.add_widget(b2)
        bl.add_widget(btn)

        return bl

    def createTitleCard(self, text, newsType):
        #boxlayout
        bl = BoxLayout(orientation = "horizontal", size_hint_x = 1, size_hint_y = None)
        bl.height = 100
        bl.width = 660

        #save button
        text = str(text).split("_")
        formattedText = ""
        for t in text:
          formattedText += str(t).capitalize() + " "
          
        backgroundColor = get_color_from_hex("#292f33")
        btn = Button(text = str(formattedText), size_hint_x = 1, size_hint_y = 1, background_color = backgroundColor, background_normal = 'transparent', background_down = 'transparent')
        btn.color = 'lightgray'
        btn.font_size = 30

        bl.add_widget(btn)

        return bl

class AddProfileScreen(Screen):
    def __init__(self, **var_args):
        super(AddProfileScreen, self).__init__(**var_args) # that has been overwritten in a class object. to inherited methods from a parent or sibling class super function can be used to gain access
    
    def on_pre_enter(self, *args):
        print("AddProfileScreen")

        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        
        #fill side panel with buttons
        for x in range(6):
            StartingScreen.AddFillerButtons(self)

    def fetch_profile_inputs(self):
        #variables
        profileName = self.ti1.text
        profileTwitter = self.ti2.text
        profileYoutube = self.ti3.text

        #prints
        # print(profileName)
        # print(profileTwitter)
        # print(profileYoutube)

        #add profile
        add_profile(self, profileName, profileTwitter, profileYoutube)

        #clear text inputs
        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""

class EditProfileScreen(Screen):
    def __init__(self, **var_args):
        super(EditProfileScreen, self).__init__(**var_args) # that has been overwritten in a class object. to inherited methods from a parent or sibling class super function can be used to gain access
        
    def on_pre_enter(self, *args):
        print("EditProfileScreen")
        
        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        totalButtons = len(self.ids.testBoxLayout2.children)

        #print profiles info
        # print(type(savedProfiles))
        # print("total saved profiles: " + str(len(savedProfiles)))
        
        #add saved profiles buttons
        if totalButtons != totalSavedProfiles:
            
            #clear widgets
            self.ids.testBoxLayout2.clear_widgets()

            #add buttons
            for x in range(totalSavedProfiles):
                reverseListCount = (totalSavedProfiles - 1) - x # reverse list to make latest added on top
                EditProfileScreen.AddProfileButtons(self, savedProfiles[reverseListCount])
                # print(savedProfiles[reverseListCount])

        #fill side panel with buttons
        for x in range(6):
            StartingScreen.AddFillerButtons(self)

    def AddProfileButtons(self, profile):
        #variables
        # totalButtons = len(self.ids.testBoxLayout2.children)

        #create button
        newButton = Button()
        newButton.size_hint_y = None
        newButton.height = 40
        newButton.text = profile['name']
        newButton.bind(on_press=lambda *args: EditProfileScreen.FillTextInputWithData(self, profile))
        # newButton.size_hint_x = None
        # newButton.width = 200
        # newButton.pos_hint = {'x':.349, 'y':0}
        # newButton.text = "#" + str(totalButtons) + " " + profile['name']
        # newButton.background_color = 'white'

        #add button
        self.ids.testBoxLayout2.add_widget(newButton)

    def DeleteProfile(self):
        #variables
        name = self.ti1.text
        youtube = self.ti2.text
        twitter = self.ti3.text
        profiles = fetch_saved_profiles()

        #prints
        # print(name)
        # print(youtube)
        # print(twitter)
        # print(profiles)

        #remove profile from list
        for p in profiles:
            if p['name'] == name:
                # print(p['id'] - 1)
                profiles.pop(p['id'] - 1)

        #remove widget from list
        for b in self.bl3.children:
            # print(str(b) + " " + b.text)
            if b.text == name:
                # self.remove_widget(b)
                b.size_hint_y = 0
        
        #add new profile to json file
        out_file = open("profiles.json", "w")
        json.dump(profiles, out_file, indent = 6)
        out_file.close()

        #clear text inputs
        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""

    def FillTextInputWithData(self, profile):
        #set text input data
        self.ti1.text = profile['name']
        self.ti2.text = profile['youtube']
        self.ti3.text = profile['twitter']

class mainApp(App): #the Base Class of our Kivy App
    def build(self):
        #set window title
        self.title = "Scraper News " + str(year_progress())
        
        #screen manager
        sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(StartingScreen(name='start'))
        sm.add_widget(AddProfileScreen(name='add'))    
        sm.add_widget(EditProfileScreen(name='edit'))    
        # sm.current = 'edit'
        return sm
  
#run kivy app
if __name__ == '__main__':
    mainApp().run()
