from django.shortcuts import render
from django.contrib.auth.models import User


def search(request):

    query = request.GET.get("q")

    users = []

    if query:

        users = User.objects.filter(
            username__icontains=query
        )

    return render(
        request,
        "search/search.html",
        {
            "users": users,
            "query": query,
        },
    )