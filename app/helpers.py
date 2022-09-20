from app import app
import os

def ensure_pages_directory_exists():
    if not os.path.exists("pages"):
        os.makedirs("pages")

def is_valid_login(user_name, password):
    return True

@app.template_filter("filename")
def filename(text):
    return text.replace("_", " ").replace(".md", "")

@app.template_global("get_page_display_name")
def get_page_display_name(page_name):
    return page_name.replace("_", " ").replace(".md", "")

@app.template_global("get_page_url_name")
def get_page_url_name(page_name):
    return page_name.replace(" ", "_").replace(".md", "")
