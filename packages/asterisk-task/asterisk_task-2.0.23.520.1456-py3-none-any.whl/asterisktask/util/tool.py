from datetime import datetime
from colorama import init
import logging.config
import sys
from deprecated.sphinx import deprecated
import warnings


# 打印出告警信息
warnings.filterwarnings("always")

# 解决Window环境中打印颜色问题
init(autoreset=True)

if  __name__ == "__main__":
    print('\033[31m%s\033[0m' % '本段代码必须从应用主入口导入执行。退出!')
    sys.exit(1)

class classproperty(property):
    '''
    类属性装饰器
    '''
    def __get__(self, cls, owner):
         return classmethod(self.fget).__get__(None, owner)()
class AsteriskContext():
    '''
    只是用于临时增加保存在内存中的上下文
    '''
    
    __keeper = {}

    __ison = True

    @classmethod
    def add_key(cls,name:str,kwargs:dict,alive=0) -> None:
        '''
        增加字典到内存中（类似web应用的session/cookie），如不设置alive时间，将在一定时间后被GC回收。
        如果有些定时任务，需要内存的变量的数据，需要制定alive时间
        Args
            name(str):名称，用于将来取用
            kwargs(dict):存储的内容，用dict格式，可以存储任意数据格式
            alive(int): 单位为秒，若果大于0，那么将启动一个线程保持该数据激活不少N秒
        '''
        from threading import Thread
        #  如果是已经存在的上下文信息，就不另外开线程
        is_new_element = True if  cls.get_content(name) is None else False
        cls.__keeper[name] = {}
        cls.__keeper[name]['content'] = kwargs if kwargs is not None else cls.__keeper[name].get('content') #防止以None添加相同key时出现报错
        # dprint(kwargs) #调试完成，暂时去掉
        cls.__keeper[name]['alive'] = alive if kwargs is not None else cls.__keeper[name].get('alive') #防止以None添加相同key时出现报错
        if alive > 0 and is_new_element:
            t = Thread(target=cls.__keep_alive,args=[name],name=f'context_{name}')
            t.daemon = True
            t.start()
    @classmethod
    def __keep_alive(cls,name:str) -> None:
        '''
        在线程中保持上下文信息活动状态
        Args:
            name(str):上下文的名称
            alive(int):保持活动的秒数
        '''
        from time import sleep
        i =0 
        while  cls.__ison and i < cls.__keeper[name]['alive']:
            if cls.get_content(name) is not None:
                i += 1
                sleep(1)
            else:
                print()
                dprint(f'[{name}]的内存变量出错，可能被GC回收。')
                print_prompt()
                i = cls.__keeper[name]['alive']
        del(i)
        if cls.get_content(name) is not None: # 加一个判断，解决在待机很久之后其实context已经回收的的问题
            cls.__keeper.pop(name)

    @classmethod
    def ison(cls,ison = False) -> None:
        '''
        设置类状态，当__ison为False时，__keep_alive 将自动停止
        Args:
            ison(bool):是否保持context
        '''
        cls.__ison = ison

    
    @classmethod
    def get_content(cls,name:str) -> dict:
        '''
        以name取得内容
        Args:
            name(str): 内存上下文的名称
        Returns:
            dict :上下文内容
        '''
        try:
            if cls.__keeper.get(name):
                # if cls.__keeper[name].get('alive') >=0: #判断不需要这条if
                return cls.__keeper.get(name).get('content')
            else:
                return None
        except KeyError:
            return None

    @classmethod
    def remove_content(cls,name:str) -> None:
        '''
        删除以此name的内存内容。如果上下文已经被gc回收，再删除会出警告
        Args:
            name(str): 内存上下文的名称
        '''
        try:
            cls.__keeper.pop(name)
        except KeyError:
            wprint(f'上下文[{name}]已被系统回收。')

    @classmethod
    def keys(cls):
        '''
        取得所有的keys，仅供调试使用
        '''
        return cls.__keeper.keys()

def random_dic(dicts) -> dict:
    '''
    将字典中顺序打乱
    Args
        dicts(dict):需要打乱顺序的字典
    Returns
        dict: 打乱后的字典
    '''
    import random
    dict_key_ls = list(dicts.keys())
    random.shuffle(dict_key_ls)
    new_dic = {}
    for key in dict_key_ls:
        new_dic[key] = dicts.get(key)
    return new_dic

