# Rabah

## Set Up Environment Variables:

Create a .env file in the project root.

Add the following environment variables with appropriate values:

```shell
SECRET_KEY=<your_secret_key>
DEBUG=True
POSTGRESDB_NAME=<your_database_name>
POSTGRESDB_USER=<your_database_user>
POSTGRESDB_PASSWORD=<your_database_password>
POSTGRESDB_HOST=<your_database_host>
EMAIL_HOST=<your_email_host>
EMAIL_HOST_USER=<your_email_host_user>
EMAIL_HOST_PASSWORD=<your_email_host_password>
EMAIL_PORT=<your_email_port>
GOOGLE_CLIENT_ID=<your_google_client_id>
GOOGLE_SECRET_KEY=<your_google_secret_key>
```
Apply Database Migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Run the Development Server:

```bash
python manage.py runserver
```


#### Access the Application:
Open your web browser and go to http://127.0.0.1:8000/ to access the Rabah Django project.