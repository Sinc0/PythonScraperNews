#------ IMPORTS ------#
import requests
import re
import datetime
import json
import os
import pyclip
import kivy
import emoji
from threading import Thread
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.utils import get_color_from_hex
from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window


#------ LOAD KIVY UI ------#
Builder.load_file("ScraperNews.kv")
# Builder.load_string("""""")


#------ GLOBALS ------#
COUNTER_SAVED_X_POSTS = -1
COUNTER_SAVED_YOUTUBE_POSTS = -1
COUNTER_SAVED_NEWS_ARTICLES = -1
COUNTER_SAVED_SUBREDDIT_POSTS = -1
COUNTER_TOTAL_NEWS_CARD = 1
TOTAL_POSTS_TWITTER = 0
TOTAL_POSTS_YOUTUBE = 0
TOTAL_POSTS_ARTICLES = 0
TOTAL_POSTS_SUBREDDIT = 0
SAVED_POSTS_TWITTER = []
SAVED_POSTS_YOUTUBE = []
SAVED_POSTS_ARTICLES = []
SAVED_POSTS_SUBREDDIT = []
DOMAIN_TWITTER = "https://nitter.lucabased.xyz"
DOMAIN_REDDIT = "https://libreddit.privacydev.net"
DOMAIN_YOUTUBE = "https://invidious.privacyredirect.com"
DOMAIN_ARTICLES = "https://search.brave.com"
DOMAIN_PROFILE_PIC = "https://wikiless.privacyredirect.com"
LIMIT_ARTICLES = 10
LIMIT_YOUTUBE_POSTS = 10
LIMIT_TWEETS = 10
LIMIT_SUBREDDIT_POSTS = 10
LIMIT_DEFAULT_TIMEOUT = 10


#------ FUNCTIONS ------#
def year_progress():
    
    #variables
    leapYear = False
    totalDaysThisYear = 365
    daysInFeb = 28
    dateObj = datetime.datetime.now()
    year = dateObj.year
    month = dateObj.month
    day = dateObj.day

    #check if leap year
    if year == 2024: leapYear = True
        
    #year is leap year
    if leapYear == True: 
        totalDaysThisYear = 366
        daysInFeb = 29

    #set month total days
    JAN = 31
    FEB = daysInFeb + JAN 
    MAR = 31 + FEB
    APR = 30 + MAR
    MAY = 31 + APR
    JUN = 30 + MAY 
    JUL = 31 + JUN
    AUG = 31 + JUL
    SEP = 30 + AUG 
    OCT = 31 + SEP 
    NOV = 30 + OCT 
    DEC = 31 + NOV

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
    formattedDate = str(day) + " " + str(month) + " " + str(year) + " · " + "Day " + str(dayOfTheYear) + "/" + str(totalDaysThisYear)
    
    return formattedDate


def screenChange(self, type):
    if type == "add": self.manager.current = 'add'
    elif type == "edit": self.manager.current = 'edit'
    elif type == "start": self.manager.current = 'start'
    elif type == "favorites": self.manager.current = 'favorites'
    elif type == "menu": self.manager.current = 'menu'


def screenRefresh(self, screenName):
    self.manager.current = 'blank' #change to blank screen
    self.manager.current = screenName #change back to previous screen


def fetch_news_feed(profile, self):
    
    #variables
    name = profile['name']
    twitter = profile['twitter']
    youtube = profile['youtube']
    articles = profile['articles']
    subreddit = profile['subreddit']
    youtube = str(youtube).replace("https://www.youtube.com/", "").replace("youtube.com", "").replace("/videos", "")
    profiles = json.load(open('data/profiles.json', "r"))
    articlesExists = False
    youtubeExists = False
    twitterExists = False
    subredditExists = False

    #reset stored values
    setGlobal("COUNTER_TOTAL_NEWS_CARD", 0)
    setGlobal("SAVED_POSTS_TWITTER", [], "assign")
    setGlobal("SAVED_POSTS_YOUTUBE", [], "assign")
    setGlobal("SAVED_POSTS_SUBREDDIT", [], "assign")
    setGlobal("SAVED_POSTS_ARTICLES", [], "assign")
    setGlobal("LIMIT_ARTICLES", 10)
    setGlobal("LIMIT_YOUTUBE_POSTS", 10)
    setGlobal("LIMIT_TWEETS", 10)
    setGlobal("LIMIT_SUBREDDIT_POSTS", 10)

    #update UI: reset news card text
    self.ids.newsCard1Post.text = ""
    self.ids.newsCard2Post.text = ""
    self.ids.newsCard3Post.text = ""
    self.ids.newsCard4Post.text = ""

    #update UI: undisplay news card
    Thread(target=lambda : newsCardHide(self, 1)).start()
    Thread(target=lambda : newsCardHide(self, 2)).start()
    Thread(target=lambda : newsCardHide(self, 3)).start()
    Thread(target=lambda : newsCardHide(self, 4)).start()

    #check if domains are available
    # checkDomainStatus()

    #fetch profile news
    for profile in profiles:
        if profile['name'] == name:
            print("fetch news feed: " + name.upper()) #log 

            #check if posts exists
            if articles != "": articlesExists = True 
            if youtube != "": youtubeExists = True 
            if twitter != "": twitterExists = True 
            if subreddit != "": subredditExists = True 

            #ARTICLES
            if articlesExists == True:
                self.ids.category1.text = "Loading Articles..."
                setGlobal("COUNTER_TOTAL_NEWS_CARD", COUNTER_TOTAL_NEWS_CARD + 1)
                fetch_news_articles(self, articles, profile)

            #YOUTUBE
            if youtubeExists == True:
                self.ids.category1.text = "Loading YouTube..."
                setGlobal("COUNTER_TOTAL_NEWS_CARD", COUNTER_TOTAL_NEWS_CARD + 1)
                fetch_youtube_channel(self, profile)

            #TWITTER
            if twitterExists == True:
                self.ids.category1.text = "Loading X..."
                setGlobal("COUNTER_TOTAL_NEWS_CARD", COUNTER_TOTAL_NEWS_CARD + 1)
                fetch_twitter_profile(self, twitter, profile)
            
            #REDDIT
            if subredditExists == True:
                self.ids.category1.text = "Loading Subreddit..."
                setGlobal("COUNTER_TOTAL_NEWS_CARD", COUNTER_TOTAL_NEWS_CARD + 1)
                fetch_subreddit(self, subreddit, profile)

            #update UI: set profile name
            self.ids.category1.text = name.upper()
    
    #log
    print("- Articles: " + str(articlesExists) + ", " + str(TOTAL_POSTS_ARTICLES))
    print("- Youtube: " + str(youtubeExists) + ", " + str(TOTAL_POSTS_SUBREDDIT))
    print("- Twitter: " + str(twitterExists) + ", " + str(TOTAL_POSTS_TWITTER))
    print("- Subreddit: " + str(subredditExists) + ", " + str(TOTAL_POSTS_YOUTUBE))


