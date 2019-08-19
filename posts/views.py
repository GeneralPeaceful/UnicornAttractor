from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import AddPostForm
from comments.models import Comment

def get_posts(request):
    """
    Returns a list of Posts that were published prior to 'now' and render them to the 'blogposts.html' template
    """
    
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'posts.html', {'posts': posts})

def post_detail(request, postid):
    """
    Returns a single Post object based on the post ID (pk) and render it to the 'postdetail.html' template.
    Return a 404 error if the post is not found.
    """
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            user = request.user
            comment = request.POST['comment']
            post = get_object_or_404(Post, pk=postid)
            if comment.strip() == '':
                messages.error(request, 'Comment message is required.')
                return redirect('post_detail', postid=post.pk)
            comment = Comment(user=user, comment=comment, post=post)
            comment.save()
            messages.success(request, 'Thanks for your comment.')
            return redirect('post_detail', postid=post.pk)

    current_post = get_object_or_404(Post, pk=postid)
    current_post.views += 1
    current_post.save()
    comments = Comment.objects.all().filter(post=postid)
    context = {
        'post': current_post,
        'comments': comments,
    }
    return render(request, 'postdetail.html', context)

@login_required
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