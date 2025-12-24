"""
Custom permissions for exam access control
"""
from rest_framework import permissions


class HasExamAccess(permissions.BasePermission):
    """
    Permission to check if user has access to a specific exam based on tier
    """
    
    message = "You need to upgrade to PRO to access this exam."
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user's tier allows access to the exam
        """
        # Allow if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Get the exam object
        exam = obj if hasattr(obj, 'access_tier') else obj.exam
        
        # Check if user's tier meets exam's required tier
        return request.user.has_tier_access(exam.access_tier)


class IsPremiumUser(permissions.BasePermission):
    """
    Permission to check if user has PRO tier
    """
    
    message = "This feature is only available for PRO users."
    
    def has_permission(self, request, view):
        """
        Check if user is PRO
        """
        return request.user and request.user.is_authenticated and request.user.is_pro()


def can_access_exam(user, exam):
    """
    Helper function to check if user can access an exam
    
    Args:
        user: User object
        exam: Exam object
    
    Returns:
        tuple: (can_access: bool, reason: str)
    """
    if not user or not user.is_authenticated:
        return False, "You must be logged in to access exams"
    
    if exam.access_tier == 'FREE':
        return True, ""
    
    if user.is_pro():
        return True, ""
    
    return False, "This exam requires PRO membership. Upgrade to access all exams!"
