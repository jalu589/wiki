from http.client import HTTPResponse
from imaplib import Time2Internaldate
from django.shortcuts import render
from . import util
import random


def index(request):
    if 'q' in request.GET:
        title = request.GET.get('q')
        if util.get_entry(title):
            return render(request, "encyclopedia/entry.html", {
                "text": util.get_entry(title)
            })
        else:
            return search(request, title)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message
    })


def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "text": util.get_entry(title)
        })
    else:
        return error(request, 'This entry does not exist')


def search(request, title):
    return render(request, "encyclopedia/search.html", {
        "matches": util.search_entries(title)
    })


def create(request):
    if request.method == "POST":
        title = request.POST.get('page-title')
        content = request.POST.get('page-content')

        if not title or not content:
            return error(request, 'Please enter a title and content')
        elif util.get_entry(title):
            return error(request, 'Page already exists')
        else:
            util.save_entry(title, content)
            return entry(request, title)

    return render(request, "encyclopedia/create.html")


def edit(request):
    if "page-title" in request.GET and "page-content" in request.GET:
        title = request.GET.get('page-title')
        content = request.GET.get('page-content')
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "text": content
        })
    elif request.method == "POST":
        new_title = request.POST.get('new-title')
        new_content = request.POST.get('new-content')
        util.save_entry(new_title, new_content)
        return entry(request, new_title)
    else:
        return render(request, "encyclopedia/edit.html")


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return entry(request, title)