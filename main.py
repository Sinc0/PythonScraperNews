### imports ###
import requests
import re
import twint
import time
import datetime
import json
from threading import Thread
import time
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.config import Config #what is this?
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition

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

### globals ###
youtubeVideos = []
youtubeVideoCounter = 0

### functions ###
def fetch_youtube_channel(url, self):
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
        # print("youtube channel fetch succesful")
        requestResultText = str(httpRequest.text)
        requestResultText = requestResultText.encode('utf8', 'ignore')
        # requestResultText = requestResultText.decode('utf8', 'ignore')
        # print(requestResultText)
        with open('test.txt', 'w') as f:
            f.write(str(requestResultText))

        formatChannelTitle1 = re.findall(r'<title>.*YouTube</title>', str(requestResultText))
        formatChannelTitle2 = str(formatChannelTitle1[0])
        formatChannelTitle3 = formatChannelTitle2[7:]
        channelTitle = formatChannelTitle3[:-18]
        # print(channelTitle + " latest videos:")
    else:
        print("youtube channel fetch failed")

    try:
        #regex youtube video data
        requestResultText = str(requestResultText).replace("\\u0026", "&")
        regexYoutubeVideos = re.findall(r'"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"', requestResultText)

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
            if youtubeVideoCounter < 10:
                # print(" " + str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
                # print("#" + str(youtubeVideoCounter) + " - " + "youtube" + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))
                print(" " + "youtube" + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))
                self.ids.svLabel.text += "\n" + "youtube" + " - " + str(formatedUploadDate) + ": " + str(formatedTitle) + "\n"
                self.ids.svScrollBar.scroll_y = 0
            # else:
            #     print(str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
    except:
        print("youtube channel does not exist")

def fetch_twitter_profile(username, self):
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
            print(" " + "twitter" + " - " + t.datestamp + " - " + t.tweet)
            self.ids.svLabel.text += "\n" + "twitter" + " - " + t.datestamp.replace("-", "/") + ": " + t.tweet + "\n"
            self.ids.svScrollBar.scroll_y = 0
        
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
    May = 31 + 28 + 31+ 30 + 31
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

    #check day of year
    if month == 9:
        dayOfTheYear = AUG + day

    #check percentage of year
    percentageOfYear = dayOfTheYear / totalDaysThisYear
    
    #check month name
    if month == 1: month = "JAN"
    if month == 2: month = "FEB"
    if month == 3: month = "MAR"
    if month == 4: month = "APR"
    if month == 5: month = "MAY"
    if month == 6: month = "JUN"
    if month == 7: month = "JUL"
    if month == 8: month = "AUG"
    if month == 9: month = "SEP"
    if month == 10: month = "OCT"
    if month == 11: month = "NOV"
    if month == 12: month = "DEC"
    
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
    
    for p in profiles:
        if p['name'] == name:
            print(p['name'])
            self.ids.svLabel.text = ""
            self.ids.svLabel.text = p['name']
            self.ids.svScrollBar.scroll_y = 0
            fetch_youtube_channel(p['youtube'], self)
            fetch_twitter_profile(p['twitter'], self)

    print("")

def fetch_saved_profiles():
    #fetch all saved profiles from profiles.json if exists
    file = open('profiles.json', "r")
    profiles = json.load(file)
    return profiles

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

### kivy ###
#settings
kivy.require('2.0.0') 
#Config.set('graphics', 'resizable', 1)
#Config.set('graphics', 'width', '200')
#Config.set('graphics', 'height', '200')

