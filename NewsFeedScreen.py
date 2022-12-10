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
from StandaloneFunctions import changeScreen
from StandaloneFunctions import refreshScreen
from StandaloneFunctions import newsTextCleaner



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

    #fetch profile news
    for profile in profiles:
        if profile['name'] == name: 
            # print(p['name'])

            if profile['articles'] != "": 
                self.ids.category1.text = "loading Articles..."
                counterTNS += 1; fetch_news_articles(self, articles, profile)
            if profile['youtube'] != "": 
                self.ids.category1.text = "loading YouTube..."
                counterTNS += 1; fetch_youtube_channel(self, profile['youtube'], profile)
            if profile['twitter'] != "": 
                self.ids.category1.text = "loading Twitter..."
                counterTNS += 1; fetch_twitter_profile(self, profile['twitter'], profile)
            if profile['subreddit'] != "": 
                self.ids.category1.text = "loading Subreddit..."
                counterTNS += 1; fetch_subreddit(self, subreddit, profile)

            self.ids.category1.text = name


def fetch_news_articles(self, name, profile):
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
                title = title.replace(" ...", "...").replace("</div></h3>", "")
                title = title.replace("&#8216;", "").replace("&#8217;", "").replace("&#8218;", "")
                title = title.replace("&#8211;", "").replace("&#8212;", "")
                title = title.replace("&#8220;", "").replace("&#8221;", "")
                title = title.replace("  ", " ")

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
                    "type": "article",
                    "profile": profile['name']
                }

                #add post obj
                savedNewsArticles.append(post)

                #increment
                count += 1

                #update news card content       
                counterSNA = -1
                Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "article", None)).start() #display card
    else:
        print("0 articles found for: " + name)
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "articles", "null")).start() #display card
        print("news articles fetch failed")
        return


def fetch_youtube_channel(self, url, profile):
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
    name = profile['name']

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
                    "type": "youtube",
                    "profile": profile['name']
                }

                #add post
                savedYoutubePosts.append(post)

            #update news card content       
            counterSYP = -1
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "youtube", savedYoutubePosts[0])).start() #display car
    else:
        print("0 youtube posts found for: " + name)
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "youtube", "null")).start() #display card
        print("youtube channel fetch failed")
        return


def fetch_twitter_profile(self, username, profile):
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
    name = profile['name']

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
                    "type": "twitter",
                    "profile": profile['name']
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
            # count = 0
            # if savedTwitterPosts[0]["images"] != "False":
            #     None 
            #     # for img in images:
            #     #     count = count + 1
            #     #     img = img.replace("%3Fname%3Dsmall", "")
            #     #     cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + img
            #     # cardText = cardText + "\n" + str(count) + ": " + "nitter.net/" + images
            # if savedTwitterPosts[0]["videos"] != "False": 
            #     count = count + 1
            #     video = videos[0]
            #     video = video.replace("https://", "")
            #     video = video.replace("http://", "")
            #     video = video.replace("http://", "")
            #     video = video.replace("www.", "")
            #     # cardText = cardText + "\n" + str(count) + ": " + video
            # if savedTwitterPosts[0]["youtube"] != "False": 
            #     count = count + 1
            #     youtube = youtube.replace("https://", "")
            #     youtube = youtube.replace("http://", "")
            #     youtube = youtube.replace("http://", "")
            #     youtube = youtube.replace("www.", "")
            #     # cardText = cardText + "\n" + str(count) + ": " + youtube

            counterSTP = -1
            savedTwitterPosts = savedTwitterPosts[0:numberOfTweetsLimit]
            Thread(target=lambda : displayNewsCard(self, counterTNS, name, "null", "twitter", savedTwitterPosts[0])).start() #display card
    else:
        print("0 twitter posts found for: " + name)
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "twitter", "null")).start() #display card
        print("twitter profile fetch failed")
        return


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
                    "type": "subreddit",
                    "profile": profile['name']
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
    else:
        print("0 subreddit posts found for: " + name)
        Thread(target=lambda : displayNewsCard(self, counterTNS, name, "default", "subreddit", "null")).start() #display card
        print("subreddit fetch failed")
        return


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


