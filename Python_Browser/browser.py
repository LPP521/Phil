from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = []
        self.setWindowTitle('亚博娱乐') # 设置窗口标题
        self.setWindowIcon(QIcon('icons/penguin.png'))  # 设置窗口图标
        navigation_bar = QToolBar('Navigation') # 添加导航栏
        navigation_bar.setIconSize(QSize(16, 16))   # 设定图标的大小
        self.setGeometry(300, 150, 1300, 800)   # 设置窗口位置大小
        self.urlbar = QLineEdit()   # 添加 URL 地址栏
        navigation_bar.addSeparator()
        
        self.addToolBar(navigation_bar)
        
        # 添加标签栏
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True) # 允许关闭标签
        self.tabs.tabCloseRequested.connect(self.close_current_tab) # 设置关闭按钮的槽
        self.add_new_tab(QUrl('https://www.google.com'), '谷歌搜索')
        self.setCentralWidget(self.tabs)
        
        self.show()

        # 设置浏览器
        # self.browser = QWebEngineView()
        # url = 'https://www.baidu.com'
        # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(url))
        # self.urlbar.setText(url)
        # 添加浏览器到窗口中
        # self.setCentralWidget(self.browser)
        
        # 添加前进、后退、停止加载和刷新按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)
        
        back_button.triggered.connect(lambda _:self.b_back())
        next_button.triggered.connect(lambda _:self.b_forward())
        stop_button.triggered.connect(lambda _:self.b_stop())
        reload_button.triggered.connect(lambda _:self.b_reload())
        
        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        # 将地址栏添加到导航栏上
        navigation_bar.addWidget(self.urlbar)
        # connect(self.urlbar, SIGNAL(returnPressed()), this, SLOT(show_url()));
        self.urlbar.returnPressed.connect(self.show_url)
        
        # 更新地址栏为当前页面链接
        # self.browser.urlChanged.connect(self.renew_urlbar)
        
    def b_back(self):
        self.urls[self.tabs.currentIndex()][1].back()
        
    def b_forward(self):
        self.urls[self.tabs.currentIndex()][1].forward()
        
    def b_stop(self):
        self.urls[self.tabs.currentIndex()][1].stop()
        
    def b_reload(self):
        self.urls[self.tabs.currentIndex()][1].reload()
        
    def show_url(self):
        s = self.urlbar.text();
        # url = QUrl(self.text())
        self.urls[self.tabs.currentIndex()][1].load(QUrl(s))
        
    def renew_urlbar(self, q, browser, n, i):
        # 将当前网页的链接更新到地址栏
        if n == self.tabs.currentIndex():
            self.urlbar.setText(q.toString())
            self.urlbar.setCursorPosition(0)
        self.urls[n][0] = q
        
    def add_new_tab(self, qurl=QUrl(''), label='Blank'):
        browser = WebEngineView()    # 为标签创建新页面
        browser.main_window = self
        browser.setUrl(qurl)
        self.urls.append([qurl,browser])
        self.urlbar.setText(qurl.toString())
        self.urlbar.setCursorPosition(0)
        i = self.tabs.addTab(browser, label)    # 为标签页添加索引方便管理
        self.tabs.setCurrentIndex(i)
        n = self.tabs.currentIndex()
        browser.urlChanged.connect(lambda qurl, browser=browser:self.renew_urlbar(qurl, browser, n, i))
        browser.titleChanged.connect(lambda _, i=i, browser=browser:self.tabs.setTabText(i, browser.page().title()))    # 加载完成后修改标签标题
        return browser
        
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
        self.urls.pop(i)
        self.urlbar.setText(self.urls[self.tabs.currentIndex()][0].toString())
        self.urlbar.setCursorPosition(0)
        
    def tab_open_doubleclick(self):
        self.add_new_tab(QUrl('https://www.google.com'), '谷歌搜索')
    
    def current_tab_changed(self):
        self.urlbar.setText(self.urls[self.tabs.currentIndex()][0].toString())
        self.urlbar.setCursorPosition(0)
        
class WebEngineView(QWebEngineView):
    main_window = None;
    def createWindow(self, QWebEnginePage_WebWindowType):
        return self.main_window.add_new_tab()
        
# class WebEngineView(QWebEngineView):
    # windowList = []
    # def createWindow(self, QWebEnginePage_WebWindowType):
        # new_webview =   WebEngineView()
        # new_window = MainWindow()
        # new_window.setCentralWidget(new_webview)

        # self.windowList.append(new_window)  #注：没有这句会崩溃！！！
        # return new_webview
        
if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用
    window = MainWindow()   # 创建主窗口
    window.show()   # 显示窗口
    app.exec_() # 运行应用，并监听事件