from typing import Any

from blog.models import Page, Post
from django.contrib.auth.models import User
# from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
# from django.http import Http404, HttpRequest, HttpResponse
from django.http import Http404
# from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

PER_PAGE = 9

# Create your views here.
class PostListView(ListView):
  model = Post
  template_name = 'blog/pages/index.html'
  context_object_name = 'posts'
  ordering = '-pk'
  paginate_by = PER_PAGE
  queryset = Post.objects.get_published()

  # def get_queryset(self):
  #   query_set = super().get_queryset()
  #   new_queryset = query_set.filter(is_published=True)
  #   return new_queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'page_title': 'Home'
    })
    return context
  

class CreatedByListView(PostListView):
  def __init__(self, **kwargs: Any) -> None:
    super().__init__(**kwargs)
    self._temp_context: dict[str, Any] = {}

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self._temp_context['user']
    user_full_name = user.username
    if user.first_name:
      user_full_name = f'{user.first_name} {user.last_name}'

    page_title = 'Posts de ' + user_full_name
    context.update({
      'page_title': page_title
    })
    return context

  def get_queryset(self) -> QuerySet[Any]:
    query_set = super().get_queryset()
    query_set = query_set.filter(created_by__pk=self._temp_context['user'].pk)
    return query_set

  def get(self, request, *args, **kwargs):
    author_pk = self.kwargs.get('author_pk')
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
      raise Http404()

    self._temp_context.update({
      'author_pk': author_pk,
      'user': user,
    })

    return super().get(request, *args, **kwargs)
    

class CategoryListView(PostListView):
  allow_empty = False

  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(
      category__slug=self.kwargs.get('slug')
    )
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    page_title = self.object_list[0].category.name + ' - Categoria'
    context.update({
      'page_title': page_title
    })
    return context


class TagListView(PostListView):
  allow_empty = False

  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(
      tags__slug=self.kwargs.get('slug')
    )
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    page_title = self.object_list[0].tags.filter(slug=self.kwargs.get('slug')).first().name + ' - Tag'
    context.update({
      'page_title': page_title
    })
    return context

class SearchListView(PostListView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._search_value = ''

  def setup(self, request, *args, **kwargs):
    self._search_value = request.GET.get('search', '').strip()
    return super().setup(request, *args, **kwargs)
  
  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(
      Q(title__icontains=self._search_value) | 
      Q(excerpt__icontains=self._search_value) | 
      Q(content__icontains=self._search_value)
    )[:PER_PAGE]
  
  def get_context_data(self, **kwargs):
    contexto = super().get_context_data(**kwargs)
    page_title = self._search_value[:30] + ' - Search'
    contexto.update({
      'page_title': page_title,
      'search_value': self._search_value
    })
    return contexto

  def get(self, request, *args, **kwargs):
    if self._search_value == '':
      return redirect('blog:index')
    return super().get(request, *args, **kwargs)
  

class PageDetailView(DetailView):
  model  = Page
  template_name = 'blog/pages/page.html'
  slug_field = 'slug'
  context_object_name = 'page'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    contexto = super().get_context_data(**kwargs)
    page = self.get_object()
    page_title = page.title + ' - Página'
    contexto.update({
      'page_title': page_title,
    })
    return contexto
  
  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(is_published=True)

class PostDetailView(DetailView):
  model  = Post
  template_name = 'blog/pages/post.html'
  context_object_name = 'post'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    contexto = super().get_context_data(**kwargs)
    post = self.get_object()
    post_tags = post.tags.all()
    page_title = post.title + ' - Post'
    contexto.update({
      'page_title': page_title,
      'post_tags' : post_tags,
    })
    return contexto
  
  def get_queryset(self) -> QuerySet[Any]:
    return super().get_queryset().filter(is_published=True)

# def index(request):
#   posts = Post.objects.get_published()
#   paginator = Paginator(posts, PER_PAGE)
#   page_number = request.GET.get("page")
#   page_obj = paginator.get_page(page_number)
#   content = {
#     'page_obj': page_obj,
#     'page_title': 'Home'
#   }
#   return render(request, 'blog/pages/index.html', content)

# def created_by(request, author_pk):
#   user = User.objects.filter(pk=author_pk).first()
#   if user is None:
#     raise Http404()
  
#   posts = Post.objects.get_published().filter(created_by__pk=author_pk)

#   user_full_name = user.username
#   if user.first_name:
#     user_full_name = f'{user.first_name} {user.last_name}'

#   page_title = 'Posts de ' + user_full_name

#   paginator = Paginator(posts, PER_PAGE)
#   page_number = request.GET.get("page")
#   page_obj = paginator.get_page(page_number)
#   content = {
#     'page_obj': page_obj,
#     'page_title': page_title
#   }
#   return render(request, 'blog/pages/index.html', content)

# def category(request, slug):
#   posts = Post.objects.get_published().filter(category__slug=slug)
  
#   paginator = Paginator(posts, PER_PAGE)
#   page_number = request.GET.get("page")
#   page_obj = paginator.get_page(page_number)

#   if len(posts) == 0:
#     raise Http404()

#   page_title = page_obj[0].category.name + ' - Categoria'

#   content = {
#     'page_obj': page_obj,
#     'page_title': page_title
#   }
#   return render(request, 'blog/pages/index.html', content)

# def tag(request, slug):
#   posts = Post.objects.get_published().filter(tags__slug=slug)

#   paginator = Paginator(posts, PER_PAGE)
#   page_number = request.GET.get("page")
#   page_obj = paginator.get_page(page_number)

#   if len(posts) == 0:
#     raise Http404()

#   page_title = page_obj[0].tags.filter(slug=slug).first().name + ' - Tag'

#   content = {
#     'page_obj': page_obj,
#     'page_title': page_title
#   }
#   return render(request, 'blog/pages/index.html', content)

# def search(request):
#   search_value = request.GET.get('search', '').strip()
#   posts = Post.objects.get_published().filter(
#     Q(title__icontains=search_value) | 
#     Q(excerpt__icontains=search_value) | 
#     Q(content__icontains=search_value)
#   )[:PER_PAGE]

#   page_title = search_value[:30] + ' - Search'

#   content = {
#     'page_obj': posts,
#     'search_value': search_value,
#     'page_title': page_title
#   }
#   return render(request, 'blog/pages/index.html', content)

# def page(request, slug):
#   page_obj = Page.objects.filter(is_published=True, slug=slug).first()

#   if page_obj is None:
#     raise Http404()

#   page_title = page_obj.title + ' - Página'

#   content = {
#     'page': page_obj,
#     'page_title': page_title
#   }
#   return render(request, 'blog/pages/page.html', content)

# def post(request, slug):
#   post_obj = Post.objects.get_published().filter(slug=slug).first()

#   if post_obj is None:
#     raise Http404()

#   page_title = post_obj.title + ' - Post'

#   post_tags = post_obj.tags.all()
#   content = {
#     'post': post_obj,
#     'post_tags' : post_tags,
#     'page_title': 'Home'
#   }
#   return render(request, 'blog/pages/post.html', content)