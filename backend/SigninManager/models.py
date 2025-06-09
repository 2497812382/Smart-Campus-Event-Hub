from django.db import models
from django.contrib.auth import get_user_model  # 获取当前项目的用户模型


class SignEvent(models.Model):
    # 活动标题，最大长度200字符
    title = models.CharField(max_length=200)

    # 活动组织者，外键关联用户模型，级联删除（当用户被删除时，其组织的活动也会删除）
    organizer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # 活动开始时间，存储精确到秒的日期时间
    start_time = models.DateTimeField()

    # 活动结束时间，存储精确到秒的日期时间
    end_time = models.DateTimeField()

    # 文字描述的活动地点（如：第一教学楼101室）
    location = models.CharField(max_length=200)


class AttendanceToken(models.Model):
    # 关联的外键活动，级联删除（活动删除时相关令牌自动删除）
    event = models.ForeignKey(SignEvent, on_delete=models.CASCADE)

    # 加密的签到令牌字符串（唯一值），用于验证签到请求的合法性
    token = models.CharField(max_length=128, unique=True)

    # 二维码图片字段，上传到media/qrcodes/目录，自动存储文件路径
    qr_code = models.ImageField(upload_to='qrcodes/')

    # 令牌生成时间，自动记录创建时的时间（不可修改）
    generated_at = models.DateTimeField(auto_now_add=True)

    # 令牌过期时间，需要手动设置的时间点
    expires_at = models.DateTimeField()


class AttendanceRecord(models.Model):
    # 关联的外键活动，级联删除（活动删除时签到记录自动删除）
    event = models.ForeignKey(SignEvent, on_delete=models.CASCADE)

    # 签到用户，外键关联用户模型，级联删除（用户删除时其签到记录删除）
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # 签到时间，自动记录记录创建时的时间（不可修改）
    checkin_time = models.DateTimeField(auto_now_add=True)


    # 有效性标志（布尔值），True表示在有效半径内的合法签到
    is_valid = models.BooleanField(default=False)

    # 使用的外键令牌，级联删除（令牌删除时相关签到记录自动删除）
    token_used = models.ForeignKey(AttendanceToken, on_delete=models.CASCADE)