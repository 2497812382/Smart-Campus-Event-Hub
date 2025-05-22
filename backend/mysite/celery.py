import os
from celery import Celery


# 设置Django默认环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('SmartCampus')

# 使用Django配置的命名空间
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有应用中的tasks.py
app.autodiscover_tasks()

# 定时任务配置（示例）
app.conf.beat_schedule = {
    'clean-expired-qrcodes': {
        'task': 'SigninManager.tasks.expire_qr_tokens',
        'schedule': 300.0,  # 每5分钟执行
        'options': {'queue': 'periodic'}
    },
}