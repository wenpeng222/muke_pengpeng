# _*_ coding: utf-8 _*_

#__author__ = 'root'
#__date__ = '2018/12/31 15:02'


import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifiyRecord, UserProfile, Banner



# 显示主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "鹏鹏教学后台管理系统"
    site_footer = "鹏鹏教学网"
    menu_style = "accordion"

'''
class UserProfileAdmin(object):
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']  # 显示列
    search_fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']  # 搜索
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']  # 过滤器
xadmin.site.register(UserProfile, UserProfileAdmin)
'''

class EmailVerifiyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']  #显示列
    search_fields = ['code', 'email', 'send_type']              #搜索
    list_filter = ['code', 'email', 'send_type', 'send_time']   #过滤器


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 显示列
    search_fields = ['title', 'image', 'url', 'index']              # 搜索
    list_filter = ['title', 'image', 'url', 'index', 'add_time']   # 过滤器


xadmin.site.register(EmailVerifiyRecord, EmailVerifiyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
