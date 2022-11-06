######### imports ######
import requests
import re
import time
import datetime
import json
from threading import Thread
import time
import requests
import os
import webbrowser
import pyclip

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

from functools import partial
from bs4 import BeautifulSoup

###### code ######
Builder.load_file("scraperNews.kv") #load kv file
# Builder.load_string("""""") #load string
kivy.require('2.0.0')

#kivy window settings
Config.set('graphics', 'resizable', '1') #changing this might break display resolution
Config.set('graphics', 'fullscreen', '0') #changing this might break display resolution
Config.write()
Window.size = (1000, 700) #width, height

#globals
global counterSTP; counterSTP = -1 # saved twitter posts
global counterSYP; counterSYP = -1 # saved youtube posts
global counterTNS; counterTNS = 1 # total news card

#variables
savedTwitterPosts = []
savedYoutubePosts = []

def displayNewsCard(self, id, username, type, platform, profileData):
    #debugging
    # print(type)
    # print(profileData)
    # print(platform)
    
    #check card pos
    if id == 1: 
        cardObj = self.ids.newsCard1Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard1; 
        cardObj.order = 1
    elif id == 2: 
        cardObj = self.ids.newsCard2Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard2; 
        cardObj.order = 2
    elif id == 3: 
        cardObj = self.ids.newsCard3Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard3; 
        cardObj.order = 3

    #check platform
    if platform == "twitter": 
        cardObj.type = "twitter"
        cardObj.text = "Twitter · No posts found for " + username #update text
    elif platform == "youtube": 
        cardObj.text = "Youtube · No posts found for " + username #update text
        cardObj.type = "youtube"
    
    #check data
    if profileData != "null" and platform == "twitter":
        cardObj.text = "Twitter · Click arrows to start..."
    elif profileData != "null" and platform == "youtube":
        cardObj.text = "Youtube · Click arrows to start..."
    
    #display card    
    boxlayoutObj.opacity = 1
    cardObj.opacity = 1


def undisplayNewsCard(self, id):
    if id == 1: 
        self.ids.boxLayoutNewsCard1.opacity = 0
    elif id == 2: 
        self.ids.boxLayoutNewsCard2.opacity = 0
    elif id == 3: 
        self.ids.boxLayoutNewsCard3.opacity = 0


def fetch_youtube_channel(url, self, name):
    #null check
    if url == "": print("youtube channel is null"); return
    elif 'http' not in url: print("youtube channel is null"); return

    #variables
    global savedYoutubePosts
    global counterSYP
    global counterTNS
    requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    channelTitle = ""
    youtubeVideoCounter = 0
    savedYoutubePosts = []
    counterSYP = -1
    # numberOfVideosLimit = 3

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
    else:
        print("youtube channel fetch failed")

    #create txt file
    # with open("Output.txt", "w") as text_file:
    #     text_file.write(str(requestResultText))
    # return

    #regex youtube video data
    requestResultText = str(requestResultText)
    requestResultText = str(requestResultText).replace("\\u0026", "&")
    regexYoutubeVideos = re.findall(r"\"title\":{\"runs\":\[{\"text\":\"[\w\d\s;:!&#$%€&,.\"?+*=\\/()}{´`¨'@£¤\-_|<>^¨]*\"}],\"a", requestResultText)
    regexYoutubeLink = re.findall(r'{\"url\":\"/watch\?v=[\w\d\-_\\/#+?&]*.', requestResultText)
    regexYoutubeUploadDate = re.findall(r'{\"simpleText\":\"[\w\d\s]*ago\"}', requestResultText)
    
    #debugging
    print(str(len(regexYoutubeVideos)))
    print(str(len(regexYoutubeLink)))
    print(str(len(regexYoutubeUploadDate)))
    
    #variables
    totalYoutubeVideos = len(regexYoutubeVideos)
    
    #null check
    if totalYoutubeVideos == 0:
        print("0 youtube posts found for: " + name)
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "youtube", "null")).start() #display card
        return
    
    #sort video info
    elif totalYoutubeVideos > 0:
        for videoTitle in regexYoutubeVideos:
            #variables
            youtubeVideoCounter += 1
            youtubeTotalVideos = str(len(regexYoutubeVideos))

            #format title
            regexYoutubeTitle = re.findall(r'"text":"[^.]*"}],"', videoTitle)
            formatYoutubeTitle = str(regexYoutubeTitle)
            formatYoutubeTitle = formatYoutubeTitle.replace("\"}],\"']", "").replace("['\"text\":\"", "")
            formatYoutubeTitle = formatYoutubeTitle.replace("\\\\\"", "").replace("\\\\", "").replace("\\", "")
            formatYoutubeTitle = formatYoutubeTitle.replace("   ", " ").replace("  ", " ")

            #format date
            formatYoutubeUploadDate = str(regexYoutubeUploadDate[youtubeVideoCounter - 1])
            formatYoutubeUploadDate = formatYoutubeUploadDate.replace('{"simpleText":"', "").replace('\"}', "")
            
            #format link
            formatYoutubeLink = str(regexYoutubeLink[youtubeVideoCounter - 1])
            formatYoutubeLink = formatYoutubeLink.replace("{\"url\":\"", "").replace("\"", "")
            formatYoutubeLink = "https://www.youtube.com" + formatYoutubeLink # piped.kavin.rocks/

            #create post obj
            post = {
                "id": str(youtubeVideoCounter),
                "user": str(name),
                "title": str(formatYoutubeTitle),
                "date": str(formatYoutubeUploadDate),
                "link": str(formatYoutubeLink)
            }

            #add post
            savedYoutubePosts.append(post)

        #update news card content       
        counterSYP = -1
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "youtube", savedYoutubePosts[0])).start() #display card


