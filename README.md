# Ecommerce System Backend

A robust Django REST API backend for an ecommerce platform, featuring user authentication, product management, order processing, and payment integration.

## Features

- **User Management**: Registration, login, and profile management with JWT authentication
- **Product Management**: CRUD operations for products with categories
- **Order Management**: Create and manage customer orders
- **Payment Integration**: Support for Stripe and bKash payment gateways
- **Admin Dashboard**: Administrative features for managing the platform
- **API Documentation**: Swagger/OpenAPI documentation with drf-yasg

## Tech Stack

- **Backend**: Django 6.0
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Payment Gateways**: Stripe, bKash
- **Documentation**: drf-yasg (Swagger)

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

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/profile/` - Get user profile

### Products
- `GET /api/products/` - List products
- `POST /api/products/` - Create product (Admin)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (Admin)
- `DELETE /api/products/{id}/` - Delete product (Admin)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (Admin)
- `GET /api/categories/categories/tree/` - Get category tree

### Orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/my-orders/` - Get user orders

### Payments
- `POST /api/payments/pay/{order_id}/` - Initiate payment
- `GET /api/payments/all/` - List all payments (Admin)
- `POST /api/payments/stripe/webhook/` - Stripe webhook

## Testing

Run the test suite:
```bash
python manage.py test
```

## API Documentation

Access the API documentation at `http://localhost:8000/swagger/` when the server is running.

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.
