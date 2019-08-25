try:
    import urllib.request
except ImportError:
    import urllib
from io import BytesIO 
import requests 
import threading
import codecs
import os
import psutil
import jalali
import time
import sys,getopt
from findnumber import findnumber
import json as m_json
from datetime import date,timedelta
from PIL import Image
from PIL import ImageFilter
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def getdatafromsearchresult(search):
    global first_code_number
    global number_reader
    search_result_link=search.find_element_by_tag_name('a').get_attribute('href')
    print(search_result_link)
    search_res_code=search_result_link.split('=')
    if first_code_number==0 :
        first_code_number = search_res_code[1]
    else:
        if first_code_number==search_res_code[1]:
            return
    image_name=data_path+search_res_code[1]+'.jpg'
    result_datafile=data_path+'res_'+search_res_code[1]+'.txt'
    if os.path.isfile(result_datafile):
        print(result_datafile)
        return
    driver = webdriver.Firefox(options=options)
    driver.get(search_result_link)
    imglinks=driver.find_elements_by_id('imgCaptcha')
                
    for img_link in imglinks:
        imglink=img_link.get_attribute('src')
                
    image=Image.open(BytesIO(requests.get(imglink).content))
    img=image.convert('L',dither=Image.NONE)
    img=img.filter(ImageFilter.GaussianBlur())
    img=img.filter(ImageFilter.SHARPEN)
    if image_view:
        img.show()
    image.close()
    ###################################
    input_code=''
    if mthreading :
        lock = threading.Lock()
        lock.acquire()
        try:
            input_code=number_reader.get_numberstr_from_image(img)
        finally:
            lock.release()
    else:
        input_code=number_reader.get_numberstr_from_image(img)
    print(input_code)
    ###################################
    img.close()
                
    input_box = driver.find_element_by_id('txtCaptcha')
    input_box.send_keys(input_code)
                
    submit_btn=driver.find_element_by_class_name('btnSearch')
    submit_btn.click()
                
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
    if image_view:
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()
    driver.close()

def main(argv):
    mthreading=False
    image_view=False
    mwalk_days=0
    opts=[]
    try:
        opts,args = getopt.getopt(argv,"hstd:",["showimage","threading","daysago",])
    except getopt.GetoptError as err:
        print ('Error in argument',str(err))
    for opt,arg in opts:
        if opt=='-h':
            print('getdatafromsite.py --showimage --threading --daysago=n')
            print('parameters are disabled by default ')
            sys.exit()
        elif opt=='--showimage':
            image_view=True;
        elif opt=='--threading':
            mthreading=True;
        elif opt=='--daysago':
            mwalk_days=arg
    return image_view,mthreading,mwalk_days
        

if __name__ == "__main__":
    while True:
        try:
            data_path='data/';
            walk_days=0;
            max_walk_days=3*365;
            options = Options()
            options.add_argument('--headless')
            global number_reader
            global first_code_number
            global image_view,mthreading
            image_view=False;
            mthreading=False;
            #print(sys.argv)
            image_view , mthreading , walk_days = main(sys.argv[1:])
            drivermain = webdriver.Firefox(options=options)
            drivermain.get('http://www.rrk.ir/News/NewsList.aspx')
            number_reader=findnumber();
            first_code_number=0
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
                    page_no=1
            
                    while True:
                        search_results1=drivermain.find_elements_by_class_name('ShowNBut')
                        #print(search_results1)
                        if len(search_results1)==0:
                            break
                        th = None
                        for search in search_results1:
                            if mthreading :
                                th=threading.Thread(target=getdatafromsearchresult,args=(search,),name='th_search')
                                th.start()
                            else:
                                getdatafromsearchresult(search)
                        if mthreading:
                            th.join()
                        btn_next = drivermain.find_element_by_id('cphMain_rptPagingRec_btnNextPage')
                        btn_next.click()
                        page_no +=1
                        if  page_no > 10 :
                            break;
                        else:
                            print('click Next Page %d'%( page_no))
            
                except Exception as e:
                    print("Except:")
                    print(u'->'.join(str(v) for v in e).encode('utf-8'))
                    drivermain.close()
                    drivermain = webdriver.Firefox(options=options)
                    drivermain.get('http://www.rrk.ir/News/NewsList.aspx')        
            
                walk_days+=1;
                first_code_number=0
                drivermain.close()
                drivermain = webdriver.Firefox(options=options)
                drivermain.get('http://www.rrk.ir/News/NewsList.aspx')
            
            drivermain.close()
        except Exception as e:
            print(str(e))
            pass

