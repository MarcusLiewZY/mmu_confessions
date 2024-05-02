import os
from flask import render_template, request, flash
from flask_login import current_user
from app.utils.decorators import login_required, logout_required

from . import main
from app.models.user import User
from app.utils.helper import format_datetime

from dummy import post


@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = User.query.get(current_user.id)

    # if post method is used, create a post
    if request.method == "POST":
        from app.post.views import create_post

        print(post, current_user.id)
        if create_post(post, current_user):
            flash("Post created successfully", "success")
        else:
            flash("Post creation failed, please try again", "error")

    return render_template("main/index.html", user=user)


@main.route("/community-guideline")
@login_required
def community_guideline():
    return render_template("main/community_guidelines.html")

@main.route("/landing")
@logout_required
def landing():
    return render_template("main/landing.html")


@main.route("/playground")
def playground():
    # load a single file with multiple colors
    colors = [
        "red",
        "green",
        "blue",
        "black",
        "yellow",
        "purple",
        "orange",
        "pink",
        "brown",
        "gray",
    ]

    admin_svg_list = []

    svg_path = "app/static/svg/Cross.svg"

    with open(svg_path, "r") as svg_file:
        svg_content = svg_file.read()

    for color in colors:
        svg = svg_content.replace('fill="black"', f'fill="{color}"')
        admin_svg_list.append(svg)

    # load multiple file from a same directory
    svg_dir = "app/static/svg"
    svg_files = []

    for file_name in os.listdir(svg_dir):
        if file_name.endswith(".svg"):
            svg_path = os.path.join(svg_dir, file_name)

            with open(svg_path, "r") as svg_file:
                svg_content = svg_file.read()

            svg_files.append(svg_content)

    return render_template(
        "other/playground.html", admin_svg_list=admin_svg_list, svg_files=svg_files
    )
