from email.mime.text import MIMEText
from smtplib import SMTP
from slacker import Slacker


# Each notification function should take a list of winners (Option objects).
# Additional keyword arguments may be provided in config.py using a partial
# (these details are hidden from the VoteController).


def email(results, host, user, password, recipients, addendum=None):
    # Build message.
    winners = [
        '<li style="font-weight: bold; font-style: italic;">{}</li>'
        .format(o.name) if o.premium else '<li>{}</li>'.format(o.name)
        for o in results
    ]
    message = (
        '<p>Voting complete! Here are the results:</p><ul>{}</ul>'
        .format('\n'.join(winners))
    )

    if addendum:
        message += '<p>{}</p>'.format(addendum)

    message = MIMEText(message, 'html')
    message['subject'] = 'Vote: Results'
    message['to'] = ', '.join(recipients)

    # Set up SMTP.
    smtp = SMTP(host)
    smtp.starttls()
    smtp.login(user, password)

    # Send message.
    smtp.sendmail(user, recipients, message.as_string())

    smtp.close()


def slack(results, token, user, icon, recipient, addendum=None):
    s = Slacker(token=token)

    winners = ['*_' + o.name + '_*' if o.premium else o.name for o in results]
    message = 'Voting complete! Here are the results:\n\n' + '\n'.join(winners)

    if addendum:
        message += '\n\n' + addendum

    try:
        s.chat.post_message(recipient, message, username=user, icon_url=icon)
    except slacker.Error as e:
        print("Slack Error: {}".format(e))
