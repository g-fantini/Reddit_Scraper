'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''
import unittest
from PicturesElaborator import PicturesElaborator 
from pathlib import Path

class Test(unittest.TestCase):

    TEST_IMGS = ["https://i.redd.it/7n04w5kdb8r01.jpg","https://i.redd.it/7htaa692gys11.jpg","https://i.redd.it/5ppvzui1pd351.jpg"]
    
    TEST_COLORS = {
    'GREEN': [0, 128, 0],
    'BLUE': [0, 0, 128],
    'YELLOW': [255, 255, 0],
    'RED': [255, 0, 0],
    'BLACK': [0, 0, 0]
    }  

    def test_reset_matches(self):
        PicturesElaborator().add_match((self.TEST_IMGS[0],4533))
        PicturesElaborator().reset_matches()
        self.assertEqual(PicturesElaborator().get_images_counter(), 0)
                          
    def test_add_match(self):
        PicturesElaborator().add_match((self.TEST_IMGS[0],4533))
        PicturesElaborator().add_match((self.TEST_IMGS[1],33))
        PicturesElaborator().add_match((self.TEST_IMGS[2],9933))
        self.assertTrue(PicturesElaborator().get_sorted_matches(),[('https://i.redd.it/7htaa692gys11.jpg', 33), ('https://i.redd.it/7n04w5kdb8r01.jpg', 4533), ('https://i.redd.it/5ppvzui1pd351.jpg', 9933)])
        self.assertEqual(PicturesElaborator().get_images_counter(), 3 )
           
    def test_get_img_path(self):
        self.assertEqual(PicturesElaborator().get_img_path(self.TEST_IMGS[0]), "tmp/7n04w5kdb8r01.jpg" ) 
        self.assertEqual(PicturesElaborator().get_img_path(self.TEST_IMGS[1]), "tmp/7htaa692gys11.jpg" )    
        
    def test_save_image(self):
        PicturesElaborator().save_image(self.TEST_IMGS[0])
        self.assertTrue(Path(PicturesElaborator().get_img_path(self.TEST_IMGS[0])).is_file())
        
        PicturesElaborator().save_image(self.TEST_IMGS[1])
        self.assertTrue(Path(PicturesElaborator().get_img_path(self.TEST_IMGS[1])).is_file())
        
        PicturesElaborator().empty_directory()
       
    def test_remove_image(self):
        PicturesElaborator().save_image(self.TEST_IMGS[0])
        PicturesElaborator().remove_image(PicturesElaborator().get_img_path(self.TEST_IMGS[0]))
        self.assertFalse(Path(PicturesElaborator().get_img_path(self.TEST_IMGS[0])).is_file())
    
    def test_RGB2HEX(self):
        self.assertEqual(PicturesElaborator().RGB2HEX(self.TEST_COLORS["RED"]), "#ff0000" ) 
        self.assertEqual(PicturesElaborator().RGB2HEX(self.TEST_COLORS["GREEN"]), "#008000" )
        
    def test_match_image_by_color(self):
        image1 = PicturesElaborator.open_img(self.TEST_IMGS[0])
        self.assertFalse(PicturesElaborator().match_image_by_color(image1, self.TEST_COLORS["GREEN"]))
        self.assertFalse(PicturesElaborator().match_image_by_color(image1, self.TEST_COLORS["RED"]))
        self.assertFalse(PicturesElaborator().match_image_by_color(image1, self.TEST_COLORS["BLUE"],70,7))
        
        image2 = PicturesElaborator.open_img(self.TEST_IMGS[1])
        self.assertFalse(PicturesElaborator().match_image_by_color(image2, self.TEST_COLORS["RED"]))
        self.assertTrue(PicturesElaborator().match_image_by_color(image2, self.TEST_COLORS["RED"],90,7))
        self.assertTrue(PicturesElaborator().match_image_by_color(image2, self.TEST_COLORS["BLUE"]))
        
        image3 = PicturesElaborator.open_img(self.TEST_IMGS[2])
        self.assertTrue(PicturesElaborator().match_image_by_color(image3, self.TEST_COLORS["RED"]))
        self.assertFalse(PicturesElaborator().match_image_by_color(image3, self.TEST_COLORS["BLUE"]))
    
    if __name__ == "__main__":
        unittest.main()