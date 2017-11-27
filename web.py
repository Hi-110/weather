#-*- coding: utf-8 -*-
import urllib
import re
import urllib2
import time
import os
import imageResize
from PIL import Image,ImageDraw,ImageFont
import json
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getHtml(url):
    req=urllib2.Request(url)
    page = urllib2.urlopen(req)
    html = page.read()
    html = html.decode('utf-8')
    #print(html)
    return html

def wenzi(im,state):

    font = ImageFont.truetype('msyh.ttc', 30)
    draw = ImageDraw.Draw(im)
    day = time.strftime(u"%Y年%m月%d日", time.localtime(time.time()))

    ########配文字################

    text = u'南山站天气' + day + u'\n凌晨 ' + state[0] + u'\n当前 ' + state[1]+ u'\n当天 ' + state[2]+ u'\n次日 ' + state[3]
    # text = u'你好\n你好'
    print(text)
    draw.text((20, 20), text, font=font, fill='#000000')
    text1 = u'凌晨云量'
    draw.text((20,220), text1, font=font, fill='#000000')
    text2 = u'当前云量'
    draw.text((20, 820), text2, font=font, fill='#000000')
    text3 = u'晴天钟预报'
    draw.text((20, 1420), text3, font=font, fill='#000000')
    text4 = u'天气预报'
    draw.text((20, 1820), text4, font=font, fill='#000000')

    return  im

def Yuntu(arr):
    global dayNow
    global state
    toImage = Image.new('RGBA', (900, 2200))
    for i in range(4):
        fromImge = Image.open(arr[i])
        loc = (50,(i * 600+270))
        if i==3:
            loc = (50,1870)
        print(loc)
        toImage.paste(fromImge, loc)

    toImage=wenzi(toImage,state)

    toImage.save("./"+dayNow+'/weatheReport.png')

def mkdir(path):
    # 引入模块
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print("创建文件夹"+path)


def download(_url, name):  # 下载函数
    if (_url == None):  # 地址若为None则跳过
        pass
    req=urllib2.Request(_url)
    result = urllib2.urlopen(req)  # 打开链接
    # print result.getcode()
    if (result.getcode() != 200):  # 如果链接不正常，则跳过这个链接
        pass
    else:
        data = result.read()  # 否则开始下载到本地
        with open(name, "wb") as code:
            code.write(data)
            code.close()


def GetNowTime():
    d=time.strftime("%Y_%m_%d",time.localtime(time.time()))
    t= time.strftime("%H_%M_%S",time.localtime(time.time()))
    return d,t

def find_midnightUrl(imglist):
    midnightUrl=''
    for i in imglist:
        if (midnightUrl=='')and(i[0].find('/00_0') != -1):
            midnightUrl =i[0]
    return midnightUrl

def get_all_and_get_midnightUrl(imglist):
    print(imglist)
    midnight = 0
    for n in range (len(imglist)):
        time = re.findall(r"\d\d_\d\d_\d\d", imglist[n][0])
        day = re.findall(r"\d\d\d\d/\d\d/\d\d", imglist[n][0])
        day[0]=day[0].replace("/","_")
        mkdir(day[0])

        if (midnight==0) and (time[0][:5]=='00_0'):
            midnight=n
            print('yuntu1 is :',time[0])

        download(imglist[n][0],"./"+day[0]+"/"+time[0]+".jpg")
        print(time[0])
    midnightUrl = imglist[midnight][0]
    return midnightUrl


def getImg(html):
    midnight=0
    d, t = GetNowTime()
    mkdir(d)
    ########晴天钟图################
    weather_clock_url = "http://202.127.24.18/v4/bin/astro.php?lon=87.177&lat=43.475&lang=zh-CN&ac=2000&unit=metric&tzshift=0"
    weather_clock="./" + str(d)+"/"+str(t) + "_weather_clock.jpg"
    download(weather_clock_url, weather_clock)

    ########天气预报图################
    weather_forecast_url = "http://202.127.24.18/v4/bin/civillight.php?lon=87.177&lat=43.475&lang=zh-CN&ac=2000&unit=metric&output=internal&tzshift=0"
    weather_forecast="./" + str(d) + "/" + str(t) + "_weather_ forecast.jpg"
    download(weather_forecast_url, weather_forecast)
    imgID = 'Image_asc'
    pattern = "\d\d\d\d/\d\d/\d\d \d:\d\d:\d\d"
    imglist = re.findall(pattern, html)
    imgurl='http://119.78.162.41:81/asc_main.aspx'
    imgMorning='%s_%s_%s.jpg'%(imglist[0][-7:-6],imglist[0][-5:-3],imglist[0][-2:])
    savePath1='%s\\%s'%(d,imgMorning)
    print 'image morning: %s'%savePath1
    midnightHour=1
    nowHour=int(imglist[0][-7])
    if nowHour<midnightHour :
        print 'Please run this program at time later than %s hour '%midnightHour
        return 0
    for i in range(len(imglist)):
        if imglist[i][-10:-8]==d[-2:]:
            if int(imglist[i][-7:-6])==midnightHour and int(imglist[i][-5:-3])<10:
                imgMidnight= '%s_%s_%s.jpg' % (imglist[i][-7:-6], imglist[i][-5:-3], imglist[i][-2:])
                savePath2 = '%s\\%s' % (d, imgMidnight)
                print 'image midnight: %s' % savePath2
                webscreen(imgurl, imgID, savePath1, savePath2)
                break

    ########打开这个会把全部全天相机图下载，返回值可以忽略################
    #midnightUrl=get_all_and_get_midnightUrl(imglist)

    # midnightUrl = find_midnightUrl(imglist)
    # print(midnightUrl)
    #
    # nowUrl = imglist[0][0]
    # urls=[midnightUrl,nowUrl,weather_clock_url,weather_forecast_url]
    urls = [ weather_clock_url, weather_forecast_url]

    weatherReport(savePath1,savePath2,urls)
    print savePath1,savePath2,urls

