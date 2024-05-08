from flask import render_template
from app.utils.decorators import login_required
from . import notification

@notification.route('/notifications')
@login_required
def notifications():
    return render_template('notifications/notification.html')