import requests
import chompjs
import random
import time
import re
import json
import traceback
import undetected_chromedriver as uc

from bs4 import BeautifulSoup
from bs4.element import Tag

from urllib.parse import urlparse, unquote, parse_qs

from .linktypes import *

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from random_user_agent.user_agent import UserAgent

from typing import Callable, Literal, overload

ua = UserAgent(limit=50).get_random_user_agent()
headers = {"User-Agent" : ua}

def resolve_redirects(url:str) -> str:
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        raise RuntimeError(f"{url}::{resp.status_code}")
    return resp.url

@overload
def webdrv_find(driver : EC.AnyDriver, 
                condition : Callable[[EC.AnyDriver], WebElement], 
                timeout : float = 3.0, 
                poll_frequency : float = 0.5, 
                strict = False,
                invert = False) -> WebElement | None: ...
@overload
def webdrv_find(driver : EC.AnyDriver, 
                condition : Callable[[EC.AnyDriver], WebElement], 
                timeout : float = 3.0, 
                poll_frequency : float = 0.5, 
                strict = True,
                invert = False) -> WebElement: ...
@overload
def webdrv_find(driver : EC.AnyDriver, 
                condition : Callable[[EC.AnyDriver], WebElement], 
                timeout : float = 3.0, 
                poll_frequency : float = 0.5, 
                strict = False,
                invert = True) -> WebElement | Literal[True] | None: ...
@overload
def webdrv_find(driver : EC.AnyDriver, 
                condition : Callable[[EC.AnyDriver], WebElement], 
                timeout : float = 3.0, 
                poll_frequency : float = 0.5, 
                strict = True,
                invert = True) -> WebElement | Literal[True]: ...

def webdrv_find(driver, condition, timeout=3.0, poll_frequency=0.5, strict=False, invert=False):
    try:
        waiter = WebDriverWait(driver, timeout, poll_frequency)
        elem = waiter.until_not(condition) if invert else waiter.until(condition)
        return elem
    except TimeoutException:
        if strict:
            raise
        else:
            print(f"Waited enough ({timeout} secs) for {condition.__name__}")
            return


def linktree_bypass(account_id:int, link_id:int) -> str:
    payload = {
        'accountId' : account_id,
        'validationInput' : {
            'acceptedSensitiveContent' : [link_id],
            'age' : random.uniform(19.2, 25.6)
        }
    }

    resp = requests.post("https://linktr.ee/api/profiles/validation/gates", json=payload, headers=headers)

    if resp.ok:
        return resp.json()['links'][0]['url']
    else:
        raise RuntimeError(f"Linktr.ee BYPASS failed: {resp.status_code} :\n\n{resp.text}")

def linktree(url:str) -> LinktreeTree:
    print("Using Linktr.ee")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        data_raw = str(soup.find('script', {'id' : '__NEXT_DATA__'}).contents[0]) # type: ignore
        data_dict = json.loads(data_raw)

        account_dict = data_dict['props']['pageProps']['account']
        account_id = account_dict['id']
        account_username = account_dict['username']
        account_avatar = account_dict['profilePictureUrl']
        account_tz = account_dict['timezone']

        links = account_dict['links']
        packed_links = []
        for link_dict in links:

            link_id = link_dict['id']
            link_title = link_dict['title']
            link_type = link_dict["type"]
            link_domain = link_dict['rules']['gate']['sensitiveContent']['domain']
            link_url = link_dict['url']
            if not link_domain:
                link_domain = urlparse(link_url).netloc

            if link_url == None:
                # sensitive content warning, age verification etc
                if "sensitiveContent" in link_dict['rules']['gate']['activeOrder']:
                    link_url = linktree_bypass(account_id,link_id)
                else:
                    raise RuntimeError(f"Linktr.ee GET_URL Failed: \n\n{link_dict}")

            packed_links.append(LinktreeLink(**{
                'id' : link_id,
                'domain' : link_domain,
                'type' : link_type,
                'title' : link_title,
                'url' : link_url
            }))

        packed_info = {
            'id' : account_id,
            'username' : account_username,
            'avatar' : account_avatar,
            'tz' : account_tz,
            'links' : packed_links
        }

        return LinktreeTree(**packed_info)

    else:
        raise RuntimeError(f"Linktr.ee GET Failed: {resp.status_code} :\n\n{resp.text}")    


