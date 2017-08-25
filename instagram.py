import os
from selenium import webdriver
import requests, json
from time import gmtime, strftime


def get_json_obj(end_cursor, hashtag):
    url = "https://www.instagram.com/graphql/query/"

    querystring = {"query_id": "17875800862117404",
                   "variables": "{\"tag_name\":\""+hashtag+"\",\"first\":8,\"after\":\"" + end_cursor + "\"}"}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_resp_obj = json.loads(response.text)
    return json_resp_obj


def get_first_endcursor(hashtag):
    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
    end_cursor_value = driver.execute_script(
        'return window._sharedData[\'entry_data\'][\'TagPage\'][0]["tag"]["media"]["page_info"]["end_cursor"]')
    driver.quit()
    return end_cursor_value


def get_content(hashtag):
    first_encursor = get_first_endcursor(hashtag)
    json_resp_obj = get_json_obj(first_encursor, hashtag)
    status = json_resp_obj['status']
    if status == 'ok':
        check_next_page = json_resp_obj['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        if check_next_page:
            for value in xrange(counter):
                next_end_cursor = json_resp_obj['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
                json_resp_obj = get_json_obj(next_end_cursor, hashtag)
                node_length = len(json_resp_obj['data']['hashtag']['edge_hashtag_to_media']['edges'])
                for index in range(0, node_length):
                    list_of_urls.append(
                        json_resp_obj['data']['hashtag']['edge_hashtag_to_media']['edges'][index]['node'][
                            'display_url'])


def download_content(url, folder_name):

    location = os.getcwd()+"/"+folder_name
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(os.path.join(location, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename



list_of_urls = []
print '''

____ _ _ __ ___ ________

             ____      
       _____/ __ \_  __
      / ___/ / / / |/_/
     / /  / /_/ />  <  
    /_/  /_____/_/|_|  


____ _ _ __ ___ ________


'''

hashtag = raw_input('Enter Hashtag:')
counter = input('Enter count of content:')
get_content(hashtag)
folder_name = hashtag + "-"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
for urls in list_of_urls:
    download_content(urls, folder_name)
    print urls
