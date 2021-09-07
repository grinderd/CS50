from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
import random
import markdown2

from . import util


class CreateEntryForm(forms.Form):
    Title = forms.CharField(label="Entry Title")
    Entry = forms.CharField(widget=forms.Textarea, label=mark_safe(" <br />Entry Body"))


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
            entry_title = form.cleaned_data["Title"]
            entry_bd = form.cleaned_data["Entry"]
            entry_ls = util.list_entries()
            if entry_title in entry_ls:
                pass
            else:
                # Writes entry to file
                f = open(f'entries/{entry_title}.md', 'w')
                f.write(entry_bd)
                f.close()
                return HttpResponseRedirect(reverse("index"))
    return render(request, "encyclopedia/create.html",{
        "form": CreateEntryForm()
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

            return render(request, "encyclopedia/search.html", {
                "fltr_list": fltr_list
            })


def editentry(request):
    if request.method == "POST":
        entry_title = request.POST['entry_title']
        entry_body = util.get_entry(entry_title)
        InitialData = {"Title": entry_title, "Entry": entry_body}
        EntryClass = CreateEntryForm(initial=InitialData)

        return render(request, "encyclopedia/entryedit.html", {
            "class": EntryClass
        })


def updateentry(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["Title"]
            entry_bd = form.cleaned_data["Entry"]
            entry_ls = util.list_entries()
            # Writes entry to file
            f = open(f'entries/{entry_title}.md', 'w')
            f.write(entry_bd)
            f.close()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "encyclopedia/entryedit.html", {
                "class": CreateEntryForm(request.Post)
            })
    else:
        return render(request, "encyclopedia/index.html")


def randomentry(request):
    entry_ls = util.list_entries()
    entry_ct = len(entry_ls)
    gen_num = random.randint(0,entry_ct-1)
    picked_entry = entry_ls[gen_num]
    return render(request, "encyclopedia/displayentry.html", {
        "title": picked_entry,
        "body": util.get_entry(picked_entry)})


