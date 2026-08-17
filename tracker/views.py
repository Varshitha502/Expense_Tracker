from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

            messages.success(
                request,
                "Registration completed successfully!"
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f"Welcome {user.first_name or user.username}!"
            )

            return redirect("dashboard")

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")


def user_logout(request):
    logout(request)

    messages.info(
        request,
        "You have logged out successfully."
    )

    return redirect("home")


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "Income"
    )

    expense = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "Expense"
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

            messages.success(
                request,
                "Transaction added successfully."
            )

            return redirect("dashboard")

    else:
        form = TransactionForm()

    return render(request, "add_transaction.html", {"form": form})


@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Transaction updated successfully."
            )

            return redirect("dashboard")

    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "add_transaction.html",
        {
            "form": form
        }
    )


@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    transaction.delete()
    messages.success(
        request,
        "Transaction deleted successfully."
    )
    return redirect("dashboard")