def nitterFilterPost(type, obj, link):
    #replace characters
    link = str(link)
    link = link.replace(" ", "-")
    link = link.replace("NEW-VIDEO---", "")
    link = link[0:20]
    
    #select filter type
    if type == "text":
        #regex
        text = re.findall(r'<div class="tweet-content media-body" dir="auto">.*', obj); text = str(text)

        #format text
        if(len(text) > 0):
            text = str(text)
            text = text.replace("\\\\\\", "")
            text = text.replace("\\\\n\\\\n", "\n")
            text = text.replace("\\\\n", "\n")
            text = text.replace(": - ", ": ")
            text = text.replace("['<div class=\"tweet-content media-body\" dir=\"auto\">", "")
            text = text.replace("</div>']", "")
            text = text.replace("']", "")
            text = text.replace("\\'", "'")
            text = text.replace("https://", "")
            text = text.replace("piped.kavin.rocks/", "youtube.com/watch?v=")
            # text = text.split('">')[0]
            # does not filter out comments # ex: <a href="youtube.com/watch?v=QsHuE0LOPIY">youtube.com/watch?v=QsHuE0LOPIY</a>
            # @.*[^</a>]
            # <a href=".*@.*</a>
            return text

        #null check
        elif(len(text) == 0): return "False"

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
            link = "https://nitter.net/" + link
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
                vid = "https://nitter.net/" + vid
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
                # img = "https://nitter.net/" + img
                # img_data = requests.get(img).content
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