#classes
class StartingScreen(Screen):   
    def __init__(self, **var_args):
        super(StartingScreen, self).__init__(**var_args) # that has been overwritten in a class object. to inherited methods from a parent or sibling class super function can be used to gain access
        #variables
        savedProfiles = fetch_saved_profiles()
        yearProgress = year_progress().replace(" - ", "\n- ")

        #add welcome message
        self.lb1.text = "Year Progress" + "\n"
        self.lb1.text += "- " + yearProgress + "\n\n"
        self.lb1.text += "Saved Profiles"
        
        #add buttons
        for p in savedProfiles:
            # StartingScreen.testAddProfileButtons(self, p)
            self.lb1.text += "\n" + "- " + p['name']

        # print("saved profiles json: " + str(savedProfiles))
        # print("total saved profiles: " + str(len(savedProfiles)))
    

    def on_pre_enter(self, *args):
        print("StartingScreen")
        
        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        print("total saved profiles: " + str(len(savedProfiles)))

        # add buttons
        for p in savedProfiles:
            # print(str(p))
            StartingScreen.testAddProfileButtons(self, p, totalSavedProfiles)

    def printNewsFeed(self, profile, selfObj):
        print(profile)
        print(selfObj)
        fetch_news_feed(profile['name'], selfObj)

    def startThreadPrintNewsFeed(self, *args):
        profile = args[0]
        # print(profile['name'])
        Thread(target=self.printNewsFeed, kwargs={"profile": profile, "selfObj": self}).start()
    
    def testAddScrollViewText(self):
        self.ids.svLabel.text += "\n" + "aksdakskdaskd"
        self.ids.svScrollBar.scroll_y = 0

    def testAddProfileButtons(self, profile, totalSavedProfiles):
        totalButtons = len(self.bl1.children)
        print("total buttons: " + str(totalButtons))

        if(totalButtons != totalSavedProfiles + 2):
            newButton = Button()
            newButton.size_hint_y = None
            newButton.text = "#" + str(totalButtons - 1)
            # newButton.bind(on_press = self.startThreadPrintNewsFeed)
            newButton.bind(on_press=lambda *args: self.startThreadPrintNewsFeed(profile))
            self.bl1.add_widget(newButton)

    def testAddProfileButtons2(self, totalSavedProfiles):
        totalButtons = len(self.bl2.children)
        # print(totalButtons)
        
        if(totalButtons != totalSavedProfiles + 2):
            newButton = Button()
            newButton.size_hint_y = None
            newButton.text = "#" + str(totalButtons - 1)
            newButton.disabled = True
            self.bl2.add_widget(newButton)

    def testAddProfileButtons3(self):
        totalButtons = len(self.bl1.children)
        print("total buttons: " + str(totalButtons))
        
        newButton = Button()
        newButton.size_hint_y = None
        newButton.text = "#" + str(totalButtons - 1)

        self.bl1.add_widget(newButton)

    def testAddProfileButtons4(self):
        # totalButtons = len(self.bl1.children)
        # print("total buttons: " + str(totalButtons))
        
        newButton = Button()
        newButton.size_hint_y = None
        newButton.text = "#"

        self.bl1.add_widget(newButton)

class AddProfileScreen(Screen):
    def __init__(self, **var_args):
        super(AddProfileScreen, self).__init__(**var_args) # that has been overwritten in a class object. to inherited methods from a parent or sibling class super function can be used to gain access
    
    def on_pre_enter(self, *args):
        print("AddProfileScreen")

        #variables
        savedProfiles = fetch_saved_profiles()
        totalSavedProfiles = len(savedProfiles)
        
        # add buttons
        for p in savedProfiles:
            StartingScreen.testAddProfileButtons2(self, totalSavedProfiles)

    def fetch_profile_inputs(self):
        profileName = self.ti1.text
        profileTwitter = self.ti2.text
        profileYoutube = self.ti3.text
        print(profileName)
        print(profileTwitter)
        print(profileYoutube)

        add_profile(self, profileName, profileTwitter, profileYoutube)

        self.ti1.text = ""
        self.ti2.text = ""
        self.ti3.text = ""

        self.manager.current = 'start'


class mainApp(App): # the Base Class of our Kivy App
    def build(self):
        self.title = "Scraper News"
        
        #screen manager
        sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(StartingScreen(name='start'))
        sm.add_widget(AddProfileScreen(name='add'))        
        # sm.current = 'add'

        # return a StartingScreen() as a root widget
        return sm
  
# run program
if __name__ == '__main__':
    mainApp().run()
