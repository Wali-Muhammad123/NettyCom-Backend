from rest_framework.permissions import BasePermission

class IsTeamLead(BasePermission):
    message="User must be a team lead in order to access"
    def has_permission(self, request, view):
        user=request.user
        if user.is_authenticated and user.isTeamLeader:
            return True
        return False
class TeamDataPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.team.leader == request.user if request.user.isTeamLead else False