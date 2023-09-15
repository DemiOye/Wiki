import re
import os
import markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def convert_md(content):
    f = open("encyclopedia/templates/encyclopedia/entry.html", "w")
    f.write('''{% extends "encyclopedia/layout.html" %}

    {% block title %}
        {{ title }}
    {% endblock %}

    {% block body %}
    <div class="entry-page">'''
    + markdown.markdown(content) +
    '''<div style="display: flex;">
            <a style="background-color: #3170f7" class="btn" href="Edit {{ title }} Page">Edit Page</a>
            <a style="background-color: red" class="btn" href="{{ title }} Page Deleted">Delete Page</a>
        </div>
    </div>
    {% endblock %}''')
    f.close()

def get_markdown(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
    for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry's markdown content by its title.
    The markdown is converted to HTML via retrun statement.
    If no such entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        entry_md = f.read().decode("utf-8")
        return convert_md(entry_md)
    except FileNotFoundError:
        return None
    
def delete_entry(title):
    """
    Deletes an encyclopedia entry by its title.
    """
    filename = f"entries/{title}.md"
    os.remove(filename)

