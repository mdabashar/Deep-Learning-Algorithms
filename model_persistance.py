# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 21:54:15 2020

@author: Dr Md Abul Bashar at QUT
"""

import pickle
import numpy as np
from keras.models import model_from_json

class ModelPersistance:
    def __init__(self, store_path=''):
        self.STORE_PATH = store_path
        print('ModelPersistance Object Created')
    
    '''
    Storing a trained model includes the following four steps
    1. store tokenizer
    2. store model architecture
    3. store model weights
    4. store maxlen (of the docs or sentences or tweets)
    '''
    def store_model(self, tokenizer, model, max_len):
        # 1. Store Tokenizer
        with open(self.STORE_PATH+'tokenizer.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('Saved tokenizer to disk')
            
        # 2. Store Model Architecture
        # serialize model architecture to JSON
        model_json = model.to_json()
        with open(self.STORE_PATH+"model.json", "w") as json_file:
            json_file.write(model_json)
            print('Saved model architecture to disk')
            
        # 3. Store Model Weights
        # serialize weights to HDF5
        model.save_weights(self.STORE_PATH+"model.h5")
        print("Saved model to disk")
        
        # 4. Store maxlen
        np.save(self.STORE_PATH+'maxlen', max_len)
        
        
    '''
    Loading a stored model includes the following four steps.
    1. Load Tokenizer
    2. Load Model Architecture
    3. Load Model Weights
    4. Load maxlen
    '''
    def restore_model(self):
        # 1. Loading Tokenizer
        tokenizer = None
        with open(self.STORE_PATH+'tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
            print('Loaded tokenizer from disk')
            
        # 2. Load Model Architecture
        # load json and create model
        json_file = open(self.STORE_PATH+'model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        print('Loaded architecture from disk')
        
        # 3. Load Weights
        # load weights into new model
        model.load_weights(self.STORE_PATH+"model.h5")
        print("Loaded model from disk")
        
        # 4. Load maxlen
        max_len = np.load(self.STORE_PATH+'maxlen.npy')
        print("Loaded max_len from disk")
            
        return tokenizer, model, max_len
    
def main():
    mp = ModelPersistance()
    
if __name__=='__main__':
    main()