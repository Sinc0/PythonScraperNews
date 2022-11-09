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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from threading import Thread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from bs4 import BeautifulSoup
from StandaloneFunctions import fetch_saved_profiles
from StandaloneFunctions import displayNewsCard
from StandaloneFunctions import undisplayNewsCard
from StandaloneFunctions import nitterFilterPost
from StandaloneFunctions import changeScreen
from StandaloneFunctions import refreshScreen



### functions ###
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
    # self.ids.category1.text = name + " loading..."

    #fetch profile youtube data
    for p in profiles:
        if p['name'] == name: 
            print(p['name'])

            if p['youtube'] != "": 
                self.ids.category1.text = name + " loading YouTube..."
                counterTNS += 1; fetch_youtube_channel(p['youtube'], self, youtube)
            if p['twitter'] != "": 
                self.ids.category1.text = name + " loading Twitter..."
                counterTNS += 1; fetch_twitter_profile(p['twitter'], self, twitter)
            if p['subreddit'] != "": 
                self.ids.category1.text = name + " loading Subreddit..."
                counterTNS += 1; fetch_subreddit(self, subreddit, p)
            if p['articles'] != "": 
                self.ids.category1.text = name + " loading Articles..."
                counterTNS += 1; fetch_news_articles(self, articles)

            self.ids.category1.text = name


def fetch_news_articles(self, name):
    #variables
    global counterSNA
    global savedNewsArticles
    counterSNA = -1
    requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    savedNewsArticles = []
    user = name
    numberOfArticlesLimit = 10
    
    #request news articles
    httpRequest = requests.get("https://www.google.com/search?q=" + name + "&source=lmns&tbm=nws&hl=en-US", headers=requestHeaders)
    
    #handle request results
    if httpRequest.status_code == 200:
        requestResultText = str(httpRequest.text)
        
        #debugging
        # with open("Output.txt", "w") as text_file:
        #     text_file.write(str(requestResultText))
        # return

        #regex
        regexTitle = re.findall(r'[\w\d\s.#\-,!:;_^\'\*\\/()÷{}@$£&?=[\]\"+^¨|]*</div></h3>', requestResultText)
        regexLink = re.findall(r'<a href="/url\?q=[\w\d\s.#\-,!:;_^\'*\\/()÷{}@$£&?=[\]\"+^¨|]*', requestResultText)
        regexDate = re.findall(r'\">[\w\d\s]*ago', requestResultText)
        # regexCompany = re.findall(r'\">[\w\d\s]*</div></div></div>', requestResultText)
        # regexSummary = re.findall(r'[\w\d\s[\w\d\s.#\-,!:;_^\'*\\/()÷{}@$£&?=[\]\"+^¨|]*<br>', requestResultText)
        
        #variables
        totalArticles = len(regexTitle)
        count = 0

        #null check
        if len(regexTitle) == 0:
            print("0 articles found for: " + name)
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "articles", "null")).start() #display card
            return
        
        #sort articles
        elif len(regexTitle) > 0:
            if len(regexTitle) < 10: numberOfArticlesLimit = len(regexTitle)

            #create post obj
            for obj in regexTitle[0:numberOfArticlesLimit]:
                title = str(obj)
                title = title.replace("&#8216;", "").replace("&#8217;", "").replace("</div></h3>", "")
                title = title.replace(" ...", "...")

                link = regexLink[count]
                link = link.replace("<a href=\"/url?q=", "")
                link = link.split("&amp;")[0]

                date = regexDate[count]
                date = date.replace("\">", "")

                post = {
                    "id": str(count + 1),
                    "title": title,
                    "link": link,
                    "date": date,
                    "user": user,
                    "type": "article"
                }

                #add post obj
                savedNewsArticles.append(post)

                #increment
                count += 1

                #update news card content       
                counterSNA = -1
                Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "article", None)).start() #display card


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
    numberOfVideosLimit = 10

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
        if len(regexYoutubeVideos) < 10: numberOfVideosLimit = len(regexYoutubeVideos)

        for videoTitle in regexYoutubeVideos[0: numberOfVideosLimit]:
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
                "link": str(formatYoutubeLink),
                "type": "youtube"
            }

            #add post
            savedYoutubePosts.append(post)

        #update news card content       
        counterSYP = -1
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "youtube", savedYoutubePosts[0])).start() #display car


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
    numberOfTweetsLimit = 10

    #request twitter profile
    httpRequest = requests.get("https://nitter.net/" + username)
    
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
                    "videos": videos,
                    "type": "twitter"
                }
                savedTwitterPosts.append(post)

        #debugging
        print(str(len(savedTwitterPosts)))
        
        #null check
        if len(savedTwitterPosts) == 0:
            print("0 twitter posts found for: " + name)

            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "twitter", "null")).start() #display card
            return

        #sort twitter posts
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
            savedTwitterPosts = savedTwitterPosts[0:numberOfTweetsLimit]
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "twitter", savedTwitterPosts[0])).start() #display card


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



