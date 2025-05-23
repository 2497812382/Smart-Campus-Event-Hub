from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import SignEvent, AttendanceRecord

class AttendanceStatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        await self.channel_layer.group_add(
            f"stats_{self.event_id}",
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        # 实时推送统计更新
        event = SignEvent.objects.get(id=self.event_id)
        total = AttendanceRecord.objects.filter(event=event).count()
        valid = AttendanceRecord.objects.filter(event=event, is_valid=True).count()

        await self.send(text_data=json.dumps({
            "total": total,
            "valid": valid,
            "valid_percent": round((valid / total) * 100, 2) if total else 0
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"stats_{self.event_id}",
            self.channel_name
        )