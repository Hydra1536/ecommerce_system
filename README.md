# Ecommerce System 

A robust Django REST API project for an ecommerce platform, featuring user authentication, product management, order processing, and payment integration.

## Features

- **User Management**: Registration, login, and profile management with JWT authentication
- **Product Management**: CRUD operations for products with categories
- **Order Management**: Create and manage customer orders
- **Payment Integration**: Support for Stripe and bKash payment gateways
- **Admin Dashboard**: Administrative features for managing the platform
- **API Documentation**: Swagger/OpenAPI documentation with drf-yasg

## Tech Stack

- **Backend**: Django 6.0
- **Frontend**: HTML
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Payment Gateways**: Stripe, bKash
- **Documentation**: drf-yasg (Swagger)

## Project Structure

```
backend/
├── accounts/          # User management
├── categories/        # Product categories
├── orders/           # Order management
├── payments/         # Payment processing
├── products/         # Product management
├── config/           # Django settings
└── templates/        # HTML templates
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce_system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

5. Run migrations:
```bash
cd backend
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

Access the API documentation at `http://localhost:8000/swagger/` when the server is running.

## Docker Setup

To run the application using Docker:

1. Ensure Docker and Docker Compose are installed.

2. Navigate to the backend directory:
```bash
cd backend
```

3. Build and start the services:
```bash
docker-compose up --build
```

This will start the PostgreSQL database and the Django backend.

4. To stop the services:
```bash
docker-compose down
```
## Unit Test Cases

Run the test suite:
```bash
python manage.py test
```

## Seeding the Database

To populate the database with sample data:

1. Seed categories and products:
```bash
python manage.py seed_data
```

2. Create a default admin user (email: admin@example.com, password: admin123):
```bash
python manage.py seed_admin
```

