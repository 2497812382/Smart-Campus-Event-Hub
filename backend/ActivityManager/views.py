from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event, Signup, Waitlist
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import permissions



class EventCreateView(APIView):
    # permission_classes = [permissions.AllowAny]

    permission_classes = [IsAuthenticated]
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        poster = request.FILES.get('poster')
        max_attendees = int(request.data.get('max_attendees', 100))

        event = Event.objects.create(
            title=title,
            content=content,
            poster=poster,
            max_attendees=max_attendees
        )
        return Response({'id': event.id}, status=201)

class SignupView(APIView):
    # permission_classes = [permissions.AllowAny]

    permission_classes = [IsAuthenticated]
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            if event.current_attendees >= event.max_attendees:
                return Response({'message': '活动已满员'}, status=409)

            Signup.objects.create(
                event=event,
                user=request.user,
                data=request.data
            )
            event.current_attendees += 1
            event.save()
            return Response({'message': '报名成功'})
        except ObjectDoesNotExist:
            return Response({'message': '活动不存在'}, status=404)

class WaitlistView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            if event.current_attendees == event.max_attendees:
                Waitlist.objects.create(event=event, user=request.user)
                return Response({'message': '已加入候补队列'})
            else:
                return Response({'message': '活动未满员'}, status=400)
        except ObjectDoesNotExist:
            return Response({'message': '活动不存在'}, status=404)


class EventDetailView(APIView):

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        # 返回活动详情
        data = {
            'id': event.id,
            'title': event.title,
            'content': event.content,
            'poster': event.poster.url if event.poster else None,
            'max_attendees': event.max_attendees,  # 最大参与人数
            'current_attendees': event.current_attendees,  # 当前报名人数
        }
        return JsonResponse(data)