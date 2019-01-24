from selenium import webdriver
from operator import eq

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('C:\python/chromedriver',options=options)

def read():

    data = ['CKFK9-QNGF2-D34FM-99QX2-8XC4K']
    count = 1

    driver.get('https://www.windows10productkeys.info/key-finder')
    for name in range(1, 100):
        driver.find_element_by_xpath('/html/body/section[3]/div/div/div/form/button').click()
        extract_data = driver.find_element_by_xpath('/html/body/section[3]/div/div/div/b')
        check=1
        for num in range(0,count):
            if eq(data[num],extract_data.text):
                check=0
                break
        if check==1:
            data.append(extract_data.text)
            count+=1
            print(len(data))

    for name in range(0, len(data)):
        print(data[name])
    print(len(data))

read()