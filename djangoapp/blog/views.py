from blog.models import Post
from django.core.paginator import Paginator
from django.shortcuts import render

PER_PAGE = 9

# Create your views here.
def index(request):
  posts = Post.objects.filter(is_published=True).order_by('-pk')
  paginator = Paginator(posts, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/index.html', content)

def page(request):
  change_here = ''
  paginator = Paginator(change_here, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/page.html', content)

def post(request):
  change_here = ''
  paginator = Paginator(change_here, PER_PAGE)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  content = {
    'page_obj': page_obj
  }
  return render(request, 'blog/pages/post.html', content)