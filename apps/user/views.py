from django.shortcuts import render
from django.contrib.auth import authenticate, login ,logout #登陆,退出
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  #并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password #对铭文加密
from django.http import HttpResponse, HttpResponseRedirect #定向和重定向
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifiyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin#必须登陆才能访问
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from course.models import Course
from user.models import Banner

#使用邮箱也可以登陆
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  #完成自定义登陆
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            #判断用户是否存在
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            #实例化
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            #用户激活
            user_profile.is_active = False
            #对铭文加密
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕雪在线网站"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


#用户注册激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifiyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


#退出登陆
class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


#用户登陆模块
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        #提交到表单form里面做验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))

                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


#密码找回
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm(request.POST)
        return render(request, "forgetpwd.html", {"forget_form": forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


#用户密码激活
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifiyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")
#密码修改提交
class ModifyPwdView(View):
    def post(self, request):
        #把请求放进表单进行验证
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            #获取页面数据
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            #取出要修改的用户
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致，请重新输入"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


#用户中心

#个人资料
class UserinfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "usercenter-info.html", {})

    def post(self, request):
        #instance=request.user指明修改form、不是新增user
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')




#用户修改头像
class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


#在个人中心修改密码
class UpdatePwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg": "密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


#个人中心发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin, View):

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')

#修改个人邮箱
class UpdateEmailView(LoginRequiredMixin, View):

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifiyRecord.objects.filter(email=email, code=code, send_type='update_email')

        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')




#我的课程
class MyCourseView(LoginRequiredMixin, View):

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })

# 我的收藏
#1.授课机构收藏
class MyFavOrgView(LoginRequiredMixin, View):

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


#2.教师的收藏
class MyFavTeacherView(LoginRequiredMixin, View):

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })

#3.公开课程的收藏
class MyFavCourseView(LoginRequiredMixin, View):

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })

#4.我的消息
class MymessageView(LoginRequiredMixin, View):

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 3, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages": messages,
        })

#首页开发
class IndexView(View):

    def get(self, request):
        #轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })


#错误信息页404 500
from django.shortcuts import render_to_response

def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response