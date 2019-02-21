# _*_ coding: utf-8 _*_

import xadmin

from .models import Course, Lesson, Video, CourseResource
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'student', 'fav_nums', 'image', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']  #显示列
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']             #搜索
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'student', 'fav_nums', 'image', 'click_nums', 'add_time']   #过滤器
    ordering = ['-click_nums']      #排序
    readonly_fields = ['fav_nums']   #只读
    list_editable = ['name', 'desc', 'detail', 'degree'] #修改名称
    exclude = ['click_nums']        #隐藏 和只读冲突，故字段不能重复
    refresh_times = [3, 5]  #刷新

    #在CourseAdmin中使用inlines添加上面两个的方法
    inlines = [LessonInline, CourseResourceInline]    #增加章节和课程资源
    #富文本编辑器
    #style_fields = {"detail": "ueditor"}

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 显示列
    search_fields = ['course', 'name']             # 搜索
    list_filter = ['course', 'name', 'add_time']   # 过滤器


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 显示列
    search_fields = ['lesson', 'name']             # 搜索
    list_filter = ['lesson', 'name', 'add_time']   # 过滤器


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 显示列
    search_fields = ['course', 'name', 'download']             # 搜索
    list_filter = ['course', 'name', 'download', 'add_time']   # 过滤器



xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

