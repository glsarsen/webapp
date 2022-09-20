from app import app
from app.helpers import ensure_pages_directory_exists, get_page_url_name, get_page_display_name, is_valid_login
from flask import render_template, request, url_for, redirect, session
import markdown
import os


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pages")
def pages():
    ensure_pages_directory_exists()
    pages = os.listdir('pages')
    return render_template("pages.html", pages=pages)

@app.route("/pages/<page_name>")
def page(page_name):
    with open("pages/" + page_name + ".md", "r", newline="") as page_file:
        contents = page_file.read()
    html = markdown.markdown(contents)
    return render_template("page.html", page_name=page_name, contents=html)

@app.route("/new_page", methods=["GET", "POST"])
def new_page():
    if request.method == "GET":
        return render_template("new_page.html")
    
    if request.method == "POST":
        ensure_pages_directory_exists()
        title = request.form["title"]
        contents = request.form["contents"]
        with open("pages/" + get_page_url_name(title) + ".md", "w", newline="") as page_file:
            page_file.write(contents)
        return redirect(url_for("pages"))

@app.route("/edit_page/<page_name>", methods=["GET", "POST"])
def edit_page(page_name):
    if request.method == "GET":
        with open("pages/" + page_name + ".md", "r", newline="") as page_file:
            contents = page_file.read()
        title = get_page_display_name(page_name)
        return render_template("edit_page.html", page_name=title, contents=contents)
    
    if request.method == "POST":
        title = request.form["title"]
        contents = request.form["contents"]
        with open("pages/" + page_name + ".md", "w", newline="") as page_file:
            page_file.write(contents)
        return redirect(url_for("page", page_name=page_name))

@app.route("/delete_page/<page_name>", methods=["GET", "POST"])
def delete_page(page_name):
    if request.method == "GET":
        return render_template("delete_page.html")
    
    if request.method == "POST":
        os.remove("pages/" + page_name + ".md")
        return redirect(url_for("pages"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["pwd"]
        if is_valid_login(user_name, password):
            session["username"] = user_name
            return redirect(url_for("index"))
        return redirect(url_for("index"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        return render_template("logout.html")
    if request.method == "POST":
        if "username" in session:
            session.pop("username")
        return redirect(url_for("index"))
