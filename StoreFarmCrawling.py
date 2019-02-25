from openpyxl import Workbook
from bs4 import BeautifulSoup
import gui
import Customer_class
from selenium import webdriver
from datetime import date
import os
import time
from multiprocessing import Pool

options = None
# 헤드리스 모드 진행시 블록아웃을 삭제
driver = None
checkList_info = ("아이디", "이름", "집주소", "전화번호", "통관번호")
customer_info_arr = []  # Customer 클래스의 배열


def make_excel(url, customer_count):
    wb = Workbook()
    ws1 = wb.active
    # ws2= wb.create_sheet(title="second_sheet")  새로운 시트 파일 하나 더 추가하기
    for col in range(1, 6):
        ws1.cell(row=1, column=col, value=checkList_info[col - 1])
    # 이름, 전번, 집주소, 통관번호 입력을 넣어준다
    for row in range(2, customer_count + 2):
        customer_info = customer_info_arr[row - 2].get_customer_info()
        for col in range(1, 6):
            ws1.cell(row=row, column=col).value = customer_info[col]
    wb.save(url)
    wb.close()


def get_excel_file_name():
    return date.today().isoformat() + '.xlsx'


def add_customer(id, name, address, phone_num, custom_num):
    customer = Customer(id, name, address, phone_num, custom_num)
    customer_info_arr.append(customer)


def open_info_pages(url):
    try:
        driver.implicitly_wait(3)
        driver.get(url)
        read_spec_order()
    except:
        print("상세정보창을 열 수 없습니다")
        exit()


def read_spec_order():
    id = driver.find_element_by_xpath('//*[@id="pop_content"]/div/table[1]/tbody/tr[4]/td').text
    name = driver.find_element_by_xpath('//*[@id="pop_content"]/div/table[3]/tbody/tr[1]/td').text
    phone_num = driver.find_element_by_xpath('//*[@id="pop_content"]/div/table[3]/tbody/tr[2]/td[1]').text
    address = driver.find_element_by_xpath('//*[@id="pop_content"]/div/table[3]/tbody/tr[3]/td').text
    custom_num = driver.find_element_by_xpath('//*[@id="pop_content"]/div/table[3]/tbody/tr[4]/td').text
    # if name=="취소완료":
    #     return False
    print(id, name, address, phone_num, custom_num)
    add_customer(id, name, address, phone_num, custom_num)

def read_order_and_return_customer_count():
    driver.implicitly_wait(3)
    driver.switch_to.frame(driver.find_element_by_id("__naverpay")) #새로운 프레임으로 이동한다

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')  #lxml 이 빠르므로 이걸로 쓰자
    content=[]
    list=soup.find_all(class_="ellipsis",columnname="PRODUCT_ORDER_ID",title=True)
    for item in list:
        content.append(item.text)
    customers_count=int(len(list))

    #TODO : list 배열에서 title 값을 읽어오는 역할을 수행한다.
    for customer_num in range(0,customers_count):
        url = 'https://sell.smartstore.naver.com/o/orderDetail/productOrder/' + content[customer_num] + '/popup'  # 상세페이지 url
        open_info_pages(url)
    # for page in list:
    #
    #     open_info_pages(url)
    # for i in customer_count:
    return customers_count

def log_in():
    try:
        driver.implicitly_wait(3)
        driver.get('https://sell.smartstore.naver.com/#/login')
        driver.find_element_by_id('loginId').send_keys('ytw1122@gmail.com')
        driver.find_element_by_id('loginPassword').send_keys('andrew3876')
        driver.find_element_by_xpath('//*[@id="loginButton"]').click()
    #     TODO: 여기에 사용자의 이메일과 아이디를 넣어줘야 작동하도록 구현
    except Exception as inst:
        print("fuck, its not working")
        print(inst.args)

#     in case when login doesnt work properly

def go_to_order_page():
    drop_down_menu = driver.find_element_by_xpath('//*[@id="seller-lnb"]/div/div[1]/ul/li[3]')
    drop_down_menu.click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector(
        '#seller-lnb > div > div:nth-child(1) > ul > li.active > ul > li:nth-child(1) > a').click()

# webdriver.ChromeOptions()
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# driver=webdriver.Chrome('C:\python/chromedriver',options=options)
if __name__=='__main__':
    # start_time = time.time()
    # log_in()
    # driver.implicitly_wait(3)
    # go_to_order_page()
    # customer_count = read_order_and_return_customer_count()
    # file_name = os.path.dirname(os.path.realpath(__file__)) + get_excel_file_name()
    # make_excel(file_name, customer_count)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # # TODO : 속도가 너무 느리다. 멀티프로세싱으로 좀 더 빠른 방법이 없을까?
    app = gui.QApplication(gui.sys.argv)
    ex = gui.MyApp()
    gui.sys.exit(app.exec_())