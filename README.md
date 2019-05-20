# kahlua
## A wagtail theme for a website about a dog.
![Kahlua homepage](/screenshots/homepage.png)

## About
This site can be used as a resume and blog and features a (relatively) responsive layout with full-screen background
images.

The colour scheme is predominantly chocolate (RGB: 78,46,40) and sand (RGB: 205,180,140) and all images featured are of
my dog Kahlúa.

This website is hosted at https://kahlua.choclab.net.

## Installation

This site uses a Jenkinsfile pipeline for deployment and installation of the site. Although not (currently) provided,
stub calls for unit, integration, load and smoke tests are included within this pipeline (one day, I might even add some).

I provide additional scripts in the etc folder within this repo.

1. A systemctl script for running the development server. Change this to match your requirements and install it as  per
   the instructions below
2. NGINX settings proxying to the development server
3. A site restart script to allow users the ability to restart their own development server without root privs.

> **Note**
> I only ever develop on Linux and my development server environment is Centos 7.
> I cannot help you with setting this up under a Windows development environment.

### Systemctl script (kahlua.service)
1. Edit this file to point to your virtualenv python and workspace and set the port to something suitable (default 8089)
2. copy this file to /usr/lib/systemd/system/
3. execute `systemctl enable kahlua`

> Make sure you change or remove every instance of `<HOSTNAME>`

### NGINX settings
1. Edit this file and set the hostname and port you are running the kahlua.service on
2. Copy this file to /etc/nginx/conf.d or /etc/nginx/sites.d (depending on your setup)
3. Set up your self signed or letsencrypt certs (`certbot --nginx -d <HOSTNAME> -d <ALT_HOSTNAME>`)

> Make sure you change or remove every instance of `<HOSTNAME>`

### site script
The site script allows users in a particular group to start/stop the python development server.

1. Edit this file and set `<DOMAIN>` as appropriate
2. Copy etc/site to /usr/local/bin
3. Set the executable bit `chmod +x /usr/local/bin/site`
4. Create a group to execute this file as `groupadd site`
5. Add users to this group `usermod -G site <USERNAME>`
6. Edit the sudoers file and add a line to allow the site group to execute site without a password
   `%site   ALL=(ALL)       NOPASSWD: /usr/local/bin/site`

### Jenkins setup
> This assumes you already know how to install and configure Jenkins

Add credentials for

* development server SSH `choclab.dev`
* production server SSH `choclab-prod`
* your git account SSH `choclab-git`
* Your git account HTTPS

Create a new Jenkins pipeline job and link it to your git repository.

This pipeline pretty much uses a vanilla install of Jenkins with community recommended plugins + HTML Publisher and ssh-agent.

Once the pipeline has been installed, execute it from Jenkins either by manual build now or git hook for either master
or develop.

If deploying to shared host; you will need to restart the python application once the deployment is complete.

### CPANEL
You will need to set up a Python app in CPanel with the following settings:

1. Python version: 3.7
2. App URI: `<DOMAIN_NAME>/`
3. WSGI File location: BLANK

Save the settings and start your application.

## MySQL
I have built this site to run with a MySQL database on shared hosting. This causes issues with MySQL connectivity from
django which predominantly wants to use the mysqlclient library. Good luck getting this to work on a shared host...

Instead, we use the mysql-connector-python library which provides a django module. To make this work, we need to run in
pure python mode. This can be set up by setting `'use_pure': True` under the database `OPTIONS`.

#### Example
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': CONFIG.dbname,
            'USER': CONFIG.dbuser,
            'HOST': CONFIG.dbhost,
            'PASSWORD': CONFIG.dbpass,
            'OPTIONS': {
                'autocommit': True,
                'use_pure': True,   # Required for shared hosting
            }
        }
    }

Configuration settings for the database and secret key are loaded from a file in `${HOME}/etc/kahlua.json`. If this file
does not exist, it will be created when the `makemigrations` step is executed. This will cause the pipeline to fail.
When this happens, log on to your host, populate the file with your database credentials and re-execute the pipeline.

#### Common database issues
**Character encoding.**
When setting up your database, you must use a utf-8 character encoding for the database tables. If you don't, your website
will not start up.

If you start seeing errors such as:

    django.db.utils.InterfaceError: (-1, 'Failed getting warnings; 2013 (HY000): Lost connection to MySQL server during query', None)

then log on to the database and check what character encoding you are using, then if necessary run the following to change
this to utf8mb4

    mysql -h <HOST> -u <USER> -p<PASS> -D <DATABASE> -e "ALTER DATABASE databasename CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    for table in $(
        mysql -h <HOST> -u <USER> -p<PASS> -D <DATABASE> -e "show tables" | awk '{ print $1 }' | tail -n +2
    ); do
        mysql -h <HOST> -u <USER> -p<PASS> -D <DATABASE> -e "ALTER TABLE $table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci";
    done

If you are using the C extension to mysql-connector-python, do not use utf8mb4 but use utf-8 only. Otherwise you will
hit an inifite loop whilst the connector waits for End of file that is never received.
