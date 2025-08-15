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


def identify_inactive_keys(token, productId, days_after_expiry=0, block=False, search_query = "True"):
    
    token = token
    product_id=productId
    
    all_keys = []
    
    time_window = datetime.timedelta(days=int(days_after_expiry))   # 30 days, etc.
    cutoff = datetime.datetime.now() - time_window
    
    filtered_keys = []
    
    not_processed_keys = []
    
    iteration = 1
    while True:
        temp = Product.get_keys(token=token, product_id=product_id, page=iteration, search_query=search_query )[0]
        print("Processed page {0}".format(str(iteration)))
        if len(temp) > 0:
            all_keys.extend(temp)
            iteration+=1
        else:
            break
        
    for key in all_keys:

        if datetime.datetime.fromisoformat(key["expires"]) < cutoff:
            filtered_keys.append(key["key"])
            print("Detected key {0}".format(key["key"]))
        else:
            not_processed_keys.append(key["key"])
            continue

            
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

    parser = argparse.ArgumentParser(description='This script will help you to identify which licenses have expired and, if desired, block them.' \
    ' If needed, you can choose to filter licenses that have been expired for more than a certain number of days.')
    
    parser.add_argument('-t', '--token', help="The access token with GetKeys and BlockKey permissions.", required=True)
    parser.add_argument('-p','--product', help="The ProductId  of the product", required=True)
    parser.add_argument('-b','--block', help="If set to true, all inactive keys will be blocked.",action="store_true")
    parser.add_argument("-w", '--window', help="How many days should have pasted after the expiry date to mark it as inactive and eventually block it. Default 0 days.", default=0)
    parser.add_argument("-s", '--search', help="An optional query you can attach to filter the licenses.", default="Block=False")

    
    args = parser.parse_args()
    
    print(identify_inactive_keys(args.token, args.product,args.window, args.block, args.search))