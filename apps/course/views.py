# _*_ coding: utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.http import HttpResponse
from django.db.models import Q  #并集

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


#公开课页面
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        #热门机构排序
        hot_courses = Course.objects.all().order_by("click_nums")[:3]

        #课程全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        # 课程列表排序   -表示降序排列
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "student":
                all_courses = all_courses.order_by("-student")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses

        })


#课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()

        #收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        #课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


#课程章节信息页面
class CourseInfoView(LoginRequiredMixin ,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #点击课程+1
        course.student += 1
        course.save()

    # 获取学过该用户学过其他的所有课程
        #查询用户是否已经关联了该课程
        user_courses_ralate = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses_ralate:
            user_course_ralate = UserCourse(user=request.user, course=course)
            user_course_ralate.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_courses = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html',  {
            "course": course,
            "course_resources": all_courses,
            "relate_courses": relate_courses,

        })

#课程评论信息
class CommentsView(View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            'all_comments':all_comments,
        })


#用户添加课程评论
class AddCommentsView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id=int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


#视频播放页面
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        course.student += 1
        course.save()
        #查询用户是否已经关联了该课程
        user_courses_ralate = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses_ralate:
            user_course_ralate = UserCourse(user=request.user, course=course)
            user_course_ralate.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_courses = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            "course": course,
            "course_resources": all_courses,
            "relate_courses": relate_courses,
            "video": video,
        })
