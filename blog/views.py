from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import CommentForm

from django.views.generic import ListView, DetailView
# Create your views here.
from django.views import View
from .models import Post


def get_date(post):
        return post['date']


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request,  "blog/index.html", {
#          "posts": latest_posts
#     })


class StartingPage(ListView):
     template_name = "blog/index.html"
     model = Post
     ordering = ["-date"]
     context_object_name = "posts"

     def get_queryset(self):
          queryset =  super().get_queryset()
          data = queryset[:3]
          return data

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#          "all_posts" : all_posts
#     })


class PostsView(ListView):
     template_name = "blog/all-posts.html"
     model = Post
     ordering = ["-date"]
     context_object_name = "all_posts"



# def post_details(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     print(identified_post.image.url)
#     return render(request, "blog/post-detail.html", {
#          "post": identified_post,
#          "tags": identified_post.tag.all()
#     })
     

class PostDetails(View):
      def get(self, request, slug):
            stored_posts = request.session.get("stored_posts")
            post = Post.objects.get(slug=slug)
            read_later = post.id in stored_posts 
            print(read_later)
            comments = post.comments.all().order_by("-id")
            return render(request, "blog/post-detail.html", {
                  "post" : post,
                  "tags" : post.tag.all(),
                  "comment_form" : CommentForm(),
                  "comments": comments,
                  "read_later" : read_later
            })
      
      def post(self, request, slug):
            post = Post.objects.get(slug=slug)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                  comment = comment_form.save(commit=False)
                  comment.post = post
                  comment.save()
                  return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
            return render(request, "blog/post-detail.html", {
                  "post" : post,
                  "tags" : post.tag.all(),
                  "comment_form" : CommentForm()
            })
               
            

class ReadLater(View):
      def get(self, request):
            stored_posts = request.session.get("stored_posts")
            context = {}

            if stored_posts is None or len(stored_posts) == 0:
                  context['posts'] = []
                  context['has_posts'] = False
            else:
               posts = Post.objects.filter(id__in=stored_posts)
               context['posts'] = posts
               context['has_posts'] = True

            return render(request, "blog/stored-posts.html", context)
      
      def post(self, request):
          post_id = int(request.POST["post_id"])
          stored_posts = request.session.get("stored_posts")
          
          if stored_posts is None:
                stored_posts = []
                
          if post_id not in stored_posts:
               stored_posts.append(post_id)
          else:
                stored_posts.remove(post_id)
          
          request.session["stored_posts"] = stored_posts
          return HttpResponseRedirect('/blog')
                
