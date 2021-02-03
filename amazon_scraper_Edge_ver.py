# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:53:00 2020

@author: winwo
"""

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# two things need to be specify, search term and product ID

##########################################################################################

'''scraping function'''

def extract_record(item):
    
    '''reviewer name'''

    reviewer_name=item.find('div','a-profile-content').text
    reviewer_name=reviewer_name.strip()
    
    '''review title'''
    
    review_title=item.find('a','review-title').text
    review_title=review_title.strip()
    
    '''text body'''
    
    text_body= item.find('div','a-row a-spacing-small review-data').text
    text_body=text_body.strip()
    
    '''star rating'''
    
    star_rating=item.find('span','a-icon-alt').text
    star_rating=star_rating.strip()
    
    '''time and place'''
    
    time_place=item.find('span','review-date').text
    time_place=time_place.strip()
    
    '''helpfulness'''
    # handling error from no helpfulness parameter
    
    try:
        helpfulness=item.find('span','a-size-base a-color-tertiary cr-vote-text').text
        helpfulness=helpfulness.strip()
    except AttributeError:
        helpfulness='0'
        
    result =(reviewer_name,review_title,text_body,star_rating,time_place,helpfulness)
    return result


####################################################################################

'''main function'''

def main(search_term,product_id):
    
    
    #variables
    page=1
    
    record_list=[]
    
    while True: 
        def get_url(search_term,product_id):
            """"generate url from search term and product ID, where search term is product's url"""
            searchterm=search_term
            productid=product_id
            template=f"https://www.amazon.com/{searchterm}/product-reviews/{productid}/ref=cm_cr_getr_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
            return template
        
        #open and soup html
        url=get_url(search_term,product_id)
        driver.get(url)
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        results=soup.find_all('div',{'data-hook' : 'review'})
        
        #scraping function
        
        item = results[0]
        
        for item in results:
            record=extract_record(item)
            if record:
                record_list.append(record)
        
        print(len(record_list))
        
        page=page+1
   
    driver.close()
    with open('AAA.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['reviewer_name','review_title','text_body','star_rating','time_place','helpfulness'])
        writer.writerows(record_list)

""" insert product name and ID here"""

main('HP-23-8-inch-Adjustment-Speakers-VH240a','B072M34RQC')

    
    
        