def fetch_twitter_profile(username, self, name):
    #null check
    if username == "":
        print("twitter username is null"); 
        return

    #variables
    global savedTwitterPosts
    global counterSTP
    savedTwitterPosts = []
    counterSTP = -1
    numberOfTweetsLimit = 3

    #request twitter profile
    httpRequest = requests.get("https://nitter.net/" + username) #nitter certificate expired 2022/Oct/30
    
    #handle request result
    if httpRequest.status_code == 200:
        #variables
        requestResultText = str(httpRequest.text)

        #debugging
        # print(requestResultText)

        #parse html
        className = "timeline-item"
        soup = BeautifulSoup(requestResultText, 'html.parser')
        tweets = soup.find_all('div', class_=className)
        print(className + ": " + str(len(tweets)))

        #handle tweets
        count = 0
        for obj in tweets:
            obj = str(obj)

            #filter post text
            link = nitterFilterPost("link", obj, False)
            date = nitterFilterPost("date", obj, link)
            pinned = nitterFilterPost("pinned", obj, link)
            retweet = nitterFilterPost("retweet", obj, link)
            text = nitterFilterPost("text", obj, link)
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
            if pinned != "True" and retweet != "True":
                count = count + 1
                post = {
                    "id": count,
                    "username": username,
                    "link": link,
                    "date": date,
                    "pinned": pinned,
                    "retweet": retweet,
                    "text": text,
                    "youtube": youtube,
                    "poll": poll,
                    "images": images,
                    "videos": videos
                }
                savedTwitterPosts.append(post)

        #debugging
        print(str(len(savedTwitterPosts)))
        
        if len(savedTwitterPosts) == 0:
            print("0 twitter posts found for: " + name)

            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "twitter", "null")).start() #display card
            return

        elif len(savedTwitterPosts) > 0:
            #update card
            username = str(savedTwitterPosts[0]["username"])
            id = "Twitter" + " · " + str(savedTwitterPosts[0]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[0]["date"])
            text = str(savedTwitterPosts[0]["text"])
            images = savedTwitterPosts[counterSTP]["images"]
            videos = savedTwitterPosts[counterSTP]["videos"]
            youtube = str(savedTwitterPosts[counterSTP]["youtube"])

            #add links to card
            count = 0
            if savedTwitterPosts[0]["images"] != "False":
                None 
                # for img in images:
                #     count = count + 1
                #     img = img.replace("%3Fname%3Dsmall", "")
                #     cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + img
                # cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + images
            if savedTwitterPosts[0]["videos"] != "False": 
                count = count + 1
                video = videos[0]
                video = video.replace("https://", "")
                video = video.replace("http://", "")
                video = video.replace("http://", "")
                video = video.replace("www.", "")
                # cardText = cardText + "\n" + str(count) + ": " + video
            if savedTwitterPosts[0]["youtube"] != "False": 
                count = count + 1
                youtube = youtube.replace("https://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("www.", "")
                # cardText = cardText + "\n" + str(count) + ": " + youtube

            counterSTP = -1
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "twitter", savedTwitterPosts[0])).start() #display card
    

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

            global counterTNS
            twitter = p['twitter']
            youtube = p['youtube']
            
            counterTNS = 1
            # fetch_twitter_profile(p['twitter'], self, name)
            # fetch_youtube_channel(p['youtube'], self, name)
            # return

            if p['twitter'] != "" and p['youtube'] != "":
                counterTNS = 1
                fetch_twitter_profile(p['twitter'], self, name)
                counterTNS = 2
                fetch_youtube_channel(p['youtube'], self, name)

            elif p['twitter'] == "":
                counterTNS = 1
                fetch_youtube_channel(p['youtube'], self, name)

            elif p['youtube'] == "":
                counterTNS = 1
                fetch_twitter_profile(p['twitter'], self, name)

            


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



