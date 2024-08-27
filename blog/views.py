from django.shortcuts import  render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Blog, BlogCategory, BlogComment
from .forms import AvatarForm, PubBlogForm
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={'blogs': blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        print(e)
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('djauth:login'))
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        print("Raw POST data:", request.POST)
        print("Content in POST:", request.POST.get('content'))
        print("Content length:", len(request.POST.get('content', '')))

        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            print("Form is valid. Created blog with title:", title)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'code': 200, 'msg': '发布成功', 'data':{'blog_id':blog.id}})
        else:
            print("Form errors:", form.errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'code': 400, 'msg': '发布失败', 'errors': form.errors})
            else:
                return render(request, 'pub_blog.html', {'form': form, 'categories': BlogCategory.objects.all()})
            
@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    #重新加載詳情頁
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id':blog_id}))

@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    #從標題和內文中查找含有q的
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={'blogs': blogs})


@login_required
def avatar_settings(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarForm(instance=request.user.profile)
    return render(request, 'avatar_settings.html', {'form': form})