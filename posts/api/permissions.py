from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'Only author of the post can update/delete the post.'
    # my_safe_method = ('GET', 'HEAD',)
    #
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        # checks/filters for user if needed.

        # if request.method in SAFE_METHODS:
        #     return True

        return obj.user == request.user
