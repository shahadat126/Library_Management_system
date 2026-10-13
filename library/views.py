from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Book,Category,Reviews
from django.contrib.auth.models import User
from .forms import BookForm,ReviewsForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
from django.core.paginator import Paginator
# Create your views here.
def Home(request):
    try:
        return render(request,"library/base.html")
    except Exception as e:
        return render(request,'library/error.html',{'error':e})

   
def book_add(request):
    try:
        form= BookForm()
        if request.method == "POST":
            form= BookForm(request.POST)
            if form.is_valid():
                # Book.objects.create(
                #     title = request.POST.get('title'),
                #     author = request.POST.get('author'),
                #     category = form.cleaned_data['category'],
                #     description = request.POST.get('description'),
                # )
                form.save()
                messages.success(request,"Book added successfully!")
                return redirect("library:dashboard")
                
        return render(request,'library/book_add.html',{'form':form})
            
    except Exception as e:
        return render(request,'library/error.html',{'error':e})


def book_list(request):
    books = Book.objects.select_related("category").all()
    categories = Category.objects.all().order_by("name")

    # Step 2: Search input collect
    query = request.GET.get("q", "").strip()

    # Step 3: Category input collect
    selected_category = request.GET.get("category", "")

    # Step 4: Title or Author search
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
        )

    # Step 5: Category wise filter
    if selected_category.isdigit():
        selected_category = int(selected_category)

        books = books.filter(category_id=selected_category)
    else:
        selected_category = ""

    paginator = Paginator(books, 4)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)
    context = {
        "books": books,
        "categories": categories,
        "query": query,
        "selected_category": selected_category,
        "page_obj": page_obj,
    }

    return render(request, "library/book_list.html", context)

    
# def book_detail(request, id):
    
#     book = Book.objects.get(id=id)

#     return render(
#         request,
#         'library/book_detail.html',
#         {'book': book}
#     )
from django.db.models import Avg



    
def book_edit(request,id):
    edit_info= Book.objects.get(id=id)
    form=BookForm(instance=edit_info)
    if request.method== "POST":
        form = BookForm(request.POST,instance=edit_info)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Update Done')
            return redirect("library:book_list")
    return render (request,"library/book_add.html",{ 'form':form})

# def book_delete(request,id):
#     book = Book.objects.get(id=id)
#     book.delete()
#     messages.add_message(request,messages.SUCCESS,'Delete Successfully')
#     return redirect("library:book_list")



def book_delete(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.delete()

        messages.success(
            request,
            "Book deleted successfully!"
        )

        return redirect("library:book_list")

    return render(
        request,
        "library/book_confirm_delete.html",
        {"book": book}
    )

    
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("user:login")

    if not request.user.is_staff:
        return redirect("library:book_list")

    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_reviews = Reviews.objects.count()
    avg_reviews = total_reviews/ total_users

    context = {
        "total_books": total_books,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_reviews": total_reviews,
        "average_reviews": avg_reviews,
    }

    return render(
        request,
        "library/dashboard.html",
        context
    )

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    reviews = book.reviews.select_related("user").order_by("-created")

    average_rating = reviews.aggregate(
        average=Avg("rating")
    )["average"]

    return render(
        request,
        "library/book_detail.html",
        {
            "book": book,
            "reviews": reviews,
            "average_rating": average_rating,
        }
    )
@login_required
def add_review(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        form = ReviewsForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.add_message(request,messages.SUCCESS,'Review Done')
            return redirect("library:book_detail", id=book.id)

    else:
        form = ReviewsForm()

    return render(
        request,
        "library/add_review.html",
        {
            "form": form,
            "book": book,
        }
    )
