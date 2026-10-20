## 🚀 Live Demo

Explore the live Shopora website here:

**[Visit Shopora](https://shopora-xd8p.onrender.com)**

Shopora is a full-stack e-commerce web application developed using Django and Python. It provides a simple shopping experience where users can browse products, manage their cart, place orders, and track their purchases.

## Features

- Browse and search products
- Add products to the shopping cart
- Increase or decrease product quantities
- Stock validation during shopping
- User registration, login, and logout
- Checkout with customer and delivery details
- Order placement and order history
- View order status
- Django Admin for managing products and orders
- Responsive user interface

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Divyayadav1912/CodeAlpha_SimpleEcommerceStore.git
   ```

2. Open the project directory:

   ```bash
   cd CodeAlpha_SimpleEcommerceStore
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```bash
   .\venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   pip install Django python-dotenv
   ```

5. Configure the Django secret key using an environment variable named `DJANGO_SECRET_KEY` in a local `.env` file. Never upload the `.env` file to GitHub.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open `http://127.0.0.1:8000/` in your browser.

## Project Structure

```text
CodeAlpha_SimpleEcommerceStore/
├── config/
├── products/
│   ├── migrations/
│   └── templates/
├── .gitignore
├── manage.py
└── README.md
```

## Internship Task

**Task 1: Simple E-commerce Store**

Developed as part of the CodeAlpha internship project.

## Author

Divya Yadav

## Future Improvements

- Online payment integration
- Product reviews and ratings
- Product category filters
