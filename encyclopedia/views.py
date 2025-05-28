from django.shortcuts import render
from markdown import markdown
from . import util



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
            return showEntry(request, title, content)

def viewPage(request, title):
    content =  util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return showEntry(request, title, content)
    
       
def showEntry(request, title,content):
        content= markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


