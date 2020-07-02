'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''
import os
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, deltaE_cie76
from sklearn.cluster import KMeans
from collections import Counter
from threading import Lock
from skimage import io
from PIL import Image
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class PicturesElaborator():
    
    IMG_DIRECTORY = "tmp/"
    __images_counter = 0
    __matches = []
    
    def __init__(self):
        pass
    
    @staticmethod 
    def add_match(match):
        """
        Add match to matches array
        
        Parameters:
        match ((img_path,num_comments)): list containing the image path and num_comments
        """
        
        data_lock = Lock()
        with data_lock:
            PicturesElaborator.__matches.append(match)
    
    @staticmethod 
    def reset_matches():
        """
        Resets matches array
        
        """
        
        data_lock = Lock()
        with data_lock:
            PicturesElaborator.__matches = []
    
    @staticmethod       
    def get_sorted_matches():
        """
        Returns matches array sorted by number of comments
        
        Returns:
        matches []: sorted list containing all the image matching the color and the related num_comments 
        """
        return sorted(PicturesElaborator.__matches, key=lambda post: post[1],reverse=True)
            
    @staticmethod 
    def get_images_counter():
        """          
        Returns: 
        int: the image_counter value          
        
        """
        data_lock = Lock()
        with data_lock:
            counter = len(PicturesElaborator.__matches)   
        return counter
   
    @staticmethod 
    def increment_images_counter():     
        """Increments the image_counter of 1"""
        
        data_lock = Lock()
        with data_lock:
            PicturesElaborator.__images_counter +=1
        logging.debug("image_counter incremented to: " + str( PicturesElaborator.__images_counter) )  
    
    @staticmethod 
    def get_img_path(url):
        """
        Returns the img path
        
        Parameters:
        url (string): img URL
        
        Returns:
        string: image path
        """
        return PicturesElaborator.IMG_DIRECTORY + url.split("/")[-1]

    @staticmethod
    def save_image(url):
        """
        Downloads the image in the IMG_DIRECTORY
        
        Parameters:
        url (string): img URL
        
        """
        
        #Create IMG_DIRECTORY if doesn't exist
        if not (os.path.isdir(PicturesElaborator.IMG_DIRECTORY)):
            try:
                os.mkdir(PicturesElaborator.IMG_DIRECTORY)
            except OSError:
                logging.debug("Creation of the directory %s failed" % PicturesElaborator.IMG_DIRECTORY)
            else:
                logging.debug("Successfully created the directory %s " % PicturesElaborator.IMG_DIRECTORY)
                    
        image =  io.imread(url)
        img_path = PicturesElaborator.get_img_path(url)        
        logging.debug("Saving " + url + " in " + img_path)
        Image.fromarray(image).save(img_path)
    
    @staticmethod
    def empty_directory():
        """Removes all the files contained in the IMG_DIRECTORY"""
        
        for f in os.scandir(PicturesElaborator.IMG_DIRECTORY):
            logging.debug("Removing: " + f.name)
            os.unlink(f)
    
    @staticmethod 
    def remove_image(path):
        """
        Removes single image
        
        Parameters: 
        path (string): img path
        
        Returns:
        bool: image removed correctly
        """
        logging.debug("Removing: " + path)
        return os.remove(path) 
    
    @staticmethod
    def open_img(url):
        """
        Returns the compressed img obj
        
        Parameters:
        url(string): img URL
        
        Returns:
        img object
        """
                
        PicturesElaborator.save_image(url)
        
        logging.debug("Opening " + PicturesElaborator.get_img_path(url))
        
        try:
            img = cv2.imread(PicturesElaborator.get_img_path(url))        
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #Resize image to improve performance
            logging.debug("Resizing " + PicturesElaborator.get_img_path(url))
            img = imutils.resize(img, width=300)
            return img
        except:
            logging.debug("Image not available")
            return False
  
        
  
    @staticmethod  
    def RGB2HEX(color):
        """
        Converts RGB to HEX 
        
        Parameters:
        color (string): RGB color
        
        Returns:
        string: color in HEX representation
        """
        
        return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

    @staticmethod
    def get_colors(image, number_of_colors=7, debug=False):
        """
        Approximates the colors present in the image, and returns the main ones.
        If the debug parameter is set to True, a pie chart representing the top number_of_colors present in the image
        will be displayed.
        
        Parameters:
        image (img obj): image object
        number_of_colors (int): number of colors to consider
        debug (bool): execution mode
        
        Returns:
        []: main RGB colors
        
        """
        modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
        try:
            modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
        except:
            logging.debug("image reshape failed")
            return False
            
        clf = KMeans(n_clusters = number_of_colors)
        labels = clf.fit_predict(modified_image)
        
        counts = Counter(labels)
        
        center_colors = clf.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]
        
        if(debug):
            hex_colors = [PicturesElaborator.RGB2HEX(ordered_colors[i]) for i in counts.keys()]
            plt.figure(figsize = (8, 6))
            plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
            plt.show()
            
        return rgb_colors
     
    @staticmethod  
    def match_image_by_color(image, rgb_color, threshold=60, number_of_colors=7): 
        """
        Evaluates if the rgb_color is present in the image with the given threshold
        
        Parameters:
        image (imb obj): img obj
        rgb_color (x,x,x): RGB rgb_color
        threshold (int): threshold value
        number_of_colors: top number_of_colors to consider
        
        Returns:
        bool: if the rgb_color given is present in the image with the given threshold
        
        """
        image_colors = PicturesElaborator.get_colors(image, number_of_colors)
        if not (image_colors):
            return False
        
        selected_color = rgb2lab(np.uint8(np.asarray([[rgb_color]])))
    
        select_image = False
        for i in range(number_of_colors):
            curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
            diff = deltaE_cie76(selected_color, curr_color)
            if (diff < threshold):
                select_image = True
        
        return select_image
    

              
    @staticmethod
    def filter_image(image_data, rgb_color, semaphore, threshold=60, colors_to_match=7):
        """
        Downloads the image from the given url and in case it contains the given RGB rgb_color with the 
        passed thresholder increase the image_counter
        
        Parameters:
        
        image_data {}: {"url":"","num_comments":""}
        rgb_color (string): RGB rgb_color
        threshold (int): rgb_color threshold 
        colors_to_match (int): number of top rgb_color to consider
        semaphore (threading.Semaphore): threading.Semaphore to limitate the creation of threads
        """
        
        data_lock = Lock()
        
        image = PicturesElaborator.open_img(image_data['img_url'])
        match = PicturesElaborator.match_image_by_color(image, rgb_color, threshold, colors_to_match)
        
        if not (match):
            PicturesElaborator.remove_image(PicturesElaborator.get_img_path(image_data['img_url']))
        else:
            logging.info("RGB"+str(rgb_color) + " found in: "+ image_data['img_url'])
            with data_lock:
                PicturesElaborator.add_match((image_data['img_url'],image_data['num_comments']))

        #release semaphore     
        semaphore.release()    