def weatherReport(imgMorn,imgMid,urls):
    global state
    arr=[]
    imgMorning=imageResize.Graphics(imgMorn[:-4])
    imgMorning.fixed_size(768, 512)
    imgMidnight=imageResize.Graphics(imgMid[:-4])
    imgMidnight.fixed_size(768, 512)
    arr.append(imgMid[:-4] + '_1.jpg')
    arr.append(imgMorn[:-4]+'_1.jpg')
    for i in range(len(urls)):
        download(urls[i], "./"+dayNow+'/'+str(i)+".jpg")
        a=imageResize.Graphics("./"+dayNow+'/'+str(i))
        if i==0:
            a.fixed_size(768, 312)
        if i==1:
            # a.fixed_size(768, 1200)
            a.fixed_size(768, 184)
        arr.append("./"+dayNow+'/'+str(i)+'_1.jpg')
        #arr=
    Yuntu(arr)

def get_state(version=1):
    global state

    ########晴天钟json数据################
    ApiUrl = "http://202.127.24.18/v4/bin/astro.php?lon=87.177&lat=43.475&ac=0&lang=en&unit=metric&output=json&tzshift=0"

    html = urllib.urlopen(ApiUrl)
    data = html.read().decode("utf-8")
    ss = json.loads(data)
    print (ss)
    data = ss['dataseries']
    print (data)

    # cloudcover=[0 for x in range(len(data))]
    cloudcover = {}
    cloudcover_state = [0,0,0,0]

    for i in data:
        cloudcover[i['timepoint']] = i['cloudcover']
    print (cloudcover)

    ########早上运行################
    if version == 1:
        cloudcover_morning = (cloudcover[6] + cloudcover[9]) / 2
        cloudcover_today = (cloudcover[21] + cloudcover[24]) / 2
        cloudcover_tomorrow = (cloudcover[45] + cloudcover[48]) / 2
        cloudcover_state = [0, cloudcover_morning, cloudcover_today, cloudcover_tomorrow]
        for i in range(3):
            if cloudcover_state[i + 1] > 0:
                state[i + 1] = u"优"
            if cloudcover_state[i + 1] > 5:
                state[i + 1] = u"良"
            if cloudcover_state[i + 1] > 7:
                state[i + 1] = u"差"

    ########前一天晚上运行，得到凌晨状况，默认优################
    if version == 2:
        cloudcover_yesterday = (cloudcover[27] + cloudcover[30]) / 2
        if cloudcover_state[0] > 0:
            state[0] = u"优"
        if cloudcover_state[0] > 4:
            state[0] = u"良"
        if cloudcover_state[0] > 7:
            state[0] = u"差"
        pass
    print (state)

def webscreen(url,eleID,savepath1,savepath2):
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(3000)
    driver.set_window_size(1280,800)
    driver.get(url)
    imgelement1 = driver.find_element_by_id(eleID)
    location = imgelement1.location
    size = imgelement1.size
    driver.save_screenshot(savepath1)
    im1 = Image.open(savepath1)
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = location['y'] + size['height']
    im1 = im1.crop((left, top, right, bottom))
    im1.save(savepath1)
    all_options = driver.find_elements_by_tag_name("option")
    for option in all_options:
        value=option.get_attribute("value")
        valueTime = '%s_%s_%s' % (value[-7:-6], value[-5:-3], value[-2:])
        if valueTime==savepath2[-11:-4]:
            print("Value is: %s" % valueTime)
            option.click()
            time.sleep(60)
            imgelement2 = driver.find_element_by_id(eleID)
            location = imgelement2.location
            size = imgelement2.size
            driver.save_screenshot(savepath2)
            im2 = Image.open(savepath2)
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = location['y'] + size['height']
            im2 = im2.crop((left, top, right, bottom))
            print size,left,top,right,bottom
            im2.save(savepath2)
            break
        else:
            continue
    return im1,im2

if __name__ == '__main__' :

    global state
    global dayNow
    dayNow = time.strftime(u"%Y_%m_%d", time.localtime(time.time()))
    state = [u'优', u'优', u'优', u'优']
    get_state()

    ########天文台全天相机################
    html = getHtml("http://119.78.162.41:81/asc_main.aspx")
    # html = getHtml("http://119.78.162.41:81")
    getImg(html)






