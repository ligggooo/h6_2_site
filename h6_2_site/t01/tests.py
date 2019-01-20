from django.test import TestCase

# Create your tests here.

from django.core.mail import send_mail
from threading import Thread
host_email = 'xx0@qq.com'
t = Thread(target=send_mail,args=
    ('这时条测试邮件','内容',host_email,['xx1@qq.com','xx2@qq.com']))
t.start()