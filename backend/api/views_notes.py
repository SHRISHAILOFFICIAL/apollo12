from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
from exams.models import Note
import os


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notes(request):
    """List all available notes grouped by subject"""
    notes = Note.objects.filter(is_active=True)
    
    # Group by subject
    subjects = {}
    for note in notes:
        if note.subject not in subjects:
            subjects[note.subject] = []
        
        # Check access (for future PRO implementation)
        can_access = True
        if note.access_tier == 'PRO':
            # Check if user has PRO access
            can_access = request.user.profile.is_pro if hasattr(request.user, 'profile') else False
            
        subjects[note.subject].append({
            'id': note.id,
            'topic': note.topic,
            'description': note.description,
            'access_tier': note.access_tier,
            'can_access': can_access,
            'is_locked': not can_access,
        })
    
    return Response({'subjects': subjects})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def serve_note(request, note_id):
    """Serve PDF file with access control"""
    try:
        note = Note.objects.get(id=note_id, is_active=True)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=404)
    
    # Check access tier
    if note.access_tier == 'PRO':
        has_pro = request.user.profile.is_pro if hasattr(request.user, 'profile') else False
        if not has_pro:
            return Response({'error': 'PRO membership required'}, status=403)
    
    # Build file path
    notes_root = os.path.join(settings.BASE_DIR, 'notes')
    file_path = os.path.join(notes_root, note.file_path)
    
    if not os.path.exists(file_path):
        return Response({'error': f'File not found on server: {file_path}'}, status=404)
    
    # Serve file directly (development)
    return FileResponse(
        open(file_path, 'rb'),
        content_type='application/pdf',
        as_attachment=False,  # Display inline, not download
        filename=f"{note.topic}.pdf"
    )
