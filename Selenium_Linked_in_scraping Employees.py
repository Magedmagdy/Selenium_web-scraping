
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import pwinput

# INPUTS START
linkedin_email_id = input("Enter Linked In Email:")
linkedin_password = pwinput.pwinput(prompt="Enter Password: ", mask='*')
Company_name=input("Enter Company:")
number_of_pages=int(input("Enter number of pages you want to extract:"))

search_url = f"https://www.linkedin.com/search/results/people/?keywords={Company_name}&origin=CLUSTER_EXPANSION&sid=%40RC"
# INPUTS END

# Login 
driver = webdriver.Chrome(executable_path='E:/Programes/chromedriver-win64/chromedriver')
driver.get("https://linkedin.com/uas/login")
time.sleep(5)
username = driver.find_element(By.ID, "username")
username.send_keys(linkedin_email_id) 
pword = driver.find_element(By.ID, "password")
pword.send_keys(linkedin_password)    
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Extract names and positions
time.sleep(20)

names,Job_titles,Cities,Profile_Links = [],[],[],[]

for page_count in range(1,number_of_pages+1) :
    current_url = search_url + "&page=" + str(page_count)
    driver.get(current_url)  
    time.sleep(5)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')

    containers=soup.find_all('div',class_="mb1")
    for container in containers:
        name=container.find_all('span',class_="")
        names.append(name[1].text)

        Profile_link=container.find('a',class_="app-aware-link")
        Profile_Links.append(Profile_link.get('href'))

        city=container.find('div',class_="entity-result__secondary-subtitle t-14 t-normal")
        Cities.append(city.text.strip())

        Job_title=container.find('div',class_="entity-result__primary-subtitle t-14 t-black t-normal")
        Job_titles.append(Job_title.text.strip())
 
df=pd.DataFrame({'Name':names,'Job Title':Job_titles,'City':Cities,'Profile Link':Profile_Links})
df.to_csv(f'{Company_name}_employees.csv')
