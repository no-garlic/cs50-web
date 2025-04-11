import random
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from markdown2 import Markdown
from . import util


class AddForm(forms.Form):
    """Form for adding a new encyclopedia entry."""
    title = forms.CharField(
        label='', 
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the title for the new page in plain text.", 
                   "class": "title-entry"}))
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(
            attrs={"placeholder": "Enter the content for the new page in markdown format."}))


class EditForm(forms.Form):
    """Form for editing an existing encyclopedia entry."""
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(
            attrs={"placeholder": "Enter the content for the new page in markdown format."}))


class SearchForm(forms.Form):
    """Form for searching encyclopedia entries."""
    title = forms.CharField(
        label='', 
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Search", 
                   "class": "search"}))


def index(request):
    """Render the index page with a list of all encyclopedia entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def view(request, title):
    """Render a specific encyclopedia entry by its title."""
    # get the content for the entry
    markdown = util.get_entry(title)

    # if the entry does not exist, redirect to the index page
    if markdown is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "search_form": SearchForm()
        })

    # convert the markdown to HTML
    converter = Markdown()
    html = converter.convert(markdown)

    # render the view page
    return render(request, "encyclopedia/view.html", {
        "title": title,
        "content": html,
        "search_form": SearchForm()
    })


def search_results(request):
    """Handle search requests and display matching results or an error."""
    if request.method == "POST":
        form = SearchForm(request.POST)

        # check if the form is valid
        # if the form is not valid then return to the index page
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)

            # if the entry exists, redirect to the view page
            # otherwise, search for partial matches
            if entry:
                return redirect(reverse("view", args=[title]))
            else:
                # search for partial matches
                # if the search term is empty, return to the index page
                search_results = util.partial_search(title)
                return render(request, "encyclopedia/search.html", {
                    "search_term": title,
                    "search_results": search_results,
                    "search_form": SearchForm(),
                })
            
    # if the form is not valid or the method is not POST then return to the index page
    messages.info(request, "Invalid search request.")
    return redirect(reverse('index'))


def add(request):
    """Handle adding a new encyclopedia entry."""
    # send the form temlates to the client
    if request.method == "GET":
        # if the request contains the title parameter, then initialise the form with that title
        title = request.GET.get("title")
        if title:
            form = AddForm(initial={"title": title})
        else:
            form = AddForm()
        
        # render the add page with the form
        return render(request, "encyclopedia/add.html", {
            "add_form": form,
            "search_form": SearchForm(),
        })
    # if the method is POST then process the form
    elif request.method == "POST":
        form = AddForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        else:
            # if the form is not valid then return to the add page
            messages.error(request, f'Failed validation adding entry "{form.cleaned_data.get("title", "")}"')
            return render(request, "encyclopedia/add.html", {
                "add_form": form,
                "search_form": SearchForm(),
            })
        
        # check if an entry already exists with the same title
        if util.get_entry(title):
            # if the entry already exists, return to the add page
            messages.error(request, f'The entry "{title}" already exists.')
            return render(request, "encyclopedia/add.html", {
                "add_form": form,
                "search_form": SearchForm(),
                "error": f'The entry "{title}" already exists.'
            })

        # save the entry
        util.save_entry(title, content)
        messages.success(request, f'Successfully created the new entry "{title}"')

        # redirect to the view page for the new entry
        return redirect(reverse("view", args=[title]))
    else:
        # if the method is not GET or POST then return an error
        return HttpResponse("Method not allowed", status=405)


def edit(request, title):
    """Handle editing an existing encyclopedia entry."""
    if request.method == "GET":
        # if the entry does not exist, redirect to the index page
        content = util.get_entry(title)
        if not content:
            messages.error(request, f'The page "{title}" does not exist.')
            return redirect(reverse('index'))

        # render the edit page with the current content
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": EditForm(initial={"content": content}),
            "search_form": SearchForm()
        })

    # if the method is POST then process the form
    elif request.method == "POST":
        form = EditForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # save the entry
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            messages.success(request, f'Saved the entry "{title}" successfully.')

            # redirect to the view page for the entry
            return redirect(reverse("view", args=[title]))

        else:
            # if the form is not valid then return to the edit page
            messages.error(request, f'Failed to save the entry "{title}".')
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": form,
                "search_form": SearchForm()
            })
    else:
        # if the method is not GET or POST then return an error
        return HttpResponse("Method not allowed", status=405)


def random_page(request):
    """Redirect to a random encyclopedia entry."""
    # get the list of entries
    entries = util.list_entries()

    # if there are entries then select a random entry
    # and redirect to its view page
    if len(entries) > 0:
        title = random.choice(entries)
        return redirect(reverse("view", args=[title]))

    # if there are no entries then go to the index page
    messages.info(request, "No entries available.")
    return redirect(reverse('index'))
