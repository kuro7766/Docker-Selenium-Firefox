import pickle

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from sys import platform
import shutil
import datetime
import ml
import re
import selelib


def get_time():
    return re.sub(r'\..*$', '', str(datetime.datetime.now())).replace(':', '.')


def report_bug(bug_string):
    bug = os.path.join(bug_dir, get_time())
    ml.write_string(bug, bug_string)


bug_dir = 'bug_log/'
linux_lock_file = '/var/selenium_lock.kuro'


class QuickFirefox:
    def __init__(self, work, args, download_dir='/selenium_default_download/'):
        # self.callback = success_callback
        self.bug_dir = bug_dir
        self.max_exec_seconds = 300
        ml.ensure_dir('bug_log')
        self.linux_download_dir = download_dir
        self.args = args
        self.work = work
        self.work_result = 0
        self.linux_lock_file = linux_lock_file
        if not work:
            self.report_bug('you have to pass your work(_driver) call back in QuickFirefox constructor !')
            raise Exception('you have to pass your work(_driver) call back in QuickFirefox constructor !')

        # if platform == "linux" or platform == "linux2":
        #     if os.path.exists(self.linux_lock_file):
        #         print('you cannot run two selenium instances at the same time!')
        #         self.report_bug('you cannot run two selenium instances at the same time!')
        #     else:
        #         ml.write_string(self.linux_lock_file, '')

        # elif platform == "win32" or platform == "win64":
        #     pass
        self.trace_file = 'last_trace_exception.txt'
        self.driver = None
        self.firefox_log = 'firefox_log.txt'
        self.start = time.time()
        self.end = 0
        print('main start')
        self.main()
        print('main end')

    def report_bug(self, bug_string):
        bug = os.path.join(self.bug_dir, get_time())
        ml.write_string(bug, bug_string)

    def create_a_driver(self, delete_dir=False):
        options = Options()
        dir = ''
        if platform == "linux" or platform == "linux2":
            # linux
            dir = self.linux_download_dir
            if delete_dir:
                if os.path.exists(dir):
                    shutil.rmtree(dir)
            ml.ensure_dir(dir)
            options.headless = True
        elif platform == "win32" or platform == "win64":
            # Windows...
            dir = 'download'
            # options.headless = True

        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", dir)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        options.set_preference("pdfjs.disabled", True)

        # https://stackoverflow.com/questions/61035556/python-selenium-dont-autoplay-videos

        options.set_preference('media.autoplay.default', 0)
        options.set_preference('media.autoplay.allow-muted', True)
        options.set_preference("print.always_print_silent", True)
        # profile = webdriver.FirefoxProfile()

        # profileDir = 'firefox_profile'
        # profile = webdriver.FirefoxProfile(profileDir)
        binary = FirefoxBinary()
        # binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

        driver = webdriver.Firefox(firefox_options=options, firefox_binary=binary)
        # driver = webdriver.Firefox(options=options, firefox_binary=binary)

        driver.set_script_timeout(2)
        driver.implicitly_wait(3)

        driver.set_page_load_timeout(self.max_exec_seconds)
        driver.set_script_timeout(self.max_exec_seconds)  # 这两种设置都进行才有效
        return driver

    # def work(self, _driver):
    #     # _driver.get(ml.read_string('spid_article_url.txt'))
    #     # selelib.lib(_driver).wait_until_text('qq_43380015')
    #     # print('wait end')
    #     self.result = self.work(_driver, self.args)

    def do_your_full_task(self):
        d = self.create_a_driver(True)
        self.driver = d
        self.work_result = self.work(d, self.args)

        selelib.platform_kill(d)

    # def new_thread():
    #
    #     while True:
    #         if time.time() - start > run_time_threshold:
    #             selelib.kill_linux(driver_list[0])
    #             os._exit(1)
    #         time.sleep(1)

    # run_time_threshold = 5

    def main(self):
        import traceback
        # print('args test ::', self)
        # _thread.start_new_thread(new_thread, ())
        ml.write_string('lock', '')
        # if os.path.exists(self.trace_file):
        #     os.remove(self.trace_file)

        if platform == "linux" or platform == "linux2":
            # linux init
            pass
        elif platform == "win32" or platform == "win64":
            # Windows...
            pass

        count = 0
        success = 0
        while True:
            try:
                self.do_your_full_task()
                success = 1
            except Exception as e:
                if platform == "linux" or platform == "linux2":
                    # linux
                    os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
                    os.system('''find /tmp -name "rust*"|xargs rm -rf''')
                    print('killing and cleaning caches ...')

                success = 0
                ml.write_string_append(self.trace_file,
                                       str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + '\n')
                traceback.print_exc(file=open(self.trace_file, 'a+'))
                self.report_bug('please see trace file\n' + str(e))
                break
            if success:
                print('process end normally !')
                break

        if platform == "linux" or platform == "linux2":
            # linux
            os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
            os.system('''find /tmp -name "rust*"|xargs rm -rf''')
            print('killing and cleaning caches ...')
            if os.path.exists(self.linux_lock_file):
                os.remove(self.linux_lock_file)
            print('delete lock file')
        elif platform == "win32" or platform == "win64":
            # Windows...
            pass
        self.end = 1
        # if self.callback:
        #     self.callback(1)
        print('All time spent', int(time.time() - self.start), 'seconds')


