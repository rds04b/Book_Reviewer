from django.shortcuts import render, redirect
import django.contrib.sessions
from django.contrib import messages
from .models import User, Book, Review

def index(request):
    return render(request, 'main/index.html')

def create(request):
    if request.method =='POST':
        valid, data = User.objects.validate_and_create(request.POST)
        if valid:
            user_email = request.POST['email']
            if user_email != '':
                info = User.objects.get(email=user_email)
                request.session['method'] = 'registered'
                request.session['id'] = info.id
                request.session['name'] = info.first_name
                request.session['email'] = info.email
        if not valid:
            for err in data:
                messages.error(request, err)
            return redirect('/')

    context = {
        "user" : request.POST['first_name'],
        "reviews" : Review.objects.all().order_by("created_at")[:5],
        }
    return render(request, 'main/book.html', context)

def login(request):
    if request.method =='POST':
        valid, data = User.objects.login(request.POST)
        if valid:

            user_email = request.POST['email']
            if user_email != '':
                info = User.objects.get(email=user_email)
                request.session['method'] = 'logged in'
                request.session['id'] = info.id
                request.session['name'] = info.first_name
                request.session['email'] = info.email
        if not valid:
            for err in data:
                messages.error(request, err)
            return redirect('/')

    return redirect('main:bookhome')

def book_entry(request):
    books = Book.objects.all()
    context = {
        'books' : books,
    }
    return render(request, 'main/add_book.html', context)

def new_book(request):
    if request.method =='POST':
        valid, data, data2 = Book.objects.new_book(request.POST, request.session['id'])
        if not valid:
            for err in data:
                messages.error(request, err)
            return redirect('/book_entry')

    return redirect('main:bookhome')

def new_review(request, id):
    if request.method =='POST':
        valid, data = Review.objects.new_review(request.POST, request.session['id'], id)

        if not valid:
            for err in data:
                messages.error(request, err)
            return redirect('/bookreview/'+str(id))

    return redirect('/bookreview/'+str(id))

def bookreview(request, id):
    books = Book.objects.get(id=id)
    reviews = Review.objects.filter(reviewed_book=books).order_by('-created_at')[:5]
    users = User.objects.all()
    context = {
        'books' : books,
        'reviews' : reviews,
        'users' : users,
    }
    return render(request, 'main/add_review.html', context)

def bookhome(request):
    books = Book.objects.all()
    reviews = Review.objects.all().order_by('-created_at')[:3]
    users = User.objects.all()
    context = {
        'books' : books,
        'reviews' : reviews,
        'users' : users,
    }
    return render(request, 'main/book.html', context)



def user(request, id):
    users = User.objects.get(id=id)
    user_review = Review.objects.filter(review_creator=id)
    books = Book.objects.all()
    reviews = Review.objects.all()
    count = 0
    for review in user_review:
        count += 1
    context = {
        'users' : users,
        'count' : count,
        'books' : books,
        'reviews' : reviews,
    }
    return render(request, 'main/user.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, r_id, b_id):
    Review.objects.delete(r_id)
    return redirect('/bookreview/'+str(b_id))

def like(request, id):
    review_like = Review.objects.get(id=id)
    review_like.like += 1
    review_like.save()
    return redirect('/bookhome')

    # for reference, not used. render two templates from same view:
    # m_list = Review.objects.filter(like=True)
    # return render(request, template_name, {'m_list': m_list})

def book_like(request, id, b_id):
    review_like = Review.objects.get(id=id, reviewed_book=b_id)
    review_like.like += 1
    review_like.save()
    return redirect('/bookreview/'+str(b_id))


def edit_review(request, id):
    reviews = Review.objects.get(id=id)
    users = User.objects.get(id=reviews.review_creator.id)
    books = Book.objects.get(id=reviews.reviewed_book.id)
    context = {
        'user' : users,
        'book' : books,
        'review' : reviews,
    }
    return render(request, 'main/update.html', context)

def update_edit(request, id, b_id):
    existing_review = Review.objects.get(id=id, reviewed_book=b_id)
    existing_review.rating = int(request.POST['ratings'])
    existing_review.review = request.POST['review']
    existing_review.save()
    return redirect('/bookreview/'+str(b_id))
