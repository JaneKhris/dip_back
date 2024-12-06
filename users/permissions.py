from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #     return True
        return request.user == obj.id
    
    # def has_permission(self, request, view):
    #     # if request.method in SAFE_METHODS:
    #     #     return True
    #     return request.user == self.id