### code ###
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
            text = "Add", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = btnFontSize,
            bold = True
        )

        #create edit button
        btnEdit = Button(
            text = "Remove", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = btnFontSize,
            bold = True
        )
        #create favorite button
        btnFavorites = Button(
            text = "Saved", 
            size_hint_y = None, 
            height = btnHeight, 
            background_color = btnBackgroundColor, 
            background_normal = 'transparent', 
            background_down = 'transparent', 
            font_size = btnFontSize,
            bold = True
        )

        #create filler button
        # btnFiller = Button(
        #     text = "", 
        #     size_hint_y = None, 
        #     height = btnHeight, 
        #     background_color = btnBackgroundColor, 
        #     background_normal = 'transparent', 
        #     background_down = 'transparent', 
        #     font_size = btnFontSize
        # )

        #bind functions to buttons
        btnAdd.bind(on_press=lambda *args: changeScreen(self, 'add'))
        btnEdit.bind(on_press=lambda *args: changeScreen(self, 'edit'))
        btnFavorites.bind(on_press=lambda *args: changeScreen(self, 'favorites'))

        #add buttons to layout
        self.bl1.add_widget(btnFavorites)
        self.bl1.add_widget(btnAdd)
        self.bl1.add_widget(btnEdit)

        #add profile sidemenu buttons
        for p in savedProfiles[::-1]:
            StartingScreen.AddProfileButtons(self, p, totalSavedProfiles)
            

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

        elif type == "article":
            post = savedNewsArticles[counterSNA]

            if len(savedNewsArticles) == 0: 
                return

            elif len(savedNewsArticles) > 0:
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

        elif type == "subreddit":
            post = savedSubredditPosts[counterSSP]

            if len(savedSubredditPosts) == 0: 
                return

            elif len(savedSubredditPosts) > 0:
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
        #variables
        obj = args[0]
        id = obj['id']
        profile = obj['profile']
        platform = obj['platform']
        savedAt = obj['savedAt']
        text = obj['text']
        img = obj['img']
        date = obj['date']
        link = obj['link']

        #check platform
        if platform == "twitter": platform = "Twitter"
        elif platform == "youtube": platform = "Youtube"
        elif platform == "article": platform = "Article"
        elif platform == "subreddit": platform = "Subreddit"

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
            font_size = 30,
            color = 'lightgray',
            opacity = 0.9
            # height = 110,
        )

        btn2 = Button(
            text = "#", 
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

        #variables colors
        colorTwitter = get_color_from_hex('#1DA1F2')
        colorYoutube = get_color_from_hex('#FF0000')
        colorArticle = get_color_from_hex('#0e1012')
        colorSubreddit = get_color_from_hex('#ff4500')

        #check platform
        if platform == "Twitter":
            btnNewsCard.background_color = colorTwitter
            btn1.background_color = colorTwitter
            btn2.background_color = colorTwitter
        elif platform == "Youtube":
            btnNewsCard.background_color = colorYoutube
            btn1.background_color = colorYoutube
            btn2.background_color = colorYoutube
        elif platform == "Article":
            btnNewsCard.background_color = colorArticle
            btn1.background_color = colorArticle
            btn2.background_color = colorArticle
        elif platform == "Subreddit":
            btnNewsCard.background_color = colorSubreddit
            btn1.background_color = colorSubreddit
            btn2.background_color = colorSubreddit

        #add widgets to boxlayout
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
        global counterSTP
        totalTwitterPosts = len(savedTwitterPosts)

        if totalTwitterPosts == 0:
            return

        elif totalTwitterPosts > 0:
            #check counter
            if counterSTP == (len(savedTwitterPosts) - 1): 
                counterSTP = -1
                undisplayNewsCard(self, order)
            
            #increment counter
            counterSTP = counterSTP + 1; 

            #set card
            username = str(savedTwitterPosts[counterSTP]["username"])
            id = str(savedTwitterPosts[counterSTP]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[counterSTP]["date"])
            text = str(savedTwitterPosts[counterSTP]["text"])
            images = savedTwitterPosts[counterSTP]["images"]
            videos = savedTwitterPosts[counterSTP]["videos"]
            youtube = str(savedTwitterPosts[counterSTP]["youtube"])
            cardText = "Twitter" + " · " + id + " · " + date + "\n\n" + text + "\n"

            #debugging
            # print("\n" + str(savedTwitterPosts[counterSTP]))

            #add links to card
            # count = 0
            # if images != "False": 
            #     for img in images:
            #         count = count + 1
            #         img = img.replace("%3Fname%3Dsmall", "")
            #         cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + img
            # if videos != "False": 
            #     count = count + 1
            #     video = videos[0]
            #     video = video.replace("https://", "")
            #     video = video.replace("http://", "")
            #     video = video.replace("http://", "")
            #     video = video.replace("www.", "")
            #     cardText = cardText + "\n" + str(count) + ": " + video
            # if youtube != "False": 
            #     count = count + 1
            #     youtube = youtube.replace("https://", "")
            #     youtube = youtube.replace("http://", "")
            #     youtube = youtube.replace("http://", "")
            #     youtube = youtube.replace("www.", "")
            #     cardText = cardText + "\n" + str(count) + ": " + youtube
            
            #check card order
            if order == 1: 
                card = self.ids.newsCard1Post
            elif order == 2: 
                card = self.ids.newsCard2Post
            elif order == 3: 
                card = self.ids.newsCard3Post
            elif order == 4: 
                card = self.ids.newsCard4Post

            #update card text
            card.text = cardText


    def youtubeNextPost(self, order):
        #variables
        global counterSYP
        totalYoutubeVideos = len(savedYoutubePosts)

        if totalYoutubeVideos == 0:
            return

        elif totalYoutubeVideos > 0:
            #check counter
            if counterSYP == (len(savedYoutubePosts) - 1): 
                counterSYP = -1
                undisplayNewsCard(self, order)

            #increment counter
            counterSYP = counterSYP + 1

            #debugging
            # print("\n" + str(savedYoutubePosts[counterSYP]))

            #check card order
            if order == 1: 
                card = self.ids.newsCard1Post
            elif order == 2: 
                card = self.ids.newsCard2Post
            elif order == 3: 
                card = self.ids.newsCard3Post
            elif order == 4: 
                card = self.ids.newsCard4Post

            #update card text
            cardText = "YouTube" + " · " + savedYoutubePosts[counterSYP]['id'] + "/" + str(totalYoutubeVideos) + " · " + savedYoutubePosts[counterSYP]['date'] + "\n\n" + savedYoutubePosts[counterSYP]['title']
            card.text = cardText


    def articleNextPost(self, order):
        #variables
        global counterSNA
        totalArticles = len(savedNewsArticles)

        if totalArticles == 0:
            return

        elif totalArticles > 0:
            #check counter
            if counterSNA == (len(savedNewsArticles) - 1): 
                counterSNA = -1
                undisplayNewsCard(self, order)

            #increment counter
            counterSNA = counterSNA + 1

            #debugging
            # print("\n" + str(savedNewsArticles[counterSNA]))

            #check card order
            if order == 1: 
                card = self.ids.newsCard1Post
            elif order == 2: 
                card = self.ids.newsCard2Post
            elif order == 3: 
                card = self.ids.newsCard3Post
            elif order == 4: 
                card = self.ids.newsCard4Post

            #update card text
            cardText = "Article" + " · " + savedNewsArticles[counterSNA]['id'] + "/" + str(totalArticles) + " · " + savedNewsArticles[counterSNA]['date'] + "\n" + savedNewsArticles[counterSNA]['title']
            card.text = cardText


    def subredditNextPost(self, order):
        #variables
        global counterSSP
        totalSubredditPosts = len(savedSubredditPosts)

        if totalSubredditPosts == 0:
            return

        elif totalSubredditPosts > 0:
            #check counter
            if counterSSP == (len(savedSubredditPosts) - 1): 
                counterSSP = -1
                undisplayNewsCard(self, order)

            #increment counter
            counterSSP = counterSSP + 1

            #debugging
            # print("\n" + str(savedSubredditPosts[counterSSP]))

            #check card order
            if order == 1: 
                card = self.ids.newsCard1Post
            elif order == 2: 
                card = self.ids.newsCard2Post
            elif order == 3: 
                card = self.ids.newsCard3Post
            elif order == 4: 
                card = self.ids.newsCard4Post

            #update card text
            cardText = "Subreddit" + " · " + savedSubredditPosts[counterSSP]['id'] + "/" + str(totalSubredditPosts) + " · " + savedSubredditPosts[counterSSP]['date'] + "\n\n" + savedSubredditPosts[counterSSP]['title']
            card.text = cardText


    def copyToClipboard(self, type):
        print("copyToClipboard")

        #linux required packages
        # Linux on x11 (xclip)
        # Linux on wayland (wl-clipboard)

        #check platform
        if type == "twitter" and len(savedTwitterPosts) != 0: pyclip.copy(savedTwitterPosts[counterSTP]['link'])
        elif type == "youtube" and len(savedYoutubePosts) != 0: pyclip.copy(savedYoutubePosts[counterSYP]['link'])
        elif type == "article" and len(savedNewsArticles) != 0: pyclip.copy(savedNewsArticles[counterSNA]['link'])
        elif type == "subreddit" and len(savedSubredditPosts) != 0: pyclip.copy(savedSubredditPosts[counterSSP]['link'])
        else: pyclip.copy(type) # favorites screen
       
        #debugging
        cb_text = pyclip.paste(text=True)
        print(cb_text) 


    def nextPost(self, order, type):
        if type == "youtube": self.youtubeNextPost(order)
        elif type == "twitter": self.twitterNextPost(order)
        elif type == "article": self.articleNextPost(order)
        elif type == "subreddit": self.subredditNextPost(order)


    def openNewsInWebBrowser(self, searchString):
        webbrowser.open('http://duckduckgo.com/?q=' + "searchString")


    def changeButtonColor(self, order, type):
        colorTwitter = get_color_from_hex('#1DA1F2')
        colorYoutube = get_color_from_hex('#FF0000')
        colorArticle = get_color_from_hex('#0e1012')
        colorSubreddit = get_color_from_hex('#ff4500')

        if order == 1:
            card = self.ids.newsCard1Post
            buttonFavorites = self.ids.buttonAddToFavs1
            buttonLink = self.ids.buttonCopyLink1 
        elif order == 2: 
            card = self.ids.newsCard2Post
            buttonFavorites = self.ids.buttonAddToFavs2
            buttonLink = self.ids.buttonCopyLink2 
        elif order == 3: 
            card = self.ids.newsCard3Post
            buttonFavorites = self.ids.buttonAddToFavs3
            buttonLink = self.ids.buttonCopyLink3 
        elif order == 4: 
            card = self.ids.newsCard4Post
            buttonFavorites = self.ids.buttonAddToFavs4
            buttonLink = self.ids.buttonCopyLink4 

        if type == "twitter":
            card.background_color = colorTwitter
            buttonFavorites.background_color =  colorTwitter
            buttonLink.background_color =  colorTwitter
        elif type == "youtube":
            card.background_color = colorYoutube
            buttonFavorites.background_color = colorYoutube
            buttonLink.background_color = colorYoutube
        elif type == "article":
            card.background_color = colorArticle
            buttonFavorites.background_color = colorArticle
            buttonLink.background_color = colorArticle
        elif type == "subreddit":
            card.background_color = colorSubreddit
            buttonFavorites.background_color = colorSubreddit
            buttonLink.background_color = colorSubreddit