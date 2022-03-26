from django.shortcuts import render, redirect
from school.models import Account


def account_list(request):
    accounts = Account.objects.all()
    data = {
        'accounts': accounts
    }
    return render(request, 'school/account/account_list.html', data)
