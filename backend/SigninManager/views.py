from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import *
import qrcode
from  qrcode.main import QRCode
import hashlib
import hmac
from datetime import timedelta  # 添加timedelta导入
from django.conf import settings  # 添加settings导入
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
import  os
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class CreateEventAPI(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        required_fields = ['name', 'start_time', 'duration_minutes']
        if not all(field in request.data for field in required_fields):
            return Response({"error": "缺少必填字段"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            duration_minutes = int(request.data['duration_minutes'])
            start_time = timezone.make_aware(
                timezone.datetime.fromisoformat(request.data['start_time'])
            )
            end_time = start_time + timedelta(minutes=duration_minutes)
            event = SignEvent.objects.create(
                title=request.data['name'],
                start_time=timezone.make_aware(
                    timezone.datetime.fromisoformat(request.data['start_time'])
                ),
                end_time = end_time,
                organizer=request.user
            )
            return Response({"id": event.id}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": f"参数格式错误: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        # GenerateQRCodeAPI中修改二维码内容
        verification_url = f"{settings.DOMAIN}/SigninManager/checkin/?event_id={event_id}&timestamp={timestamp}&signature={signature}"
        qr.add_data(verification_url)
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(qr_dir, exist_ok=True)  # 自动创建目录
        img = qr.make_image(fill_color="black", back_color="white")

        # 保存令牌记录
        token = AttendanceToken.objects.create(
            event=event,
            token=signature,
            expires_at= event.end_time,
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

    # 为GET请求渲染HTML，POST返回JSON
    def get_renderers(self):
        # GET请求使用模板渲染器
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        # 其他请求使用JSON渲染器
        return [JSONRenderer()]

    def get(self, request):
        """扫码后的GET请求返回HTML页面"""
        return Response(
            template_name='checkin.html',  # HTML模板
            content_type='text/html',  # 强制指定类型
            status=200
        )

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


        # 创建签到记录
        record = AttendanceRecord.objects.create(
            event=token.event,
            user=user,
            is_valid=True,
            token_used=token
        )


        return Response({
            "success": record.is_valid,
            "message": "签到成功" if record.is_valid else "签到失败",
            "event_id": token.event.id,
            "user_id": request.user.id
        }, status=status.HTTP_200_OK)

