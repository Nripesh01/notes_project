from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    #   Object-level permission: only owner can edit/delete.
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
    
    # when request comes from browser then the DRF use has_permission to check the 
    # request if it valid then the request goes to the views to run.
    # has_object_permission runs after has_permission allow access, it checks whether
    # the user can interact to the specific data.
    
    # has_object_permission runs only if request targets one specific data,like:
    # get/1, put/1, delete/1 data..