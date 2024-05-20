'''
把的smtp进行再次封装，以便简化操作
'''
from email.mime.multipart import MIMEMultipart
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from asterisktask.error.util import EmailNotValidError
import re
from asterisktask.util.tool import error_print, wprint
class MosMailMsg():
    '''
    为Submarine封装邮件消息
    '''
    

    def __init__(self,from_eamil_address,from_name:str='系统管理员') -> None:
        '''
        初始化
        Args:
            from_email_address(str):发送者的邮件地址
        '''
        self.__to_addr = []
        self.__from_addr = from_eamil_address
        self.msg = MIMEMultipart()
        self.add_from_addr(from_name,self.__from_addr)
        
    @property
    def from_addr(self) -> str:
        '''
        邮件的发件人地址信息
        Returns
            str: 邮件发件人的信息
        '''
        return self.__from_addr
    @property
    def to_addr(self) -> list:
        '''
        Returns
            list    收件人地址list
        '''
        return self.__to_addr
    def add_to_addr(self,name:str,email:str) -> None:
        '''
        把收件人加到邮件中
        Args
            name(str):收件人名称
            email(str):收件人邮件地址

        '''
        self.__add_addr(name,email,'to')
        self.__to_addr.append(email)
    def add_cc_addr(self,name:str,email:str) -> None:
        '''
        把抄送人加到邮件中
        Args
            name(str):抄送人名称
            email(str):抄送人邮件地址

        '''
        self.__add_addr(name,email,'cc')
        self.__to_addr.append(email)
    
    def add_bcc_addr(self,name:str,email:str) ->None:
        '''
        把暗送人加到邮件中
        Args
            name(str):暗送人名称
            email(str):暗送人邮件地址

        '''
        self.__add_addr(name,email,'bcc')
        self.__to_addr.append(email)

    def add_reply_addr(self,name:str,email:str) -> None:
        '''
        把回复人加到邮件中
        Args
            name(str):回复人名称
            email(str):回复人邮件地址

        '''
        self.__add_addr(name,email,'bcc')

    def add_from_addr(self,name:str,email:str) -> None:
        '''
        把发件人加到邮件中
        Args
            name(str):发件人名称
            email(str):发件人邮件地址

        '''
        self.__add_addr(name,email,'from')

    def __add_addr(self,name:str,email:str,add_type = 'from')-> None:
        '''
        把相关人加到邮件中
        Args
            name(str):相关人名称
            email(str):相关人邮件地址

        '''
        if self.__validate_email(email):
            if str.lower(add_type) == 'to':
                self.msg['To'] = self.__format_addr('{} <{}>'.format(name,email))
            elif str.lower(add_type) == 'cc':
                self.msg['Cc'] = self.__format_addr('{} <{}>'.format(name,email))
            elif str.lower(add_type) == 'bcc':
                self.msg['Bcc'] = self.__format_addr('{} <{}>'.format(name,email))
            elif str.lower(add_type) == 'replyto':
                self.msg['Reply-To'] == self.__format_addr('{} <{}>'.format(name,email))
                self.mdg['Return-Path'] = self.__format_addr('{} <{}>'.format(name,email))
            else:
                self.msg['From'] = self.__format_addr('{} <{}>'.format(name,email))
        else:
            raise EmailNotValidError(email)

    def add_title(self,title:str) -> None:
        '''
        给邮件增加标题
        Args
            title(str):邮件标题
        '''
        self.msg['Subject'] = Header(title, 'utf-8').encode()
    def add_content(self,content:str,is_html=False) -> None:
        '''
        给邮件增加内容
        Args
            content(str):邮件内容，可以是纯文本，或者html
            is_html(bool)：plain / html的标记
        '''
        self.msg.attach(MIMEText(content, 'html' if is_html else 'plain', 'utf-8'))


    def __format_addr(self,s):
        '''
        给邮件地址信息格式美化
        Args
            s(str): 按照{} <{}>传进来的邮件地址信息
        '''
        return formataddr(parseaddr(s))

    def __validate_email(self,email:str) -> bool:
        '''
        验证邮件地址
        Args
            email(str):邮件地址
        Returns
            bool:如果地址合法返回True
        '''
        return True if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", \
            email) != None else False
    def as_string(self) -> str:
        '''
        将邮件对象返回string
        '''
        return self.msg.as_string()
class MosMail():

    def __init__(self,smtp_server:str,smtp_port:int,smtp_username:str,smtp_password:str) -> None:
        '''
        初始化时实例化smtp对象，并读取AppConfig.json中设置，连接服务器，并登陆
        Args:
            smtp_server(str):smtp服务器地址，域名或者ip地址
            smtp_port(int):smtp服务器的端口号
            smtp_username(str):smtp服务器用户名
            smtp_password(str):smtp服务器密码
        '''
        self.smtp_obj = smtplib.SMTP_SSL(smtp_server,smtp_port) 
        self.smtp_obj.login(smtp_username,smtp_password) 

    def sendmail(self,msg:MosMailMsg) -> None:
        '''
        将email msg发送出去
        Args
            msg(MosMailMsg):需要发送的email msg实例
        '''
        try:
            self.smtp_obj.sendmail(msg.from_addr, msg.to_addr, msg.as_string())

        except EmailNotValidError as em:
            wprint('email 地址无效，邮件未发送')
            error_print(em)
        except smtplib.SMTPServerDisconnected:
            self.smtp_obj.connect()
            self.smtp_obj.sendmail(msg.from_addr, msg.to_addr, msg.as_string())
        except smtplib.SMTPException as e:
            error_print(e)

        

    def __del__(self) -> None:
        '''
        对象解构时断开smtp的连接
        '''
        if self.smtp_obj:
            self.smtp_obj.quit()
            self.smtp_obj.close
        
        

                
    