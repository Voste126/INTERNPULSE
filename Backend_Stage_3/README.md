# Individual Task: Develop a RESTful Payment Gateway API for Small Businesses

## Objective

Create a basic RESTful API that enables small businesses to accept payments from customers using payment gateways such as PayPal, Paystack, or Flutterwave. The API should focus on minimal customer information, including:

- Name
- Email
- Payment amount

### Key Requirements

- **No user authentication**: The API should function without requiring user authentication.
- **Versioning**: Implement API versioning for better maintainability.
- **CI/CD**: Automate testing and deployment using Continuous Integration and Continuous Deployment pipelines.

## Endpoints

The API should follow RESTful best practices and include versioning.

### 1. Initiate a Payment

**Endpoint**: `POST /api/v1/payments`  
**Description**: Initiates a payment.  
**Request Body**:

```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
}
```

### 2. Retrieve Payment Status

**Endpoint**: `GET /api/v1/payments/{id}`  
**Description**: Retrieves the status of a specific payment transaction.  

**Example Response**:

```json
{
    "payment": {
        "id": "PAY-123",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": 50.00,
        "status": "completed"
    },
    "status": "success",
    "message": "Payment details retrieved successfully."
}
```

## Notes

- Ensure the API adheres to RESTful principles.
- Use proper HTTP status codes for responses.
- Include automated tests to validate functionality.
- Implement CI/CD pipelines for seamless deployment.
- Focus on simplicity and usability for small businesses.

## For Django Developers

### Task Details

#### Backend Setup

- Develop using Django REST Framework.
- Use a payment gateway plugin or manually integrate the payment API.

#### CI/CD Pipeline

- **Test**: Use Django's testing framework or `pytest-django` to verify payment processing and status checks.
- **Build**: Ensure the application builds and all dependencies are installed.
- **Deploy**: Deploy to platforms like Netlify, Vercel, Render, or similar.

#### Sample `.github/workflows/django.yml`

```yaml
name: Django CI

on:
    push:
        branches: [ main ]
    pull_request:
        branches: [ main ]

jobs:
    build:
        runs-on: ubuntu-latest
        strategy:
            max-parallel: 4
            matrix:
                python-version: [3.8]

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python ${{ matrix.python-version }}
            uses: actions/setup-python@v2
            with:
                python-version: ${{ matrix.python-version }}
        - name: Install Dependencies
            run: |
                python -m pip install --upgrade pip
                pip install -r requirements.txt
        - name: Run Tests
            run: |
                python manage.py test
```

---

### Deliverables

1. A functional RESTful API for processing payments with:
     - Versioning
     - No user authentication
     - Clear status messages
2. A CI/CD pipeline setup in GitHub Actions for automated testing and deployment.
3. Documentation detailing:
     - How to run the service locally
     - How to understand the tests
     - How to deploy using the CI/CD pipeline

## Payment Gateway API

This project implements a basic RESTful API for a payment gateway that allows small businesses to accept payments. It is built with Django REST Framework and uses Swagger for API documentation.

## Features

- **Endpoints**:
  - **POST /api/v1/payments**: Initiate a payment.
  - **GET /api/v1/payments/{id}**: Retrieve the status of a payment.
- **API Versioning**: All endpoints are versioned (v1).
- **Swagger Documentation**: Accessible at  `/redoc/`.
- **No User Authentication**: The API functions without requiring user authentication.
- **CI/CD Ready**: Includes a sample GitHub Actions workflow for testing and deployment.

Below is an example README.md section with setup instructions that you can include in your repository:

---

## Setup Instructions

Follow these steps to set up your development environment, configure your PostgreSQL database using an `.env` file, run migrations, and execute your test cases using pytest.

### 1. Clone the Repository and Create a Virtual Environment

Open your terminal and run the following commands:

```bash
git clone https://github.com/Voste126/INTERNPULSE
cd Backend_Stage_3
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Create and Configure the `.env` File

In the root of the `Backend_Stage_3` directory, create a file named `.env` with the following content. Adjust the values as needed for your PostgreSQL setup:

```dotenv
# Optional: Use DATABASE_URL for production or Render deployments
# DATABASE_URL=

# Local PostgreSQL configuration
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 3. Update Django Settings to Load Environment Variables

Ensure that your Django settings load environment variables from the `.env` file. At the top of your `settings.py`, add the following:

```python
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import dj_database_url

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "PulseDB"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# Optional: Override the test database name when running tests
if "test" in sys.argv:
    DATABASES["default"]["TEST"] = {
        "NAME": "test_" + DATABASES["default"].get("NAME", "PulseDB")
    }
```

### 4. Run Database Migrations

Ensure your PostgreSQL server is running (locally or via Docker) and that your `.env` values match your PostgreSQL credentials. Then, apply the migrations:

```bash
python manage.py migrate
```

### 5. Run All Test Cases Using Pytest

To execute all tests in your project, simply run:

```bash
pytest
```

Pytest will discover and run all test cases in your project.

---

By following these steps, you'll have your development environment set up with a PostgreSQL database, the database schema migrated, and your tests running with pytest. Happy coding!

---

Feel free to adjust the instructions based on your project's specific requirements.
