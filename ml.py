import re
import os
import base64
from sys import platform
import shutil

SCREEN_SHOT_BASE_DIR = 'tmp/'
# 可以判断数字
DESKTOP = r'C:/Users/1/Desktop/'
WORKSPACE = DESKTOP + r'workspace/'
WORKSPACEINPUT = WORKSPACE + 'input/'
WORKSPACEOUTPUT = WORKSPACE + 'output/'
# 分割长度 last:50
SPLIT = 40

MINUTE_MILLIS = 60000


def init_cross_platform_variables():
    ensure_dir(DESKTOP)
    ensure_dir(WORKSPACE)
    ensure_dir(WORKSPACEINPUT)
    ensure_dir(WORKSPACEOUTPUT)
    if platform == "linux" or platform == "linux2":
        # linux
        pass
    elif platform == "win32" or platform == "win64":
        # Windows...
        pass


from aip import AipOcr

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def log(s):
    print(s)
    with open('ml_logs.txt', 'a+', encoding='utf-8') as f:
        f.write(s)
        f.close()


def json_decode(json):
    encoded = json
    decoded = {}
    for i in encoded:
        if type(encoded[i]) == str:
            decoded[base64decode(str(i))] = base64decode((encoded[i]))
        else:
            decoded[base64decode(str(i))] = encoded[i]
    print(decoded)
    return decoded


def json_encode(json):
    x = json
    encoded = {}
    for i in x:
        if type(x[i]) == str:
            encoded[base64encode(str(i))] = base64encode((x[i]))
        else:
            encoded[base64encode(str(i))] = x[i]
    print(encoded)
    return encoded


def windows_file_name(file_name='default'):
    x = re.sub(r'[\\/:*?"<>|]', '', file_name)
    x = x[0:30]
    return x


def get_file_size(path):
    return os.path.getsize(path)


def base64encode(s):
    en = (base64.encodebytes(bytes(s, encoding='utf-8')).decode('utf-8')).replace('\n', '')
    return en


def exists(path):
    return os.path.exists(path)


def extract_url_param_dict(full_path_info):
    dic = {}
    param_container = re.findall(r'(?<=\?).*', full_path_info)
    if param_container:
        param = param_container[0]
        params = param.split('&')
        for par in params:
            key, value = par.split('=', maxsplit=1)
            dic[key] = value
    return dic


def extract_url_path_list(full_path_info):
    """
    # on request http://127.0.0.1:8000/test/w/
    # this function /test/w/
    :param full_path_info:
    :return: a list of vars length > 1
    """
    rt = []
    # print(r.path)
    # print(r.get_full_path_info())
    full_path_info = re.findall(r'[^?]*', full_path_info)[0]
    panthers = str(full_path_info).split('/')
    for i in panthers:
        if i:
            rt.append(i)
    return rt


def log_print(s):
    print(s)
    write_string_append('log_ml.txt', f'{datetime.datetime.now()} ... {s}')


def base64decode(s):
    de = (base64.decodebytes(bytes(s, encoding='utf-8')).decode('utf-8'))
    return de


def time_():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def screen_shot(target=''):
    name = ''
    if (target):
        name = target
    else:
        name = str(time.time())
        try:
            os.remove(f'{SCREEN_SHOT_BASE_DIR + str(name)}.png')
        except:
            pass
    ensure_dir(SCREEN_SHOT_BASE_DIR)
    os.system(f'ffmpeg -f gdigrab -i desktop -frames:v 1 {SCREEN_SHOT_BASE_DIR + str(name)}.png')
    return SCREEN_SHOT_BASE_DIR + str(name) + '.png'


def high_light_string(string_highlight, full_str):
    if (full_str):
        return full_str.replace(string_highlight, '\033[1;31;40m' + string_highlight + '\033[0m')
    else:
        return '\033[1;31;40m' + string_highlight + '\033[0m'


def get_screen_string():
    return ''.join(get_screen_string_list())


def get_screen_string_list():
    oo = ocr(screen_shot())
    s = []
    for i in oo['words_result']:
        s.append(i['words'])
    return s


def pic_to_string(pic_path):
    oo = ocr(pic_path)
    s = []
    for i in oo['words_result']:
        s.append(i['words'])
    return ''.join(s)


def region_ocr(l, t, r, b):
    return pic_to_string(region_screenshot(l, t, r, b))


def region_screenshot(l, t, r, b):
    from PIL import Image
    output = 'tmp/quick/0.png'
    ensure_dir('tmp/quick')
    pic = screen_shot()
    im = Image.open(pic)
    region_chat = im.crop((l, t, r, b))
    region_chat.save(output)
    return output


def ocr(file_path):
    """ 读取图片 """

    def get_file_content():
        with open(file_path, 'rb') as fp:
            return fp.read()

    try:
        image = get_file_content()
        """ 调用通用文字识别, 图片参数为本地图片 """
        client.basicGeneral(image)

        """ 如果有可选参数 """
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        return client.basicGeneral(image, options)
    except Exception as e:
        print(e)
        time.sleep(1)
        return ocr(file_path)


