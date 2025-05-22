from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import *
import qrcode
from  qrcode.main import QRCode
import hashlib
import hmac
from geopy.distance import geodesic
from datetime import timedelta  # 添加timedelta导入
from django.conf import settings  # 添加settings导入


class GenerateQRCodeAPI(APIView):
    '''
    生成二维码用的, 需要event id
    '''
    def post(self, request, event_id):
        event = SignEvent.objects.get(id=event_id)
        secret_key = settings.SECRET_KEY

        # 生成动态令牌
        timestamp = str(int(timezone.now().timestamp()))
        signature = hmac.new(
            secret_key.encode(),
            f"{event_id}|{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()

        # 生成二维码
        qr = QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{event_id}|{timestamp}|{signature}")
        img = qr.make_image(fill_color="black", back_color="white")

        # 保存令牌记录
        token = AttendanceToken.objects.create(
            event=event,
            token=signature,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        img.save(f"media/qrcodes/{token.id}.png")

        return Response({
            "qr_code_url": f"/media/qrcodes/{token.id}.png",
            "expires_at": token.expires_at
        })


class CheckInAPI(APIView):

    '''

    验证二维码， 返回"success"或者"invalid_location"
    '''
    def post(self, request):
        user = request.user
        data = request.data

        # 验证二维码有效性
        try:
            token = AttendanceToken.objects.get(token=data['token'])
            if token.expires_at < timezone.now():
                return Response({"error": "二维码已过期"}, status=400)
        except AttendanceToken.DoesNotExist:
            return Response({"error": "无效的二维码"}, status=400)

        # 验证地理位置
        event_location = (token.event.gps_lat, token.event.gps_lng)
        user_location = (data['latitude'], data['longitude'])
        distance = geodesic(event_location, user_location).meters

        # 创建签到记录
        record = AttendanceRecord.objects.create(
            event=token.event,
            user=user,
            checkin_lat=data['latitude'],
            checkin_lng=data['longitude'],
            is_valid=distance <= token.event.valid_radius,
            token_used=token
        )

        return Response({
            "status": "success" if record.is_valid else "invalid_location",
            "distance": round(distance, 2)
        })
