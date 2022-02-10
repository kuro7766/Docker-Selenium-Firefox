# BilibiliUp2

kuro7766 原 [BilibiliUp](https://github.com/kuro7766/BilibiliUp/) (40⭐100 fork)残余的代码，可以在windows上运行

bilibili刷播放量，b站刷播放量，哔哩哔哩刷播放量

为了避免悲剧再次发生，请只star，不要fork。

QQ群 : [825766491](https://jq.qq.com/?_wv=1027&k=ufk3KrUQ)

# Windows 安装

需要下载firefox

安装对应的python pip环境

然后直接运行python bilibili_playcount_up.py。如果无法运行，需要找到适合的geckodriver版本

运行成功之后，修改bilibili_playcount_up.py里面的url即可

# ubuntu installation

### requirement:

ubuntu 20 or 18 .
if you are using other versions of ubuntu , you have to find a compatible version of firefox and geckodriver

run this command:
```
apt-get install firefox=75.0+build3-0ubuntu1
```
and then install corresponding firefox gecko-driver to your env

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xf geckodriver-v0.24.0-linux64.tar.gz
mv geckodriver /usr/local/bin
```

then install Selenium for python

```python
pip3 install selenium
```

libs for ml.py if you want to include it:
```shell
pip3 install baidu-aip bs4 pdf2image markdown python-magic requests furl tendo pyperclip pillow

```
### usage:
#### copy 

```quick_firefox.py```,```ml.py```,```selelib.py```

and write your code like 0_google_screenshot.py

#### and then start coding

#### example:
```python
import quick_firefox
import ml
ml.ensure_dir('screenshots')
links = quick_firefox.run_sync(work=callback_fun, args=())
```
#### then write your callback function like this,you have to leave two arguments

```python
def work(_driver: WebDriver, args): 
    # do anything you want
    google = 'https://www.google.hk/search?q='
    _driver.get(google + 'python百度搜索提示api')
    
    # this javascript code may not work in the future 
    l = _driver.execute_script('''
    var elements = document.getElementsByClassName("yuRUbf");
    var r=[];
    for (var i = 0; i < elements.length; i++) {
        console.log(elements[i].children[0].href);
        r.push(''+elements[i].children[0].href);
    }
    return r;
    ''')
```
#### So you can manipulate the webdriver in reference from the selenium document
#### After this 'work' callback ,the firefox process will be killed automatically,so you don't need to call driver.quit() any more

### Notice:

#### On Windows firefox will run with head as default,while on ubuntu it will run headless as default

"# BilibiliUp2" 
