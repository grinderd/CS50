from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    render(request, "encyclopedia/title.html", {
    "title": title,
    "body": util.get_entry(title)})
