export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y locales netcat-openbsd gcc gettext && \
	sed -i -e 's/# fa_IR UTF-8/fa_IR UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales && \
	apt-get clean

export LANG="fa_IR.UTF-8"
export LC_ALL="fa_IR.UTF-8"

cp -rT /src /app
rm -rf /src

cd /app

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

gunicorn config.wsgi:application --bind 0.0.0.0:8000
