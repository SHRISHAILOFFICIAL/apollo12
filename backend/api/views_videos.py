from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from exams.models import VideoSolution


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_videos(request):
    """List all available video solutions grouped by topic (PRO only)"""
    
    # Check if user has PRO access
    try:
        has_pro = request.user.profile.is_pro if hasattr(request.user, 'profile') else False
    except:
        has_pro = False
    
    if not has_pro:
        return Response({
            'error': 'PRO membership required',
            'is_pro': False,
            'topics': {}
        }, status=403)
    
    videos = VideoSolution.objects.filter(is_active=True)
    
    # Group by topic
    topics = {}
    for video in videos:
        if video.topic not in topics:
            topics[video.topic] = []
            
        topics[video.topic].append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'youtube_url': video.youtube_url,
            'duration_minutes': video.duration_minutes,
        })
    
    return Response({
        'is_pro': True,
        'topics': topics
    })