def hoobe(url:str) -> HoobeTree:
    print("Using Hoo.be")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        data_raw = str(soup.find('script', {'id' : '__NEXT_DATA__'}).contents[0]) # type: ignore
        data_dict = json.loads(data_raw)

        account_dict = data_dict['props']['pageProps']['user']
        account_id = account_dict['id']
        account_username = account_dict['handle']
        account_fullname = account_dict['fullName']
        account_usertype = account_dict['userType']
        account_avatar = ''
        account_created = account_dict['createdUtc']
        account_updated = account_dict['updatedUtc']
        if account_dict['hasPhoto']:
            unparsed_url = soup.find('div', {'class' : re.compile('^StaticProfileImage_staticImageContainer.*?')}).find('img').get('src') #type: ignore
            account_avatar = unquote(re.search(r"\?url=(.*)\&w=", unparsed_url).group(1)) #type: ignore
        
        social_buttons = data_dict['props']['pageProps']['userSocialPlatform']
        packed_links = []
        for button in social_buttons:
            button_id = button['id']
            button_url = button['link']
            button_domain = urlparse(button_url).netloc
            packed_links.append(HoobeLinkShort(**{
                'id' : button_id,
                'domain' : button_domain,
                'url' : button_url
            }))

        links = data_dict['props']['pageProps']['content']
        for link in links:
            link_data = link['content']
            link_id = link_data['id']
            link_title = link_data['title']
            link_url = link_data['link']
            link_domain = urlparse(link_url).netloc
            link_created = link_data['createdUtc']
            link_updated = link_data['updatedUtc']
            packed_links.append(HoobeLink(**{
                'id' : link_id,
                'title' : link_title,
                'domain' : link_domain,
                'created' : link_created,
                'updated' : link_updated,
                'url' : link_url
            })) 

            

        packed_info = {
            'id' : account_id,
            'username' : account_username,
            'displayname' : account_fullname,
            'usertype' : account_usertype,
            'avatar' : account_avatar,
            'created' : account_created,
            'updated' : account_updated,
            'links' : packed_links
        }

        return HoobeTree(**packed_info)

    else:
        raise RuntimeError(f"Hoo.be GET Failed: {resp.status_code} :\n\n{resp.text}")


def snipfeed(url:str) -> SnipfeedTree:
    print("Using Snipfeed.co")
    try:
        options = uc.ChromeOptions()
        #options.add_argument('headless')
        #drv = uc.Chrome(driver_executable_path=CHROMEDRIVER, options=options)
        drv = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
        drv.get(url)
        drv.reconnect(timeout=0.2)

        timeout = 10

        element_present = EC.presence_of_element_located((By.ID, '__next'))
        webdrv_find(drv, element_present, timeout, strict=True)

        soup = BeautifulSoup(drv.page_source, 'html.parser') #type: ignore
        data_raw = str(soup.find('script', {'id' : '__NEXT_DATA__'}).contents[0]) # type: ignore
        data_dict = json.loads(data_raw)

        account_dict = data_dict['props']['pageProps']['creatorLink']
        account_id = account_dict['owner']['databaseId']
        account_username = account_dict['username']
        account_avatar = account_dict['profile']['avatarAsset']['facades']['image']['url']

        blocks = account_dict['blocks']
        packed_links = []
        for block in blocks:
            if block['__typename'] == 'SocialIconsBlock':
                for link_dict in block['links']:
                    link_id = link_dict['id']
                    link_platform = link_dict['platform']
                    link_url = link_dict['url']
                    link_domain = urlparse(link_url).netloc
                    packed_links.append(SnipfeedLinkShort(**{
                        'id' : link_id,
                        'domain' : link_domain,
                        'platform' : link_platform,
                        'url' : link_url
                    }))

            elif block['__typename'] == 'CustomBlock':
                link_id = block['id']
                link_url = block['url']
                link_title = block['title']
                link_domain = urlparse(link_url).netloc
                try:
                    link_image = block['coverAsset']['facades']['image']['url']
                except TypeError:
                    link_image = None

                packed_links.append(SnipfeedLink(**{
                        'id' : link_id,
                        'domain' : link_domain,
                        'title' : link_title,
                        'image' : link_image,
                        'url' : link_url
                    }))

        packed_info = {
            'id' : account_id,
            'username' : account_username,
            'avatar' : account_avatar,
            'links' : packed_links
        }

        return SnipfeedTree(**packed_info)

    finally:
        drv.quit()

