from rest_framework.decorators import action
from rest_framework.response import Response
from ..utils import add_like, remove_like


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        """
        Create like.
        """
        obj = self.get_object()
        add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        """
        Delete like.
        """
        obj = self.get_object()
        remove_like(obj, request.user)
        return Response()