def date_string():
    return str(datetime.datetime.now())[:10]


def get_baidu_recommended(keyword):
    url = f'https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&wd={keyword}&req=2&bs={keyword}&csor=2&pwd={keyword}&_={int(time.time() * 1000)}'
    import requests
    import json
    r = requests.get(url)
    # print(r.text)
    return json.loads(r.text)


def get_google_recommended(keyword):
    url = f'https://www.google.com.hk/complete/search?q={keyword}&cp=5&client=psy-ab&xssi=t&gs_ri=gws-wiz&hl=zh-CN&authuser=0&dpr=1.25'
    # url = f'https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&wd={keyword}&req=2&bs={keyword}&csor=2&pwd={keyword}&_={int(time.time() * 1000)}'
    import requests
    import json
    r = requests.get(url)
    # print(r.text)
    return json.loads(r.text[4:])
    # return json.loads(r.text)


def scanf():
    inputs = []
    while True:
        inputs.append(input())
        if inputs[len(inputs) - 1] == '0':
            inputs.pop(len(inputs) - 1)
            break
    s = ''
    for i in inputs:
        s += i + "\n"

    return s[:-1]


class waiting:
    def __init__(self, size):
        import time
        self.start = time.time()
        self.full_task_count = size
        self.progress = 0

    def countup(self):
        self.progress += 1

    def countup_print(self):
        self.countup()
        print((time.time() - self.start) * (self.full_task_count / self.progress))


def read_input():
    return read_string('../input/input.txt')


def random_pick(container, count):
    # group_of_items = {1, 2, 3, 4}  # a sequence or set will work here.
    # num_to_select = 2  # set the number to select here.
    import random
    return random.sample(container, min(len(container), count))


import urllib.parse


def url_encode(s):
    return urllib.parse.quote_plus(s)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def bigCamelClass(bigcamel):
    return bigcamel[0].upper() + bigcamel[1:]


def bigCamel(s):
    rt = ''
    nextUpper = False
    for j in range(len(s)):
        i = str(s[j])
        if (ord(i[0]) > 91 and i != '_'):
            if nextUpper:
                rt += i.upper()
                nextUpper = False
            else:
                rt += i
        elif i == '_':
            nextUpper = True
        else:
            rt += i
            pass
    return rt


def upperString(smallcamel):
    rt = ''
    for i in smallcamel:
        if (i != '_'):
            rt += i.upper()
        else:
            rt += '_'
    return rt


def smallCamel(s):
    rt = ''
    index = 0
    for j in range(len(s)):
        i = str(s[j])
        if (ord(i[0]) < 91):
            if (index != 0):
                rt += '_'
                rt += i.lower()
            else:
                rt += i.lower()
        else:
            rt += i
        index += 1
    return rt


def find_first(string, pattern):
    """
    没找到返回0
    :param string:
    :param pattern:
    :return:
    """
    regList = re.findall(pattern, string)
    if (len(regList) != 0):
        return regList[0]
    else:
        return 0


def random(low, up):
    import random as r
    return r.randint(low, up)


def getAllFileRecursively(path, all_files=[]):
    """
    using '/' instead of '\' is suggested, it's ok to append '/' at the end
    of the file path string
    :param path:
    :param all_files:
    :return:
    """
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            getAllFileRecursively(cur_path, all_files)
        else:
            all_files.append(re.sub(r'//|\\', '/', path + '/' + file))

    return all_files


import pickle


def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def getAllFiles(path):
    list = []
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        list.append(os.path.join(path, file))
    return list


def getAllFiles_NoDirectory(path):
    list = []
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        if not os.path.isdir(os.path.join(path, file)):
            list.append(os.path.join(path, file))
    return list


# remember /a like path is forbidden , change it to a
def path_join(*args):
    path = ''
    index = 0
    for i in args:
        if index > 0:
            if i.startswith('/') or i.startswith('\\'):
                i = i[1:]
        path = os.path.join(path, i)
        index += 1
    return path


def split_long_word_to_lines(word, length):
    ipre = 0
    i = length
    s = ''
    while (i < len(word)):
        s += word[ipre:i]
        s += '\n'
        ipre = i
        i += length
    s += word[ipre:]
    return s


def similarity(s1, s2):
    longer = max(len(s1), len(s2))
    return 1 - (edit_distance(s1, s2) / longer)


def edit_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    states = []
    for i in range(0, m + 1):
        tmp = [i]
        for j in range(1, n + 1):
            tmp.append(0)
        states.append(tmp)
    for i in range(0, n + 1):
        states[0][i] = i

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if (s1[i - 1] == s2[j - 1]):
                states[i][j] = states[i - 1][j - 1]
            else:
                states[i][j] = min(states[i - 1][j - 1], min(states[i - 1][j], states[i][j - 1])) + 1
    return states[m][n]


def write_string(path, str):
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(str)
        f.close()


