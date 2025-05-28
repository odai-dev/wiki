from django.shortcuts import render
from . import util  
from django.http import HttpResponse
import random  
import re  

# View for the index page (homepage)
def index(request):
    title = request.GET.get("q")  # Check if there's a search query
    if not title:
        # If no search, display all entries
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        # If search query exists, check for exact match
        content = util.get_entry(title)
        if content is None:
            # If no exact match, render search results with all entries
            entries = util.list_entries()
            print(entries)  # Debugging line
            return render(request, "encyclopedia/search.html", {
                "query": title,
                "entries": entries
            })
        else:
            # If exact match found, show the entry
            return show_entry(request, title, content)

# View for displaying a specific entry page by title
def view_page(request, title):
    content = util.get_entry(title)
    if content is None:
        # If the entry doesn't exist, show error page
        return render(request, "encyclopedia/error.html")
    else:
        # If it exists, show the entry
        return show_entry(request, title, content)

# Helper function to render an entry using Markdown to HTML conversion
def show_entry(request, title, content):
    content = markdown_to_html(content)  # Convert Markdown to HTML
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

# View for creating a new entry
def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")
        if title in util.list_entries():
            # Prevent duplicate titles
            return HttpResponse('<h3 style="color:red;">ERROR: Entry title already exists</h3>')
        print(content)  # Debugging line
        util.save_entry(title, content)
        return show_entry(request, title, content)
    
    # If GET request, show new entry form
    return render(request, "encyclopedia/new_entry.html")

# View for editing an existing entry
def edit_page(request, title):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")
        if not content:
            return HttpResponse('<h3 style="color:red;">ERROR: Entry content missing</h3>')
        util.save_entry(title, content)
        return show_entry(request, title, content)

    # If GET request, show edit form with current content
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

# View for displaying a random entry
def random_page(request):
    random_title = random.choice(util.list_entries())  # Pick a random entry
    content = util.get_entry(random_title)
    return show_entry(request, random_title, content)

# Optional: Custom Markdown to HTML converter (if not using markdown2)
def markdown_to_html(markdown):
    # Convert # headings to <h1>
    markdown = re.sub(r'^# (.*)', r'<h1>\1</h1>', markdown, flags=re.MULTILINE)
    
    # Convert **bold** to <strong>
    markdown = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown)

    # Convert * list items to <ul><li>
    lines = markdown.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        if line.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if line.strip() != "":
                html_lines.append(f"<p>{line}</p>")
    
    if in_list:
        html_lines.append("</ul>")  # Close any open list

    markdown = "\n".join(html_lines)

    # Convert [text](link) to <a href="link">text</a>
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)

    return markdown