def fetch_news_articles(self, name, profile):
    
    try:
        #variables
        setGlobal("COUNTER_SAVED_NEWS_ARTICLES", -1)
        totalNewsLinks = 0
        newsArticleObjects = []
        counter = 0
        
        #request news articles
        httpRequest = requests.get(DOMAIN_ARTICLES + "/news?q=" + name, timeout=LIMIT_DEFAULT_TIMEOUT)
        
        #regex articles data
        regexNewsTitles = re.findall(r'line-clamp-2  heading-serpresult">[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”|‘]*', httpRequest.text)
        regexNewsLinks = re.findall(r'<a href="[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”|]*<span class=\"snippet-title', httpRequest.text)
        regexNewsDate = re.findall(r'<span class="attr">[\w\d\s]*', httpRequest.text)
        regexNewsPublisher = re.findall(r'>[\w\d\s.\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#\"\'\\’=>\[\]“”|]*</span></div> <span class="attr', httpRequest.text)
        totalNewsLinks = len(regexNewsLinks)
        
        #debugging
        # print(httpRequest.text)
        # print("regexNewsTitles: " + str(len(regexNewsTitles)))
        # print("regexNewsLinks: " + str(len(regexNewsLinks)))
        # print("regexNewsDate: " + str(len(regexNewsDate)))
        # print("regexNewsPublisher: " + str(len(regexNewsPublisher)))

        #add news articles objects
        for item in regexNewsTitles:
            counter += 1
            title = item.replace('line-clamp-2  heading-serpresult">', "").replace("</span>" , "").replace("</a>", "").replace("&amp;", "&")
            title = title.split(" | ")[0].split(" - ")[0].split(" : ")[0]
            link = regexNewsLinks[counter - 1].split("class=\"")[0].replace('<a href="', "").replace("\"", "")
            date = regexNewsDate[counter - 1].replace('<span class="attr">', "").replace("</span> </cite>", "")
            publisher = regexNewsPublisher[counter - 1].replace("</span></div> <span class=\"attr", "").replace(">", "")
            newsArticleObjects.append({"id": str(counter), "date": date, "publisher": publisher, "title": str(title), "link": link})
        
        #update globals
        setGlobal("TOTAL_POSTS_ARTICLES", totalNewsLinks)

        #articles null check
        if TOTAL_POSTS_ARTICLES == 0:
            print("0 articles found for: " + name)
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "articles", "null")).start()
            return
        
        #articles exists
        elif TOTAL_POSTS_ARTICLES > 0:
            
            if TOTAL_POSTS_ARTICLES < 10: setGlobal("LIMIT_ARTICLES", TOTAL_POSTS_ARTICLES)

            #add post obj
            for article in newsArticleObjects[0:LIMIT_ARTICLES]:
                post = {
                    "id": article['id'],
                    "title": article['title'],
                    "link": article['link'],
                    "date": article['date'],
                    "publisher": article['publisher'],
                    "type": "article",
                    "profile": profile['name'],
                    "profilepic": profile['profilepic']
                }
                setGlobal("SAVED_POSTS_ARTICLES", post, "add")
                setGlobal("COUNTER_SAVED_NEWS_ARTICLES", -1)

            setGlobal("TOTAL_POSTS_ARTICLES", len(SAVED_POSTS_ARTICLES))

            #update UI
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "article", None)).start()

    #error: fetch news articles failed
    except Exception as e:
        print(e); print("error: fetch news articles failed")
        setGlobal("TOTAL_POSTS_ARTICLES", 0)
        Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "articles", "null")).start()
        return


def fetch_youtube_channel(self, profile):
    
    try:
        #variables
        channelVideoObjects = []
        setGlobal("COUNTER_SAVED_YOUTUBE_POSTS", -1)
        name = profile['name']
        youtubeName = profile['youtube']
        
        #fetch channel id/name
        httpRequest1 = requests.get(DOMAIN_YOUTUBE + "/search?q=" + youtubeName, timeout=LIMIT_DEFAULT_TIMEOUT)
        regexChannelName = re.findall(r'<a href="/channel/[\w\d._-]*">', httpRequest1.text)
        youtubeChannelId = regexChannelName[0].replace('<a href=\"/channel/', "").replace('">', "")

        #fetch channel videos
        httpRequest2 = requests.get(DOMAIN_YOUTUBE + "/channel/" + youtubeChannelId, timeout=LIMIT_DEFAULT_TIMEOUT)
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
        
        #update globals
        setGlobal("TOTAL_POSTS_YOUTUBE", len(channelVideoObjects))

        #youtube videos null check
        if TOTAL_POSTS_YOUTUBE == 0:
            print("0 youtube posts found for: " + name)
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "youtube", "null")).start()
            return
        
        #youtube videos exists
        elif TOTAL_POSTS_YOUTUBE > 0:
            
            #set total cards
            if TOTAL_POSTS_YOUTUBE < 10: setGlobal("LIMIT_YOUTUBE_POSTS", TOTAL_POSTS_YOUTUBE)

            #create/add post objects
            for video in channelVideoObjects[0:LIMIT_YOUTUBE_POSTS]:
                post = {
                    "id": video['id'],
                    "title": video['title'],
                    "date": video['date'],
                    "link": video['link'],
                    "duration": video['duration'],
                    "type": "youtube",
                    "profile": name,
                    "profilepic": profile['profilepic']
                }
                setGlobal("SAVED_POSTS_YOUTUBE", post, "add")

            #update globals
            setGlobal("TOTAL_POSTS_YOUTUBE", len(SAVED_POSTS_YOUTUBE))
            setGlobal("COUNTER_SAVED_YOUTUBE_POSTS", -1)

            #update UI       
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "youtube", SAVED_POSTS_YOUTUBE[0])).start()
    
    #error: fetch youtube channel failed
    except Exception as e:
        print(e); print("youtube channel fetch failed")
        setGlobal("TOTAL_POSTS_YOUTUBE", 0)
        Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "youtube", "null")).start()
        return


