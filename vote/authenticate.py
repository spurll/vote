from ldap3 import Server, Connection
from json import loads
import requests

from vote import app
from vote.models import User


def authenticate(username, password):
    if app.config.get('AUTH_METHOD', 'ldap').lower() == 'ldap':
        return ldap(username, password)
    else:
        return auth(username, password)


def ldap(username, password):
    user = None
    message = None

    # Initial connection to the LDAP server.
    server = Server(app.config['LDAP_URI'])
    connection = Connection(server)

    try:
        if not connection.bind(): return None

        # Verify that the user exists.
        result = connection.search(search_base=app.config['LDAP_SEARCH_BASE'],
                                   search_filter='(uid={})'.format(username),
                                   attributes=['mail', 'cn'])

        if not result: return None

        # The user exists!
        name = connection.response[0]['attributes']['cn'][0]
        email = connection.response[0]['attributes']['mail'][0]

        # Now attempt to re-bind and authenticate with the password.
        distinguished_name = connection.response[0]['dn']
        connection = Connection(server, user=distinguished_name,
                                password=password.encode('iso8859-1'))

        if not connection.bind(): return None

        # We're authenticated! Create the actual user object.
        user = User(id=username, name=name, email=email)
    
    except Exception as e:
        message = e

    finally:
        connection.unbind()
        return user, message


def auth(username, password):
    user = None
    message = None

    data = {'id': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    r = requests.post(app.config['AUTH_URI'], json=data, headers=headers)

    if r.status_code == 200:
        json = loads(r.text)
        user = User(id=json['id'], name=json['name'], email=json['email'])
    else:
        message = r.text

    return user, message

