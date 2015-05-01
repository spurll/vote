Vote
====

A web application that allows users to place votes by ranking several options. Once votes are placed, the selection algorithm is highly configurable. Written in Python 3 (using Flask and SQLAlchemy) and JavaScript (using Sortable). Authentication is done via LDAP. voting system that makes use of a basic scoring (voting) method to select a restaurant to order lunch from or a game to play (or any number of other things). Can also send reminders and results via Slack messages.

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
* [Sortable](https://github.com/RubaXa/Sortable/)
* [slackutils](https://github.com/spurll/slackutils/) (optional, for notifications via Slack)

Configuration
-------------

You'll need a copy of [Sortable](https://github.com/RubaXa/Sortable/) in Vote's `vote/static/sortable`. I'd recommend cloning the repository to the location of your choice and then creating a symbolic link to it.

For example, if you have Vote installed to `~/Development/vote/` and you want to install Sortable to `~/Development/Sortable/`:

```sh
git clone git@github.com:RubaXa/Sortable.git ~/Development/Sortable
ln -s ~/Development/Sortable ~/Development/vote/vote/static/sortable
```

You'll also need to create a `config.py` file, which specifies details such as which method to use to select winning votes (instant runoff, Condorcet, etc.), how many winners to select, how to post notifications of the winners, etc. A sample configuration file can be found at `sample_config.py`.

Before starting the server for the first time, run `db_create.py`.

Starting the Server
-------------------

Start the server with `run.py`. By default it will be accessible at `localhost:9999`. To make the server world-accessible or for other options, see `run.py -h`.

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Need to create `sample_config.py`.

Known Bugs
----------

* The "Remember Me" option on the login page doesn't seem to work anymore.

Special Thanks
==============

Vote was based on the earlier [Lunch Voter](https://github.com/spurll/lunch). The `weighted_sample` selection function was designed by Eric Davies. [Curtis Vogt](https://github.com/omus) did quite a bit of work on the front end.

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).

This work makes use of [Sortable](http://rubaxa.github.io/Sortable) by [Lebedev Konstantin](mailto:ibnRubaXa@gmail.com) for ranking, licensed under the MIT License.

Fork-and-knife icon by [Freepik](http://www.freepik.com) from [Flaticon](http://www.flaticon.com), licensed under Creative Commons [BY 3.0](https://creativecommons.org/licenses/by/3.0/).

Remember: [GitHub is not my CV.](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/)