def displayNewsCard(self, id, username, type, platform, profileData):
    #check card id
    if id == 1: 
        cardObj = self.ids.newsCard1Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard1; 
        cardObj.order = 1
        self.changeButtonColor(1, platform)
    elif id == 2: 
        cardObj = self.ids.newsCard2Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard2; 
        cardObj.order = 2
        self.changeButtonColor(2, platform)
    elif id == 3: 
        cardObj = self.ids.newsCard3Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard3; 
        cardObj.order = 3
        self.changeButtonColor(3, platform)
    elif id == 4: 
        cardObj = self.ids.newsCard4Post; 
        boxlayoutObj = self.ids.boxLayoutNewsCard4; 
        cardObj.order = 4
        self.changeButtonColor(4, platform)

    #check platform
    if platform == "twitter": 
        cardObj.type = "twitter"
        cardObj.text = "Twitter · No posts found..."
    elif platform == "youtube": 
        cardObj.text = "YouTube · No posts found..."
        cardObj.type = "youtube"
    elif platform == "article": 
        cardObj.text = "Articles · No posts found..."
        cardObj.type = "article"
    elif platform == "subreddit": 
        cardObj.text = "Subreddit · No posts found..."
        cardObj.type = "subreddit"
    
    #check data
    if profileData != "null" and platform == "twitter":
        cardObj.text = "Twitter · Click to start..."
    elif profileData != "null" and platform == "youtube":
        cardObj.text = "YouTube · Click to start..."
    elif profileData != "null" and platform == "article":
        cardObj.text = "Articles · Click to start..."
    elif profileData != "null" and platform == "subreddit":
        cardObj.text = "Subreddit · Click to start..."
    
    #display card    
    boxlayoutObj.opacity = 1
    cardObj.opacity = 1


def undisplayNewsCard(self, id):
    if id == 1: self.ids.boxLayoutNewsCard1.opacity = 0
    elif id == 2: self.ids.boxLayoutNewsCard2.opacity = 0
    elif id == 3: self.ids.boxLayoutNewsCard3.opacity = 0
    elif id == 4: self.ids.boxLayoutNewsCard4.opacity = 0



### code ###
class NewsFeedScreen(Screen):
    def __init__(self, **var_args):
        super(NewsFeedScreen, self).__init__(**var_args)
        self.ids.category1.text = "\nWelcome to Scraper News \n               § = link\n               + = save"


    def on_pre_enter(self, *args):
        print("NewsFeedScreen")
        
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
                    "profile": post['profile'], 
                    "date": post['date'],
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['text'],
                    "img": "/thumbnails/" + post['profile'] + ".jpg",
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
                    "profile": post['profile'],
                    "date": post['date'], 
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['title'],
                    "img": "/thumbnails/" + post['profile'] + ".jpg",
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
                    "profile": post['profile'],
                    "date": post['date'], 
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['title'],
                    "img": "/thumbnails/" + post['profile'] + ".jpg",
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
                    "profile": post['profile'],
                    "date": post['date'], 
                    "platform": type, 
                    "savedAt": str(datetime.datetime.now())[0:10], 
                    "text": post['title'],
                    "img": "/thumbnails/" + post['profile'] + ".jpg",
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
        print(str(obj))
        id = obj['id']
        profile = obj['profile']
        platform = obj['platform']
        savedAt = obj['savedAt']
        text = obj['text']
        img = obj['img']
        date = obj['date']
        link = obj['link']

        #clean card text
        if platform == "twitter": text = newsTextCleaner(self, platform, text)

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
        imgSrc = os.getcwd() + "/thumbnails/" + str(profile) + ".jpg"
        btnProfileImg = Button(
            size_hint_x = None, 
            size_hint_y = None, 
            height = 220, 
            width = 220, 
            background_normal =  imgSrc,
            background_down =  imgSrc,
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
        btn1.bind(on_press=lambda *args: NewsFeedScreen.removeFromFavorites(self, id))
        btn2.bind(on_press=lambda *args: NewsFeedScreen.copyToClipboard(self, link))

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

            #variables
            username = str(savedTwitterPosts[counterSTP]["username"])
            id = str(savedTwitterPosts[counterSTP]["id"]) + "/" + str(len(savedTwitterPosts))
            date = str(savedTwitterPosts[counterSTP]["date"])
            text = str(savedTwitterPosts[counterSTP]["text"])
            images = savedTwitterPosts[counterSTP]["images"]
            videos = savedTwitterPosts[counterSTP]["videos"]
            youtube = str(savedTwitterPosts[counterSTP]["youtube"])

            #clean card text
            text = newsTextCleaner(self, 'twitter', text)

            #set card text
            cardText = id + " · " + "Twitter" + " · " + date + "\n\n" + text + "\n"
            # print(cardText)

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
            cardText = savedYoutubePosts[counterSYP]['id'] + "/" + str(totalYoutubeVideos) + " · " + "YouTube" + " · " + savedYoutubePosts[counterSYP]['date'] + "\n\n" + savedYoutubePosts[counterSYP]['title']
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
            cardText = savedNewsArticles[counterSNA]['id'] + "/" + str(totalArticles) + " · " + "Article" + " · " + savedNewsArticles[counterSNA]['date'] + "\n\n" + savedNewsArticles[counterSNA]['title']
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
            cardText = savedSubredditPosts[counterSSP]['id'] + "/" + str(totalSubredditPosts) + " · " + "Subreddit" + " · " + savedSubredditPosts[counterSSP]['date'] + "\n\n" + savedSubredditPosts[counterSSP]['title']
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