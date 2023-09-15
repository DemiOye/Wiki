from django.shortcuts import render
from django import forms
from django.shortcuts import redirect  
import random
from django.http import HttpResponse
from . import util
from django_bootstrap_markdown.widgets import MarkdownInput


#class NewEntryForm(forms.Form):
    #title = forms.CharField(label="Title", min_length=1, max_length=30)
    #content = forms.CharField(label="Content", min_length=1)

class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title", min_length=1, max_length=30)
    content = forms.CharField( widget=MarkdownInput )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random_page(request):
    entry_list = util.list_entries()
    random_entry = random.choice(entry_list)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": util.get_entry(random_entry)
    })

def search(request):
    entry_list = util.list_entries() 
    if request.method == "GET":
        search_query = request.GET.get('q').upper()
        for entry in entry_list:
            if entry.upper() == search_query:
                return render(request, "encyclopedia/entry.html", {
                    "title": entry,
                    "content": util.get_entry(entry)
                })
        for entry in entry_list:
            if entry.upper() != search_query:
                for entry in entry_list:
                    if search_query in entry.upper():
                        return render(request, "encyclopedia/search.html", {
                            "search": request.GET.get('q'),
                            "result": entry
                        })
                for entry in entry_list:
                    if search_query not in entry.upper():
                        return render(request, "encyclopedia/no entry.html", {
                            "title": request.GET.get('q')
                        })
                                         
def entry_page(request, entry_title):
    entry_list = util.list_entries()
    for entry in entry_list:
        if entry == entry_title:
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "content": util.get_entry(entry)
            })
    for entry in entry_list:
        if entry != entry_title:
            return render(request, "encyclopedia/no entry.html", {
                "title": entry_title
            })
        
def create_page(request):
    entry_list = util.list_entries()
    title = request.POST.get('title')
    content = request.POST.get('content')
    if request.method == 'POST':
        for entry in entry_list:
            if title.upper() == entry.upper():
                return render(request, "encyclopedia/create page.html", {
                    "entry_exists": True,
                    "existing_entry": entry
                })
        for entry in entry_list:
            if title.upper() != entry.upper():
                util.save_entry(title, content)
                return redirect(entry_page, entry_title = title)
    else:
        title = ""
        content = ""
        return render(request, "encyclopedia/create page.html")
    
def edit_page(request, entry_title):
    entry_list = util.list_entries()
    for entry in entry_list:
        if entry.upper() == entry_title.upper():
            return render(request, "encyclopedia/edit page.html", {
                "title": entry,
                "content": util.get_markdown(entry)
            })
    for entry in entry_list:
        if entry.upper() != entry_title.upper():
            return render(request, "encyclopedia/no entry.html", {
                "title": entry_title
            })
        
def delete_page(request, entry_title):
    entry_list = util.list_entries()
    for entry in entry_list:
        if entry_title.upper() == entry.upper():
            util.delete_entry(entry_title)
            return render(request, "encyclopedia/deleted.html", {
                "entry": entry
            })
    for entry in entry_list:
        if entry_title.upper() != entry.upper():
            return redirect(entry_page, entry_title = entry_title)
        
def save_page(request, entry_title):
    if request.method == 'POST':
        entry_list = util.list_entries()
        for entry in entry_list:
            if entry_title.upper() == entry.upper():
                content = request.POST.get('edit-content')
                util.save_entry(entry, content)
                return redirect(entry_page, entry_title = entry)
        for entry in entry_list:
            if entry_title.upper() != entry.upper():
                HttpResponse(f"ERROR 404: PAGE NOT FOUND")
    else:
        return HttpResponse(f"ERROR 404: PAGE NOT FOUND")
    
