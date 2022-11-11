### imports ###
import datetime
import json
import requests
import re
import time
from threading import Thread
import time
import os
import webbrowser
import pyclip


### functions ###















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
            
    #set formatted date
    formattedDate = str(month) + " " + str(day) + " " + str(year) + " · " + str(dayOfTheYear) + "/" + str(totalDaysThisYear)
    
    return formattedDate


def add_profile(self, name, youtube = None, twitter = None, articles = None, subreddit = None):
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

    #fetch profiles from profiles.json
    file = open('profiles.json', "r")
    profiles = json.load(file)
    totalProfiles = len(profiles)

    #reset news card text
    self.ids.newsCard1Post.text = ""
    self.ids.newsCard2Post.text = ""
    self.ids.newsCard3Post.text = ""
    self.ids.newsCard4Post.text = ""

    #reset news card category
    # self.ids.category1.text = ""
    # self.ids.category2.text = ""
    # self.ids.category3.text = ""
    # self.ids.category4.text = ""

    #undisplay news card
    Thread(target=lambda : undisplayNewsCard(self, 1)).start()
    Thread(target=lambda : undisplayNewsCard(self, 2)).start()
    Thread(target=lambda : undisplayNewsCard(self, 3)).start()
    Thread(target=lambda : undisplayNewsCard(self, 4)).start()

    #set loading text
    self.ids.category1.text = name + " loading..."

    #fetch profile youtube data
    for p in profiles:
        if p['name'] == name: 
            print(p['name'])

            if p['articles'] != "":
                counterTNS += 1
                fetch_news_articles(self, articles)
                # if counterTNS == 1: self.ids.category1.text = "Articles"
                # elif counterTNS == 2: self.ids.category2.text = "Articles"
                # elif counterTNS == 3: self.ids.category3.text = "Articles"
                # elif counterTNS == 4: self.ids.category4.text = "Articles"

            if p['youtube'] != "":
                counterTNS += 1
                fetch_youtube_channel(p['youtube'], self, youtube)
                # if counterTNS == 1: self.ids.category1.text = "Youtube" # self.ids.category1.color = get_color_from_hex("#FF0000")
                # elif counterTNS == 2: self.ids.category2.text = "Youtube"
                # elif counterTNS == 3: self.ids.category3.text = "Youtube"
                # elif counterTNS == 4: self.ids.category4.text = "Youtube"

            if p['twitter'] != "":
                counterTNS += 1
                fetch_twitter_profile(p['twitter'], self, twitter)
                # if counterTNS == 1: self.ids.category1.text = "Twitter"
                # elif counterTNS == 2: self.ids.category2.text = "Twitter"
                # elif counterTNS == 3: self.ids.category3.text = "Twitter"           
                # elif counterTNS == 4: self.ids.category4.text = "Twitter"            

            if p['subreddit'] != "":
                counterTNS += 1
                fetch_subreddit(self, subreddit, p)
                # if counterTNS == 1: self.ids.category1.text = "Subreddit"
                # elif counterTNS == 2: self.ids.category2.text = "Subreddit"
                # elif counterTNS == 3: self.ids.category3.text = "Subreddit"            
                # elif counterTNS == 4: self.ids.category4.text = "Subreddit"          

            self.ids.category1.text = name


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


def changeScreen(self, type):
    if type == "add": self.manager.current = 'add'
    elif type == "edit": self.manager.current = 'edit'
    elif type == "start": self.manager.current = 'start'
    elif type == "favorites": self.manager.current = 'favorites'
    elif type == "menu": self.manager.current = 'menu'


def refreshScreen(self, screenName):
    self.manager.current = 'blank' #change to blank screen
    self.manager.current = screenName #change back to previous screen


def fetch_subreddit(self, name, profile):
    print("fetch_subreddit")
    
    #variables
    # requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    global savedSubredditPosts
    global counterSSP
    startFrom = 0
    limitSubredditPosts = 10
    savedSubredditPosts = []
    counterSSP = -1
    profileName = profile['name']

    #request news articles
    httpRequest = requests.get("https://libreddit.de/r/" + name + "/hot")
    
    #handle request results
    if httpRequest.status_code == 200:
        requestResultText = str(httpRequest.text)
        
        #regex
        regexTitle = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', requestResultText)
        regexLink = re.findall(r'<a href="/r/.*/comments.*\s\s</h2>', requestResultText)
        regexDate = re.findall(r'<span class="created" title=".*', requestResultText)
        regexStickied = re.findall(r'<div class="post stickied".*', requestResultText)
        
        #debugging
        # print(str(len(regexTitle)))
        # print(str(len(regexStickied)))
        # print(str(len(regexStickied)))
        
        #variables
        totalStickied = len(regexStickied)
        totalSubredditPosts = len(regexTitle)
        count = 0

        #set correct total items
        regexTitle = regexTitle[totalStickied:limitSubredditPosts + totalStickied]
        regexLink = regexLink[totalStickied:limitSubredditPosts + totalStickied]
        regexDate = regexDate[totalStickied:limitSubredditPosts + totalStickied]

        #null check
        if totalSubredditPosts == 0:
            print("0 subreddit posts found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "subreddit", "null")).start() #display card
            return
        
        #sort subreddit posts
        elif totalSubredditPosts > 0:
            if totalSubredditPosts < 10: limitSubredditPosts = totalSubredditPosts #check total posts
            
            for item in regexTitle:
                title = str(item)
                title = title.split(">")[1]
                title = title.replace("&quot;", "").replace("&#x27;", "").replace(".</a", "").replace("</a", "")
                title = title.replace("â", "a").replace("¦", "").replace("Isit", "Is it").replace("isit", "is it")
                title = title.replace("a\x80", "").replace("\x80", "").replace("\x9c", "")
                title = title.replace("\x9f", "").replace("\x8e", "").replace("\x9d", "")
                title = title.replace("\x99", "").replace("ð ", "").replace("ð", "")
                title = title.replace("¶", " ")

                link = regexLink[count]
                link = str(link)
                link = link.replace("<a href=\"", "")
                link = link.split("/\">")[0]
                link = "https://libreddit.de" + link

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
                    "user": profileName,
                    "type": "subreddit"
                }

                #add obj post
                savedSubredditPosts.append(post)

                #increment
                count += 1

        #update news card content       
        counterSSP = -1
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "subreddit", None)).start() #display card
        
        for p in savedSubredditPosts:
            print(p)

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