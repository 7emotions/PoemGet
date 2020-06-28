from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib import parse
from selenium.webdriver.support import expected_conditions as EC
from bs4 import element

def getsoup(url):
    brower = webdriver.Chrome()
    brower.get(url)
    wait = WebDriverWait(brower, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'main')))
    soup = BeautifulSoup(brower.page_source, 'html.parser')
    brower.close()
    return soup

def getpoem(msg):
    arg = msg.split('#')
    title = arg[0]
    author = ''
    if '#' in msg:
        author = arg[1]
    base_url = r'https://hanyu.baidu.com'
    url = base_url + '/s?wd=' + parse.quote(title)

    soup = getsoup(url)
    text = soup.findAll(id='body_p')

    Bpoem = ''
    if text == []:
        if author == '':
            return '无法获取古诗，试试加上作者吧~PS:标题与作者用#分开'
        for tag in soup.findAll():
            if tag.name == 'spen' and '朝代' in tag.get_text():
                tag.decompose()
        items = soup.findAll(name='div', attrs={'class': 'poem-list-item'})
        for item in items:
            for child in item.children:
                if type(child) is element.Tag and author in child.get_text():
                    link = item.a['href']
                    text = getsoup(base_url + link).findAll(id='body_p')

    for item in text:
        Bpoem += item.get_text()

    return Bpoem

if __name__ == '__main__':
    print(getpoem('春望#杜甫'))