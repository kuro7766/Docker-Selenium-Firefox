import os
import pickle
import time
import re
import ml
from selenium.common.exceptions import NoSuchElementException
from sys import platform


def platform_kill(driver=None):
    print('platform::', str(platform))
    if platform == "linux" or platform == "linux2":
        # linux
        driver.close()
        driver.quit()
        os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
        print('killing all firefox processes...')
    elif platform == "win32" or platform == "win64":
        # Windows...
        print('win32 killing ...')
        # print(driver)
        if driver:
            driver.close()
            driver.quit()


def screen_shot(driver, dir_pic='默认截图.png'):
    # ml.ensure_dir('截图')
    # driver.save_screenshot('截图/' + str(datetime.datetime.now()) + '.png')
    driver.save_screenshot(dir_pic)

# def all_finish():
#     if platform == "linux" or platform == "linux2":
#         # linux
#         os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
#         os.system('''find /tmp -name "rust*"|xargs rm -rf''')
#         print('killing and cleaning caches ...')


# def load_cookie(cookie_path):
#     if os.path.exists(cookie_path):
#         with open(cookie_path, "rb") as f:
#             cookies = pickle.load(f)
#             print('dump_cookie ::: ', cookies)
#             f.close()
#             return cookies


class lib:

    def __init__(self, driver):
        self.driver = driver

    def findall(self, pattern):
        text = self.get_html()
        return re.findall(pattern, text)

    def wait_until_text(self, pattern):
        while not self.findall(pattern):
            time.sleep(1)

    def get_html(self):
        return self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    def wait_until_xpath(self, xpath):
        find = False
        while not find:
            try:
                if self.driver.find_element_by_xpath(xpath):
                    find = True
                    return self.driver.find_element_by_xpath(xpath)
                else:
                    time.sleep(1)
            except NoSuchElementException as e:
                print(e)
        return self.driver.find_element_by_xpath(xpath)

    def load_cookie(self, cookie_path, load_in=True):
        if os.path.exists(cookie_path):
            with open(cookie_path, "rb") as f:
                cookies = pickle.load(f)
                print('dump_cookie ::: ', cookies)
                if load_in:
                    for cookie in cookies:
                        try:
                            self.driver.add_cookie(cookie)
                        except Exception:
                            pass
                f.close()
                return cookies

    def dump_cookie(self, cookie_path):
        with open(cookie_path, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
            print('dump_cookie ::: ', self.driver.get_cookies())
            f.close()
            return self.driver.get_cookies()

    def screen_shot(self, path):
        self.driver.save_screenshot(path)
        return path

    def get_current_window_text_ocr(self):
        oo = ml.ocr(self.screen_shot('tmp.png'))
        s = []
        for i in oo['words_result']:
            s.append(i['words'])
        return ''.join(s)
