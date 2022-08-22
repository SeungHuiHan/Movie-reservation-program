#pip install selenium 설치
#python -m pip install bs4 설치
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time

theater='IMAX 용산아이파크몰' #영화관 선택 (IMAX 전용)
date=datetime.strptime("20220824", "%Y%m%d") #예매 희망 날짜, 단 현재부터 2주 이내
title='놉'#영화 제목
people=2 #일반 예매 인원(청소년,경로,우대 안됨) 최대 8명까지
#자기 chrome에 맞는 버전을https://chromedriver.chromium.org/downloads에서 설치
#압축을 풀고 파일 경로 설정
browser = webdriver.Chrome("C:\chromedriver.exe") #chromedriver가 있는 파일 경로 입력
browser.get('https://www.cgv.co.kr/')
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="cgvwrap"]/div[2]/div[1]/div/ul/li[1]/a').click()

browser.implicitly_wait(2)
browser.find_element_by_name('txtUserId').send_keys('*******') #아이디 입력
browser.find_element_by_name('txtPassword').send_keys('******') #비밀번호 입력
browser.find_element_by_xpath('//*[@id="submit"]/span').click() #로그인

browser.implicitly_wait(2)
#비밀번호 변경하라고 뜬다면 if browser.find_element_by_class_name('sect-passwardchange'):
if browser.find_element_by_xpath('//*[@id="contents"]/div/div'):
    print('비밀번호 변경하는 창 나옴')
    browser.find_element_by_xpath('//*[@id="ctl00_PlaceHolderContent_btn_pw_chag_later"]').click()
else:
    print("비밀번호 변경하라는 창 안나옴")

#홈화면에 특별관 배너가 바뀔때가 있으니 xpath 확인하기
some_tag_1 = browser.find_element_by_xpath('//*[@id="btn_allView_Special"]') #스크롤 내리기
action = ActionChains(browser)
action.move_to_element(some_tag_1).perform()
browser.implicitly_wait(2)

browser.find_element_by_xpath('//*[@id="btn_allView_Special"]').click()
browser.implicitly_wait(2)
browser.find_element_by_xpath('//*[@id="contaniner"]/article[2]/div/ul/li[1]/a/div').click()


some_tag_1 = browser.find_element_by_xpath('//*[@id="contaniner"]/article[3]/div/div/div[1]/div[2]/div') #스크롤 내리기
action = ActionChains(browser)
action.move_to_element(some_tag_1).perform()
browser.implicitly_wait(2)

browser.find_element_by_xpath('//*[@id="contaniner"]/article[2]/ul/li[2]/a').click()

some_tag_1 = browser.find_element_by_xpath('//*[@id="contaniner"]/div[2]/div/div[1]') #스크롤 내리기
action = ActionChains(browser)
action.move_to_element(some_tag_1).perform()
browser.implicitly_wait(2)

browser.find_element_by_link_text(theater).click()
browser.implicitly_wait(5)
iframe = browser.find_element_by_id("ifrm_movie_time_table") 
browser.switch_to.frame(iframe) 


some_tag_1 = browser.find_element_by_id('slider') #스크롤 내리기
action = ActionChains(browser)
action.move_to_element(some_tag_1).perform()
browser.implicitly_wait(2)

'''
browser.switch_to.default_content()

if browser.find_element_by_id("ad_float1"):
    iframe2 = browser.find_element_by_id("ad_float1") 
    browser.switch_to.frame(iframe2)
    if browser.find_element_by_class_name('btn_ad_close'):
        browser.find_element_by_class_name('btn_ad_close').send_keys(Keys.ENTER)
    browser.switch_to.default_content()
    browser.implicitly_wait(1)

iframe = browser.find_element_by_id("ifrm_movie_time_table") 
browser.switch_to.frame(iframe)
'''
soup=BeautifulSoup(browser.page_source)
now=datetime.now()
date_1=date.strftime("%d")

slider_1=soup.find(class_="item").text
if date_1 in slider_1:
    browser.find_element_by_partial_link_text(date_1).click()

else:
    browser.find_element_by_class_name('btn-next').click()
    browser.implicitly_wait(1)

