from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    '''
        permission for only owner to access and modify  
    '''
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user