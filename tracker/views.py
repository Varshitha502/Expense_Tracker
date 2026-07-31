from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, TransactionForm
from .models import Transaction


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    income = sum(
        t.amount for t in transactions if t.transaction_type == "Income"
    )

    expense = sum(
        t.amount for t in transactions if t.transaction_type == "Expense"
    )

    balance = income - expense

    context = {
        "transactions": transactions,
        "income": income,
        "expense": expense,
        "balance": balance,
    }

    return render(request, "dashboard.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("dashboard")

    else:
        form = TransactionForm()

    return render(request, "add_transaction.html", {"form": form})
from django.shortcuts import get_object_or_404

@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "add_transaction.html", {"form": form})
@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    transaction.delete()

    return redirect("dashboard")