def beacons(url:str) -> BeaconsTree:
    print("Using Beacons.ai")
    try:
        options = uc.ChromeOptions()
        #options.add_argument('headless')
        drv = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
        drv.get(url)
        drv.reconnect(timeout=3)

        timeout = 5

        element_present = EC.presence_of_element_located((By.ID, '__image__'))
        webdrv_find(drv, element_present, 5)

        element_present = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'I am 18 or older')]"))
        elem = webdrv_find(drv, element_present)
        if elem:
            elem.click()

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'mt-0'))
        header_elem = webdrv_find(drv, element_present, strict=True)

        header_tag : str = header_elem.get_attribute('innerHTML') #type: ignore
        header = BeautifulSoup(header_tag, 'html.parser')
        header_tags = list(header.find_all('div'))
        
        account_username = header_tags[1].contents[0] 
        print(account_username)
        if isinstance(account_username, Tag):
            account_username = header.find('div', {'aria-label' : 'profile tag'}).find('span').contents[0] # type: ignore
        assert account_username
        account_avatar = header_tags[0].find('img', {'alt' : lambda x: 'profile' in x}).get('src') # type: ignore

        element_present = EC.presence_of_element_located((By.CLASS_NAME, "Links"))
        links_elem = webdrv_find(drv, element_present, strict=True)
        links_tag : str = links_elem.get_attribute('outerHTML') #type: ignore

        link_block = BeautifulSoup(links_tag, 'html.parser')
        links = link_block.find_all('a') # type: ignore

        packed_links = []
        for link in links:
            link_url = link.get('href')
            link_title = link.find('div', {'class' : 'text-16'}).contents[0]
            link_image = link.find('img', {'alt':'link'}).get('src')
            link_domain = urlparse(link_url).netloc
            packed_links.append(BeaconsLink(**{
                'title' : link_title,
                'domain' : link_domain,
                'image' : link_image,
                'url' : link_url
            }))

        element_present = EC.presence_of_element_located((By.CLASS_NAME, "flex-wrap"))
        small_links_elem = webdrv_find(drv, element_present)
        if small_links_elem:
            small_links_tag : str = small_links_elem.get_attribute('outerHTML') #type: ignore
            small_links = BeautifulSoup(small_links_tag, 'html.parser').find('a') 
            for small_link in small_links: #type: ignore
                link_url = small_link.get('href')
                if not link_url: continue
                link_domain = urlparse(link_url).netloc
                packed_links.append(BeaconsLinkShort(**{
                    'domain' : link_domain,
                    'url' : link_url
                }))

        packed_info = {
            'username' : account_username,
            'avatar' : account_avatar,
            'links' : packed_links
        }
        
        return BeaconsTree(**packed_info)
    
    finally:
        drv.quit()