def fetch_twitter_profile(self, username, profile):
    
    try:
        #variables
        setGlobal("COUNTER_SAVED_X_POSTS", -1)
        name = profile['name']
        count = 0

        #fetch twitter profile
        httpRequest = requests.get(DOMAIN_TWITTER + "/" + username, timeout=LIMIT_DEFAULT_TIMEOUT)

        #parse html
        className = "timeline-item"
        soup = BeautifulSoup(httpRequest.text, 'html.parser')
        tweets = soup.find_all('div', class_=className)
        
        #handle tweets
        for obj in tweets:

            #filter post text
            obj = str(obj)
            text = twitterFilterPost("text", obj, None)
            link = twitterFilterPost("link", obj, False)
            date = twitterFilterPost("date", obj, link)
            pinned = twitterFilterPost("pinned", obj, link)
            retweet = twitterFilterPost("retweet", obj, link)
            youtube = twitterFilterPost("youtube", obj, link)
            poll = twitterFilterPost("poll", obj, link)
            images = twitterFilterPost("images", obj, text)
            videos = twitterFilterPost("videos", obj, link)

            #post text is empty
            if text == "": None
            
            #post text exists
            elif text != "" and pinned != "True" and retweet != "True":
                count = count + 1
                post = {
                    "id": str(count),
                    "username": username,
                    "link": link,
                    "date": date,
                    "pinned": pinned,
                    "retweet": retweet,
                    "text": text,
                    "title": text,
                    "youtube": youtube,
                    "poll": poll,
                    "images": images,
                    "videos": videos,
                    "type": "twitter",
                    "profile": profile['name'],
                    "profilepic": profile['profilepic']
                }
                setGlobal("SAVED_POSTS_TWITTER", post, "add")

        #update globals
        setGlobal("TOTAL_POSTS_TWITTER", len(SAVED_POSTS_TWITTER))
        if TOTAL_POSTS_TWITTER < LIMIT_TWEETS: setGlobal("LIMIT_TWEETS", TOTAL_POSTS_TWITTER)

        #twitter posts null check
        if TOTAL_POSTS_TWITTER == 0:
            print("0 twitter posts found for: " + name)
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "twitter", "null")).start()
            return

        #twitter posts exists
        elif TOTAL_POSTS_TWITTER > 0:
            setGlobal("COUNTER_SAVED_X_POSTS", -1)
            setGlobal("SAVED_POSTS_TWITTER", SAVED_POSTS_TWITTER[0:LIMIT_TWEETS], 'assign')
            setGlobal("TOTAL_POSTS_TWITTER", LIMIT_TWEETS)
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "twitter", SAVED_POSTS_TWITTER[0])).start()

    #error: fetch twitte profile failed        
    except Exception as e:
        print(e); print("error: twitter profile fetch failed")
        setGlobal("TOTAL_POSTS_TWITTER", 0)
        Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "twitter", "null")).start()
        return


def fetch_subreddit(self, name, profile):

    try:    
        #variables
        setGlobal("COUNTER_SAVED_SUBREDDIT_POSTS", -1)
        totalStickied = 0
        count = 0
        profileName = profile['name']
        profileSubreddit = profile['subreddit']
        profilePic = profile['profilepic']

        #fetch subreddit posts
        httpRequest = requests.get(DOMAIN_REDDIT + "/r/" + name + "/hot", timeout=LIMIT_DEFAULT_TIMEOUT)
        
        #regex subreddit data
        regexTitle = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', httpRequest.text)
        regexLink = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', httpRequest.text)
        regexDate = re.findall(r'<span class="created" title=".*', httpRequest.text)
        regexStickied = re.findall(r'<div class="post stickied".*', httpRequest.text)
        totalStickied = len(regexStickied)
        regexTitle = regexTitle[totalStickied:LIMIT_SUBREDDIT_POSTS + totalStickied]
        regexLink = regexLink[totalStickied:LIMIT_SUBREDDIT_POSTS + totalStickied]
        regexDate = regexDate[totalStickied:LIMIT_SUBREDDIT_POSTS + totalStickied]

        #update globals
        setGlobal("TOTAL_POSTS_SUBREDDIT", len(regexTitle))

        #subreddit posts null check
        if TOTAL_POSTS_SUBREDDIT == 0:
            print("0 subreddit posts found for: " + name)
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "subreddit", "null")).start()
            return
        
        #subreddit posts exists
        elif TOTAL_POSTS_SUBREDDIT > 0:
            
            #set total posts
            if TOTAL_POSTS_SUBREDDIT < 10: setGlobal("LIMIT_SUBREDDIT_POSTS", TOTAL_POSTS_SUBREDDIT)
           
            #format post text
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
                    "profile": profileName,
                    "profilepic": profilePic
                }
                setGlobal("SAVED_POSTS_SUBREDDIT", post, "add")
                
                #increment
                count += 1
            
            #update globals
            setGlobal("TOTAL_POSTS_SUBREDDIT", len(SAVED_POSTS_SUBREDDIT))
            setGlobal("COUNTER_SAVED_SUBREDDIT_POSTS", -1)

            #update UI    
            Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "subreddit", None)).start()
    
    #error: fetch subreddit failed
    except Exception as e:
        print(e); print("error: subreddit fetch failed")
        setGlobal("TOTAL_POSTS_SUBREDDIT", 0)
        Thread(target=lambda : newsCardDisplay(self, COUNTER_TOTAL_NEWS_CARD, "subreddit", "null")).start()
        return


