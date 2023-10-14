# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 22:01:27 2023

@author: User
"""
import os
import requests
import time
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Connect_php():
    # 設置 EdgeDriver 的路徑
    edge_driver_path = 'msedgedriver.exe'  # 例如: 'C:\\path_to\\msedgedriver.exe'
    
    # 創建 Edge 選項對象
    edge_options = webdriver.EdgeOptions()

    # 啟用無痕模式
    edge_options.add_argument('--inprivate')
    
    # 創建 WebDriver 對象，使用 Microsoft Edge
    driver_service = Service(edge_driver_path)
    driver = webdriver.Edge(service=driver_service, options=edge_options)
    
    # 訪問目標網站
    driver.get('https://imagic.ntue.edu.tw/magic/index.php')
    return driver
    
def wait_and_click_image(driver):
    try:
        # 等待最多10秒，直到圖片元素出現
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[@src="images/nav_login.png"]'))
        )
        # 點擊圖片元素
        image_element.click()
    except Exception as e:
        print(f"An error occurred: {e}")

def login(driver, username_str, password_str):
    try:
        # 等待最多10秒，直到username元素出現
        username_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        # 在username元素中輸入字串
        username_element.send_keys(username_str)

        # 等待最多10秒，直到password元素出現
        password_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'spotify'))
        )
        # 在password元素中輸入字串
        password_element.send_keys(password_str)

    except Exception as e:
        print(f"An error occurred: {e}")
        
    try:
         # 等待最多10秒，直到圖片元素出現
         image_element = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.XPATH, '//img[@src="images/btn_login.gif"]'))
         )
         # 點擊圖片元素
         image_element.click()
    except Exception as e:
         print(f"An error occurred: {e}")
         

        
def get_course_list(driver):
    try:
        # Step 1: Click on the span.caret to open the dropdown
        span_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.caret'))
        )
        driver.execute_script("arguments[0].click();", span_elements[1])

        # Step 2: Wait for the dropdown to appear and locate all courses using only the <a> inside <li>.
        course_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.dropdown-menu li a'))  # adjust this selector
        )

        # Step 3: Extract text from each course element
        courses = [element.text for element in course_elements if element.text.strip() != '']  # Only include non-empty texts
        return courses
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []





def get_all_links(driver):
    main_div_xpath = '//div[@class="col-lg-3 col-sm-6 col-xs-12"]'
    links = []

    try:
        # Wait for the main content section to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//section[@class="content"]/div[@class="row"]'))
        )

        # Locate all divs with the specific class
        div_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, main_div_xpath))
        )

        for div_element in div_elements:
            # Find all links inside the current div
            link_elements = div_element.find_elements(By.XPATH, './/a')
            for link_element in link_elements:
                links.append(link_element.get_attribute("href"))

    except Exception as e:
        print(f"An error occurred: {e}")

    return links

def visit_links(driver, links):
    for link in links:
        try:
            print(f"Visiting link: {link}...")
            driver.get(link)
            # TODO: Add any logic here if you need to interact with the page.
            pdf_data_urls = get_all_pdf_data_urls(driver)
            print("PDF_Url:",pdf_data_urls)
            download_pdfs_from_data_urls(pdf_data_urls)
            
            
        except Exception as e:
            print(f"An error occurred while visiting {link}: {e}")

# Modify this function
def click_each_course(driver):
    try:
        # Step 1: Click on the span.caret to open the dropdown
        span_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.caret'))
        )
        driver.execute_script("arguments[0].click();", span_elements[1])

        # Step 2: Wait for the dropdown to appear and locate all courses using only the <a> inside <li>.
        course_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.dropdown-menu li a'))
        )

        total_courses = len(course_elements)
        for index in range(total_courses):
            # Re-locate elements after going back
            span_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.caret'))
            )
            driver.execute_script("arguments[0].click();", span_elements[1])
            
            course_elements = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.dropdown-menu li a'))
            )
            
            course_element = course_elements[index]
            course_name = course_element.text.strip()
            
            # If course name is not empty, click on the course
            if course_name:
                print(f"Clicking on course: {course_name}")
                
                # Use JavaScript to click the course
                driver.execute_script("arguments[0].click();", course_element)
                
                # Get all the links for the course
                links = get_all_links(driver)
                
                # Visit each link
                visit_links(driver, links)
                
                
                # Return to the previous page (course list)
                driver.back()

    except Exception as e:
        print(f"An error occurred: {e}")

def get_all_pdf_data_urls(driver):
    try:
        # 定位包含.pdf的所有a標籤
        pdf_links = driver.find_elements(By.XPATH, '//div[@class="info-box-content"]//a[contains(@data-url, ".pdf")]')
        
        # 從每個a標籤中提取data-url屬性
        data_urls = [link.get_attribute('data-url') for link in pdf_links]

        return data_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def download_pdf_from_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:  # 檢查響應碼是否為200（OK）
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")



def download_pdfs_from_data_urls(pdf_data_urls):
    base_url = "https://imagic.ntue.edu.tw/magic/"
    
    for url in pdf_data_urls:
        # 生成完整的URL
        absolute_url = base_url + url
        
        # 從URL中提取文件名
        filename = os.path.join("PDF", os.path.basename(url))
        
        # 下載PDF
        download_pdf_from_url(absolute_url, filename)        

def main_process():
    driver = Connect_php()
    wait_and_click_image(driver)
    username_str = input("請輸入INTUE學號:")
    password_str = input("請輸入INTUE密碼:")
    login(driver, username_str, password_str)
    click_each_course(driver)
    print("download ok .pdf in PDF Folder!!")
    driver.close()
    os.system("pause")
    
   

if __name__ == '__main__':
    main_process()
   

   
