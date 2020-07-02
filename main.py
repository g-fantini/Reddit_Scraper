'''
Created on 17 Jun 2020

@author: Gabriele Fantini
'''

from UIForm import UIForm 

if __name__ == '__main__':
    form = UIForm()
    
    #Define form
    form.build_form()
    #Lunch application
    form.window.mainloop()
