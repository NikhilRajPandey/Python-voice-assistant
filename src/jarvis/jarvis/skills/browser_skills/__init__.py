import wikipedia
import requests
import logging
import time
import re
import urllib.request
import subprocess
from bs4 import BeautifulSoup as bs

from jarvis.utils.response_utils import assistant_response


def _decoded_wiki_response(topic):
    """
    A private method for decoding the wiki response.
    :param topic: string
    :return:
    """
    ny = wikipedia.page(topic)
    data = ny.content[:500].encode('utf-8')
    response = ''
    response += data.decode()
    return response


def tell_me_about(tag, voice_transcript, **kargs):
    """
    Tells about something by searching in wikipedia
    :param tag: string (e.g 'about')
    :param voice_transcript: string (e.g 'about google')
    """
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            response = _decoded_wiki_response(topic)
            assistant_response(response)
    except Exception as e:
        logging.debug(e)
        assistant_response(" I can't find on the internet what you want")


def open_in_youtube(tag, voice_transcript, **kwargs):
    """
    Open a video in youtube.
    :param tag: string (e.g 'open')
    :param voice_transcript: string (e.g 'open in youtube tdex')
    """
    # TODO:  Replace with YOUTUBE API
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            search_text = reg_ex.group(1)
            base = "https://www.youtube.com/results?search_query=" + "&orderby=viewCount"
            r = requests.get(base + search_text.replace(' ', '+'))
            page = r.text
            soup = bs(page, 'html.parser')
            vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
            video = 'https://www.youtube.com' + vids[0]['href']
            subprocess.Popen(["python", "-m", "webbrowser", "-t", video], stdout=subprocess.PIPE)
    except Exception as e:
        logging.debug(e)
        assistant_response("I can't find what do you want in Youtube..")


def _create_url(tag):
    """
    Creates a url. It checks if there is .com suffix and add it if it not exist.
    :param tag: string (e.g youtube)
    :return: string (e.g http://www.youtube.com)
    """
    if re.search('.com', tag):
        url = 'http://www.' + tag
    else:
        url = 'http://www.' + tag + '.com'
    return url


def open_website_in_browser(tag, voice_transcript, **kwargs):
    """
    Opens a web page in the browser.
    :param tag: string (e.g 'open')
    :param voice_transcript: string (e.g 'open youtube')

    NOTE: If in the voice_transcript there are more than one commands_dict
    e.g voice_transcript='open youtube and open netflix' the application will find
    and execute only the first one, in our case will open the youtube.
    """
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            domain = reg_ex.group(1)
            url = _create_url(domain)
            assistant_response('Sure')
            subprocess.Popen(["python", "-m", "webbrowser", "-t", url], stdout=subprocess.PIPE)
            time.sleep(1)
            assistant_response('I opened the {0}'.format(domain))
    except Exception as e:
        logging.debug(e)
        assistant_response("I can't find this domain..")


def tell_me_today_news(**kwargs):
    try:
        news_url = "https://news.google.com/news/rss"
        Client = urllib.request.urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup = bs(xml_page, "xml")
        news_list = soup.findAll("item")
        for news in news_list[:5]:
            response = ""
            data = news.title.text.encode('utf-8')
            response += data.decode()
            assistant_response(response)
    except Exception as e:
        print(e)
        logging.debug(e)
