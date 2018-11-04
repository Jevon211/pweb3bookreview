
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import users, Book, review
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'booksite/loginpage.html')

def dashboard(request):
    if len(request.session['email']) < 1:
        return redirect('/')
    context = {
        'books': Book.objects.all(),
        'review': review.objects.all().order_by('-created_at')[:3],
        'user': users.objects.get(email=request.session['email'])
    }
    return render(request, 'booksite/dashboard.html', context)
def add_book(request):
    if request.POST['select'] != 'none':
        r = Book.objects.get(book_title = request.POST['select'])
        review.objects.create(review= request.POST['review'], book= Book.objects.get(id = r.id), user = users.objects.get(email= request.session['email']))
    else:
        r = Book.objects.create(book_title=request.POST['title'], author=request.POST['author'])
        review.objects.create(review= request.POST['review'], book= Book.objects.get(id = r.id), user = users.objects.get(email= request.session['email']))
    return redirect(dashboard)

def add(request):
    if len(request.session['email']) < 1:
        return redirect('/')
    context = {
        'books': Book.objects.all(),
        'review': review.objects.all()
    }
    return render(request, 'booksite/addbook.html', context)

def register(request):
    if request.method == 'POST':
        errors = users.objects.registration_validator(request.POST)
        if len(errors):
            for tag, errors in errors.iteritems():
                messages.error(request, errors, extra_tags=tag)
            return redirect(index)
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash1)
            messages.error(request, 'Registration complete, please login!')
            
    return redirect(index)

def log_in(request):
    if request.method == 'POST':
        errors = users.objects.log_in(request.POST)
        if len(errors):
            for tag, errors in errors.iteritems():
                messages.error(request, errors, extra_tags=tag)
            return redirect(index)
        else:
            user = users.objects.filter(email=request.POST['email'])
            request.session['email'] = request.POST['email']
            request.session['alias'] = user[0].alias
            return redirect('/dashboard')

def book(request, id):
    if len(request.session['email']) < 1:
        return redirect('/')
    context = {
        'book': Book.objects.get(id=id),
        'review': review.objects.filter(book=Book.objects.get(id=id)).order_by('-created_at'),
    }
    return render(request, 'booksite/books.html', context)

def user(request, id):
    if len(request.session['email']) < 1:
        return redirect('/')
    context = {
        'user': users.objects.get(id=id),
        'review': review.objects.filter(user=users.objects.get(id=id)).order_by('-created_at'),
        'review_count': review.objects.filter(user = users.objects.get(id=id)).count()
    }
    return render(request, 'booksite/user.html', context)
def log_out(request):
    request.session['email'] = ""
    request.session['alias'] = ""
    return redirect('/')
