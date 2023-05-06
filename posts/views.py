from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db import IntegrityError
from .models import Post
from .serializers.common import PostSerializer
from .serializers.populated import PopulatedPostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator


class PostListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
# Get all posts
    def get(self, _request):
        posts = Post.objects.all()  
        serialized_products = PopulatedPostSerializer(posts, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)
    
# Create a post
    def post(self, request):
        request.data["owner"] = request.user.id
        # if request.user.is_authenticated:
        #     request.data["owner"] = request.user.id
        # else:
        #     request.data["owner"] = 1

        post_to_add = PostSerializer(data=request.data)
    
        try: 
            post_to_add.is_valid()
            post_to_add.save()
            return Response(post_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({ "detail": str(e) }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
     
        except:
            return Response({ "detail": "Apologies this is a Unprocessable Entity!" }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
class PostDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound(
                detail="Can not find an post with that primary key")
# Get an individual post
    def get(self, _request, pk):
        post = self.get_post(pk=pk)
        serialized_post = PostSerializer(post)
        return Response(serialized_post.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        post_to_update = self.get_post(pk=pk)
   
        if request.user != post_to_update.owner and not request.user.is_staff:
               raise PermissionDenied()
        updated_post = PostSerializer(post_to_update, data=request.data)
        try: 
            updated_post.is_valid()
            updated_post.save()
            return Response(updated_post.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessible Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    def delete(self,  request , pk):
        post_to_delete = self.get_post(pk=pk)
        if request.user != post_to_delete.owner and not request.user.is_staff:
               raise PermissionDenied()
            
        post_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

