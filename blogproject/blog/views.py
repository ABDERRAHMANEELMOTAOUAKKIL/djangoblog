from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.
def home(request):
     posts = Post.objects.all().order_by('-date_potsed') # Use '=' instead of ':    
     p = Paginator(posts, 3)  
     page = request.GET.get('page')
     page_obj = p.get_page(page)



     return render(request, 'blog/home.html', {"page_obj": page_obj})

def about(request):
    return render(request , 'blog/about.html',  {'title':"About Page"})



class PostsByCategoryView(View):
    template_name = 'blog/category.html'

    def get(self, request, category_name):
        category = Category.objects.get(name=category_name)
        posts = Post.objects.filter(category=category).order_by('-date_potsed')


        p = Paginator(posts, 3)  
        page = request.GET.get('page')
        page_obj = p.get_page(page)

        context = {
            'category': category,
            'posts': posts,
            'page_obj':page_obj,

            
        }
        return render(request,'blog/category.html', context)
    

    
class ArticleDetailView(DetailView):
   model = Post
   template_name = 'blog/article_details.html'
   
   def get_context_data(self, **kwargs: Any):
     
     context = super().get_context_data(**kwargs)  # Start with the base context

     stuff = get_object_or_404(Post, id= self.kwargs['pk'])
     total_likes = stuff.total_likes()

     liked= False
     if stuff.likes.filter(id= self.request.user.id).exists():
        liked = True

     context["total_likes"] = total_likes
     context["liked"] = liked
     return context


class AddPostView(LoginRequiredMixin, CreateView):
   model = Post
   template_name = 'blog/add_post.html'
   fields=['title','category', 'content','image','date_potsed']
   def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   success_url = reverse_lazy('blog-home')
     # fields = '__all__'
 
class UpdatePostView(UpdateView):
   model = Post
   template_name= 'blog/crud/update.html'
   fields=['title','category', 'content','image','date_potsed']
   success_url = reverse_lazy('blog-home')



class DeletePostView(DeleteView):
   model = Post
   template_name= 'blog/crud/delete.html'
   success_url = reverse_lazy('blog-home')


def LikeView (request , pk):
   post = get_object_or_404(Post, id =request.POST.get('post_id'))
   liked = False
   if post.likes.filter(id=request.user.id).exists():
      post.likes.remove(request.user)
      liked = False
   else:
      post.likes.add(request.user)
      liked = True
   return HttpResponseRedirect(reverse('article',args=[str(pk)] ))


def search_post(request):
   if request.method =='POST':
      search_post = request.POST.get("search_post")
      posts = Post.objects.filter(title__contains = search_post )
      return render(request, 'blog/search.html',{'search_post':search_post, 'posts':posts})
   else:
       return render(request, 'blog/search.html')

 

