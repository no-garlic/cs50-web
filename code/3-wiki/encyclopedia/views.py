import random
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from markdown2 import Markdown
from . import util


class AddForm(forms.Form):
    title = forms.CharField(
        label='', 
        widget=forms.TextInput(
            attrs={"placeholder": "Page Title"}))
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(
            attrs={"placeholder": "Page Content"}))


class EditForm(forms.Form):
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(
            attrs={"placeholder": "Page Content"}))


class SearchForm(forms.Form):
    title = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={"class": "search", "placeholder": "Enter Search"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def view(request, title):
    markdown = util.get_entry(title)
    if markdown is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "search_form": SearchForm()
        })

    converter = Markdown()
    html = converter.convert(markdown)
    return render(request, "encyclopedia/view.html", {
        "title": title,
        "content": html,
        "search_form": SearchForm()
    })


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
    # if the form is not valid or the method is not POST then return to the index page
    return redirect(reverse('index'))


def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "add_form": AddForm(),
            "search_form": SearchForm(),
        })

    elif request.method == "POST":
        form = AddForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        else:
            messages.error(request, 'Failed validation adding entry "{title}"')
            return render(request, "encyclopedia/add.html", {
                "add_form": form,
                "search_form": SearchForm(),
            })

        util.save_entry(title, content)
        messages.success(request, '"Sucessfully created the new entry "{title}"')
        return redirect(reverse("view", args=[title]))


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if not content:
            messages.error(request, f'The page "{title}" does not exist.')

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": EditForm(initial={"content": content}),
            "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            messages.success(request, f'Saved the entry "{title}" sucessfully.')
            return redirect(reverse("view", args=[title]))

        else:
            messages.error(request, f'Failed to save the entry "{title}".')
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": form,
                "search_form": SearchForm()
            })


def random_page(request):
    entries = util.list_entries()
    if len(entries) > 0:
        title = random.choice(entries)
        return redirect(reverse("view", args=[title]))

    # if there are no entries then go to the index page
    return redirect(reverse('index'))


