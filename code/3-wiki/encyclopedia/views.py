from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util


class NewEntryForm(forms.Form):
    name = forms.CharField(label="Name")
    content = forms.CharField(label="Content")


class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Enter Search"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def view(request, title):
    markdown = util.get_entry(title)

    if markdown is None:
        html = None
    else:
        converter = Markdown()
        html = converter.convert(markdown)

    return render(request, "encyclopedia/view.html", {
        "title": title,
        "content": html,
        "search_form": SearchForm()
    })


def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form,
                "search_form": SearchForm(),
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm(),
            "search_form": SearchForm(),
        })


def edit(request, title):
    pass


def random_page(request):
    entries = util.list_entries()
    if len(entries) > 0:
        page = random.choice(entries)
        return redirect("view", title=page)


def search_results(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)

            if entry:
                return redirect(reverse("view", args=[title]))
            else:
                search_results = util.partial_search(title)

                return render(request, "encyclopedia/search.html", {
                    "search_term": title,
                    "search_results": search_results,
                    "search_form": SearchForm(),
                })




