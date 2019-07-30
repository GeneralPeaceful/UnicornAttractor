from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import AddPostForm

def get_posts(request):
    """
    Returns a list of Posts that were published prior to 'now' and render them to the 'blogposts.html' template
    """
    
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'posts.html', {'posts': posts})

def post_detail(request, pk):
    """
    Returns a single Post object based on the post ID (pk) and render it to the 'postdetail.html' template.
    Return a 404 error if the post is not found.
    """
    
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'postdetail.html', {'post': post})

def create_post(request, pk=None):
    """
    Create a post depending on if the Post ID is null or not.
    """
    
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been published successfully.')
            return redirect(post_detail, post.pk)
    else:
        form = AddPostForm(instance=post)
    return render(request, 'addpost.html', {'form': form})