def write_string_append(path, str):
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(str)
        f.close()


def read_string(path, default_string=''):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            s = f.read()
            f.close()
            return s
    else:
        write_string(path, default_string)
        return default_string


def write_byte(path, str):
    with open(path, 'wb+') as f:
        f.write(str)
        f.close()


def read_byte(path):
    with open(path, 'rb') as f:
        s = f.read()
        f.close()
        return s


def write_obj(path, obj3):
    obj3 = pickle.dumps(obj3)
    with open(path, 'wb')as f:
        f.write(obj3)
        f.close()


def minute(seconds):
    return str(seconds // 60) + '分' + str(seconds % 60) + '秒'


def ffmpegThread(url, save):
    os.system(
        f'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i {url} -c copy -bsf:a aac_adtstoasc {save}.mp4')


from threading import Thread


def ffmpeg(url, save):
    thread_03 = Thread(target=ffmpegThread, args=(url, save,))
    thread_03.start()


def ffmpeg(url):
    thread_03 = Thread(target=ffmpegThread, args=(url, format_windows_name(url),))
    thread_03.start()


def format_windows_name(origin):
    return re.sub('[\/:*?"<>|]', '-', origin)[:50]


def delete_dir(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        else:
            os.remove(dir)


def delete_dir_if_exists(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        else:
            os.remove(dir)


from pathlib import Path


def path_to_filename(path):
    return os.path.basename(path)
    # return re.findall(r'(?<=[\\/]).*?$', path)[0]


def parent_dir(path):
    path = Path(path)
    return path.parent


def get_file_dir(path):
    return os.path.dirname(os.path.realpath(path))


def current_millis_13():
    return int(time.time() * 1000)


from shutil import copyfile


def copy_file(src, dst):
    copyfile(src, dst)


def scanf_lines():
    inputs = []
    while True:
        inputs.append(input())
        if inputs[len(inputs) - 1] == '0':
            inputs.pop(len(inputs) - 1)
            break
    s = ''
    for i in inputs:
        s += i + "\n"
    return s


def read_obj(path):
    f = open(path, "rb")
    try:
        obj = pickle.load(f)
    except:
        pass
    f.close()
    return obj


def ffmpeg_command_mp4_to_mp3(path_from, path_to):
    os.system(f'ffmpeg -i {path_from} -f mp3 {path_to}')
    return path_to


def execCmdWithResult(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def ensure_dir(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass


# def ffmpeg_command_video_merge(folder):
def ffmpeg_command_mp3_mp4_to_pcm(path):
    import os
    os.system(f'ffmpeg -y  -i {path}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {path}.pcm')
    return f'{path}.pcm'


def ffmpeg_command_video_split(path, to_folder, timeGap):
    length = int(re.findall(('[\d]+'), getLength(path))[0])
    i = 1
    ensure_dir(to_folder)
    list = []
    while (i - 1) * timeGap < length:
        file = os.path.join(to_folder, str(i))
        list.append(f'{file}.mp4')
        os.system(f'ffmpeg -ss {(i - 1) * timeGap} -i {path} -c copy -t {timeGap} {file}.mp4')
        i += 1
    return list


def getLength(input_video):
    cmd = 'ffprobe -i %s -show_entries format=duration -v quiet -of csv="p=0"' % input_video
    output = os.popen(cmd, 'r')
    output = output.read()
    return output


def pinyin_list(s):
    import pypinyin
    return pypinyin.lazy_pinyin(s, pypinyin.Style.NORMAL)


def pinyin_str(s):
    rt = ''
    for i in pinyin_list(s):
        rt += i
    rt = re.sub(symbols, '', rt)
    return rt


symbols = r'[,，。、\.\)\(]'

import os
import time
import datetime


def time2localString(time_sj):  # 传入参数
    time_sj /= 1000
    data_sj = time.localtime(time_sj)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", data_sj)  # 时间戳转换正常时间
    return time_str  # 返回日期，格式为str


def currentMillicon():
    t = time.time()
    # print(t)  # 原始时间数据
    # print(int(t))  # 秒级时间戳
    return int(round(t * 1000))
    # print(int(round(t * 1000)))  # 毫秒级时间戳
    # print(int(round(t * 1000000)))  # 微秒级时间戳


def swipeY(a):
    y1 = 500
    y2 = y1 + a
    os.system(f'adb shell input swipe 0 {y2} 0 {y1}')


def tap(x, y):
    os.system(f'adb shell input tap {x} {y}')


def getUi(fileCache):
    if (not os.path.exists(fileCache)):
        os.mkdir(fileCache)
    os.system(f'adb shell uiautomator dump /sdcard/ui.xml')
    os.system(f'adb pull /sdcard/ui.xml {fileCache}')


def back():
    os.system('adb shell input keyevent 4')


def rename(file_path, new_name):
    dir = os.path.dirname(file_path)
    os.rename(file_path, os.path.join(dir, new_name))


def move(file_path, new_path):
    import shutil
    shutil.copy(file_path, new_path)