def fetch_saved_file(type):

    if type == "profiles":
        profiles = json.load(open('data/profiles.json', "r"))
        return profiles

    elif type == "favorites":
        favorites = json.load(open('data/favorites.json', "r"))
        return favorites


def fetch_profile_image(name):

    try:
        print("fetch profile image: " + name) #log
        
        #variables
        selectedImage = ""
        fileFormat = ""
        response = requests.get(DOMAIN_PROFILE_PIC + "/wiki/" + name.replace(" ", "%20").lower() + "?lang=en", timeout=LIMIT_DEFAULT_TIMEOUT) #&category_general=&language=auto&time_range=&safesearch=1&theme=simple
        
        #profile image exists
        if response.status_code == 200:
            
            regexImages = re.findall(r'src="/media/wikipedia/commons/thumb/[\w\d\s]*[\w\d\s\-\/%]*.\.[\w]*/[\d]*px-[\w\d\s_%]*.\.[\w\d\s.]*\"', response.text)
            
            for item in regexImages:
                selectedImage = item.replace("src=\"/", "").replace('\"', "")
                selectedImage = DOMAIN_PROFILE_PIC + "/" + selectedImage

                if ".jpg" in selectedImage: fileFormat = ".jpg"
                elif ".png" in selectedImage: fileFormat = ".png"

                httpRequestProfileImage = requests.get(selectedImage, timeout=LIMIT_DEFAULT_TIMEOUT)
                if httpRequestProfileImage.status_code == 200:
                    name = name.replace(" ", "_")
                    file = open(os.getcwd() + '/thumbnails/' + name + fileFormat,'wb')
                    file.write(httpRequestProfileImage.content)
                    file.close()
                    return "/thumbnails/" + name + fileFormat
    
    #error: fetch profile image failed
    except Exception as e:
        print(e); print("error: profile image fetch failed")
        return "/images/fallbackProfilePic.png"


def twitterFilterPost(type, obj, link):
    
    if type == "text":

        #format text
        obj = emoji.demojize(obj) #handle emojis
        obj = obj.replace('<a href="/', '').replace("</a>", "").replace('">@', '@').replace('" title="', ' ').replace("\n\n", "\n").replace("\n", ":newline:")
        obj = re.findall(r'dir="auto">[\w\s\d\/\_\-\:\;\&\!\@\$\,\.\?\%\+\(\)\#~\"\'\\’=>\[\]“”]*', obj)
        obj = str(obj).replace("['dir=\"auto\">", "").replace("<\']", "").replace("&amp;", "&").replace("\\", "").replace("'dir=\"auto\">", "")
        obj = obj.replace("<',", "").replace(".", ". ").replace(":newline:", "\n").replace("search?q=%23", "").replace("::", ",").replace("\">", "")
        obj = obj.replace("  ", " ").replace("']", "").replace(".  ", ". ").replace("&gt;", ">")
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
            link = "https://x.com/" + link # link = DOMAIN_TWITTER + link
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
                vid = DOMAIN_TWITTER + vid
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
                # img = DOMAIN_TWITTER + img
                # img_data = requests.get(img, timeout=LIMIT_DEFAULT_TIMEOUT).content
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


def newsCardDisplay(self, id, platform, profileData):
    
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
    self.change_button_color(id, platform)

    #check platform
    if platform == "twitter": cardObj.type = "twitter"; cardObj.text = "X · No Posts Found... \n\n"
    elif platform == "youtube": cardObj.type = "youtube"; cardObj.text = "YouTube · No Posts Found... \n\n"
    elif platform == "article": cardObj.type = "article"; cardObj.text = "Articles · No Posts Found... \n\n"
    elif platform == "subreddit": cardObj.type = "subreddit"; cardObj.text = "Subreddit · No Posts Found... \n\n"

    #check profile data
    if profileData != "null" and platform == "twitter": cardObj.text = "X · Click to Read... \n\n"
    elif profileData != "null" and platform == "youtube": cardObj.text = "YouTube · Click to Read... \n\n"
    elif profileData != "null" and platform == "article": cardObj.text = "Articles · Click to Read... \n\n"
    elif profileData != "null" and platform == "subreddit": cardObj.text = "Subreddit · Click to Read... \n\n"
    
    #update UI: display card    
    try: boxlayoutObj.opacity = 1; cardObj.opacity = 1
    except: print("- Kivy UI Error")


def newsCardHide(self, id):
    try:
        if id == 1: self.ids.boxLayoutNewsCard1.opacity = 0
        elif id == 2: self.ids.boxLayoutNewsCard2.opacity = 0
        elif id == 3: self.ids.boxLayoutNewsCard3.opacity = 0
        elif id == 4: self.ids.boxLayoutNewsCard4.opacity = 0
    
    except: 
        print("- Kivy UI Error")


