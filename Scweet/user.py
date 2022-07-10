import requests

from . import utils
from time import sleep
import random
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
def get_user_id(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = requests.Session()
    r = s.post('https://tweeterid.com/ajax.php',data={'input': username},headers=headers)

    return r

def find_user_id(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
         }
    s = requests.Session()
    r = requests.post('https://virtualfollow.com/search-profile-get-twitter-ID-username-converter',data={'SearchMe':username,'search' : '提交', 'session_csrf':''},headers=headers,timeout=(6,10))
    r = r.text
    r = r.split("ID for")[1]
    r = r.split(": ")[1]
    r = r.split("<")[0]
    print(r)
    return r

def get_user_idlocation(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    with requests.get("https://truetn.com/"+username,headers=headers,stream=True) as r:
        r = r.text
        id = r.split("profile_banners/")[1]
        id = id.split('/')[0]
        print(id)
        location = r.split('location":"')[1]
        location = location.split('"')[0]
        print(location)
    return id,location

def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    for i, user in enumerate(users):

        log_user_page(user, driver)

        if user is not None:

            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                # print(e)
                return

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e:
                # print(e)
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else:
                        location = span1
                        birthday = ""
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e:
                        # print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            id = get_user_id(user)
            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)
            print("id : ", id)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            if i == len(users) - 1:
                driver.close()
                #return users_info
                return id,location
        else:
            print("You must specify the user")
            continue

def get_user_info_request(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'cookie':'guest_id_marketing=v1%3A165742842451594540; guest_id_ads=v1%3A165742842451594540; personalization_id="v1_7RzmXAenHye3xdeOYVEYFg=="; guest_id=v1%3A165742842451594540; ct0=ed0c2e3e82d65c7afa0abbc0e19273e0; gt=1545993001041768448; _ga=GA1.2.1283528093.1657428431; _gid=GA1.2.1446441807.1657428431',
        'x-csrf-token':'ed0c2e3e82d65c7afa0abbc0e19273e0',
        'x-guest-token':'1545993001041768448',
        'x-connection-hash':'10746c07f2bbc7acc3e077e18c7bae70e816bce24e58467185070511a9dade4f',
    }
    s = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('https://',adapter)

    va = {"screen_name":username,"withSafetyModeUserFields":True,"withSuperFollowsUserFields":True}
    r = s.get('https://twitter.com/i/api/graphql/mCbpQvZAw6zu_4PvuAUVVQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22china_amb_india%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D' , headers=headers, timeout=(5, 10))
    r = r.text
    print(r)

def get_user_info(username,driver=None,headless=True):
    driver = utils.init_driver(headless=headless)
    log_user_page(username, driver)

    try:

        location = driver.find_element_by_xpath(
            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
    except Exception as e:
        # print(e)
        try:

            span1 = driver.find_element_by_xpath(
                '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            if hasNumbers(span1):
                birthday = span1
                location = ""
            else:
                location = span1
                birthday = ""
        except Exception as e:
            # print(e)
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                location = ""
            except Exception as e:
                # print(e)

                location = ""
    driver.close()
    #id = find_user_id(username)
    print(location)
    return location

def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following

def get_users_following_info(users,env,verbose = 1, headless = False, wait = 2, limit = float('inf'),file_path = None):
    user_following = get_users_following(users,env,file_path='users_following.csv')
    print(user_following)
    follow_elem,follow_id = utils.get_users_follow_info(users,headless,env,"following",verbose,wait=wait,limit=limit,outputfile=file_path)
    print(follow_elem,follow_id)
    return follow_elem,follow_id

def get_users_followers_info(users,env,verbose = 1, headless = False, wait = 2, limit = float('inf'),file_path = None):
    user_followers = get_users_followers(users,env)
    print(user_followers)
    follow_elem,follow_id = utils.get_users_follow_info(users,headless,env,"followers",verbose,wait=wait,limit=limit,outputfile=file_path)
    print(follow_elem)
    print(follow_id)

    return follow_elem,follow_id

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
