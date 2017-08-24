#coding:utf-8

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC

from bs4 import BeautifulSoup
import json
import os
import time
import datetime

# 폴더 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


##json file load
# teacher
with open('teacher.json') as json_data:
	jsonTeacherList = json.load(json_data)["teacherList"]

# id, pw
with open('account.json') as json_data:
	jsonAccount = json.load(json_data)["account"]


# web driver
driver = webdriver.PhantomJS('/lib/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#driver = webdriver.Chrome('/Users/ohjonghyuk/Documents/programs/chromedriver_mac64/chromedriver')
driver.implicitly_wait(3)

## urls
signInUrl = "https://engoo.co.kr/members/sign_in"
favoriteUrl = "https://engoo.co.kr/teachers/favorite"

# making targetTeacherUrl List
targetTeacherUrlList = []
for jsonTeacherNum in jsonTeacherList:
	targetTeacherUrlList.append("https://engoo.co.kr/teachers/" + jsonTeacherNum)

#targetTeacherUrlList = [
#"https://engoo.co.kr/teachers/16130",
#"https://engoo.co.kr/teachers/17968"
#]

## date
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)
strToday = today.strftime('%Y-%m-%d')
strTomorrow = tomorrow.strftime('%Y-%m-%d')

# target time tag id
if jsonAccount["day"]=="today":
	targetTimeId = "dt_" + strToday + jsonAccount["time"]
else :
	targetTimeId = "dt_" + strTomorrow + jsonAccount["time"]

print(targetTimeId);

## login start
driver.get(signInUrl)

html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
facebookLogin = driver.find_element_by_class_name('facebook-link-me')
# print(facebookLogin)


if jsonAccount["isFacebook"]:
	# facebook login btn click
	facebookLogin.click()
	# Login
	driver.find_element_by_id('email').send_keys(jsonAccount["id"])
	driver.find_element_by_id('pass').send_keys(jsonAccount["pw"])
	driver.find_element_by_id('loginbutton').click()
else :
	# engoo login
	driver.find_element_by_id('member_email').send_keys(jsonAccount["id"])
	driver.find_element_by_id('member_password').send_keys(jsonAccount["pw"])
	driver.find_elements_by_xpath('//button[@class="btn btn-primary"]')[0].click()


# teacher list ########## 즐겨찾기에서 가져오는 부분은 나중에 다시 구현하자
#############################################

# favorite teacher
# driver.get(favoriteUrl)
# teacherList =  driver.find_elements_by_xpath('//a[@class="teacher-favorite-link"]')
#
# for idx in range(0, 1) :  #len(teacherList)
# 	teacherList[0].click()
#############################################

# target list loop
for targetTeacher in targetTeacherUrlList:
	driver.get(targetTeacher)
	targetElem = driver.find_elements_by_xpath("//li[contains(@id,'" + targetTimeId + "')]/a")
	if len(targetElem)>0 :
		targetElem[0].click()
		wait = ui.WebDriverWait(driver,10)
		#driver.execute_script("arguments[0].setAttribute('display','block')", driver.find_element_by_id('teacher_booked_modal'))
		wait.until( EC.element_to_be_clickable((By.ID, "engoo_materials")))
		engooBooks = driver.find_element_by_id('engoo_materials')
		labelList = driver.find_elements_by_xpath('//div[@class="modal-book-lesson-answer reserve_lesson_style"]/label')
		print(labelList)
		#labelList[3].click()
		#engooBooks.click()
		driver.execute_script("arguments[0].click()",labelList[3])
		#driver.execute_script("arguments[0].setAttribute('value','10')",engooBooks)
		#driver.execute_script("arguments[0].setAttribute('value','10')",driver.find_element_by_id('reserve_lesson_style'))
		el = driver.find_element_by_id('reserve_lesson_style')
		for option in el.find_elements_by_tag_name('option'):
		    if option.text == 'Daily News':
		        option.click() # select() in earlier versions of webdriver
		        break
		driver.find_element_by_id('reserve_id').click()
