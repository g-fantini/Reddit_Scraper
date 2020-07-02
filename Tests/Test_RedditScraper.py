'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''
import unittest
from RedditScraper import RedditScraper 

class Test(unittest.TestCase):

    def test_set_reddit_url(self):
        rs = RedditScraper()
        rs.set_reddit_url("beta","100","top")
        self.assertEqual(rs.get_reddit_url(),"https://www.reddit.com/search.json?q=title:beta&is_sort:true&limit=100&sort=top" )

    def test_is_image(self):
        rs = RedditScraper()
        self.assertTrue(rs.is_image("https://i.redd.it/7n04w5kdb8r01.jpg") )
        self.assertFalse(rs.is_image("https://i.redd.it/7n04w5kdb8r01.html4") )
        
if __name__ == "__main__":
    unittest.main()