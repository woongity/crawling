import requests
from bs4 import BeautifulSoup
import os, smtplib
from email.mime.text import MIMEText
import logging, re
import datetime
import django,json
from operator import eq
from email.mime.multipart import MIMEMultipart

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chungnaEmail.settings")

django.setup()
from parsed_data.models import UserInfo

dt = datetime.datetime.now()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOB_URL ='http://www.seo.incheon.kr/open_content/main/part/job/news.jsp'
    
#공통된느 부분 삭제를 위한 함수
def get_req(url):
    req=requests.get(url)
    req.encodeing = 'utf-8'
    return req

#태그 삭제 함수
def remove_tag(content):
    return re.sub('<.+?>', '', content, 0).strip()

#게시글 제목 가져오는 함수 
def get_titles(url):
    html=get_req(url).text
    soup=BeautifulSoup(html,'html.parser')
    posts_titles=soup.select('td.left.title')
    for i in range(len(posts_titles)):
        posts_titles[i]=str(posts_titles[i])
        posts_titles[i]=remove_tag(posts_titles[i])
    return posts_titles

#게시글 날짜 가져오는 함수
def get_date(url):
    html=get_req(url).text
    soup=BeautifulSoup(html,'html.parser')
    posts_date=soup.select('tr > td:nth-child(5)')
    for post in posts_date:
        post=post.contents[0]
    return posts_date
    
#게시글 url가져오는 함수
def get_url(url):
    html=get_req(url).text
    soup=BeautifulSoup(html,'html.parser')
    posts_url=[]
    for link in soup.select("td.left.title > a"):
        post="http://www.seo.incheon.kr"+link.get('href')
        posts_url.append(post)
    return posts_url

#이메일 보내는 함수
def send_email(titles,links):
    smtp=smtplib.SMTP('smtp.gmail.com',587)
    
    smtp.ehlo()
    smtp.starttls()
    smtp.login('chungna2dongbot@gmail.com', 'andrew3876!')
    
    msg=MIMEMultipart('alternative')
    email_body= "<html><head>오늘 청라 2동 주민센터 소식입니다.<head>"
    email_body+="<body>"
    for num in range(len(titles)):
        email_body+="""<p><a href="""+"\""+str(links[num])+"\""+">"+str(titles[num])+"""</a></p>"""
    email_body+="</body>"
    email_body+="""</html>"""  
    body=MIMEText(email_body,'html')
    
    msg['Subject']=dt.strftime("%Y년 %m월 %d일 청라2동주민센터 새소식")
    msg['To']="ytw5754@naver.com"
    msg.attach(body)
    
    smtp.sendmail('chungna2dongbot@gmail.com','ytw5754@naver.com',msg.as_string())
    smtp.quit()
    
    
if __name__=='__main__':
    
    today_date = dt.strftime("<td>%Y.%m.%d</td>")
    logging.warning(today_date)
    titles=get_titles(JOB_URL)
    dates=get_date(JOB_URL)
    
    links=get_url(JOB_URL)
    arr_len=len(dates)
   
    #오늘 온 포스딩을 저장할 배열
    today_titles=[]
    today_links=[]  
    
    for post in range(0,arr_len):
        
        year = dates[post].contents[0].split('.')[0]
 
#게시글이 이상하게 표시되어있어서 오늘 날짜인 경우 예외처리를 해줘야한다
        if str(dates[post]) == today_date or len(year)>4 :
            today_titles.append(titles[post])
            today_links.append(links[post])
#오늘 보낼내용이 없다면
    if len(today_links)!=0:
        logging.warning(len(today_links))
        send_email(today_titles,today_links)
#TODO : 텍스트파일이 아닌 modeling해서 db로 옮기자 ok but is that necessary??
#TODO : 오늘 날짜 확인하고 그 날짜 맞으면 메일 보내주자. ok
#TODO : 링크도 같이 따서 하이퍼링크 형식으로 보낸다.  ok 
    