from django.shortcuts import render,redirect
from .models import*
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate

# for session
from django.contrib.auth import login

# for user logout
from django.contrib.auth import logout

# for django decorator,isse ye hoga ki koi bhi recipe ka url daalke ,open nhi kr skta,jab tk login nhi krta voh user
from django.contrib.auth.decorators import login_required


# Create your views here.

# this line helps to first login then access the home page
@login_required(login_url="/login/")
def recipes(request):
    
    # to store the data from frontend to backend
    
    if request.method=="POST":
        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        # to check in console
        # print(recipe_name)
        # print(recipe_description)
        # print(recipe_image)
        
        
        
        Recipe.objects.create(
            recipe_name=recipe_name,recipe_description=recipe_description,recipe_image=recipe_image
            )
        return redirect('/recipes/')
    
    # to render the data from backend to frontend
    queryset=Recipe.objects.all()
    
    # for searching the recipe...it only filters that specific recipe_name
    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
        
    
    context={'recipes':queryset}
    return render(request,'recipes.html',context)

@login_required(login_url="/login/")
def update_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    
    if request.method=="POST":
        data=request.POST
        
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        queryset.recipe_name=recipe_name
        queryset.recipe_description=recipe_description
        
        if recipe_image:
            queryset.recipe_image=recipe_image
            
        queryset.save()
        
        return redirect('/recipes/')
         
            
    context={'recipe':queryset}
    return render(request,'update_recipes.html',context)
  

@login_required(login_url="/login/")    
def delete_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    # return HttpResponse("a")
    
    return redirect('/recipes/')


# user authentication
def login_page(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username.")
            return redirect('/login/')
        
        
        # if username exists,then check ki password right h  ya nhi
        
        user=authenticate(username=username,password=password)
        
        
        # if user enters wrong password then,show this
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        
        
        
        # is user ne right details se login kia,then apn uske lie ek session create krdenge and use redirect krwa denge home page pe,and session env mai chle jaega
        else:
            login(request,
                  user)
            return redirect('/recipes/')
        
        
        
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')
    

def register(request):
    
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        
    # for checking whether,same name ka usernmae hai ya nhi,keeping all username unique
       
       
        user=User.objects.filter(username=username)
       
        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect('/register/')
         
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()  
        
        messages.success(request, "Account created successfully.")
        
        return redirect('/register/')      
    
    return render(request,'register.html')