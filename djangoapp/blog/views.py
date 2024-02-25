from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

PER_PAGE = 9

# Create your views here.
def index(request):
  posts = Post.objects.get_published()
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj,
    'page_title': 'Home'
  }
  return render(request, 'blog/pages/index.html', content)

def created_by(request, author_pk):
  user = User.objects.filter(pk=author_pk).first()
  if user is None:
    raise Http404()
  
  posts = Post.objects.get_published().filter(created_by__pk=author_pk)

  user_full_name = user.username
  if user.first_name:
    user_full_name = f'{user.first_name} {user.last_name}'

  page_title = 'Posts de ' + user_full_name

  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj,
    'page_title': page_title
  }
  return render(request, 'blog/pages/index.html', content)

def category(request, slug):
  posts = Post.objects.get_published().filter(category__slug=slug)
  
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  if len(posts) == 0:
    raise Http404()

  page_title = page_obj[0].category.name + ' - Categoria'

  content = {
    'page_obj': page_obj,
    'page_title': page_title
  }
  return render(request, 'blog/pages/index.html', content)

def tag(request, slug):
  posts = Post.objects.get_published().filter(tags__slug=slug)

  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  if len(posts) == 0:
    raise Http404()

  page_title = page_obj[0].tags.filter(slug=slug).first().name + ' - Tag'

  content = {
    'page_obj': page_obj,
    'page_title': page_title
  }
  return render(request, 'blog/pages/index.html', content)

def search(request):
  search_value = request.GET.get('search', '').strip()
  posts = Post.objects.get_published().filter(
    Q(title__icontains=search_value) | 
    Q(excerpt__icontains=search_value) | 
    Q(content__icontains=search_value)
  )[:PER_PAGE]

  page_title = search_value[:30] + ' - Search'

  content = {
    'page_obj': posts,
    'search_value': search_value,
    'page_title': page_title
  }
  return render(request, 'blog/pages/index.html', content)

def page(request, slug):
  page_obj = Page.objects.filter(is_published=True, slug=slug).first()

  if page_obj is None:
    raise Http404()

  page_title = page_obj.title + ' - Página'

  content = {
    'page': page_obj,
    'page_title': page_title
  }
  return render(request, 'blog/pages/page.html', content)

def post(request, slug):
  post_obj = Post.objects.get_published().filter(slug=slug).first()

  if post_obj is None:
    raise Http404()

  page_title = post_obj.title + ' - Post'

  post_tags = post_obj.tags.all()
  content = {
    'post': post_obj,
    'post_tags' : post_tags,
    'page_title': 'Home'
  }
  return render(request, 'blog/pages/post.html', content)