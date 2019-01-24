from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

# driver = webdriver.Chrome('C:\python/chromedriver',options=options)
customer_info=("이름","전화번호","집주소","통관번호")
driver = webdriver.Chrome('C:\python/chromedriver')
class Customer:

    def __init__(self,name,address,phone,custom_num):
        self.name=name
        self.address=address
        self.phone=phone
        self.custom_num=custom_num

# num = 주문이 몇개나 들어왔는지 확인
def make_excel(url, num):
    wb = Workbook()
    ws1 = wb.active
    # ws2= wb.create_sheet(title="second_sheet")  새로운 시트 파일 하나 더 추가하기
    for col in range(1,5):
        ws1.cell(row=1,column=col,value=customer_info[col-1])
    # 이름, 전번, 집주소, 통관번호
    for row in range(2, num+1):
        for col in range(1, 5):
            ws1.cell(row=row, column=col, value=int("{}{}".format(row, col))) # TODO value값에 그냥 숫자들이 아니라 개인 신상들어가야함
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


def read_every_order_info():
    driver.implicitly_wait(3)
    links=driver.find_elements_by_class_name('_click(nmp.seller_admin.order.popup.openProductOrderDetail')
    print(links)
    for link in links:
        link.click()
    #     TODO 여기 부분 수정해야한다. 링크를 클릭하면 창들이 탭으로 뜨면서 정보들을 크롤링해오는 방향으로 간다
    # html=driver.page_source
    # soup=BeautifulSoup(html,'html.parser')
    # notices=soup.select(('body > div.npay_content._root > div.napy_sub_content > div:nth-child(2) > div.npay_grid_area > div.grid._detailGrid._grid_container.uio_grid > div._inflexible_area.inflexible_area > div._body.body > div._table_container > table > tbody > tr:nth-child(1) > td:nth-child(2) > a'))
    #
    # for notice in notices:
    #     print(notice.text.strip())

    # driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a').click()
def read_order():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    orders = soup.select('')

log_in()
go_to_order_page()
make_excel("C:\study/test.xlsx",10)
driver.implicitly_wait(3)
read_every_order_info()
read_order()
