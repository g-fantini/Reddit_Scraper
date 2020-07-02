'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''
from tkinter import *
from RedditScraper import RedditScraper
import logging
from PicturesElaborator import PicturesElaborator

class UIForm():
    
    FORM_TITLE = "Reddit Web Scraper"
    SORT = "TOP"
    THRESHOLD = 55
    NUM_COLORS = 7
    LIMIT = 500
    
    window = Tk()
    window.title(FORM_TITLE)
    window.geometry('450x200')
    
    def __init__(self):
        pass
    
    def is_valid_rgb(self,rgb_code):
        """
        Returns True if the rgb_code is valid
        
        Parameters:
        rgb_code(int): single RGB value
        
        Returns:
        bool: Returns True if the rgb_code is valid, False otherwise
        
        """
        return (rgb_code.isdigit() and int(rgb_code)>=0 and int(rgb_code)<=255)
    
    def display_msg(self, valid_topic, valid_rgb):
        """
        Displays pre-defined message to the user, depending if the
        parameters inserted in the form are valid or not.
        
        
        Parameters:
        valid_topic(bool): topic format
        valid_rgb(bool): RGB format
        
        """
        
        error = ""
        
        if not (valid_topic):
            error += "Topic needs to have at least 1 character \n"
            
        if not (valid_rgb):
            error += "RGB values needs to be between 0 and 255 \n"
        
        if(valid_rgb and valid_topic):
            error = "Searching for: " + self.topic.get()
            
        self.output.configure(text= error)
        
    def get_parameters(self):
        """
        Parse input of the user and change the field background if the value is valid or not
        
        Returns:
        bool: True if all the fields contains a valid value, False otherwise
        """
        valid_rgb = True
        valid_topic = True#
        
        #Reset field background
        self.rgb0.configure(bg="white")
        self.rgb1.configure(bg="white")
        self.rgb2.configure(bg="white")
        self.output.configure(bg="white")
        
        if not (len(self.topic.get())>0):
            logging.debug("topic invalid")
            self.topic.configure(bg="red")
            valid_topic = False     
            
        if not (self.is_valid_rgb(self.rgb0.get())):
            self.rgb0.configure(bg="red")
            logging.debug("rgb0 invalid")
            valid_rgb = False            
        
        if not (self.is_valid_rgb(self.rgb1.get())):
            logging.debug("rgb1 invalid")
            self.rgb1.configure(bg="red")
            valid_rgb = False
        
        if not (self.is_valid_rgb(self.rgb2.get())):
            logging.debug("rgb2 invalid")
            self.rgb2.configure(bg="red")
            valid_rgb = False
            
        self.display_msg(valid_topic,valid_rgb)
        
        return (valid_topic and valid_rgb)
    
    def luncher(self):
        """
        Parses the user input and lunch the Reddit Scraper
        
        """
        
        if(self.get_parameters()):
            
            rs = RedditScraper((self.rgb0.get(),self.rgb1.get(),self.rgb2.get()), self.topic.get(),self.LIMIT,self.SORT)
            
            #Reset matches in case is not the first execution
            PicturesElaborator.reset_matches()
            
            logging.info("Reddit Scraper started")
            results = rs.parse_posts(self.THRESHOLD, self.NUM_COLORS)
            
            results = results[:3]
            output ="Top images found: \n \n"  
           
            for result in results:
                output+=str(result[0]) + "\n"
                
            self.output.configure(text= output  )     
        
    def build_form(self):
        """
        Builds the form, to interact with the user
        """
        col = 0
        row = 0
        Label(self.window, text=" ").grid(column=col,row=row)
        col+=1
        Label(self.window, text="Subject", justify=LEFT, anchor="w").grid(sticky = W, column=col,row=row)
        col+=2
        Label(self.window, text="RGB", justify=LEFT, anchor="w").grid(sticky = W, column=col,row=row)
         
        row+=1
        col=0
        Label(self.window, text=" ").grid(column=col,row=row)
        col+=1
        self.topic = Entry(self.window,width=35)
        self.topic.grid(column=col, row=row)
        col+=1
        Label(self.window, text=" ").grid(column=col,row=row)
        col+=1
        self.rgb0 = Entry(self.window,width=5)
        self.rgb0.grid(column=col, row=row)
        col+=1
        self.rgb1 = Entry(self.window,width=5)
        self.rgb1.grid(column=col, row=row)
        col+=1
        self.rgb2 = Entry(self.window,width=5)
        self.rgb2.grid(column=col, row=row)
        col+=1
        Label(self.window, text=" ").grid(column=col,row=row)
        col+=1
        btn = Button(self.window, text="Search", command=self.luncher)
        btn.grid(column=col, row=row)
        
        row+=1
        col=1
        self.output = Label(self.window, justify=LEFT, anchor="w")
        self.output.grid(sticky = W, column=col, row=row)
