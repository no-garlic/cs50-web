from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view(request, name):
    markdown = util.get_entry(name)

    if markdown is None:
        return render(request, "encyclopedia/error.html", {
            "name": name
        })

    converter = Markdown()
    html = converter.convert(markdown)

    return render(request, "encyclopedia/view.html", {
        "name": name,
        "content": html
    })
