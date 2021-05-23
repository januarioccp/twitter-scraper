def deEmojify(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u00AB"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def remove_emojis(text: str) -> str:
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

def create_headers(bearer_token):
    """ Creates headers for requests """
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(query_field):
    """ Creates a API URL for reuqests """
    url = f'https://api.twitter.com/2/tweets/search/all?query={query_field}'
    return url

def connect_to_endpoint(url, headers):
    """ Connects to API URL endpoint """
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    # df = pandas.read_json()
    # df.to_csv()

    return response.json()

def main():

    token = ''
    stop = False
    tweets = set()
    for x in range(8000):
        print(x)
        time.sleep(3.1) # Sleep for 3 seconds
        headers = create_headers(settings.BEARER_TOKEN)
        query = '(#metooinceste OR #metooamnesie) lang:fr'
        # query = '(#metooincest OR #theflyingchildproject) lang:en'
        queryHTML = quote(query, safe='')

        start_time = 'start_time=2019-01-01T00:00:00.00Z'
        end_time   =   'end_time=2021-05-21T23:59:59.00Z'
        if token == '':
            url = create_url(queryHTML+'&max_results=100&'+start_time+'&'+end_time+'&tweet.fields=author_id,created_at,geo,id,lang,text')
        else:
            url = create_url(queryHTML+'&max_results=100&'+start_time+'&'+end_time+'&tweet.fields=author_id,created_at,geo,id,lang,text&next_token='+token)
        data = connect_to_endpoint(url, headers)
        
        
        # Find every instance of `text` in a Python dictionary.
        text = json_extract(data, 'text')
        for t in text:
            tweets.add(t)            
        
        # print(json.dumps(data, indent=4, sort_keys=True))
        
        try:
            token = json_extract(data, 'next_token')[0]
            with open(token+'.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
            # print(token)
        except:
            with open('last.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
            print("finished")
            stop = True

        if stop:
            break
    
    # print(tweets)
    tweetsList = list(tweets)
    tweetsList1 = [i.replace('\n','a') for i in tweetsList]
    tweetsList2 = [remove_emojis(i) for i in tweetsList1]
    complete = [deEmojify(i) for i in tweetsList2]
    hashtags = set()
    for t in complete:
            # print(t)
            # print()
            for h in re.findall(r"#(\w+)", t):
                hashtags.add(h.lower())
    
    hashtagList = list(hashtags)
    hashtagList.sort()

    tweetsFile=open('tweets: '+query+'.txt','w')
    for element in complete:
        tweetsFile.write(element)
        tweetsFile.write('\n')
        tweetsFile.write('\n')
    tweetsFile.close()

    hashtagFile=open('hashtag: '+query+'.txt','w')
    for element in hashtagList:
        hashtagFile.write(element)
        hashtagFile.write('\n')
        hashtagFile.write('\n')
    hashtagFile.close()

if __name__ == '__main__':

    from extract import json_extract
    import json
    import csv
    import settings
    import requests
    import pandas
    import time
    from requests.utils import quote
    import emoji
    import re


    main()