def allmylinks(url:str) -> AllmylinksTree:
    print("Using Allmylinks.com")

    try:
        options = uc.ChromeOptions()
        #options.add_argument('headless')
        #drv = uc.Chrome(driver_executable_path=CHROMEDRIVER, options=options)
        drv = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
        drv.get(url)
        drv.reconnect(timeout=1)

        timeout = 10

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'wrap'))
        webdrv_find(drv, element_present, timeout, strict=True)

        soup = BeautifulSoup(drv.page_source, 'html.parser')
        account_username = soup.find('span', {'class' : 'profile-usertag'}).contents[0].replace('@','').strip() # type: ignore
        account_displayname = soup.find('span', {'class' : 'profile-username profile-page'}).contents[0].strip() # type: ignore
        account_avatar = soup.find('img', {'alt' : 'Profile avatar'}).get('src') # type: ignore
        links = soup.find_all('div', {'class' : 'link-content'})
        packed_links = []
        for link in links:
            link_title = link.find('span', {'class' : 'link-title'}).contents[0]
            link_image = link.find('img', {'class' : 'cover-img'}).get('src')
            if not urlparse(link_image).netloc:
                parsed_url = urlparse(url)
                link_image = f"{parsed_url.scheme}://{parsed_url.netloc}/{link_image}"
            link_url = link.find('a', {'class' : re.compile('link'), 'title' : True}).get('data-x-url')
            link_url = link_url.strip("mailto:")
            link_domain = urlparse(link_url).netloc
            packed_links.append(AllmylinksLink(**{
                'title' : link_title,
                'image' : link_image,
                'domain' : link_domain,
                'url' : link_url
            }))
        packed_info = {
            'username' : account_username,
            'displayname' : account_displayname,
            'avatar' : account_avatar,
            'links' : packed_links
        }
        
        return AllmylinksTree(**packed_info)
    
    finally:
        drv.quit()

    

def milkshake(url:str) -> MilkshakeTree:
    print('Using Msha.ke')
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore

        # :(
        account_username = urlparse(url).path

        link_panel = soup.find('div', {'class' : 'look1-links__links-panel'})
        links = link_panel.find_all('a', {'rel' : 'ugc'}) # type: ignore
        packed_links = []
        for link in links:
            link_url = link.get('href')
            link_title = link.contents[0]
            link_domain = urlparse(link_url).netloc
            packed_links.append(MilkshakeLink(**{
                'title' : link_title,
                'domain' : link_domain,
                'url' : link_url
            }))
        
        packed_info = {
            'username' : account_username,
            'avatar' : "",
            'links' : packed_links
        }

        return MilkshakeTree(**packed_info)

    else:
        raise RuntimeError(f"Msha.ke GET Failed: {resp.status_code} :\n\n{resp.text}")  


def linkr(url:str) -> LinkrTree:
    print("Using Linkr.bio")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        raw_data = soup.find('script').contents[0] #type: ignore
        profile = re.search(r"r\.data=(.*);return", raw_data).group(1) #type: ignore
        parsed_profile = chompjs.parse_js_object(profile)

        account_username = urlparse(url).path
        account_avatar = parsed_profile['profilePic']
        account_desc = parsed_profile['bio']

        links = re.search(r"\{modules:(.*),pageInfo:", raw_data).group(1) #type: ignore
        parsed_links = chompjs.parse_js_object(links)
        packed_links = []
        for link in parsed_links:

            if isinstance(link, str): continue
            link = link['data']

            link_id = link['id']
            link_title = link['title']
            link_image = link['image']
            link_created = link['createdAt']
            link_url = link['ourl']
            if len(link_image) == 1:
                link_image = None
            if len(link_created) == 1:
                link_created = None
            link_domain = urlparse(link_url).netloc
            packed_links.append(LinkrLink(**{
                'id' : link_id,
                'title' : link_title,
                'image' : link_image,
                'created' : link_created,
                'domain' : link_domain,
                'url' : link_url
            }))

        packed_info = {
            'username' : account_username,
            'description' : account_desc,
            'avatar' : account_avatar,
            'links' : packed_links
        }

        return LinkrTree(**packed_info)

    else:
        raise RuntimeError(f"Linkr.bio GET Failed: {resp.status_code} :\n\n{resp.text}")  


