========================
Sustainable Souk Install 
========================

Getting the gears
=================

Postgresql database
-------------------

We will use postgresql as our database backend, therefore we need to install it

More info here, https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#creating-a-spatial-database-template-for-postgis,
however we this is the way to do it on an Ubuntu (10.10).

    sudo apt-get install binutils gdal-bin postgresql-8.4-postgis \
         postgresql-server-dev-8.4
         

Now we have to create the template to include spatial information on the database.
If you want to know everything, just read here 
https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#creating-a-spatial-database-template-for-postgis
otherwise there is ascript that can do it for you

    wget https://docs.djangoproject.com/en/dev/_downloads/create_template_postgis-debian.sh
    sudo -u postgres sh create_template_postgis-debian.sh

Ok, now we can create the user, the database and make sure we can connect
  
    sudo -u postgres createuser geouser
    sudo -u postgres createdb -O geouser -t template_postgis geodatabase
    sudo -u postgres psql -c "alter user geouser with password 'geopassword';"





We need be able to connect, even if our user is the one running the process..
This is for local development, so no worries.


Now change the line on this file /etc/postgresql/8.4/main/pg_hba.conf

From 

    local   all         all                               ident
    
To 

    local   all         all                               md5


and restart postgresql

    sudo /etc/init.d/postgresql restart

More info here http://www.depesz.com/index.php/2007/10/04/ident/


Python enviroment
------------------

Required packages:

- virtualenv http://pypi.python.org/pypi/virtualenv
- pip http://pypi.python.org/pypi/pip
- virtualenvwrapper http://www.doughellmann.com/projects/virtualenvwrapper/


If you have them install it skip, otherwise 

    sudo apt-get install python-pip

After that

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper

To finish up, make sure to add this two line to your bashrc (or anything that your
shell source)

    export WORKON_HOME=~/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

Creating the ssouk_env environment
==============================

To follow the tutorial, go to the original site!

http://invisibleroads.com/tutorials/geodjango-googlemaps-build.html

Ok, if you've got everything we need, let's go.

    mkvirtualenv --no-site-packages --distribute ssouk_env

This create a ssouk_env, with only the packages you need

switch to this environment

    workon ssouk_env

Clone the ssouk

    git clone git@github.com:ssouk/geodjango-googlemaps.git

Install all the stuff you need with

    pip install --requirement requirements.txt

Synch the tables in the database

    python manage.py syncdb 
    
Run it!

    python manage.py runserver
    
Done. :)

Git is your friend
==================

Check out the doc for git under the docs folder
https://github.com/ssouk/ssouk_web/blob/master/docs/How_to_merge_with_git.md



