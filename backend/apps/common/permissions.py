from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):

    message = "Only recruiters can perform this action."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "recruiter"
        )


class IsCandidate(BasePermission):

    message = "Only candidates can perform this action."

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "candidate"
        )


class IsJobOwner(BasePermission):

    message = "You can only modify your own jobs."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        return obj.recruiter == request.user