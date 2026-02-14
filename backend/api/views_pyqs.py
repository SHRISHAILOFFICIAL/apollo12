from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
from exams.models import PYQ
import os


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pyqs(request):
    """List all available PYQs grouped by year"""
    pyqs = PYQ.objects.filter(is_active=True)
    
    # Group by year
    years = {}
    for pyq in pyqs:
        year_str = str(pyq.year)
        if year_str not in years:
            years[year_str] = []
        
        # Check access (for future PRO implementation)
        can_access = True
        if pyq.access_tier == 'PRO':
            # Check if user has PRO access
            can_access = request.user.profile.is_pro if hasattr(request.user, 'profile') else False
            
        years[year_str].append({
            'id': pyq.id,
            'exam_name': pyq.exam_name,
            'description': pyq.description,
            'access_tier': pyq.access_tier,
            'can_access': can_access,
            'is_locked': not can_access,
        })
    
    return Response({'years': years})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def serve_pyq(request, pyq_id):
    """Serve PYQ PDF file with access control"""
    try:
        pyq = PYQ.objects.get(id=pyq_id, is_active=True)
    except PYQ.DoesNotExist:
        return Response({'error': 'PYQ not found'}, status=404)
    
    # Check access tier
    if pyq.access_tier == 'PRO':
        has_pro = request.user.profile.is_pro if hasattr(request.user, 'profile') else False
        if not has_pro:
            return Response({'error': 'PRO membership required'}, status=403)
    
    # Build file path
    pyqs_root = os.path.join(settings.BASE_DIR, 'pyq')
    file_path = os.path.join(pyqs_root, pyq.file_path)
    
    if not os.path.exists(file_path):
        return Response({'error': f'File not found on server: {file_path}'}, status=404)
    
    # Serve file directly (development)
    return FileResponse(
        open(file_path, 'rb'),
        content_type='application/pdf',
        as_attachment=False,  # Display inline, not download
        filename=f"{pyq.exam_name}_{pyq.year}.pdf"
    )
