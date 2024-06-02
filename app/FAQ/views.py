from flask import render_template
from flask_login import current_user
from app.utils.decorators import login_required, require_accept_community_guideline
from . import faq


@faq.route("/faq")
@login_required
@require_accept_community_guideline
def get_faq():
    return render_template("faq/faq.html", user=current_user)
