from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from tkinter import Tk, Label
import sys
import os
import subprocess

import time

if hasattr(sys, '_MEIPASS'):
    chrome_driver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
else:
    chrome_driver_path = 'chromedriver.exe'  # 替换为实际的 chromedriver.exe 路径


url = "https://coinmarketcap.com/currencies/bitcoin/"
# 设置Chrome选项以启用无头模式
chrome_options = Options()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument("--headless")
# 启动浏览器
service = Service(chrome_driver_path)
service.start()
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

# 更新标签文本
def update_label():

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    element = soup.find('span', {'class': 'sc-16891c57-0 dxubiK base-text'})
    current_number = element.text
    label.config(text="当前价格: " + current_number)
    label.after(1000, update_label)  # 每隔一秒更新一次

def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

# 创建一个简单的GUI窗口
root = Tk()
root.overrideredirect(True)
root.wm_attributes('-topmost', 1)
label = Label(root, text="")
label.pack()
label.bind('<B1-Motion>', move_window)

# 开始更新数字
update_label()

# 运行tkinter主循环
root.mainloop()

# 关闭浏览器
driver.quit()
service.stop()
