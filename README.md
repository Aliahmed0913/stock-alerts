# Stock Alerts Django Project

A Django stock price alert system for managing user defined alert rules and receiving notifications.

## Features

- User registration and authentication
- Create, update, and delete stock alert rules
- Threshold and duration-based alert evaluation
- Email notifications on triggered alerts
- Environment variable management with `.env`
- REST API for frontend integration

## Tech Stack

- Python
- Django & Django REST Framework
- SimpleJWT
- SQLite (default)
- Redis
- Celery

- ## Setup & Run Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create and activate virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load sample seed data (optional):**
   ```bash
   python manage.py loaddata seed_data.json
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoint List

| Endpoint                        | Method | Description                          |
|---------------------------------|--------|------------------------------------- |
| `users/register`                | POST   | Create a new user                    |
| `users/token/`                  | POST   | Create access token                  |
| `users/token/refresh/`          | POST   | Referesh access token                |
| `users/me`                      | GET    | Retrieve a user information          |
| `users/me/notification-settings`| GET    | Retrieve a user notification settings|
| `alerts/`                       | GET    | List all alerts for request user     |
| `alerts/`                       | POST   | Create a new stock alert             |
| `alerts/<id>/`                  | PATCH  | Update stock alert                   |
| `alerts/<id>/`                  | DELETE | Delete a stock alert by ID           |
| `alerts/triggered/`             | GET    | List triggered alert for request user|


## Sample Seed Data

Here is an example JSON snippet you can save as `seed_data.json` to load sample data into your database:

```json
[
  {
    "model": "User.user",
    "pk": 1,
    "fields": {
      "username": "admin",
      "password": "pbkdf2_sha256$216000$...",
      "email": "admin@example.com",
    }
  },
  {
    "model": "alerts.alert",
    "pk": 2,
    "fields": {
      "user": 1,
        "stock_symbol": "TSLA",
        "alert_type": "threshold",
        "comparison": ">",
        "target_price": "50.50",
        "duration": "00:00:00",
    }
  }
]
```

# Stock Alerts Django Project — Deployment Guide

This guide explains how to deploy the Stock Alerts Django app on a remote server.

## Prerequisites

- Remote server with SSH access (Ubuntu EC2 instance)
- Python installed
- Git installed
- Redis installed

## Deployment Steps

### 1. Connect to your server

```bash
ssh -i path.to.keyPair ubuntu@your-server-ip
```

### 2. Clone your repository

```bash
git clone https://github.com/Aliahmed0913/stock-alerts.git
cd stock-alerts/stock_alerts
```

### 3. Set up virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up `.env` file on the server

Create `.env` with production secrets:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql://user:password@localhost:3306/yourdb
EMAIL_HOST=...
EMAIL_PORT=...
# other secrets
```

### 6. Apply database migrations

```bash
python manage.py migrate
```


### 7. Configure Gunicorn service

Create a systemd service file `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/stock-alerts/stock_alerts
ExecStart=/path/to/stock-alerts/stock_alerts/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8000 stock_alerts.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:

```bash
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 8. Configure Nginx as reverse proxy

Create `/etc/nginx/sites-available/stock_alerts`:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/stock-alerts /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configure celery worker service

Create celery systemd file `sudo nano /etc/systemd/system/celery.service`
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=ubuntu
WorkingDirectory=/home/ubuntu/stock-alerts
EnvironmentFile=/home/ubuntu/stock-alerts/.env
ExecStart=/home/ubuntu/stock-alerts/venv/bin/celery -A stock_alerts multi start worker -l info --pidfile=/home/ubuntu/celery.pid
ExecStop=/home/ubuntu/stock-alerts/venv/bin/celery multi stopwait worker --pidfile=/home/ubuntu/celery.pid
Restart=always

[Install]
WantedBy=multi-user.target
```

### 10. Configure celery beat service

Create celery-beat systemd file `sudo nano /etc/systemd/system/celery-beat.service`

```ini
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/stock-alerts
EnvironmentFile=/home/ubuntu/stock-alerts/.env
ExecStart=/home/ubuntu/stock-alerts/venv/bin/celery -A stock_alerts beat -l info
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable and start celery worker and celery-beat:

```bash
sudo systemctl daemon-reload
sudo systemctl enable celery
sudo systemctl enable celery-beat
sudo systemctl start celery
sudo systemctl start celery-beat
```
