try:
    import urllib.request
except ImportError:
    import urllib
from io import BytesIO 
import requests 
import codecs
import os
import psutil
import jalali
import time
from findnumber import findnumber
import json as m_json
from datetime import date,timedelta
from PIL import Image
from PIL import ImageFilter
from selenium import webdriver
#rom HTMLParser import HTMLParser
from selenium.webdriver.firefox.options import Options

data_path='data/';
walk_days=0;
max_walk_days=365;
options = Options()
options.add_argument('--headless')


drivermain = webdriver.Firefox(options=options)
drivermain.get('http://www.rrk.ir/News/NewsList.aspx')
number_reader=findnumber();
while (walk_days<max_walk_days):
    today=date.today()-timedelta(days=walk_days)
    today_shamsi=jalali.Gregorian(today).persian_string("{}{:02d}{:02d}")
    print(today_shamsi)
    
    #alert=drivermain.switch_to.alert
    #alert.accept()
    #time.sleep(5)
    
    NewsDate_input=drivermain.find_element_by_id('cphMain_dteFromNewspaperDate_dteFromNewspaperDate_txtDate')
    NewsDate_input.send_keys(today_shamsi)
    #time.sleep(5)
    try:
        btn_search = drivermain.find_element_by_id('cphMain_btnSearch')
        btn_search.click()
        #time.sleep(1)
        image_name=''
        #alert=drivermain.switch_to.alert
        #alert.accept()
        print ('***search result loaded***')
    
        while True:
            search_results1=drivermain.find_elements_by_class_name('ShowNBut')
            #print(search_results1)
            if len(search_results1)==0:
                break
            for search in search_results1:
                search_result_link=search.find_element_by_tag_name('a').get_attribute('href')
                print(search_result_link)
                search_res_code=search_result_link.split('=')
                image_name=data_path+search_res_code[1]+'.jpg'
                result_datafile=data_path+'res_'+search_res_code[1]+'.txt'
                if os.path.isfile(result_datafile):
                    print(result_datafile)
                    continue
                #print search_res_code[1]
                driver = webdriver.Firefox(options=options)
                driver.get(search_result_link)
                imglinks=driver.find_elements_by_id('imgCaptcha')
                
                for img_link in imglinks:
                    imglink=img_link.get_attribute('src')
        
                #try:
                #    urllib.request.urlretrieve(imglink,'image_name.jpg')
                #except Exception:
                #    urllib.urlretrieve(imglink,'image_name.jpg')
                #
                #image=Image.open('image_name.jpg')
                
                image=Image.open(BytesIO(requests.get(imglink).content))
                #image=Image.open(urllib2.urlopen(imglink))
                #img=image.filter(ImageFilter.BLUR)
                img=image.convert('L',dither=Image.NONE)
                img=img.filter(ImageFilter.GaussianBlur())
                #img=img.filter(ImageFilter.BLUR)
                img=img.filter(ImageFilter.SHARPEN)
                #img=img.filter(ImageFilter.SMOOTH_MORE)
                img.show()
                image.close()
                #img.save(image_name)
                ###################################
                input_code=number_reader.get_numberstr_from_image(img)
                print(input_code)
                ###################################
                img.close()
                #input_code=input('Enter numbercode :')
                
                input_box = driver.find_element_by_id('txtCaptcha')
                input_box.send_keys(input_code)
                
                submit_btn=driver.find_element_by_class_name('btnSearch')
                submit_btn.click()
                
                #detail_rcv=driver.find_element_by_class_name('Padder2')
                try:
                    detail_rcv=driver.find_element_by_id('cphMain_pnlNewsInfo')
                    strlink=detail_rcv.text
                    save_output = codecs.open(result_datafile,'w','utf-8')
                    save_output.write(strlink)
                    save_output.close()
                except Exception as e:
                    print('Exceptions....: %s'% e)
                # print search.text
                # print '-----------'
                for proc in psutil.process_iter():
                    if proc.name() == "display":
                        proc.kill()
                driver.close()
            btn_next = drivermain.find_element_by_id('cphMain_rptPagingRec_btnNextPage')
            btn_next.click()
    except Exception as e:
        print("Except:")
        print(u'->'.join(e).encode('utf-8'))
        drivermain = webdriver.Firefox(options=options)
        drivermain.get('http://www.rrk.ir/News/NewsList.aspx')        

    walk_days+=1;
drivermain.close()

