'''
Created on 18 Jun 2020

@author: Gabriele
'''
import unittest
from UIForm import UIForm

class Test(unittest.TestCase):

    def test_is_valid_rgb(self):
        uif = UIForm()
       
        self.assertTrue(uif.is_valid_rgb("255"))
        self.assertTrue(uif.is_valid_rgb("200"))
        self.assertTrue(uif.is_valid_rgb("1"))
        self.assertFalse(uif.is_valid_rgb(""))
        self.assertFalse(uif.is_valid_rgb("256"))
        self.assertFalse(uif.is_valid_rgb("-10"))


if __name__ == "__main__":
    unittest.main()