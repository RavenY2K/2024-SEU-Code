import keyboard
import webbrowser

url = "https://www.google.com/"  # 指定要打开的网页地址
browser_is_open = False  # 用来标记浏览器是否已经打开了指定URL
last_url = None  # 用来记录上一次打开的URL

def open_browser():
    global browser_is_open, last_url
    
    # 如果浏览器已经打开了指定URL，则直接回到之前的URL
    if browser_is_open:
        if last_url:
            webbrowser.get().open(last_url)
        return
    
    webbrowser.get().open(url)
    browser_is_open = True
    last_url = url

keyboard.add_hotkey('ctrl+e', open_browser)

keyboard.wait()  # 让程序一直运行，直到按下快捷键
