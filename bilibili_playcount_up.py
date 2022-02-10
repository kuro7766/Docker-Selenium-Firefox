from selenium.webdriver.firefox.webdriver import WebDriver
import selelib


def work(_driver: WebDriver, args):
    import sys
    import ml
    import time
    import selelib
    print('work start ')
    ml.ensure_dir('screenshots')
    ml.ensure_dir('bili')
    _driver.get('https://www.bilibili.com/video/你的bv号')
    # 旧xpath，已经失效
    # xpath = '/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[10]/div[2]/div[2]/div[1]/div[1]/button'
    # xpath = '/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[11]/div[2]/div[2]/div[1]/div[1]/button'
    # selelib.lib(_driver).wait_until_xpath(xpath)
    # time.sleep(10)

    lb=selelib.lib(_driver)
    while not lb.get_html().count('人正在看'):
        print('not loaded')
        time.sleep(1)
    print('button ok........')
    time.sleep(3)
    print('before exec')
    _driver.execute_script('''
    function click(x,y){
    var ev = document.createEvent("MouseEvent");
    var el = document.elementFromPoint(x,y);
    ev.initMouseEvent(
        "click",
        true, true,
        window, null,
        x, y, 0, 0,
        false, false, false, false,
        0 , null
    );
    el.dispatchEvent(ev);
    } 
    click(200,200);
    ''')
    x = selelib.lib(_driver).findall(r'总播放数\d+')
    print(x)
    ml.write_string_append('bili/count.txt', ml.time_() + " " + str(x) + '\n')
    selelib.lib(_driver).screen_shot('screenshots/bilibili播放量up_播放前.png')
    time.sleep(15)
    selelib.lib(_driver).screen_shot('screenshots/bilibili播放量up_播放10秒后.png')
    return 1


if __name__ == '__main__':
    import quick_firefox
    import ml

    # while True:
    r = quick_firefox.run_sync(work=work, args=())
    print('run success')
