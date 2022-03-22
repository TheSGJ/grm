from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from tv.models import Post, TvComment
from django.contrib import messages
from tv.templatetags import extras

def tvHome(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "tvHome.html", context)


def tvPost(request, slug):
    
    post=Post.objects.filter(slug=slug).first()
    comments= TvComment.objects.filter(post=post, parent=None)
    
    replies= TvComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user,'replyDict': replyDict}
    if post==Post.objects.filter(slug=slug).first():
         return render(request, "tvPost.html", context)

    else:
         return HttpResponse("404 Not Found")
         
def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=TvComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= TvComment.objects.get(sno=parentSno)
            comment=TvComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/tv/{post.slug}")