def get_logger()-> logging.Logger:
    '''
    根据AppConfig设置log基本配置，并返回logger对象
    Returns
        logger: 日志实例
    '''
    from asterisktask.setup.setting import AppConfig
    
    import os
    # 根据AppConfig的设置拼接日志文件名
    fn = '{}.log'.format(datetime.now().strftime(AppConfig['log']['log_file_name']))
    # 使用join的目的是适配不同操作系统
    # 载入日志的配置文件
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'setup/log.config'))
    logger = logging.getLogger('MainLogger')
    try:
        fh = logging.FileHandler(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path'],fn),'a','utf-8')
    except FileNotFoundError:
        try:
            os.mkdir(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path']))
            fh = logging.FileHandler(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path'],fn) )
        except:
            raise FileNotFoundError
        
    fh.setFormatter(logging.Formatter(AppConfig['log']['log_format']))
    logger.addHandler(fh)
    return logger


def success_print(txt,header=True,*args,**kwargs) -> None:
    '''
    成功信息打印，绿色
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[成功信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = '[成功信息]' if header else ''
    print(f'\033[32m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().info(f'{s}{txt}')
def error_print(txt,header=True,*args,**kwargs):
    '''
    错误信息打印，红色
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[成功信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = '[错误信息]' if header else ''
    print(f'\033[31m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().error(f'{s}{txt}',exc_info=True, stack_info=True,)
@deprecated(reason='将逐步提供多语言header，将由iprint()代替',version='1.4.0') 
def info_print(txt,header=True,*args,**kwargs) -> None:
    '''
    输出信息打印，蓝色。注：将在1.4.0后逐步废弃
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[运行信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    warnings.warn('将逐步提供多语言header，将由iprint()代替',DeprecationWarning) # 稍后版本也将废弃
    s = '[运行信息]:' if header else ''
    print(f'\033[36m{s}{txt}\033[0m',*args,**kwargs)
    if header:
        get_logger().info(f'{s}{txt}')

def iprint(txt,header:str='运行信息',*args,**kwargs) -> None:
    '''
    输出信息打印，蓝色
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[运行信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = f'[{header}]' if header else ''
    print(f'\033[36m{s}{txt}\033[0m',*args,**kwargs)
    if header:
        get_logger().info(f'{s}{txt}')
@deprecated(reason='将逐步提供多语言header，将由wprint()代替',version='1.4.0')
def warn_print(txt:str,header=True,*args,**kwargs) -> None:
    '''
    警告信息打印，黄色
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[警告信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    warnings.warn('将逐步提供多语言header，将由wprint()代替',DeprecationWarning)
    s = '[警告信息]:' if header else ''
    print(f'\033[33m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().warning(f'{s}{txt}')
def wprint(txt:str,header:str='警告信息',*args,**kwargs) -> None:
    '''
    警告信息打印，黄色
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[警告信息]的文字，默认为'警告信息'
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = f'[{header}]:' if header else ''
    print(f'\033[33m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().warning(f'{s}{txt}')
@deprecated(reason='将逐步提供多语言header，将由dprint()代替',version='1.7.7')
def debug_print(txt,header=True,*args,**kwargs) -> None:
    '''
    当配置文件中AppConfig的debug属性为true时打印，否则不打印
    按照以下格式:
    [调试信息] [{参数名/函数名}] :{value}
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[调试信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    from asterisktask.setup.setting import AppConfig
    import inspect
    if AppConfig['debug']:
        s = "[调试信息]:" if header else ''
        txt_name = 'Unknown' # 默认值
        txt_name = inspect.stack()[1][4][0].split("(")[1].split(")")[0] # 获取参数名称或者函数名称        
        print(f'\033[35m{s}[{txt_name}] => {txt}\033[0m',*args,**kwargs)
        get_logger().debug(f'{s}[{txt_name}] => {txt}')

def dprint(txt,header:str='调试信息',*args,**kwargs) -> None:
    '''
    当配置文件中AppConfig的debug属性为true时打印，否则不打印
    按照以下格式:
    [调试信息] [{参数名/函数名}] :{value}
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[调试信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    from asterisktask.setup.setting import AppConfig
    import inspect
    if AppConfig['debug']:
        s = f"[{header}]:" if header else ''
        txt_name = 'Unknown' # 默认值
        txt_name = inspect.stack()[1][4][0].split("(")[1].split(")")[0] # 获取参数名称或者函数名称        
        print(f'\033[35m{s}[{txt_name}] => {txt}\033[0m',*args,**kwargs)
        get_logger().debug(f'{s}[{txt_name}] => {txt}')

def cmd_help() -> None:
    '''
    把AppConfig.json中任务（taak）以作为命令，以表格展示出来
    '''
    import prettytable as pt
    from asterisktask.setup.setting import AppConfig
    iprint(f"欢迎使用{AppConfig['app_name']}命令行工具!请参考如下命令:")
    tb = pt.PrettyTable()
    tb.field_names = ["命令","说明","类型"]
    tb.add_row(["help","命令帮助","系统命令"])
    tb.add_row([":q 或 exit 或 exit()","退出程序","系统命令"])
    tb.add_row(["version 或者 version()",f"显示{AppConfig['app_name']}的版本信息","系统命令"])
    tb.add_row(["ctrl + C","中断正在执行的任务","系统命令"])
    tb.add_row(["start_schedule_tasks","开启定时任务","系统命令"])
    tb.add_row(["stop_schedule_tasks","关闭定时任务","系统命令"])

    for task_item in AppConfig['tasks']:
        tb.add_row([task_item,AppConfig['tasks'][task_item]['description'],'自定义'])
        
    from asterisktask.lib.taskcontrol import TaskPool
    from asterisktask.lib.task import AsteriskTask
    for task_name in TaskPool.items:
        task_class = TaskPool.get_task(task_name)
        if AsteriskTask in task_class.__mro__:
            if task_class.is_sub_task:
                tb.add_row([f'* {task_name}',task_class.__dict__.get('description'),'自定义（V2），子任务不可单独启动运行'])
            else:
                tb.add_row([task_name,task_class.__dict__.get('description'),'自定义（V2）'])
            

        # iprint(tb,header=False)
    iprint(tb,header=False)

def print_logo(with_title=False,with_copyrights=False,with_version=False) -> None:
    '''
    以info_print的方式方式打印logo以及相关信息
    Args
        with_title(bool):是否一起打印标题头，默认为否
        with_copyrights(bool):是否一起打印版权信息，默认为否
        with_version(bool):是否一起打印版本信息，默认为否
    '''
    # info_print(AppConfig['VI']['titles']['for_gitee'])
    from asterisktask.setup.setting import AppConfig
    if with_title:
        iprint(AppConfig['title_text'],header=False)
    iprint(AppConfig['logo_text'],header=False)
    
    if with_copyrights:
        import time
        this_year = time.strftime('%Y',time.localtime())
        author = AppConfig['author']
        iprint(f' 基于Asterisk-Task框架V{AppConfig["version"]}构建。 © 版权所有  {author} 2018-{this_year}',header=False)
    if with_version:
        version()
        print()
        print() # 增加空行

def version() -> None:
    '''
    打印Submarine的版本信息
    '''
    from asterisktask.setup.setting import AppConfig
    iprint(f" {AppConfig['app_name']} V{AppConfig['app_version']} 由{AppConfig['app_author']}编写并维护 {AppConfig['app_email']}",header=False)
def print_prompt() -> None:
    '''
    在command模式下打印提示符
    提示符可在AppConfig.json中设置
    '''
    from asterisktask.setup.setting import AppConfig
    print(AppConfig['prompt'],end='',flush=True)
'''
以下列表是gitee http api返回json的text中需要进行url编码的检查字符串
'''    
json_escape_list = ['https://','http://','/']
def json_escape(txt:str) -> str:
    '''
    将json字符串中的url进行编码，以避免出现protocal unknown的错误
    Args:
        txt(str):需要进行检查替换url编码的字符串
    Returns:
        str: 检查替换url编码后的字符串
    '''
    from urllib.parse import quote
    for s in json_escape_list:
        txt = txt.replace(s,quote(s,safe=''))
    return txt

class AsteriskSinDout():
    
    
    '''
    加密类提供了加密和解密的方法
    在初始化类时需要提供加密和解密的密钥
    密钥为字符串，不能为“-_”，初始化方法会自动进行密钥处理
    加密方法使用了哈希+DES的算法。
    '''


    def __init__(self, key:str):
        '''
        加密用的key字符串，一般为字母和数字数字
        Args:
            key(str): a-z,A-Z,0-9

        '''
        
        # key的字符串长度不能超过22个字符，否则，进行左右11个字符截取
        if not self.__valid_key(key):
            from asterisktask.error.util import InvalidEncriptionKey
            raise InvalidEncriptionKey()
        k_b = len(key)
        if k_b == 22:
            self.key = key+'=='
        elif k_b > 11:
            self.key = key[:11] + key[-11:] + '=='
        else:
            self.key = key + (22-k_b) * '0' + '=='


    
    def __valid_key(self, key:str) -> bool:
        """
        Validate the key format using regular expression.
        Args:
            key(str): The key to be validated.
        Returns:
            bool: True if the key format is valid, False otherwise.
        """
        import re
        pattern = r'^[a-zA-Z0-9]+$'
        if re.match(pattern, key):
            return True
        return False
    

    def encrypt(self, s:str)->str:
        """
        先哈希后DES加密，以base64输出字符串
        Args：
            s(str):需要加密的字符串
        Return:
            str:加密后的字符串
        """
        from pyDes import des, CBC, PAD_PKCS5
        import hashlib
        import base64
        key_f = base64.b64decode(self.key)[:8]
        key_b = base64.b64decode(self.key)[8:]
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        m_body = m.digest()
        data = str(m_body) + str(s)
        KEY = key_f
        IV = key_b
        k_des = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
        des_date = k_des.encrypt(data)
        _final = base64.b64encode(des_date)
        return bytes.decode(_final)

    def descrypt(self, s:str)->str:
        """
        encrypt对应的解密方法
        Args：
            s(str):加密后的字符串
        Returns:
            str: 解密后的字符串
        """
        from pyDes import des, CBC, PAD_PKCS5
        import base64

        decode_b64 = base64.b64decode(bytes(s, encoding='utf8') )
        key_f = base64.b64decode(self.key)[:8]
        key_b = base64.b64decode(self.key)[8:]
        KEY = key_f
        IV = key_b
        k_des = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
        decode_des = k_des.decrypt(decode_b64)
        i = decode_des.find(b"'",2) + 1
        return bytes.decode(decode_des[i:])