def carrd(url:str) -> CarrdTree:
    print("Using Carrd.co")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore

        account_username = soup.find('h1', {'id' : 'text03'}).contents[0].replace('@', '') # type: ignore
        account_avatar_uri = soup.find('div', {'id' : 'image01'}).find('img').get('src') # type: ignore
        account_avatar = f"{url if url.endswith('/') else url + '/'}{account_avatar_uri}" 
        account_desc = soup.find('p', {'id' : 'text02'}).contents[0] # type: ignore

        links = soup.find('ul', {'id' : 'buttons01'}).find_all('li') # type: ignore
        packed_links = []
        for link in links:
            link_title = link.find('span', {'class' : 'label'}).contents[0]
            link_url = link.find('a').get('href')
            link_domain = urlparse(link_url).netloc
            packed_links.append(CarrdLink(**{
                'title' : link_title,
                'domain' : link_domain,
                'url' : link_url
            }))

        packed_info = {
            'username' : account_username,
            'avatar' : account_avatar,
            'description' : account_desc,
            'links' : packed_links
        }

        return CarrdTree(**packed_info)

    else:
        raise RuntimeError(f"Carrd.co GET Failed: {resp.status_code} :\n\n{resp.text}")

def lnkbio_geturl(url:str) -> str:
    return parse_qs(urlparse(url).query)['d'][0]

def lnkbio(url:str) -> LnkbioTree:
    print("Using Lnk.bio")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        account_id = soup.find('input', {'id' : 'LB_UserID'}).get('value') # type: ignore
        account_tz = soup.find('input', {'id' : 'LB_UserTimezone'}).get('value') # type: ignore
        account_username = soup.find('a', {'class' : re.compile('pb-username')}).contents[0].replace('@','') # type: ignore
        account_avatar = soup.find('img', {'id' : 'profile_picture_catch_error'}).get('src') # type: ignore

        packed_links = []

        deeplinks = soup.find('div', {'class' : re.compile('deep-links')}).find_all('a') # type: ignore
        for deeplink in deeplinks:
            link_url = lnkbio_geturl(deeplink.get('href'))
            link_domain = urlparse(link_url).netloc
            packed_links.append(LnkbioLinkShort(**{ #type: ignore
                'domain' : link_domain,
                'url' : link_url
            }))

        links = soup.find('div', {'id' : 'links_container_overall'}).find_all('a') # type: ignore
        for link in links:
            link_id = link.get('id')
            link_title = link.get('title')
            link_url = lnkbio_geturl(link.get('href'))
            link_domain = urlparse(link_url).netloc
            packed_links.append(LnkbioLink(**{
                'id' : link_id,
                'title' : link_title,
                'domain' : link_domain,
                'url' : link_url
            }))
        
        packed_info = {
            'id' : account_id,
            'username' : account_username,
            'avatar' : account_avatar,
            'tz' : account_tz,
            'links' : packed_links
        }

        return LnkbioTree(**packed_info)

    else:
        raise RuntimeError(f"Lnk.bio GET Failed: {resp.status_code} :\n\n{resp.text}")

