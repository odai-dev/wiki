from django.shortcuts import render
from markdown2 import markdown
from . import util
from django.http import HttpResponse



def index(request):
    title = request.GET.get("q")
    if not title:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        content =  util.get_entry(title)
        if content == None:
            entries =  util.list_entries()
            print(entries)
            return render (request, "encyclopedia/search.html", {
                "query": title ,
                "entries":  entries
            })
        else:
            return show_entry(request, title, content)


def view_page(request, title):
    content =  util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return show_entry(request, title, content)
    

def show_entry(request, title,content):
        content= markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")
        if title in util.list_entries():
            return HttpResponse('<h3 style="color:red;">ERROR: Entry title already exist</h3>')
        print(content)
        util.save_entry(title, content)
        return show_entry(request, title, content)
    
    return render(request, "encyclopedia/new_entry.html")

def edit_page(request, title):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")
        if not content:
            return HttpResponse('<h3 style="color:red;">ERROR: Entry content missing</h3>')
        util.save_entry(title, content)
        return show_entry(request, title, content)

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
        "title": title,
        "content": content
    })
       