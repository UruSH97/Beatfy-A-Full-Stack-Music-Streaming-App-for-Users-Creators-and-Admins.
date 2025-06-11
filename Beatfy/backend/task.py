from backend.models import User, Song, Album
from backend.mail import send_mail
from celery.schedules import crontab
from backend.models import User
from backend.worker import celery
from jinja2 import Template 
import datetime


def get_report(templateFile, song_details, username):
    with open(templateFile) as fileTemp:
        template = Template(fileTemp.read())
        html_report = template.render(song_details=song_details, username=username)
        return html_report

  
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls deadlineReminder.s() daily.
    sender.add_periodic_task(10, daily_reminder.s(), name='DailyReminder') 

    # Calls monthReport.s() on 1st day of the month.
    sender.add_periodic_task(10, monthly_report.s(), name='MonthlyReport')

    sender.add_periodic_task(
        crontab(minute=0, hour=19, day_of_month='*'),
        daily_reminder.s(),
        name = 'Daily reminder everyday @7PM via mail.'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        monthly_report.s(),
        name = 'Monthly Music Report @1st of every month via mail.'
    )


@celery.task
def daily_reminder():
    users = User.query.all()
    for user in users:
        if user.last_login < datetime.datetime.now():
            reciver_mail = user.email
            send_mail(reciver_mail, subject="Daily Reminder", message="Hey! Visit Beatfy.")
    return "Reminder done!"


@celery.task
def monthly_report(): 
    users = User.query.filter_by(is_creator = True).all()
    for user in users:
        username = user.username
        usermail = user.email

        songs = Song.query.filter_by(user_id = user.user_id).all()
        albums = Album.query.filter_by(user_id = user.user_id).all()

        song_details = []

        for song in songs:
            song_detail = []
            song_detail.append(song.name)
            song_detail.append(song.artist)
            song_detail.append(song.ratings)

            song_details.append(song_detail)

        msg = get_report("src/monthly_report.html", song_details, username)

        send_mail(usermail, subject="Monthly Report", message = msg, content="html")
    return "Reports Sent!"

