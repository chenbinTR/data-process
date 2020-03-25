# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import email.MIMEBase
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import traceback
import time
import mimetypes
import os

# 第三方 SMTP 服务
MAIL_FROM = 'chenbin@uzoo.cn'
MAIL_HOST = 'smtp.exmail.qq.com'
MAIL_PORT = 465
MAIL_USER = 'chenbin@uzoo.cn'
MAIL_PASS = 'wd6ghVAzBymfEExc'
# MAIL_PASS = 'TUring2013'
MAIL_TO = ['chenbin@uzoo.cn']

def send_mail(subject, content='', content_type='plain', attachments=[], to=MAIL_TO):
    main_msg = MIMEMultipart()
    main_msg['Subject'] = Header(subject, 'utf-8')
    main_msg['From'] = Header(MAIL_FROM, 'utf-8')
    main_msg['To'] = Header(', '.join(to), 'utf-8')

    text_message = MIMEText(content + '\n', content_type, 'utf-8')
    main_msg.attach(text_message)

    for attachment in attachments:
        data = open(attachment, 'rb')
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        file_message = MIMEBase.MIMEBase(maintype, subtype)
        file_message.set_payload(data.read())
        data.close()
        encoders.encode_base64(file_message)
        basename = os.path.basename(attachment)
        # file_message.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
        main_msg.attach(file_message)

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(MAIL_HOST, MAIL_PORT)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(MAIL_FROM, to, main_msg.as_string())

    except smtplib.SMTPException as e:
        traceback.print_stack()
        print(e)
        pass

# def asyn_send_mail(subject, content='', attachments=[]):
#     thread.start_new_thread(send_mail, (subject, content, attachments))

if __name__ == '__main__':
    # asyn_send_mail("测试", "收到邮件了, 有附件呀～")
    send_mail("测试", "收到邮件了, 有附件呀～\n", ['Q:\\log.txt'])
    print('send mail....')
    # time.sleep(15)
