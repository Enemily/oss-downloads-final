import os
import pandas as pd
import stscraper as scraper
gh_api = scraper.GitHubAPI("INSERT TOKENS")
gh_api.repo_info("embark-framework/embark") #test scraper

os.chdir("/Users/emilynguyen/Desktop/data2")
#csv of unique slugs and basic info about them (date they peaked (if so), how many contributors, size of repo, etc.)
df = pd.read_csv ("noUglySlugs.csv")
print(len(df))

# traverse through list of slugs
for i in range(0,len(df)):
    s = df['slug'][i]
    dead = False
    try:
        info = gh_api.repo_info(s)
        #see if project is archived
        dead = info['archived']
        ##TO FIND THE NUMBER OF STARGAZERS AND THE REPOSITORY'S SIZE, replace with info['stargazers_count'] and info['size'], respectively
        if i%10==0:
            print(i)
            df.to_csv("noUglySlugs.csv")
    except:
        pass
    df['archived'][i] = dead
