#TASK 1

#Twitter Free API tier does not provide access to any GET endpoints to scrape data from profiles 
# The free tier only allows for posting and deleting tweets on my own personal account (to my knowledge)
#I used the snscrape library: https://github.com/JustAnotherArchivist/snscrape

#Import libraries
import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv

#Initialize list for usernames and finalOutputs
usernames = []
finalOutput = []

#Tweet ID length: will be used to print the full ID of the pinned tweet, not in scientific notation
TWEET_ID_LENGTH = 18

#Read csv file containing the 20 Twitter account links and print only the usernames
with open('Twitter_Accounts.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    #Strip the "https://twitter.com/" portion of the link so that only the username remains. Each link is on a separate row in the csv file
    for row in csvReader:
        username = row[0].removeprefix("https://twitter.com/").strip()
        #Add each username to usernames list
        usernames.append(username)


#Note: A limitation of this code is that user profiles that do not have any tweets cannot have their data scraped
#The data scraped is based on the tweet at the top of the user's feed 

#Scrape data on Twitter profiles
#5 values should be outputted for each profile: Username, Followers Count, Location, Description/Bio, Pinned Tweet ID
#If the profile does not exist or does not have any tweets, "This account does not exist" will appear in the Username field and the rest of the fields will be empty
for username in usernames:
    items = next(sntwitter.TwitterUserScraper(username).get_items(), None)
    if items == None:
        finalOutput.append([f"{username} - This account does not exist", None, None, None, None])
        continue
  
    #Take list of usernames to scrape data on the Twitter profiles that exist and contain at least one tweet
    items = next(sntwitter.TwitterProfileScraper(username).get_items(), None)
    user = items.user
    pinnedTweetID = items.id
    finalOutput.append([user.username, user.followersCount, user.location, user.renderedDescription, f"{pinnedTweetID:{TWEET_ID_LENGTH}}"])
    #Note: If the profile has no pinned tweet, the ID of latest tweet at the top of the feed is printed

#Print values in csv file in rows and columns
twitterProfileInfo = pd.DataFrame(finalOutput, columns=['Username', 'Followers Count', 'Location', 'Description/Bio', 'Pinned Tweet ID'])
twitterProfileInfo.to_csv("Twitter_Profiles_Scraping.csv", index = False)
