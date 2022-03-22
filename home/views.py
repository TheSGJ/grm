from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from datetime import date, datetime

from tv.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "index.html", context)
    




def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'search.html', params)

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        usernamel = username.lower()
        # check for errorneous input
        if len(username)<3:
            messages.error(request, " Your username must be more than 3 characters!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')
        # Create the user
        myuser = User.objects.create_user(usernamel, pass1)
        
        myuser.save()

        user=authenticate(username= usernamel, password= pass1)
        login(request, user)
        messages.success(request, "Your RigelGrin account has been created & logged in successfully!")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['username']
        loginpassword=request.POST['pass1']
        # Defines uppercase username letters to lowercase
        loginusernamel = loginusername.lower()
        user=authenticate(username= loginusernamel, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again!!")
            return redirect("home")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')