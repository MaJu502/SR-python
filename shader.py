"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
import random
import glMatematica

def Shiba(**kwargs):
    color = (0,0,0)
    temp = random.randint(1,3)
    
    if temp == 1:
        #cafe claro
        color = (139/255,69/255,19/255)
    elif temp == 2:
        #cafe crema
        color = (245/255,222/255,179/255)
    elif temp == 3:
        #cafe obscuro
        color = (128/255,0,0)
        
    return color
