from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.views.generic import ListView
from django.views import View
from datetime import date
from .forms import CommentForm


# def get_date(post):
#     return post['date']

# def home(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     # sorted_posts = sorted(all_posts, key=get_date)
#     # latest_posts = sorted_posts[-3:]
#     return render(request, 'blog/home.html', {
#         "posts": latest_posts
#     })
    
class HomeView(ListView):
    template_name = "blog/home.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, 'blog/all-posts.html', {
#         "posts": all_posts
#     })

class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post_detail.html', {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })
    
class SinglePostView(View):
    template_name = "blog/post_detail.html"
    model = Post
    
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
            
        return is_saved_for_later
    
    def get(self ,request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post_detail.html", context)
        
    def post(self ,request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post 
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post_detail.html", context)
    
class ReadLaterView(View):
    
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
            
        return render(request, "blog/stored-posts.html", context)
            
    
    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        
        if stored_posts is None:
            stored_posts = []
            
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts
            
        return HttpResponseRedirect("/")
        
    
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context
    
        
    


# context["comments_form"] = CommentForm()
# return context




# all_posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Maximilian",
#         "date": date(2021, 7, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
#         "content": """
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     },
#     {
#         "slug": "programming-is-fun",
#         "image": "coding.jpg",
#         "author": "Aashutosh",
#         "date": date(2022, 3, 10),
#         "title": "Programming Is Great!",
#         "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
#         "content": """
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     },
#     {
#         "slug": "into-the-woods",
#         "image": "woods.jpg",
#         "author": "Maximilian",
#         "date": date(2020, 8, 5),
#         "title": "Nature At Its Best",
#         "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
#         "content": """
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#         aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#         velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     }
# ]