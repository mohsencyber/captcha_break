import urllib.request
import codecs
import os
import jalali
import time
import findnumber
import json as m_json
from datetime import date,timedelta
from PIL import Image
from PIL import ImageFilter
from selenium import webdriver
#rom HTMLParser import HTMLParser
from selenium.webdriver.firefox.options import Options

data_path='data/';
options = Options()
options.add_argument('--headless')

#req = urllib.urlopen('http://www.rrk.ir/News/ShowNews.aspx?Code=14744520')

#class MyHtmlParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        print "img is : ", tag
#    
#    def handle_endtag(self, tag):
#        print "end : ", tag 
#
#    def handle_data(self, data):
#        print "data : " , data

today=date.today()-timedelta(days=0)
today_shamsi=jalali.Gregorian(today).persian_string("{}/{}/{}")
print(today_shamsi)
drivermain = webdriver.Firefox(options=options)
drivermain.get('http://www.rrk.ir/News/NewsList.aspx')

#alert=drivermain.switch_to.alert
#alert.accept()
#time.sleep(5)
#NewsDate_input=drivermain.find_element_by_id('cphMain_dteFromNewspaperDate_dteFromNewspaperDate_txtDate')
#NewsDate_input.send_keys(today_shamsi)
btn_search = drivermain.find_element_by_id('cphMain_btnSearch')
btn_search.click()
time.sleep(5)
image_name=''
print ('***search result loaded***')
#print (btn_search) 
while True:
    #alert=drivermain.switch_to.alert
    #alert.accept()
    search_results1=drivermain.find_elements_by_class_name('ShowNBut')
    #print(search_results1)
    if len(search_results1)==0:
        break
    for search in search_results1:
        search_result_link=search.find_element_by_tag_name('a').get_attribute('href')
        print(search_result_link)
        search_res_code=search_result_link.split('=')
        image_name=data_path+search_res_code[1]+'.jpg'
        if os.path.isfile(image_name):
            print(image_name)
            continue
        #print search_res_code[1]
        driver = webdriver.Firefox(options=options)
        driver.get(search_result_link)
        imglinks=driver.find_elements_by_id('imgCaptcha')
        
        for img_link in imglinks:
            imglink=img_link.get_attribute('src')

        urllib.request.urlretrieve(imglink,image_name)
        
        image=Image.open(image_name)
        #img=image.filter(ImageFilter.BLUR)
        img=image.convert('L',dither=Image.NONE)
        #img=img.filter(ImageFilter.GaussianBlur())
        #img=img.filter(ImageFilter.BLUR)
        img=img.filter(ImageFilter.SHARPEN)
        #img=img.filter(ImageFilter.SMOOTH_MORE)
        img.show()
        image.close()
        img.save(image_name)
        ###################################
        numberlist=findnumber.findnumber(img).get_number_image_list()
        print(type(numberlist))
        for numberimg in numberlist:
            numberimg.show()
            break;
        ###################################
        img.close()
        input_code=input('Enter numbercode :')
        
        input_box = driver.find_element_by_id('txtCaptcha')
        input_box.send_keys(input_code)
        
        submit_btn=driver.find_element_by_class_name('btnSearch')
        submit_btn.click()
        
        #detail_rcv=driver.find_element_by_class_name('Padder2')
        detail_rcv=driver.find_element_by_id('cphMain_pnlNewsInfo')
        strlink=detail_rcv.text
        save_output = codecs.open(data_path+'res_'+search_res_code[1]+'.txt','w','utf-8')
        save_output.write(strlink)
        save_output.close()

        # print search.text
        # print '-----------'
        driver.close()
    #if os.path.isfile(image_name):
    #    print(image_name)
    #    break
    btn_next = drivermain.find_element_by_id('cphMain_rptPagingRec_btnNextPage')
    btn_next.click()


drivermain.close()