def setGlobal(name, value, type = None):
    global COUNTER_SAVED_X_POSTS
    global COUNTER_SAVED_YOUTUBE_POSTS
    global COUNTER_SAVED_NEWS_ARTICLES
    global COUNTER_SAVED_SUBREDDIT_POSTS
    global COUNTER_TOTAL_NEWS_CARD
    global LIMIT_ARTICLES
    global LIMIT_YOUTUBE_POSTS
    global LIMIT_TWEETS
    global LIMIT_SUBREDDIT_POSTS
    global LIMIT_DEFAULT_TIMEOUT
    global SAVED_POSTS_TWITTER
    global SAVED_POSTS_YOUTUBE
    global SAVED_POSTS_ARTICLES
    global SAVED_POSTS_SUBREDDIT
    global TOTAL_POSTS_TWITTER
    global TOTAL_POSTS_YOUTUBE
    global TOTAL_POSTS_ARTICLES
    global TOTAL_POSTS_SUBREDDIT
    global DOMAIN_TWITTER
    global DOMAIN_REDDIT
    global DOMAIN_YOUTUBE
    global DOMAIN_ARTICLES
    global DOMAIN_PROFILE_PIC
    
    #counters
    if name == "COUNTER_SAVED_X_POSTS": COUNTER_SAVED_X_POSTS = value
    elif name == "COUNTER_SAVED_YOUTUBE_POSTS": COUNTER_SAVED_YOUTUBE_POSTS = value
    elif name == "COUNTER_SAVED_NEWS_ARTICLES": COUNTER_SAVED_NEWS_ARTICLES = value
    elif name == "COUNTER_SAVED_SUBREDDIT_POSTS": COUNTER_SAVED_SUBREDDIT_POSTS = value
    elif name == "COUNTER_TOTAL_NEWS_CARD": COUNTER_TOTAL_NEWS_CARD = value
    elif name == "TOTAL_POSTS_TWITTER": TOTAL_POSTS_TWITTER = value
    elif name == "TOTAL_POSTS_YOUTUBE": TOTAL_POSTS_YOUTUBE = value
    elif name == "TOTAL_POSTS_ARTICLES": TOTAL_POSTS_ARTICLES = value
    elif name == "TOTAL_POSTS_SUBREDDIT": TOTAL_POSTS_SUBREDDIT = value
    
    #limits
    elif name == "LIMIT_ARTICLES": LIMIT_ARTICLES = value
    elif name == "LIMIT_YOUTUBE_POSTS": LIMIT_YOUTUBE_POSTS = value
    elif name == "LIMIT_TWEETS": LIMIT_TWEETS = value
    elif name == "LIMIT_SUBREDDIT_POSTS": LIMIT_SUBREDDIT_POSTS = value

    #arrays    
    elif name == "SAVED_POSTS_TWITTER" and type == "add": SAVED_POSTS_TWITTER.append(value)
    elif name == "SAVED_POSTS_YOUTUBE" and type == "add": SAVED_POSTS_YOUTUBE.append(value)
    elif name == "SAVED_POSTS_ARTICLES" and type == "add": SAVED_POSTS_ARTICLES.append(value)
    elif name == "SAVED_POSTS_SUBREDDIT" and type == "add": SAVED_POSTS_SUBREDDIT.append(value)
    elif name == "SAVED_POSTS_TWITTER" and type == "assign": SAVED_POSTS_TWITTER = value
    elif name == "SAVED_POSTS_YOUTUBE" and type == "assign": SAVED_POSTS_YOUTUBE = value
    elif name == "SAVED_POSTS_ARTICLES" and type == "assign": SAVED_POSTS_ARTICLES = value
    elif name == "SAVED_POSTS_SUBREDDIT" and type == "assign": SAVED_POSTS_SUBREDDIT = value


def checkDomainStatus():
    print("\ncheckDomainStatus") #log

    #variables
    statusTwitter = ""
    statusArticles = ""
    statusReddit = ""
    statusYoutube = ""
    statusProfilePic = ""

    #check domain is available
    try: reqDomain = requests.get(DOMAIN_TWITTER, timeout=LIMIT_DEFAULT_TIMEOUT); statusTwitter = str(reqDomain.status_code)
    except: statusTwitter = "not responding"
    try: reqDomain = requests.get(DOMAIN_ARTICLES, timeout=LIMIT_DEFAULT_TIMEOUT); statusArticles = str(reqDomain.status_code)
    except: statusArticles = "not responding"
    try: reqDomain = requests.get(DOMAIN_REDDIT, timeout=LIMIT_DEFAULT_TIMEOUT); statusReddit = str(reqDomain.status_code)
    except: statusReddit = "not responding"
    try: reqDomain = requests.get(DOMAIN_YOUTUBE, timeout=LIMIT_DEFAULT_TIMEOUT); statusYoutube = str(reqDomain.status_code)
    except: statusYoutube = "not responding"
    try: reqDomain = requests.get(DOMAIN_PROFILE_PIC, timeout=LIMIT_DEFAULT_TIMEOUT); statusProfilePic = str(reqDomain.status_code)
    except: statusYoutube = "not responding"

    #log
    print("- Twitter: " + statusTwitter + " - " + DOMAIN_TWITTER)
    print("- Articles: " + statusArticles + " - " + DOMAIN_ARTICLES)
    print("- Reddit: " + statusReddit + " - " + DOMAIN_REDDIT)
    print("- Youtube: " + statusYoutube + " - " + DOMAIN_YOUTUBE)
    print("- ProfilePic: " + statusProfilePic + " - " + DOMAIN_PROFILE_PIC + "\n")


