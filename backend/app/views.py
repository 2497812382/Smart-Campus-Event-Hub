from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .models import EventParticipation
import matplotlib.font_manager as fm


def create_img(request):

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    records = EventParticipation.objects.filter(date__range=[start_date, end_date]).order_by('date')

    if not records:
        return JsonResponse({'error': 'No data to generate chart.'}, status=400)

    dates = [record.date.strftime('%Y-%m-%d') for record in records]
    participation_rates = [record.participation_rate for record in records]

    try:
        # 尝试加载系统中可用的中文字体
        font_path = fm.findfont(fm.FontProperties(family=['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']))
        font = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font.get_name()
    except:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    # 生成图表
    plt.figure(figsize=(10, 5))
    plt.plot(dates, participation_rates, marker='o')
    plt.title('近7日签到率')
    plt.xlabel('日期')
    plt.ylabel('签到率 (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 确保static目录存在
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # 保存图片
    img_name = 'participation_rate.png'
    img_path = os.path.join(static_dir, img_name)
    plt.savefig(img_path)
    plt.close()

    img_url = f'{settings.STATIC_URL}{img_name}'


    return JsonResponse({'image_url': img_url})