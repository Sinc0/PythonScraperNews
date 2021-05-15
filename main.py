### imports ###
import requests
import re

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

    #make request
    httpRequest = requests.get(url, headers=requestHeaders)

    #handle request result
    if httpRequest.status_code == 200:
        print("youtube channel fetch succesful")
        requestResultText = str(httpRequest.text)
    else:
        print("youtube channel fetch failed")

    #regex youtube video data
    requestResultText = str(requestResultText).replace("\\u0026", "&")
    regexYoutubeVideos = re.findall(r'"title":{"runs":\[{"text":"[^.]*"}],"[^.]*"publishedTimeText":{"simpleText":[^.]*ago"', requestResultText)

    for videoTitle in regexYoutubeVideos:
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
            print(" " + str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))
        else:
            print(str(youtubeVideoCounter) + ". " + str(formatedTitle) + " - " + str(formatedUploadDate))

### tests ###
fetch_youtube_channel('https://www.youtube.com/c/animalplanet/videos')
