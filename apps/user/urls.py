# _*_ coding: utf-8 _*_
from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView ,UpdateEmailView, MyCourseView ,MyFavOrgView, MyFavTeacherView, MyFavCourseView, MymessageView

urlpatterns = [
    # 用户中心
    #个人资料页
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),
    #用户上传头像
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    #用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    #我的课程页
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    #我的收藏页
    #我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    #我收藏的教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    #我收藏的公开课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    #我的消息
    url(r'^mymessage/$', MymessageView.as_view(), name="mymessage"),

]