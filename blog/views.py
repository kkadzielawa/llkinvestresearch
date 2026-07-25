from django.views import generic
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(
        status=Post.PostStatus.PUBLISHED
    ).order_by("-created_on")
    context_object_name = "posts"
    paginate_by = 6
    template_name = 'blog.html'

class PostDetail(generic.DetailView):
    template_name = 'post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(status=Post.PostStatus.PUBLISHED)
