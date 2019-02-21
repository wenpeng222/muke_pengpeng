# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve#处理media文件
from MxOnline.settings import MEDIA_ROOT, STATIC_ROOT #media路径

from user.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, IndexView
from organization.views import OrgView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #首页
    url('^$', IndexView.as_view(), name="index"),
    #用户登陆
    url('^login/$', LoginView.as_view(), name="login"),

    #退出
    url('^logout/$', LogoutView.as_view(), name="logout"),
    #注册页面
    url('^register/$', RegisterView.as_view(), name="register"),
    #图片验证码的配置
    url(r'^captcha/', include('captcha.urls')),
    #用户激活
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    #密码找回
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    #课程列表url配置
    url(r'^course/', include('course.urls', namespace="course")),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #配置debug=False下的静态文件处理函数
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    #用户中心
    url(r'^users/', include('user.urls', namespace="users")),
    # 富文本编辑器url
    #url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 全局404页面配置
handler404 = 'user.views.page_not_found'
# 全局500页面配置
handler500 = 'user.views.page_error'