###### kivy ######
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
                background_normal =  os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg",
                background_down =  os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg",
                size_hint_y = None,
                opacity = 0.9,
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


    def saveToFavorites(screen, self, type):
        # print(savedTwitterPosts[counterSTP])
        # print(savedYoutubePosts[counterSYP])
        
        if type == "twitter":
            if len(savedTwitterPosts) == 0: 
                return

            elif len(savedTwitterPosts) > 0:
                post = savedTwitterPosts[counterSTP]

                #create button id
                id = post['username'] + post['text'] + post['date']
                id = id.replace(" ", "").replace("_", "").replace("-", "").replace("\n", "").replace("·", "").replace("u00b7", "")
                id = id[0:60]

                newFavorite = {
                    "id": id,
                    "profile": post['username'], 
                    "date": post['date'],
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['text'],
                    "img": "/thumbnails/" + post['username'] + ".jpg",
                    "link": post['link']
                }

        elif type == "youtube":
            post = savedYoutubePosts[counterSYP]

            if len(savedYoutubePosts) == 0: 
                return

            elif len(savedYoutubePosts) > 0:
                #create button id
                id = post['user'] + post['title'] + post['date']
                id = id.replace(" ", "").replace("_", "").replace("-", "").replace("\n", "").replace("·", "").replace("u00b7", "")
                id = id[0:60]

                newFavorite = {
                    "id": id,
                    "profile": post['user'],
                    "date": post['date'], 
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['title'],
                    "img": "/thumbnails/" + post['user'] + ".jpg",
                    "link": post['link']
                }
        
        #fetch favorites from favorites.json
        file = open('favorites.json', "r")
        favorites = json.load(file)
        totalFavorites = len(favorites)

        #check if favorite already saved
        for f in favorites:
            if f['id'] == id: print('news card already saved'); return
        
        #save favorite
        favorites.append(newFavorite)
        out_file = open("favorites.json", "w")
        json.dump(favorites, out_file, indent = 6)
        out_file.close()
        

    def removeFromFavorites(self, cardId):
        print("removeFromFavorites")
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
        obj = args[0]
        id = obj['id']
        profile = obj['profile']
        platform = obj['platform']
        savedAt = obj['savedAt']
        text = obj['text']
        img = obj['img']
        date = obj['date']
        link = obj['link']

        if platform == "twitter": platform = "Twitter"
        elif platform == "youtube": platform = "Youtube"

        #create boxlayout
        bl = BoxLayout(
            orientation = "horizontal", 
            size_hint_x = None, 
            size_hint_y = None,
            height = 240,
            width = 600,
            # spacing = (40, 40),
            # padding = (40, 40)
        )

        #fetch favorites from favorites.json
        file = open('favorites.json', "r")
        favorites = json.load(file)

        #create profile image button
        btnProfileImg = Button(
            size_hint_x = None, 
            size_hint_y = None, 
            height = 220, 
            width = 220, 
            background_normal =  os.getcwd() + "/thumbnails/" + profile + ".jpg",
            color = 'lightgray'
        )
        
        #create remove button
        btn1 = Button(
            text = "-", 
            size_hint_y = 0.5,
            size_hint_x = None, 
            width = 70, 
            background_color = get_color_from_hex('#0e1012'), 
            background_normal = 'transparent',
            background_down = 'transparent',
            font_size = 19,
            color = 'lightgray',
            opacity = 0.9
            # height = 110,
        )

        btn2 = Button(
            text = "§", 
            size_hint_y = 0.5,
            size_hint_x = None, 
            width = 70, 
            background_color = get_color_from_hex('#0e1012'), 
            background_normal = 'transparent',
            background_down = 'transparent',
            font_size = 19,
            color = 'lightgray',
            opacity = 0.9
            # height = 110,
        )

        #create boxlayout
        sl = StackLayout(
            orientation = "tb-lr", 
            size_hint_y = 0.917,
            size_hint_x = None, 
            # height = 300,
            # width = 600,
            # spacing = (0, 20),
            # padding = (0, 20)
        )
        
        #bind functions to buttons
        btn1.bind(on_press=lambda *args: StartingScreen.removeFromFavorites(self, id))
        btn2.bind(on_press=lambda *args: StartingScreen.copyToClipboard(self, link))

        #create news card
        btnNewsCard = Button(
            text = "Saved: " + savedAt + "\n" + platform + " · " + profile + " · " + date + "\n\n" + text,
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
            background_color = get_color_from_hex("#0e1012"), # #292f33
            background_normal = 'transparent',
            background_down = 'transparent',
            bold = True,
            font_size = 16,
            opacity = 0.9
            )

        #add widgets to boxlayout
        bl.add_widget(btnProfileImg)
        bl.add_widget(btnNewsCard)
        sl.add_widget(btn2)
        sl.add_widget(btn1)
        bl.add_widget(sl)

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

    
    def twitterNextPost(self, order):
        print("twitterNextPost")
        #variables
        global counterSTP
        totalTwitterPosts = len(savedTwitterPosts)

        if totalTwitterPosts == 0:
            return

        elif totalTwitterPosts > 0:
            #check counter
            if counterSTP == (len(savedTwitterPosts) - 1): 
                counterSTP = -1
            
            #increment counter
            counterSTP = counterSTP + 1; 

            #set card
            username = str(savedTwitterPosts[counterSTP]["username"])
            id = "Twitter" + " · " + str(savedTwitterPosts[counterSTP]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[counterSTP]["date"])
            text = str(savedTwitterPosts[counterSTP]["text"])
            images = savedTwitterPosts[counterSTP]["images"]
            videos = savedTwitterPosts[counterSTP]["videos"]
            youtube = str(savedTwitterPosts[counterSTP]["youtube"])
            cardText = id + " · " + username + " · " + date + "\n\n" + text + "\n"

            #debugging
            print("\n" + str(savedTwitterPosts[counterSTP]))

            
            #add links to card
            count = 0
            if images != "False": 
                for img in images:
                    count = count + 1
                    img = img.replace("%3Fname%3Dsmall", "")
                    cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + img
            if videos != "False": 
                count = count + 1
                video = videos[0]
                video = video.replace("https://", "")
                video = video.replace("http://", "")
                video = video.replace("http://", "")
                video = video.replace("www.", "")
                cardText = cardText + "\n" + str(count) + ": " + video
            if youtube != "False": 
                count = count + 1
                youtube = youtube.replace("https://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("www.", "")
                cardText = cardText + "\n" + str(count) + ": " + youtube
            
            #update card text
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post

            card.text = cardText
        
    
    def twitterPreviousPost(self, order):
        print("twitterPreviousPost")
        #variables
        global counterSTP
        totalTwitterPosts = len(savedTwitterPosts)

        if totalTwitterPosts == 0:
            return

        elif totalTwitterPosts > 0:
            #check counter
            if counterSTP == 0: 
                counterSTP = len(savedTwitterPosts)

            #decrement counter
            if counterSTP != 0: 
                counterSTP = counterSTP - 1

            #debugging
            print("\n" + str(savedTwitterPosts[counterSTP]))
            
            #set card
            username = str(savedTwitterPosts[counterSTP]["username"])
            id = "Twitter" + " · " + str(savedTwitterPosts[counterSTP]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[counterSTP]["date"])
            text = str(savedTwitterPosts[counterSTP]["text"])
            images = savedTwitterPosts[counterSTP]["images"]
            videos = savedTwitterPosts[counterSTP]["videos"]
            youtube = str(savedTwitterPosts[counterSTP]["youtube"])
            cardText = id + " · " + username + " · " + date + "\n\n" + text + "\n"
            
            #add links to card
            count = 0
            if images != "False": 
                for img in images:
                    count = count + 1
                    img = img.replace("%3Fname%3Dsmall", "")
                    cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + img
            if videos != "False": 
                count = count + 1
                video = videos[0]
                video = video.replace("https://", "")
                video = video.replace("http://", "")
                video = video.replace("http://", "")
                video = video.replace("www.", "")
                cardText = cardText + "\n" + str(count) + ": " + video
            if youtube != "False": 
                count = count + 1
                youtube = youtube.replace("https://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("http://", "")
                youtube = youtube.replace("www.", "")
                cardText = cardText + "\n" + str(count) + ": " + youtube

            #update card text
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post

            card.text = cardText

    def youtubeNextPost(self, order):
        print("youtubeNextPost")
        #variables
        global counterSYP
        totalYoutubeVideos = len(savedYoutubePosts)

        if totalYoutubeVideos == 0:
            return

        elif totalYoutubeVideos > 0:
            #check counter
            if counterSYP == (len(savedYoutubePosts) - 1): 
                counterSYP = -1

            #increment counter
            counterSYP = counterSYP + 1

            #debugging
            print("\n" + str(savedYoutubePosts[counterSYP]))

            #update card text
            cardText = "Youtube" + " · " + savedYoutubePosts[counterSYP]['id'] + "/" + str(totalYoutubeVideos) + " · " + savedYoutubePosts[counterSYP]['user'] + " · " + savedYoutubePosts[counterSYP]['date'] + "\n\n" + savedYoutubePosts[counterSYP]['title']
            
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post

            card.text = cardText

    def youtubePreviousPost(self, order):
        print("youtubePreviousPost")
        #variables
        global counterSYP
        totalYoutubeVideos = len(savedYoutubePosts)

        if totalYoutubeVideos == 0:
            return

        elif totalYoutubeVideos > 0:
            #check counter
            if counterSYP == 0: counterSYP = len(savedYoutubePosts)

            #decrement counter
            if counterSYP != 0: 
                counterSYP = counterSYP - 1

            #debugging
            print("\n" + str(savedYoutubePosts[counterSYP]))

            #update card text
            cardText = "Youtube" + " · " + savedYoutubePosts[counterSYP]['id'] + "/" + str(totalYoutubeVideos) + " · " + savedYoutubePosts[counterSYP]['user'] + " · " + savedYoutubePosts[counterSYP]['date'] + "\n\n" + savedYoutubePosts[counterSYP]['title']
            
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post

            card.text = cardText

    def copyToClipboard(self, type):
        print("copyToClipboard")
        # Linux on x11 (xclip)
        # Linux on wayland (wl-clipboard)

        if type == "twitter" and len(savedTwitterPosts) != 0:
            pyclip.copy(savedTwitterPosts[counterSTP]['link'])
            cb_text = pyclip.paste(text=True)
            print(cb_text)
            
        elif type == "youtube" and len(savedYoutubePosts) != 0:
            pyclip.copy(savedYoutubePosts[counterSYP]['link'])
            cb_text = pyclip.paste(text=True)
            print(cb_text)

        else:
            pyclip.copy(type)
            cb_text = pyclip.paste(text=True)
            print(cb_text) 
        
    def nextPost(self, order, type):
        # print("nextPost")
        # print(order, type)
        
        if type == "youtube": self.youtubeNextPost(order)
        elif type == "twitter": self.twitterNextPost(order)
        
    def previousPost(self, order, type):
        # print("nextPost")
        # print(order, type)
        
        if type == "youtube": self.youtubePreviousPost(order)
        elif type == "twitter": self.twitterPreviousPost(order)



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
        for fav in favorites[::-1]:
            if totalButtons < totalFavorites:
                # savedAt =  "Saved " + str(fav['savedAt']) + ": "
                bl = StartingScreen.createNewsCard(self, fav)
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



###### start app ######
if __name__ == '__main__':
    scraperNewsApp().run()
