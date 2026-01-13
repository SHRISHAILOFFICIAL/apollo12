from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from exams.models import Announcement


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_announcements(request):
    """List all active announcements"""
    announcements = Announcement.objects.filter(is_active=True)
    
    data = []
    for announcement in announcements:
        data.append({
            'id': announcement.id,
            'title': announcement.title,
            'message': announcement.message,
            'type': announcement.announcement_type,
            'created_at': announcement.created_at.strftime('%B %d, %Y'),
        })
    
    return Response({'announcements': data})