try:
    browser.find_element_by_partial_link_text(date_1).click()
    browser.implicitly_wait(1)

except NoSuchElementException: #해당 날짜가 열리지 않았다면 브라우저 종료
    print("해당 날짜는 열리지 않았습니다.")
    browser.close()

soup=BeautifulSoup(browser.page_source)

browser.implicitly_wait(3)
while True:  
    title_one=soup.find(class_="sect-showtimes").text
    
    if title in title_one:
        break
    else:
        browser.find_element_by_partial_link_text(date_1).click()
        browser.implicitly_wait(1)

elemt_1=browser.find_element_by_class_name('sect-showtimes').find_element_by_tag_name('ul')
li_2=elemt_1.find_elements_by_class_name('col-times')

time.sleep(1)
for i in range(len(li_2)):
    if title in li_2[i].text:
        info_timetable=li_2[i].find_element_by_class_name('info-timetable').find_element_by_tag_name('ul')
        li=info_timetable.find_elements_by_tag_name('li')
        
        if len(li)<=2: #영화 시간 임의 선택할 수 없음(대략 오후3시~5시 사이 상영작)
            li[len(li)-1].click()
        elif len(li)<=4:
            li[len(li)-2].click()
        elif len(li)>=5:
            li[len(li)-3].click()
        break

time.sleep(5)
iframe1 = browser.find_element_by_id("ticket_iframe") 
browser.switch_to.frame(iframe1) 
browser.implicitly_wait(2)
browser.find_element_by_id('tnb_step_btn_right').click()
browser.implicitly_wait(3)

popup_check1=WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "닫기")))
popup_button1=browser.find_elements_by_link_text('닫기')[0]
popup_button1.click()
popup_check2=WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "닫기")))
popup_button2=browser.find_elements_by_link_text('닫기')[0]
popup_button2.click()


time.sleep(2)
browser.find_element_by_xpath('//*[@id="nop_group_adult"]/ul/li[{0}]'.format(people+1)).click()

seats_list=browser.find_elements_by_xpath('//*[@id="seats_list"]/div[1]/div')

if (len(seats_list)/2==0):
    seats_list_1=int(len(seats_list)/2)
else:
    seats_list_1=int((len(seats_list)/2)+1)

seats_list_2=browser.find_elements_by_xpath('//*[@id="seats_list"]/div[1]/div[{0}]/div/div/div'.format(seats_list_1))
if (len(seats_list_2)/2==0):
    seats_list_3=int(len(seats_list_2)/2)
else:
    seats_list_3=int((len(seats_list_2)/2)+1)
browser.implicitly_wait(2)

seats_list_4=browser.find_element_by_xpath('//*[@id="seats_list"]/div[1]/div[{0}]'.format(seats_list_1))
seats_list_4.find_element_by_link_text('{0}'.format(seats_list_3))
action = ActionChains(browser)
action.move_to_element(seats_list_4.find_element_by_link_text('{0}'.format(seats_list_3))).perform()

if people<=2:
    time.sleep(2)
elif people<=4:
    time.sleep(4)
else:
    time.sleep(5)

browser.find_element_by_id('tnb_step_btn_right').click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="discCoupon"]/div[1]').click()

coupon=browser.find_element_by_id('cgvCoupon').find_element_by_class_name('content')
coupon_list=coupon.find_elements_by_tag_name('li')

if coupon_list:
    for i in range(people):
        coupon_list[i].click()
        time.sleep(1)
        
        if (len(coupon_list)-(i+1))==0:
            break
try:
        WebDriverWait(browser,2).until(EC.alert_is_present())
        alert=browser.switch_to.alert

        alert.dismiss()
        alert.accept()       
except:
        "there is no alert"

browser.find_element_by_id('last_pay_radio3').click()
browser.find_element_by_id('payKakao_btn').click()
browser.implicitly_wait(1)
browser.find_element_by_id('tnb_step_btn_right').click()
time.sleep(2)

browser.find_element_by_id('agreementAll').click()
browser.find_element_by_id('resvConfirm').click()
browser.implicitly_wait(1)
browser.find_element_by_class_name('reservation').click()

while(True):
    pass

