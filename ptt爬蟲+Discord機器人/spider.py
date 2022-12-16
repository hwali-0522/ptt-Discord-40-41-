import requests
from bs4 import BeautifulSoup


def PTT_board_finding():  # 找尋熱門看板
    hotpage = requests.get('https://www.ptt.cc/bbs/hotboards.html')  # 向網站要求資料
    soup = BeautifulSoup(hotpage.text, 'html5lib')  # 用套件解析
    # 找出所有標籤為"a"且class為'board'的元素，應該是一個列表
    board_find = soup.find_all('a', class_='board')
    for board in board_find:  # 用for迴圈印出來
        header_name = board.find('div', class_='board-name')
        print("看板名稱：", header_name.text)
        header_page = board.select('span')[0]
        print("看板分類文章數：", header_page.text)
        header_classes = board.find('div', class_='board-class')
        print("看板分類：", header_classes.text)
        header_title = board.select('div.board-title')[0]
        print("看板標題：", header_title.text)
        header_url = 'https://www.ptt.cc' + board['href']
        print("看板網址：" + header_url)
        print('\n\n')


def PTT_page_finding_newest(board):
    url = 'https://www.ptt.cc/'
    web = requests.get('https://www.ptt.cc/bbs/%s/index.html' % board,
                       cookies={'over18': '1'})  # 將所要找尋的看板名稱加到網址中，加入cookies去迴避18歲警告
    soup = BeautifulSoup(web.text, 'html5lib')
    titles = soup.find_all('div', class_='title')
    for i in titles:
        if i.find('a') != None:
            print(i.find('a').get_text())
            print(url+i.find('a')['href'], end='\n\n')


def PTT_page_finding_select(board):
    page_num = int(input("輸入你想要尋找的頁數"))  # 輸入想尋找的頁數
    url = 'https://www.ptt.cc/'
    web = requests.get("https://www.ptt.cc/bbs/%s/index%d.html" %
                       (board, page_num), cookies={'over18': '1'})
    soup = BeautifulSoup(web.text, 'html5lib')
    titles = soup.find_all('div', class_='title')
    if len(titles) == 0:
        print("404 Not Found.")  # 如果伺服器未回應，便提醒用戶端
    else:
        for i in titles:
            if i.find('a') != None:
                print(i.find('a').get_text())
                print(url+i.find('a')['href'], end='\n\n')


def PTT_page_finding_select_formHead(board):
    page_num = int(input("輸入你想要尋找到的頁數"))
    url = 'https://www.ptt.cc/'
    for j in range(1, page_num):
        web = requests.get("https://www.ptt.cc/bbs/%s/index%d.html" %
                           (board, j), cookies={'over18': '1'})
        soup = BeautifulSoup(web.text, 'html5lib')
        titles = soup.find_all('div', class_='title')
        if len(titles) == 0:
            print('404 not found ')
            break
        else:
            for i in titles:
                if i.find('a') != None:
                    print(i.find('a').get_text())
                    print(url+i.find('a')['href'], end='\n\n')


def PTT_page_finding_select_specific(board):
    page_num = int(input("輸入你想要尋找的頁數(頭)"))
    page_num_1 = int(input("輸入你想要尋找的頁數(尾)"))
    url = 'https://www.ptt.cc/'
    for j in reversed(range(page_num_1, page_num)):
        web = requests.get("https://www.ptt.cc/bbs/%s/index%d.html" %
                           (board, j), cookies={'over18': '1'})
        soup = BeautifulSoup(web.text, 'html5lib')
        titles = soup.find_all('div', class_='title')
        if len(titles) == 0:
            print('404 not found ')
            break
        else:
            for i in titles:
                if i.find('a') != None:
                    print(i.find('a').get_text())
                    print(url+i.find('a')['href'], end='\n\n')


def help():
    print("help: list the commands")
    print("\n")
    print("*********************************")
    print("1: board finding")
    print("\n")
    print("*********************************")
    print("2: page finding (newest)")
    print("\n")
    print("*********************************")
    print("3: page finding (particular page)")
    print("\n")
    print("*********************************")
    print("4: page finding (form the oldest to you chose)")
    print("\n")
    print("*********************************")
    print("5: page finding (particular pages from 'a' to 'b')")


while command_ != "0":
    command_ = str(input())
    if command_ == "help":
        help()
    elif command_ == "1":
        PTT_board_finding()
    elif command_ == "2":
        board = str(input("which board do you want to find: "))
        PTT_page_finding_newest(board)
    elif command_ == "3":
        board = str(input("which board do you want to find: "))
        PTT_page_finding_select(board)
    elif command_ == "4":
        board = str(input("which board do you want to find: "))
        PTT_page_finding_select_formHead(board)
    elif command_ == "5":
        board = str(input("which board do you want to find: "))
        PTT_page_finding_select_specific(board)