def wait_to_kill_thread(f: QuickFirefox):
    print('clocking start...')
    while True:
        print('checking ended ?', f.end)
        if f.end:
            return
        if time.time() > f.start + f.max_exec_seconds:
            print('time up ...')
            # print(f.driver)
            f.report_bug('time exceed limit:' + str(f.max_exec_seconds) + ',real time' + str(time.time() - f.start))
            if f.driver:
                selelib.platform_kill(f.driver)
            if platform == "linux" or platform == "linux2":
                # linux
                os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
                os.system('''find /tmp -name "rust*"|xargs rm -rf''')
                print('killing and cleaning caches ...')
                if os.path.exists(f.linux_lock_file):
                    os.remove(f.linux_lock_file)
                print('delete lock file')
            elif platform == "win32" or platform == "win64":
                # Windows...
                pass
            break
        time.sleep(2)
    # exit(-1)
    # raise Exception('time exceeded exception !')


# if f.driver_list:
#     f.driver_list[0].quit()

pipe = 'pipe_finish.obj'
pipe_obj = 'pipe.obj'

result = [None]


def _async_fun(work, args):
    r = QuickFirefox(work=work, args=args).work_result
    ml.write_obj(pipe, True)
    ml.write_obj(pipe_obj, r)
    # print('result', r)
    # print(r)


# work(driver,args) callback
def run_sync(work, args, timeout=300):
    if os.path.exists(pipe_obj):
        os.remove(pipe_obj)
    if os.path.exists(pipe):
        os.remove(pipe)

    if platform == "linux" or platform == "linux2":
        if os.path.exists(linux_lock_file):
            t = ml.read_obj(linux_lock_file)
            if time.time() - t > timeout:
                os.remove(linux_lock_file)
                ml.write_obj(linux_lock_file, time.time())
            else:
                print('you cannot run two selenium instances at the same time!')
                report_bug('you cannot run two selenium instances at the same time!')
                return 0
        else:
            ml.write_obj(linux_lock_file, time.time())

    elif platform == "win32" or platform == "win64":
        pass

    import multiprocessing
    start = time.time()

    proc = multiprocessing.Process(target=_async_fun, args=(work, args))
    proc.start()
    # Terminate the process
    while True:
        print('time left', int(start + timeout - time.time()))
        if time.time() - start > timeout:
            proc.terminate()  # sends a SIGTERM
            if platform == "linux" or platform == "linux2":
                # linux
                os.system('''ps aux|grep firefox|awk '{print $2}' |xargs kill -9''')
                os.system('''find /tmp -name "rust*"|xargs rm -rf''')
                print('killing and cleaning caches ...')
                if os.path.exists(linux_lock_file):
                    os.remove(linux_lock_file)
                print('delete lock file')
            elif platform == "win32" or platform == "win64":
                os.system('taskkill /im firefox.exe -f')
                # Windows...
                print('please close firefox manually , if it runs on linux , it will be close with force')
                pass
            return 'time exceed'
        if os.path.exists(pipe):
            if ml.read_obj(pipe):
                if os.path.exists(pipe_obj):
                    return ml.read_obj(pipe_obj)
                # print('returnv ', r[0])
                # return r[0]
        time.sleep(1)


'''
Documentation
# WARNING ip pool test
### `. if you want to add a proxy in the future , add this to firefox constructor as firefox_capabilities
###    please use your proxy ip in firefox windows first to save test time!
        # remember to remove firefox_capabilities in firefox driver constructor
        hh = ml.read_string('ip_pool.txt').split('\n')
        x = hh.pop(0)
        x2 = re.sub('^.*//', '', x)
        ml.write_string('ip_pool.txt', '\n'.join(hh))
        sp = x.rindex(':')
        url = x[:sp]
        port = x[sp + 1:]
        print(url, ';;;;', port)
        print('x2',x2)
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        # PROXY = "58.216.202.149:8118"
        PROXY = x2

        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY
        }
### TODO
    kill single process on linux
    
'''
if __name__ == '__main__':
    # QuickFirefox(work=0)
    pass
