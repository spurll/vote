Vote
====

A web application that allows users to place votes by ranking several options. Once votes
are placed, the selection algorithm is highly configurable. Written in Python 3 (using
Flask and SQLAlchemy) and JavaScript (using Sortable). Authentication is done via LDAP.
Can also send reminders and results via Slack messages.

Usage
=====

Requirements
------------

* flask
* flask-login
* flask-wtf
* flask-sqlalchemy
* sqlalchemy
* ldap3
* numpy
* requests
* [Sortable](https://github.com/RubaXa/Sortable/)
* [slackutils](https://github.com/spurll/slackutils/) (optional, for notifications via
  Slack)

Configuration
-------------

[slackutils](https://github.com/spurll/slackutils/) must be cloned and installed with
`python3 setup.py install` (unfortunately someone else has grabbed the `slackutils`
project on PyPI, so you can't install it with `pip`).

[Sortable](https://github.com/RubaXa/Sortable/) is used as a Git submodule. To initialize
the submodule after cloning the Vote repository run:

```sh
git submodule init
git submodule update
```

You'll also need to create a `config.py` file, which specifies details such as which
method to use to select winning votes (instant runoff, Condorcet, etc.), how many winners
to select, how to post notifications of the winners, etc. A sample configuration file can
be found at `sample_config.py`.

Starting the Server
-------------------

Start the server with `run.py`. By default it will be accessible at `localhost:9999`. To
make the server world-accessible or for other options, see `run.py -h`.

If you're having trouble configuring your sever, I wrote a
[blog post](http://blog.spurll.com/2015/02/configuring-flask-uwsgi-and-nginx.html)
explaining how you can get Flask, uWSGI, and Nginx working together.

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Import/export of ballots/voting preferences (CSV or whatever).
* Ability to ignore selections from last time, this time.

Known Bugs
----------

* There seems to be an issue with `numpy` at the moment, though that may be a result of
  uWSGI doing multiple imports in different vassals, so other users may not be affected

Special Thanks
==============

Vote was based on the earlier [Lunch Voter](https://github.com/spurll/lunch). The
`weighted_sample` selection function was designed by
[Eric Davies](https://github.com/iamed2). [Curtis Vogt](https://github.com/omus) did
quite a bit of work on the front end.

License Information
===================

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

This work makes use of [Sortable](http://rubaxa.github.io/Sortable) by [Lebedev Konstantin](mailto:ibnRubaXa@gmail.com) for ranking, licensed under the MIT License.

Fork-and-knife icon by [Freepik](http://www.freepik.com) from [Flaticon](http://www.flaticon.com), licensed under Creative Commons [BY 3.0](https://creativecommons.org/licenses/by/3.0/).

Remember: [GitHub is not my CV.](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/)