#------ SCREEN 1: News Feed ------#
class NewsFeedScreen(Screen):
    
    def __init__(self, **var_args):
        super(NewsFeedScreen, self).__init__(**var_args)
        self.ids.category1.text = year_progress()


    def on_pre_enter(self, *args):

        #log
        print("Change Screen: newsfeed") 
        
        #variables
        savedProfiles = fetch_saved_file("profiles")
        totalSavedProfiles = len(savedProfiles)
        btnBackgroundColor = get_color_from_hex("#292f33")

        #update UI: clear widgets
        self.bl1.clear_widgets()

        #create buttons
        btnAdd = Button(text = "+", size_hint_y = None, height = "40", background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = "29", bold = True)
        btnEdit = Button(text = "-", size_hint_y = None, height = "40", background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = "39", bold = True)
        btnFavorites = Button(text = "~", size_hint_y = None, height = "40", background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = "29", bold = True)
        # btnFiller = Button(text = "", size_hint_y = None, height = btnHeight, background_color = btnBackgroundColor, background_normal = 'transparent', background_down = 'transparent', font_size = btnFontSize)

        #bind functions to buttons
        btnAdd.bind(on_press=lambda *args: screenChange(self, 'add'))
        btnEdit.bind(on_press=lambda *args: screenChange(self, 'edit'))
        btnFavorites.bind(on_press=lambda *args: screenChange(self, 'favorites'))

        #update UI: add buttons
        self.bl1.add_widget(btnFavorites) #favorite button
        self.bl1.add_widget(btnAdd) #add button
        self.bl1.add_widget(btnEdit) #edit button
        for p in savedProfiles[::-1]: #sidemenu buttons
            NewsFeedScreen.profile_add_buttons(self, p, totalSavedProfiles)
            

    def printNewsFeed(self, profile, selfObj):
        fetch_news_feed(profile, selfObj)


    def startThreadPrintNewsFeed(self, *args):
        
        #variables
        profile = args[0]

        #start thread
        Thread(target=self.printNewsFeed, kwargs={"profile": profile, "selfObj": self}).start()


    def profile_add_buttons(self, profile, totalSavedProfiles):
        
        #variables
        totalMenuButtons = 4
        totalButtons = len(self.bl1.children)

        #check total profile buttons
        if(totalButtons != totalSavedProfiles + totalMenuButtons):
            
            profilePicUrl = os.getcwd() + str(profile['profilepic'])

            #create button
            # newButton = Button(background_normal = os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg", background_down = os.getcwd() + "/thumbnails/" + profile['name'] + ".jpg", size_hint_y = None, opacity = 0.9)
            newButton = Button(background_normal = profilePicUrl, background_down = profilePicUrl, size_hint_y = None, opacity = 0.9)
            newButton.bind(on_press=lambda *args: self.startThreadPrintNewsFeed(profile)) #bind function buttons

            #update UI: add button
            self.bl1.add_widget(newButton)


    def favorites_save(screen, self, type):

        try:
            #variables
            TOTAL_POSTS_TWITTER = len(SAVED_POSTS_TWITTER)
            TOTAL_POSTS_YOUTUBE = len(SAVED_POSTS_YOUTUBE)
            TOTAL_POSTS_ARTICLES = len(SAVED_POSTS_ARTICLES)
            TOTAL_POSTS_SUBREDDIT = len(SAVED_POSTS_SUBREDDIT)

            #check post platform
            if type == "twitter" and TOTAL_POSTS_TWITTER > 0: post = SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS] #TWITTER
            elif type == "youtube" and TOTAL_POSTS_YOUTUBE > 0: post = SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS] #YOUTUBE
            elif type == "article" and TOTAL_POSTS_ARTICLES > 0: post = SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES] #ARTICLE
            elif type == "subreddit" and TOTAL_POSTS_SUBREDDIT > 0: post = SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS] #SUBREDDIT
            else: return
            
            fav_id = post['profile'] + "-" + post['title'] + "-" + post['date']
            fav_profile = post['profile']
            fav_date = post['date']
            fav_platform = type
            fav_savedAt = str(datetime.datetime.now()).replace("-", " ")[0:10]
            fav_text = post['title']
            fav_img = post['profilepic']
            fav_link = post['link']

            #load favorites file
            favorites = json.load(open('data/favorites.json', "r"))

            #check if post already saved
            for f in favorites:
                if f['id'] == fav_id: print('post already saved'); return
            
            #handle favorite obj
            newFavorite = {
                "id": fav_id,
                "profile": fav_profile,
                "date": fav_date, 
                "platform": fav_platform, 
                "savedAt": fav_savedAt, 
                "text": fav_text,
                "link": fav_link,
                "img": fav_img
            }
            favorites.append(newFavorite)
            
            #log
            print("save post:"); print(post)

            #update favorites file
            out_file = open("data/favorites.json", "w"); json.dump(favorites, out_file, indent = 6); out_file.close()

        #error: save post failed
        except Exception as e:
            print(e); print("error: save "  + type + " post failed")
        

    def favorites_remove(self, cardId):
        print("favorites_remove") #log

        #variables
        favorites = json.load(open('data/favorites.json', "r"))
        
        #remove selected favorite
        count = 0
        for f in favorites:
            if f['id'] == cardId:
                favorites.pop(count)
                out_file = open("data/favorites.json", "w")
                json.dump(favorites, out_file, indent = 6)
                out_file.close()
            count += 1

        #Update UI: refresh favorites screen
        if 'favorites' in str(self): screenRefresh(self, 'favorites')


    def favorites_create_card(self, *args):
        
        #variables
        obj = args[0]
        id = obj['id']
        profile = obj['profile']
        platform = obj['platform']
        savedAt = obj['savedAt']
        text = obj['text']
        date = obj['date']
        link = obj['link']
        colorTwitter = get_color_from_hex('#1DA1F2')
        colorYoutube = get_color_from_hex('#FF0000')
        colorArticle = get_color_from_hex('#0e1012')
        colorSubreddit = get_color_from_hex('#ff4500')
        imgSrc = os.getcwd() + obj['img']
        img = obj['img']
        favorites = json.load(open('data/favorites.json', "r"))

        #check platform
        if platform == "twitter": platformText = "X"
        elif platform == "youtube": platformText = "Youtube"
        elif platform == "article": platformText = "Article"
        elif platform == "subreddit": platformText = "Subreddit"

        #create widgets 
        bl = BoxLayout(orientation = "horizontal", size_hint_x = None, size_hint_y = None, height = 240, width = 600) #, spacing = (40, 40), padding = (40, 40)
        btnProfileImg = Button(size_hint_x = None, size_hint_y = None, height = 220, width = 220, background_normal =  imgSrc,background_down =  imgSrc,color = 'lightgray') #profile button
        btn1 = Button(text = "-", size_hint_y = 0.5,size_hint_x = None, width = 70, background_color = get_color_from_hex('#0e1012'), background_normal = 'transparent', background_down = 'transparent', font_size = 30, color = 'lightgray', opacity = 0.9) #remove button
        btn2 = Button(text = "§", size_hint_y = 0.5,size_hint_x = None, width = 70, background_color = get_color_from_hex('#0e1012'), background_normal = 'transparent',background_down = 'transparent',font_size = 19,color = 'lightgray',opacity = 0.9)
        sl = StackLayout(orientation = "tb-lr", size_hint_y = 0.917,size_hint_x = None) #stacklayout # height = 300, width = 600, spacing = (0, 20), padding = (0, 20)
        btnNewsCard = Button(
            text = profile.upper() + " · " + "Saved " + savedAt + "\n\n" + platformText + " · " + date + "\n\n" + text,
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
        btn1.bind(on_press=lambda *args: NewsFeedScreen.favorites_remove(self, id))
        btn2.bind(on_press=lambda *args: NewsFeedScreen.copy_to_clipboard(self, link))

        #set widget platform colors
        if platformText == "X": btnNewsCard.background_color = colorTwitter; btn1.background_color = colorTwitter; btn2.background_color = colorTwitter
        elif platformText == "Youtube": btnNewsCard.background_color = colorYoutube; btn1.background_color = colorYoutube; btn2.background_color = colorYoutube
        elif platformText == "Article": btnNewsCard.background_color = colorArticle; btn1.background_color = colorArticle; btn2.background_color = colorArticle
        elif platformText == "Subreddit": btnNewsCard.background_color = colorSubreddit; btn1.background_color = colorSubreddit; btn2.background_color = colorSubreddit

        #update UI: add widgets to layouts
        bl.add_widget(btnProfileImg)
        bl.add_widget(btnNewsCard)
        sl.add_widget(btn2)
        sl.add_widget(btn1)
        bl.add_widget(sl)
        return bl


    def UI_clear(self):
        self.ids.boxLayoutPost.clear_widgets()
    

    def copy_to_clipboard(self, type):

        #check platform
        if type == "twitter" and TOTAL_POSTS_TWITTER != 0: pyclip.copy(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]['link'])
        elif type == "youtube" and TOTAL_POSTS_YOUTUBE != 0: pyclip.copy(SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS]['link'])
        elif type == "article" and len(SAVED_POSTS_ARTICLES) != 0: pyclip.copy(SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['link'])
        elif type == "subreddit" and len(SAVED_POSTS_SUBREDDIT) != 0: pyclip.copy(SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS]['link'])
        else: pyclip.copy(type) # favorites screen
       
        #log
        clipboardText = pyclip.paste(text=True); print("copy_to_clipboard: " + clipboardText) 


    def next_post(self, order, type):
        
        #YOUTUBE
        if type == "youtube" and TOTAL_POSTS_YOUTUBE > 0: 
            
            #check if last card
            if COUNTER_SAVED_YOUTUBE_POSTS == TOTAL_POSTS_YOUTUBE - 1: setGlobal("COUNTER_SAVED_YOUTUBE_POSTS", -1)
            
            #increment counter
            setGlobal("COUNTER_SAVED_YOUTUBE_POSTS", COUNTER_SAVED_YOUTUBE_POSTS + 1)

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #set card text
            videoId = SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS]['id'] + "/" + str(TOTAL_POSTS_YOUTUBE)
            videoUploadDate = SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS]['date']
            videoDuration = SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS]['duration']
            videoTitle = SAVED_POSTS_YOUTUBE[COUNTER_SAVED_YOUTUBE_POSTS]['title']
            cardText = "YouTube" + " · " + videoId + " · " + videoUploadDate + "\n\n" + videoTitle + " (" + videoDuration + ")"

            #update UI card text
            card.text = cardText
        
        #TWITTER
        elif type == "twitter" and TOTAL_POSTS_TWITTER > 0:
            
            #check if last
            if COUNTER_SAVED_X_POSTS == TOTAL_POSTS_TWITTER - 1: setGlobal("COUNTER_SAVED_X_POSTS", -1)
        
            #increment counter
            setGlobal("COUNTER_SAVED_X_POSTS", COUNTER_SAVED_X_POSTS + 1) 

            #set card text
            id = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["id"]) + "/" + str(TOTAL_POSTS_TWITTER)
            date = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["date"])
            text = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["text"])
            # username = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["username"])
            # images = SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["images"]
            # videos = SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["videos"]
            # youtube = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["youtube"])
            # retweet = str(SAVED_POSTS_TWITTER[COUNTER_SAVED_X_POSTS]["retweet"])
            cardText = "\n" + "X" + " · " + id + " · " + date + " · " + "Self-Post" + "\n\n" + text + "\n"
            
            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #update UI card text
            card.text = cardText
        
        #ARTICLES
        elif type == "article" and TOTAL_POSTS_ARTICLES > 0:
            
            #check if last
            if COUNTER_SAVED_NEWS_ARTICLES == TOTAL_POSTS_ARTICLES - 1: setGlobal("COUNTER_SAVED_NEWS_ARTICLES", -1)
            
            #increment counter
            setGlobal("COUNTER_SAVED_NEWS_ARTICLES", COUNTER_SAVED_NEWS_ARTICLES + 1)

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post

            #set card text
            articleId = SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['id'] + "/" + str(TOTAL_POSTS_ARTICLES)
            articleDate = SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['date']
            articleTitle = SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['title']
            articlePublisher =  SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['publisher'].split(".")[0].capitalize()
            # articleLink = SAVED_POSTS_ARTICLES[COUNTER_SAVED_NEWS_ARTICLES]['link']
            cardText = "Article" + " · " + articleId + " · " + articleDate + " · " + articlePublisher + "\n\n" + articleTitle

            #update UI text
            card.text = cardText
        
        #SUBREDDIT
        elif type == "subreddit" and TOTAL_POSTS_SUBREDDIT > 0:
            
            #check if last
            if COUNTER_SAVED_SUBREDDIT_POSTS == (len(SAVED_POSTS_SUBREDDIT) - 1): setGlobal("COUNTER_SAVED_SUBREDDIT_POSTS", -1)

            #increment counter
            setGlobal("COUNTER_SAVED_SUBREDDIT_POSTS", COUNTER_SAVED_SUBREDDIT_POSTS + 1)

            #check card order
            if order == 1: card = self.ids.newsCard1Post
            elif order == 2: card = self.ids.newsCard2Post
            elif order == 3: card = self.ids.newsCard3Post
            elif order == 4: card = self.ids.newsCard4Post
            
            #set card text
            cardId = SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS]['id'] + "/" + str(TOTAL_POSTS_SUBREDDIT)
            cardDate = SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS]['date']
            cardTitle = SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS]['title']
            cardSubreddit = SAVED_POSTS_SUBREDDIT[COUNTER_SAVED_SUBREDDIT_POSTS]['subreddit']
            cardText = "Subreddit" + " · " + cardId + " · " + cardDate + "\n\n" + cardTitle
            
            #update UI card text
            card.text = cardText

        else: 
            return


    def change_button_color(self, order, type):
        
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
        print("Change Screen: favorites")

        #clear card widgets
        self.ids.boxLayoutPost.clear_widgets()

        #variables
        savedProfiles = fetch_saved_file("profiles")
        favorites = fetch_saved_file("favorites")
        totalButtons = len(self.ids.boxLayoutPost.children)
        totalFavorites = len(favorites)
        totalSavedProfiles = len(savedProfiles)

        #create UI widgets
        lbl1 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")
        lbl2 = Label(size_hint_y = 1, size_hint_x = 1, text = str(totalFavorites) + " Saved Posts", font_size = 22, bold = True)
        lbl3 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")

        #update UI widgets
        self.ids.boxLayoutPost.add_widget(lbl1)
        self.ids.boxLayoutPost.add_widget(lbl2)
        for fav in favorites[::-1]:
            if totalButtons < totalFavorites:
                bl = NewsFeedScreen.favorites_create_card(self, fav)
                self.ids.boxLayoutPost.add_widget(bl)
        self.ids.boxLayoutPost.add_widget(lbl3)


