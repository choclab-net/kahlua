find . -type d -exec chmod -R 775 {} \;
find . -type f -exec chmod -R 664 {} \;
find . -exec chown -R nginx:nginx {} \;
chmod +x manage.py migrate.bash
if [ "$1" = 'migrate' ]; then
    ./manage.py makemigrations
    ./manage.py migrate
fi

