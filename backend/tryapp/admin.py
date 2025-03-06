# 示例：api/admin.py
from django.contrib import admin
from .models import Task  # 确保导入了 Task 模型
admin.site.register(Task)

