# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 13:05:08 2023

@author: Cryptolens AB
"""

import datetime
import argparse
import time
from licensing.models import *
from licensing.methods import Key, Helpers, Message, Product, Customer, Data, AI


def identify_inactive_keys(token, productId, window=30, block=False):
    
    token = token
    product_id=productId
    
    all_keys = []
    
    time_window = 60*60*24*int(window) # 1 month back in time
    time_now = int(time.time())
    
    filtered_keys = []
    
    not_processed_keys = []
    
    iteration = 1
    while True:
        temp = Product.get_keys(token, product_id, iteration)[0]
        print("Processed page {0}".format(str(iteration)))
        if len(temp) > 0:
            all_keys.extend(temp)
            iteration+=1
        else:
            break
        
    for key in all_keys:
        
        req = []
        try:
            req = AI.get_web_api_log(token, product_id, key["key"], limit=1, order_by="Id descending")[0]
        except:
            not_processed_keys.append(key["key"])
            continue
        
        if len(req) > 0:
            req = req[0]

            if int(req["time"]) + time_window < time_now:
                filtered_keys.append(req["key"])
                print("Detected key {0}".format(req["key"]))
            else:
                print("Skipped key {0}".format(req["key"]))
        else:
            filtered_keys.append(key["key"])
            print("Detected key {0}".format(key["key"]))
            
    if block:
        
        for key in filtered_keys:
            try:
                res = Key.block_key(token, product_id, key)
                if res[0] ==True:
                    print("Key {0} was blocked successfully.".format(key))
                else:
                    print("Key {0} was not blocked.".format(key))
            except:
                print("Key {0} was not blocked.".format(key))
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script will help you to identify which keys are not active and, if desired, block them.')
    
    parser.add_argument('-t', '--token', help="The access token with GetWebAPILog, GetKeys and BlockKey permissions.", required=True)
    parser.add_argument('-p','--product', help="The ProductId  of the product", required=True)
    parser.add_argument('-b','--block', help="If set to true, all inactive keys will be blocked.",action="store_true")
    parser.add_argument("-w", '--window', help="How many days should the key have been inactive to mark it as inactive and eventually block it. Default 30 days.", default=30)
    
    args = parser.parse_args()
    
    print(identify_inactive_keys(args.token, args.product,args.window, args.block))