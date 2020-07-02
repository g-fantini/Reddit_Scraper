'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''
import sys
import io
import logging
import json
import requests
import threading
from PicturesElaborator import PicturesElaborator
from string import Template

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class RedditScraper():
    
    N_TARGET = 3
    MAXTHREADS = 7
    total = 0
    rgb_color = ""
    __reddit_url = "https://www.reddit.com/search.json"
    
    def __init__(self, rgb_color, topic, limit=30, sort='top'):
        self.rgb_color = rgb_color
        self.set_reddit_url(topic,limit,sort)
        
    
    def set_reddit_url(self,topic,limit=100,sort='top'):
        """
        Set the reddit url
        
        Parameters:
        topic (string): topic to search
        limit (int): limit for the results
        sort (string): sort type ("top","hot","relevance","new","comments")
                 
        """
        template_url = Template('https://www.reddit.com/search.json?q=title:$topic&is_sort:true&limit=$limit&sort=$sort')
        self.__reddit_url = template_url.substitute(topic=topic, limit=limit, sort=sort)
        logging.debug("Reddit URL set to: " + self.__reddit_url)
        
    def get_reddit_url(self):
        """
        Get the reddit url
                 
        """
        return  self.__reddit_url
    
    def get_reddit_response(self):
        """
        Returns the Reddit page parsed into a dictionary
        
        Returns:
        {} : reddit page parsed
        """
        return json.loads(requests.get(self.get_reddit_url(), headers = {'User-agent': 'Reddit Scraper v1'}).text)
    
    def is_image(self, img_url):
        """
        Returns True if the url is referring to an image, False otherwise
        
        Parameters:
        img_url (string): img URL
        
        Returns:
        bool: True if the url is referring to an image, False otherwise
        """
        return img_url.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
        
    def parse_posts(self, threshold=70, num_colors=7):
        """
        Parse the Reddit page and iterates through the posts
        
        Parameters:
        threshold (int): threshold value for the colors
        number_of_colors: top number_of_colors to consider
        
        Returns:
        matches []: sorted list containing all the image matching the color and the related num_comments 
        """
        PicturesElaborator.empty_directory()
        
        semaphore = threading.Semaphore(value=self.MAXTHREADS)
        threads = list()
        
        response = self.get_reddit_response()    
        
        for post in response["data"]['children']:
            
            if(PicturesElaborator.get_images_counter()>=self.N_TARGET):
                break
            elif(post['data']['url'] and self.is_image(post['data']['url'])):
                semaphore.acquire()
                thread = threading.Thread(target=PicturesElaborator.filter_image, args=({"img_url":post['data']['url'],"num_comments":post['data']['num_comments']}, self.rgb_color, semaphore, threshold, num_colors))
                threads.append(thread)
                thread.start()      
        
        for x in threading.enumerate():
            if(threading.currentThread() == x):
                pass
            else:
                x.join()
                
        logging.debug("Result: " + str(PicturesElaborator.get_sorted_matches()))
        
        return PicturesElaborator.get_sorted_matches()