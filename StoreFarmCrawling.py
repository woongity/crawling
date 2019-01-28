from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

# driver = webdriver.Chrome('C:\python/chromedriver',options=options)
checkList_info=("이름","집주소","전화번호","통관번호")
driver = webdriver.Chrome('C:\python/chromedriver')
customer_info_arr=[]

class Customer:

    def __init__(self,name,address,phone,custom_num):
        self.name=name
        self.address=address
        self.phone=phone
        self.custom_num=custom_num

    def get_customer_info(self):
        info=[0,self.name,self.address,self.phone,self.custom_num]
        return info
    #
    # def __next__(self):
    #     if self.index==0:
    #         raise StopIteration
    #     self.index=self.index-1
    #     return self.data[self.index]

#TODO : num = 주문이 몇개나 들어왔는지 확인
def make_excel(url, num):
    wb = Workbook()
    ws1 = wb.active
    # ws2= wb.create_sheet(title="second_sheet")  새로운 시트 파일 하나 더 추가하기
    for col in range(1,5):
        ws1.cell(row=1,column=col,value=checkList_info[col-1])
    # 이름, 전번, 집주소, 통관번호 입력을 넣어준다
    for row in range(2, num+2):
        customer_info=customer_info_arr[row - 2].get_customer_info()
        for col in range(1, 5):
            ws1.cell(row=row, column=col).value=customer_info[col]  # TODO : value값에 그냥 숫자들이 아니라 개인 신상들어가야함
    wb.save(url)
    wb.close()

# 엑셀파일
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # driver = webdriver.Chrome('C:\python/chromedriver', options=options)
# 헤드리스 모드 진행시 블록아웃을 삭제

def get_html(url):
    _html = ""
    resp = driver.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def add_customer(name,address,phone_num,custom_num):
    customer=Customer(name,address,phone_num,custom_num)
    customer_info_arr.append(customer)

def read_order():
    customer_count=0
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # TODO: 여기서 리스트를 넣어주지 말고 읽어와서 처리하도록
    name="양태웅"
    address="서구청"
    phone_num="01057543876"
    custom_num="148342342342"
    add_customer(name,address,phone_num,custom_num)
    customer_count+=1
    # for i in customer_count:

    return customer_count

def log_in():
    try:
        driver.implicitly_wait(3)
        driver.get('https://sell.smartstore.naver.com/#/login')
        driver.find_element_by_id('loginId').send_keys('ytw1122@gmail.com')
        driver.find_element_by_id('loginPassword').send_keys('andrew3876')
        driver.find_element_by_xpath('//*[@id="loginButton"]').click()
    except Exception as inst:
        print("fuck, its not working")
        print(inst.args)
#     in case when login doesnt work properly

def go_to_order_page():
    drop_down_menu = driver.find_element_by_xpath('//*[@id="seller-lnb"]/div/div[1]/ul/li[3]')
    drop_down_menu.click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#seller-lnb > div > div:nth-child(1) > ul > li.active > ul > li:nth-child(1) > a').click()

def open_info_pages():
    driver.implicitly_wait(3)

#     TODO 여기 부분 수정해야한다. 링크를 클릭하면 창들이 탭으로 뜨면서 정보들을 크롤링해오는 방향으로 간다


log_in()
driver.implicitly_wait(3)
go_to_order_page()
open_info_pages()
customer_count=read_order()
make_excel("C:\study/test.xlsx",customer_count)
# 3의 의미 : 데이터의 갯수가 3개다
# todo: 갯수를 자동으로 읽어온다