def directme(url:str) -> DirectmeTree:
    print("Using Direct.me")
    try:
        options = uc.ChromeOptions()
        #options.add_argument('headless')
        #drv = uc.Chrome(driver_executable_path=CHROMEDRIVER, options=options)
        drv = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
        drv.get(url)
        #drv.reconnect(timeout=3)

        timeout = 5

        element_present = EC.presence_of_element_located((By.ID, 'profile'))
        webdrv_find(drv, element_present, timeout, strict=True)

        soup = BeautifulSoup(drv.page_source, 'html.parser')

        account_header = soup.find('div', {'class' : 'profileHeader'})
        account_username = account_header.find('h1').contents[0].strip() # type: ignore
        account_avatar = account_header.find('img', {'id' : 'profileAvatar'}).get('src') # type: ignore
        account_desc = account_header.find('p', {'class' : 'bio'}).contents[0].strip() # type: ignore
        packed_links = []
        links = soup.find('div', {'class' : re.compile('profileItemsContainer')}) # type: ignore
        social_media_icons = links.find('div', {'class' : ('profileSocialIcons')}).find_all('a') # type: ignore
        for social_media_icon in social_media_icons:
            link_url = social_media_icon.get('href')
            link_domain = urlparse(link_url).netloc
            packed_links.append(DirectmeLinkShort(**{
                'domain' : link_domain,
                'url' : link_url
           }))
        main_links = links.find('div').find_all('div', recursive=False)[1:] # type: ignore
        for main_link in main_links:
            link_title = main_link.find('div', {'class' : 'profileElementContent'}).find('h2').contents[0]
            link_url = main_link.find('a').get('href')
            if link_url == "#updatesEmail":
                continue
            link_domain = urlparse(link_url).netloc
            packed_links.append(DirectmeLink(**{
                'title' : link_title,
                'domain' : link_domain,
                'url' : link_url
            }))

        packed_info = {
            'username' : account_username,
            'avatar' : account_avatar,
            'description' : account_desc,
            'links' : packed_links
        }

        return DirectmeTree(**packed_info)
    
    finally:
        drv.quit()

def linkme(url:str) -> LinkmeTree:
    print("Using Link.me...")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        data_raw = str(soup.find('script', {'id' : '__NEXT_DATA__'}).contents[0]) # type: ignore
        data_dict = json.loads(data_raw)

        media_endpoint = data_dict['runtimeConfig']['mediaEndpoint'] + '/images'
        user_endpoint = data_dict['runtimeConfig']['apiEndpoints']['user']

        ip = data_dict['props']['pageProps']['ip']
        
        user_info = data_dict['props']['pageProps']['profile']

        user_id = user_info['id']
        user_firstname = user_info['firstName']
        user_lastname = user_info['lastName']
        user_username = user_info['username']
        user_verified = user_info['verifiedAccount']
        user_bio = user_info['bio']
        user_ambassador = user_info['isAmbassador']
        user_avatar = media_endpoint+'/'+user_info['profileImage']
        user_profile_visits = user_info['profileVisitCount']

        user_weblinks_raw : list[dict] = user_info['webLinks']
        user_weblinks = []

        for weblink_raw in user_weblinks_raw:
            weblink = {}
            weblink.update({'id':weblink_raw['links'][0]['webLinkId']})
            weblink.update({'title':weblink_raw['title']})
            weblink.update({'url':weblink_raw['links'][0]['linkValue']})
            weblink.update({'image':media_endpoint+'/'+weblink_raw['links'][0]['linkImage']})
            weblink.update({'domain':urlparse(weblink_raw['links'][0]['baseUrl']).netloc})
            user_weblinks.append(LinkmeLinkShort(**weblink))

        params = {
            'userId' : user_id,
            'limit' : 9999 # arbitrary max value
        }

        headers['version'] = '3.0.0'
        resp = requests.get(f'{user_endpoint}/user/api/v2/profile/profileWebLinks', headers=headers, params=params)
        if resp.ok:
            user_weblinks_raw : list[dict] = resp.json()['response']['list']
            del headers['version']
            for weblink_raw in user_weblinks_raw:
                weblink = {}
                weblink.update(weblink_raw)
                weblink['image'] = media_endpoint + '/' + weblink['image']
                weblink['type']['icon'] = media_endpoint + '/' + weblink['type']['icon']
                weblink['domain'] = urlparse(weblink['url']).netloc
                for _field in ('link_order', 'multilink'):
                    if weblink.get(_field, None) is not None:
                        del weblink[_field]
                
                user_weblinks.append(LinkmeLink(**weblink))

        else:
            raise RuntimeError(f"Link.me GET WebLinks failed: {resp.status_code} :\n\n{resp.text}")

        packed_info = {
            'ip' : ip,
            'id' : user_id,
            'first_name' : user_firstname,
            'last_name' : user_lastname,
            'username' : user_username,
            'verified' : user_verified,
            'bio' : user_bio,
            'ambassador' : user_ambassador,
            'avatar' : user_avatar,
            'profile_visits' : user_profile_visits,
            'links' : user_weblinks
        }

        return LinkmeTree(**packed_info)

    else:
        raise RuntimeError(f"Link.me GET failed: {resp.status_code} :\n\n{resp.text}")