#------ SCREEN 3: Profile Add ------#
class AddProfileScreen(Screen):
    
    def __init__(self, **var_args):
        super(AddProfileScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("Change Screen: profile add") #log
        

    def add_profile(self, name, youtube = None, twitter = None, articles = None, subreddit = None):
    
        #variables
        profiles = []
        totalProfiles = 0
        youtubeChannelName = youtube

        #load profiles file
        try: 
            #variables
            profiles = json.load(open('data/profiles.json', "r"))
            totalProfiles = len(profiles)
            
            #name is taken
            for p in profiles:
                if p['name'] == name: print("profile name already taken"); return

            #name is null
            if name == "": print("profile name empty"); return
        
        #create profiles file
        except: 
            file = open('data/profiles.json', "w")
            file.close()

        #youtube url check
        if youtube == "": print("profiles youtube channel is null")
        else: youtube = youtubeChannelName
        
        #fetch profile image
        profileImageUrl = fetch_profile_image(name)

        #create profile obj
        newProfile = {
            "id": totalProfiles + 1, 
            "name": name, 
            "youtube": youtube, 
            "twitter": twitter, 
            "articles": articles, 
            "subreddit": subreddit,
            "profilepic": profileImageUrl
        }

        #add profile to profiles file
        profiles.append(newProfile)
        out_file = open("data/profiles.json", "w")
        json.dump(profiles, out_file, indent = 6)
        out_file.close()

        #update UI: go to start screen
        screenChange(self, "start")
        

    def fetch_profile_inputs(self):
        
        #variables
        profileName = self.ti1.text
        profileYoutube = self.ti2.text
        profileTwitter = self.ti3.text
        profileArticles = self.ti4.text
        profileSubreddit = self.ti5.text

        #add profile
        self.add_profile(profileName, profileYoutube, profileTwitter, profileArticles, profileSubreddit)

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
        print("Change Screen: profile remove") #log

        #update UI: clear widgets
        self.ids.boxLayout2.clear_widgets()

        #variables
        savedProfiles = fetch_saved_file("profiles")
        totalSavedProfiles = len(savedProfiles)
        totalButtons = len(self.ids.boxLayout2.children)

        #update UI: add saved profiles buttons
        if totalButtons != totalSavedProfiles:
            
            #clear widgets
            self.ids.boxLayout2.clear_widgets()

            #add buttons
            for x in range(totalSavedProfiles):
                reverseListCount = (totalSavedProfiles - 1) - x # reverse list to make latest added on top
                RemoveProfileScreen.profile_add_buttons(self, savedProfiles[reverseListCount])

        #update UI: set remove profile button text
        self.btnRemoveProfile.text = "Remove Profile"


    def profile_add_buttons(self, profile):
        
        #create button widget
        newButton = Button(size_hint_y = None, height = 40, text = profile['name'].upper(), background_color = get_color_from_hex("#292f33"))
        newButton.bind(on_press=lambda *args: RemoveProfileScreen.fill_text_input_with_data(self, profile)) #add functions to buttons

        #update UI: add button layout
        self.ids.boxLayout2.add_widget(newButton)


    def profile_delete(self):
        
        #variables
        name = self.ti1.text
        profiles = fetch_saved_file("profiles")
        count = 0

        #remove saved profile from list
        for p in profiles:
            if p['name'] == name: profiles.pop(count)
            count += 1

        #remove profile from profiles file
        out_file = open("data/profiles.json", "w")
        json.dump(profiles, out_file, indent = 6)
        out_file.close()

        #remove profile thumbnail file
        # thumbnails = os.listdir(os.getcwd() + '/thumbnails')
        # for image in thumbnails:
        #     imageFile = os.getcwd() + '/thumbnails' + '/' + image
        #     if name in image:
        #         try: os.remove(imageFile)
        #         except: print("delete thumbnail " + name + " failed")

        
        #update UI
        self.ti1.text = "" #clear text inputs
        screenRefresh(self, 'edit') #refresh edit screen


    def fill_text_input_with_data(self, profile):
        self.ti1.text = profile['name']
        self.btnRemoveProfile.text = "Remove " + profile['name'].upper()

 
#------ SCREEN 5: Blank ------#
class BlankScreen(Screen):

    def __init__(self, **var_args):
        super(BlankScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("Change Screen: blank") #log


#------ Base Class ------#
class ScraperNewsApp(App):
    
    def build(self):
        
        #update UI: set window title
        self.title = "Scraper News" #"Scraper News · " + str(year_progress())

        #create files/directories
        if os.path.isdir('data') == False: os.mkdir('data')
        if os.path.exists('data/profiles.json') == False: file = open('data/profiles.json', "w"); file.write("[]"); file.close()
        if os.path.exists('data/favorites.json') == False: file = open('data/favorites.json', "w"); file.write("[]"); file.close()
        if os.path.isdir('thumbnails') == False: os.mkdir('thumbnails')
        
        #set kivy screen manager configs
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
# Config.set('graphics', 'resizable', '0') #changing this might break display resolution
# Config.set('graphics', 'fullscreen', '0') #changing this might break display resolution
# Config.write()


#------ START APP ------#
if __name__ == '__main__': ScraperNewsApp().run()