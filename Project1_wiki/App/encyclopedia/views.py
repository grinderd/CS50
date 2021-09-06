from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util


class CreateEntryForm(forms.Form):
    Title = forms.CharField(label='title')
    Entry = forms.TextField(label='entry')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/entrynotfound.html",{
            "title": title
            })
    else:
        return render(request, "encyclopedia/displayentry.html", {
        "title": title,
        "body": util.get_entry(title)})


def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Title"]
            entry = form.cleaned_data["Entry"]
            entry_ls = util.list_entries()
            if title in entry_ls:
                pass
            else:
                with open(f'{title}.md, 'w') as f:
                    f.write(entry)
                return render(request, "")
    return render(request, "encyclopedia/create.html",{
        "form":form
    })


def entrysearch(request):
    entry_ls = util.list_entries()
    if request.method == "POST":
        if request.POST['q'] in entry_ls:
            return HttpResponseRedirect(request.POST["q"])
        else:
            fltr_list = []
            for ent in entry_ls:
                if request.POST['q'] in ent:
                    fltr_list.append(ent)

            return render(request, "encyclopedia/search.html",{
                "fltr_list": fltr_list
            })


