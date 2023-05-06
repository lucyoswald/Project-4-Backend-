from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers.common import CommentSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Comment
from rest_framework.permissions import IsAuthenticated

class CommentListView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data["owner"] = request.user.id
        comment_to_create = CommentSerializer(data=request.data)
        try: 
            comment_to_create.is_valid()
            comment_to_create.save()
            return Response(comment_to_create.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({
                "detail": str(e),}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except AssertionError as e:
            return Response({"detail": str(e)}, 
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response("Apologies, this is an unprocessable entity!", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            comment_to_delete = Comment.objects.get(pk=pk)
            if comment_to_delete.owner != request.user and not request.user.is_staff:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response("You successfully deleted a comment!", status=status.HTTP_204_NO_CONTENT)
        
        except Comment.DoesNotExist:
            raise NotFound(detail="Apologies, this comment was not found.")
