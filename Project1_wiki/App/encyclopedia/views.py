from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/titlenotfound.html",{
            "title": title
            })
    else:
        return render(request, "encyclopedia/title.html", {
        "title": title,
        "body": util.get_entry(title)})


def create(request):
    return render(request, "encyclopedia/create.html")


