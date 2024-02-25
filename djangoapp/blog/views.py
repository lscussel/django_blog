from blog.models import Page, Post
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

PER_PAGE = 9

# Create your views here.
def index(request):
  posts = Post.objects.get_published()
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/index.html', content)

def created_by(request, author_pk):
  posts = Post.objects.get_published().filter(created_by__pk=author_pk)
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/index.html', content)

def category(request, slug):
  posts = Post.objects.get_published().filter(category__slug=slug)
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/index.html', content)

def tag(request, slug):
  posts = Post.objects.get_published().filter(tags__slug=slug)
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/index.html', content)

def search(request):
  search_value = request.GET.get('search', '').strip()
  posts = Post.objects.get_published().filter(
    Q(title__icontains=search_value) | 
    Q(excerpt__icontains=search_value) | 
    Q(content__icontains=search_value)
  )[:PER_PAGE]
  content = {
    'page_obj': posts,
    'search_value': search_value
  }
  return render(request, 'blog/pages/index.html', content)

def page(request, slug):
  page = Page.objects.filter(is_published=True, slug=slug).first()
  content = {
    'page': page
  }
  return render(request, 'blog/pages/page.html', content)

def post(request, slug):
  post = Post.objects.get_published().filter(slug=slug).first()
  post_tags = post.tags.all()
  content = {
    'post': post,
    'post_tags' : post_tags
  }
  return render(request, 'blog/pages/post.html', content)