# Introduction

## Project Structure

Here's an overview of the key components of the project:

- **Django App (bdio-app)**: The main application built with Django.
- **PostgreSQL (bdio-db)**: A PostgreSQL database for storing application data.
- **Redis**: Used for caching and as a message broker for Celery.
- **Celery**: A distributed task queue used for running asynchronous tasks.
- **Flower**: A web-based tool for monitoring Celery tasks.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone The Repository

```bash
git clone https://github.com/ProOnDesk/nauczajka-back.git
cd .\bdio-back\
```

### 2. Set Up Environment Variables

Create a .env file in the project root directory with necessary environment variables. Below is an example of what the .env should have

```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DJANGO_SECRET_KEY=6_446v2p0$8tfg_m_4tna7v$-^lo3+8zc*ktlbsk@j$$k_0izp
POSTGRES_DB=maciek_PL
POSTGRES_USER=maciek_PL
POSTGRES_PASSWORD=maciek_PL
DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=maciek_PL
DB_USER=maciek_PL
DB_PASSWORD=maciek_PL
DB_HOST=bdio-db
DB_PORT=5432
ADMIN_EMAIL=adminek@adminek.pl
ADMIN_PASSWORD=DjangoToSuperFramework
AUTH_COOKIE_SECURE=False
REDIRECT_URLS=http://localhost:3000/auth/google http://localhost:3000/auth/facebook
GOOGLE_AUTH_KEY=
GOOGLE_AUTH_SECRET_KEY=
EMAIL_USER=
EMAIL_PASS=
```

#### How to Get EMAIL_USER and EMAIL_PASS:

- **If you're using Gmail**:

  1. **EMAIL_USER**: Your Gmail address (e.g., `your-email@gmail.com`).
  2. **EMAIL_PASS**: If you have two-factor authentication enabled on your account, you'll need to generate an app-specific password:
     - Go to your [Google Account](https://myaccount.google.com/security).
     - Under "Signing in to Google," select **App Passwords**.
     - Choose **Other (Custom name)**, label it something like "Django App," and generate an app password.
     - Use this generated password as your **EMAIL_PASS**.

- **If you're using other email providers**:

  1. **EMAIL_HOST**: You must first update your Django settings to configure the correct email server. For example, to use Gmail, update `EMAIL_HOST` in your `./bdio_backend/bdio_backend/settings.py` file:

     ```python
     EMAIL_HOST = 'smtp.gmail.com'
     ```

     For other providers like Yahoo or Outlook, replace `'smtp.gmail.com'` with their respective SMTP host (e.g., `smtp.mail.yahoo.com` or `smtp.office365.com`).

  2. **EMAIL_USER**: Your email address from the email provider (e.g., `your-email@yahoo.com` or `your-email@outlook.com`).
  3. **EMAIL_PASS**: The password or an app-specific password from your email provider, similar to how it's done with Gmail.

##### Example for Gmail:

```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=generated-app-password
```

#### How to Get GOOGLE_AUTH_KEY and GOOGLE_AUTH_SECRET_KEY:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing project).
3. In the **APIs & Services** section, go to **Credentials** and create **OAuth 2.0 Client IDs**.
4. For the **Authorized Redirect URIs**, use the URL where your application will handle the Google login response, such as:

   - `http://localhost:8000/accounts/google/login/callback/`

5. After creating the credentials, you will get:
   - **GOOGLE_AUTH_KEY**: Your client ID.
   - **GOOGLE_AUTH_SECRET_KEY**: Your client secret.

##### Example:

```env
GOOGLE_AUTH_KEY=your-google-client-id
GOOGLE_AUTH_SECRET_KEY=your-google-client-secret
```

### 3. Build and Run the Containers

Open a terminal and run the following command:

```bash
docker-compose up --build
```

### 4. Accessing The Application

Once the services are running, you can access the Django application using the following URLs:

- **Main Application**: `http://localhost:8000`
- **API Documentation (Swagger)**: `http://localhost:8000/api/swagger/docs`  
  Access detailed API documentation via Swagger.
- **Admin Panel**: `http://localhost:8000/admin`  
  Log into the Django Admin Panel to manage the application.

The Flower monitoring tool for Celery tasks will be available at:

- **Celery Monitoring (Flower)**: `http://localhost:5555`  
  Flower provides real-time monitoring of Celery tasks.

### 5. Stopping the Containers

To stop all running services, use the following command:

```bash
docker-compose down
```

#### Creating a Superuser for the Admin Panel

To access the Django Admin Panel, you'll need to create a superuser account. You can do this by running the following command inside the `bdio-app` container:

1. **Access the Container**:

   ```bash
   docker-compose exec bdio-app sh
   ```

2. **Create a Superuser**
   ```sh
   python manage.py createsuperuser
   ```
   Follow the prompts to enter the username, email, and password for the superuser account.
