from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import streamlit as st

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome()
driver.maximize_window()
header = st.container()
cont_url = st.cotainer()
cont_prioerties = st.container

@st.experimental.memo()
def data_scrape():
  list = ['https://www.foody.vn/ho-chi-minh/food/quan-an','https://www.foody.vn/ho-chi-minh/food/sang-trong'
       ,'https://www.foody.vn/ho-chi-minh/food/buffet','https://www.foody.vn/ho-chi-minh/food/an-vat-via-he'
       ,'https://www.foody.vn/ho-chi-minh/food/an-chay','https://www.foody.vn/ho-chi-minh/food/cafe'
       ,'https://www.foody.vn/ho-chi-minh/food/bar-pub','https://www.foody.vn/ho-chi-minh/food/quan-nhau'
       ,'https://www.foody.vn/ho-chi-minh/food/tiem-banh']
  for h in range(2,2):
      driver.get(list[h])
      print(driver.title)
      store_name = []
      store_name_ = []
      store_add = []
      cmt = []
      time_cmt = []
      rating_very_good = []
      rating_good = []
      rating_avg = []
      rating_bad = []
      rating_very_bad = []
      factor_position = []
      factor_price = []
      factor_quality = []
      factor_service = []
      factor_space = []
      store = len(driver.find_elements(By.XPATH, "//span[@class = 'fa fa-comment']"))
      a = len(driver.find_elements(By.XPATH, "//span[@class = 'fa fa-comment']"))
      for x in range(0,a):
          a = len(driver.find_elements(By.XPATH, "//span[@class = 'fa fa-comment']"))
          print("Food_Store_Number",x)
          time.sleep(1)
          driver.find_elements(By.XPATH, "//span[@class = 'fa fa-comment']")[x].click()
          for i in range(1,50):
              try:
                  driver.find_elements(By.XPATH, "//a[@class = 'fd-btn-more']")[0].click()
              except:
                  length = driver.find_elements(By.XPATH, "//div[@class = 'review-des fd-clearbox ng-scope']")
          print("How many comment",len(length))
          store_name.append(driver.find_elements(By.XPATH, "//div[@class = 'fldr-res-title ng-binding']")[1].text)
          store_add.append(driver.find_elements(By.XPATH, "//div[@class = 'fldr-res-address ng-binding']")[1].text)
          rating_very_good.append(driver.find_elements(By.XPATH, "//div[@class = 'counts ng-binding']")[-4].text)
          rating_good.append(driver.find_elements(By.XPATH, "//div[@class = 'counts ng-binding']")[-3].text)
          rating_avg.append(driver.find_elements(By.XPATH, "//div[@class = 'counts ng-binding']")[-2].text)
          rating_bad.append(driver.find_elements(By.XPATH, "//div[@class = 'counts ng-binding']")[-1].text)
          factor_position.append(driver.find_elements(By.XPATH, "//span[@ng-bind = 'rate.Point|number:1']")[-5].text)
          factor_price.append(driver.find_elements(By.XPATH, "//span[@ng-bind = 'rate.Point|number:1']")[-4].text)
          factor_quality.append(driver.find_elements(By.XPATH, "//span[@ng-bind = 'rate.Point|number:1']")[-3].text)
          factor_service.append(driver.find_elements(By.XPATH, "//span[@ng-bind = 'rate.Point|number:1']")[-2].text)
          factor_space.append(driver.find_elements(By.XPATH, "//span[@ng-bind = 'rate.Point|number:1']")[-1].text)
          print((driver.find_elements(By.XPATH, "//div[@class='fldr-res-title ng-binding']")[1].text))
          for i in range(len(length)):
              store_name_.append(driver.find_elements(By.XPATH, "//div[@class='fldr-res-title ng-binding']")[1].text)
              time_cmt.append(driver.find_elements(By.XPATH, "//span[@class = 'ru-time ng-binding']")[i].text)
              cmt.append(driver.find_elements(By.XPATH, "//div[@class = 'review-des fd-clearbox ng-scope']")[i].text)
          print("Done_Food_Store_Number",i)
          driver.find_elements(By.XPATH, "//div[@class = 'fd-btn-close']")[0].click()

      df_store = pd.DataFrame({'store_name': store_name_,'cmt':cmt,'time_cmt':time_cmt})
      df_store_infor = pd.DataFrame({'store_name': store_name,'rating_very_good':rating_very_good,'rating_good':rating_good,'rating_avg':rating_avg
                    ,'rating_bad':rating_bad,'factor_position':factor_position,'factor_price':factor_price,
                'factor_quality':factor_quality,'factor_service':factor_service,'factor_space':factor_space})
      df_store.to_csv(list[h].split('/')[-1]+ '.csv')
      df_store_infor.to_csv(list[h].split('/')[-1]+ '_info.csv')
      driver.close()
      driver.quit()
      return df_store

with cont_url:
  st.title("FOOD_REVIEW")
  url = data_scrape()
  st.table(url)