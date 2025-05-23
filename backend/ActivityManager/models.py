from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='活动标题')
    content = models.TextField(verbose_name='活动内容')
    poster = models.ImageField(upload_to='event_posters/', verbose_name='海报')
    max_attendees = models.IntegerField(verbose_name='最大人数')
    current_attendees = models.IntegerField(default=0, verbose_name='当前人数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.title

class Signup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='活动')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    data = models.JSONField(default=dict, verbose_name='报名数据')  # 存储动态表单数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'

class Waitlist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='活动')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'

