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
    formattedDate = str(month) + " " + str(day) + " " + str(year)
    # formattedDate = str(month) + " " + str(day) + " " + str(year) + " - " + str(dayOfTheYear) + "/" + str(totalDaysThisYear) + " - " + str(percentageOfYear)[2:4] + "%"
    
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