def taplink(url:str) -> TaplinkTree:
    print("Using Taplink.cc")
    resp = requests.get(url, headers=headers)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser') #type: ignore
        script = soup.find('script').contents[0].strip() #type: ignore

        account_dict = json.loads(re.search(r"window\.account =(.*);", script).group(1)) #type: ignore
        data_dict = json.loads(re.search(r"window\.data =(.*);", script).group(1)) #type: ignore

        storage = account_dict['storage_domain']

        account_id = account_dict['account_id']
        profile_id = account_dict['profile_id']
        account_username = account_dict['username']
        account_nickname = account_dict['nickname']
        account_avatar = f"https://{storage}{account_dict['avatar']['url']}"

        links = data_dict['fields'][0]['items']
        packed_links = []
        for link in links:
            packed_link = {}
            if link['block_type_id'] == 1:
                account_name = link['options']['text']
            elif link['block_type_id'] == 2:
                link_title = link['options']['title']
                link_url = link['options']['value']
                link_domain = urlparse(link_url).netloc

                packed_link.update({
                    'title' : link_title,
                    'url' : link_url,
                    'domain' : link_domain
                })

                packed_links.append(TaplinkLink(**packed_link))

        assert account_name

        packed_info = {
            'id' : account_id,
            'profile_id' : profile_id,
            'username' : account_username,
            'displayname' : account_name,
            'nickname' : account_nickname,
            'avatar' : account_avatar,
            'links' : packed_links
        }

        return TaplinkTree(**packed_info)

    else:
        raise RuntimeError(f"Taplink.cc GET failed: {resp.status_code} :\n\n{resp.text}")

SUPPORTED = [linktree, hoobe, snipfeed, beacons, allmylinks, milkshake, linkr, carrd, lnkbio, directme, linkme, taplink]

def gather_links(url:str, /, *, _resolved=False) -> SocialsTree | None:

    """
    Parses supported Link Services' URLs, 
    detects if custom domain uses a supported service via redirects and worst case scenario, 
    tries all of the services on an unsupported URL (custom domain with no redirects).

    Parameters:
    url (str) : The URL to be parsed.
    _resolved (bool) : Internal argument passed to determine if the URL is resolved. Do NOT change its value.
    """

    match urlparse(url).netloc:
        case "linktr.ee":
            return linktree(url)
        case "hoo.be" | "moxylink.be":
            return hoobe(url)
        case "snipfeed.co":
            return snipfeed(url)
        case "beacons.ai" | "beacons.page":
            return beacons(url)
        case "allmylinks.com":
            return allmylinks(url)
        case "msha.ke":
            return milkshake(url)
        case "linkr.bio":
            return linkr(url)
        case str(string) if "carrd.co" in string:
            return carrd(url)
        case "lnk.bio":
            return lnkbio(url)
        case "direct.me":
            return directme(url)
        case "link.me":
            return linkme(url)
        case "taplink.cc":
            return taplink(url)
        case _:
            if not _resolved:
                print(f"Resolving possible redirects for {url}.")
                url = resolve_redirects(url)
                return gather_links(url, _resolved=True)
            else:
                print(f"Trying existing parsers for {url}.")
                for func in SUPPORTED:
                    try:
                        return func(url)
                    except:
                        traceback.print_exc()

