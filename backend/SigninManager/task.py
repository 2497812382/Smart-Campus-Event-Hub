from celery import shared_task
from django.utils import timezone

@shared_task
def expire_qr_tokens():
    from .models import AttendanceToken
    expired = AttendanceToken.objects.filter(
        expires_at__lt=timezone.now()
    ).delete()
    return f"已清理{expired}个过期二维码"