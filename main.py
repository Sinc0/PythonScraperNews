### imports ###
import requests
import re
import twint
import time
import datetime
import json

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
def fetch_youtube_channel(url):
    #variables
    requestHeaders = {'user-agent': 'my-app/0.0.1', 'Cookie':'CONSENT=YES+cb.20210418-17-p0.en+FX+917;PREF=hl=en'}
    numberOfVideosLimit = 3
    channelTitle = ""

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
        print(channelTitle + " latest videos:")
    else:
        print("youtube channel fetch failed")

    #regex youtube video data
    requestResultText = str(requestResultText).replace("\\u0026", "&")
    regexYoutubeVideos = re.findall(r'"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"', requestResultText)

    for videoTitle in regexYoutubeVideos[:numberOfVideosLimit]:
        global youtubeVideoCounter
        youtubeVideoCounter += 1

        #format youtube video upload date
        formatFindUploadDate = re.findall(r':"[\d]*\s[^.]*ago"', videoTitle)
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
            print("#" + str(youtubeVideoCounter) + " - " + str(formatedUploadDate) + " - " + str(formatedTitle))
        else:
            print(str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
        
    print("")

def fetch_twitter_profile(username):
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
        print(username + " latest tweets:")
        tCounter = 0
        for t in userTweets[:numberOfTweetsLimit]:
            tCounter += 1
            # print("#" + str(tCounter) + " - " + t.username + " - " + t.datestamp + " - " + t.tweet)
            print("#" + str(tCounter) + " - " + t.datestamp + " - " + t.tweet)
        
        # print(str(len(userTweets)))
        print("")
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

def add_profile(name, youtube = None, twitter = None):
    #fetch all saved profiles from json file
    file = open('profiles.json', "r")
    profiles = json.load(file)
    totalProfiles = len(profiles)

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

### tests ###
year_progress()
print("")

# fetch_youtube_channel('https://www.youtube.com/c/animalplanet/videos')
# fetch_youtube_channel('https://www.youtube.com/c/KimerLorens/videos')

# fetch_twitter_profile("animalplanet")
# fetch_twitter_profile("elonmusk")
# fetch_twitter_profile("spacex")
# fetch_twitter_profile("tesla")

add_profile("test")
