# Techhub - E-Commerce Platform

A feature-rich, full-stack E-Commerce web application built using **Flask (Python)** and **MySQL**, designed specifically for computer hardware, peripherals, and custom PC components.

---

## 📌 Features

### 👤 User / Buyer
- **Product Catalog & Browsing**: Explore components and tech gear by category and brand with responsive UI cards.
- **Product Details**: View product specifications, pricing, stock availability, and descriptions.
- **Cart Management**: Add items to shopping cart, update quantities, and calculate totals dynamically.
- **Secure Checkout**: Place orders with shipping information and simulated payment handling.
- **Order Tracking**: View order history, order statuses, and detailed itemized receipts.
- **User Authentication**: Secure user registration and login sessions.

### 🛠️ Admin Panel
- **Dashboard Overview**: Metrics for total products, orders, categories, and registered buyers.
- **Product Management**: Add, edit, update stock, and delete products.
- **Category & Brand Management**: Organize components by custom categories and brand tags.
- **Order Management**: Monitor customer orders, update delivery statuses, and inspect buyer details.
- **Customer List**: View registered buyers and activity records.

---

## 🏗️ Project Architecture

```text
techhub/
│
├── app/
│   ├── __init__.py               # App factory and Blueprint registration
│   ├── routes/
│   │   ├── admin_routes.py       # Admin authentication & dashboard logic
│   │   ├── auth_routes.py        # User login & registration
│   │   ├── cart_routes.py        # Shopping cart functionality
│   │   ├── checkout_routes.py    # Order placement & checkout process
│   │   ├── main_routes.py        # Landing page & navigation
│   │   ├── order_routes.py       # User order history & order details
│   │   └── product_routes.py     # Product browsing & catalog
│   ├── static/
│   │   └── css/                  # Custom CSS stylesheets
│   └── templates/                # Jinja2 HTML templates
│       ├── admin/                # Admin views (dashboard, inventory, orders)
│       ├── auth/                 # Sign in & Sign up templates
│       ├── cart/                 # Cart view
│       ├── checkout/             # Checkout form
│       ├── orders/               # My orders & order detail pages
│       ├── products/             # Catalog, product details, admin CRUD
│       ├── base.html             # Base layout template
│       └── home.html             # Homepage template
│
├── config.py                     # Database and environment configurations
├── requirements.txt              # Python package dependencies
├── run.py                        # Application entry point
└── README.md                     # Documentation
```

---

## ⚙️ Tech Stack

- **Backend**: Python 3, Flask (Blueprints architecture)
- **Database**: MySQL, Flask-MySQLdb / mysqlclient
- **Frontend**: HTML5, CSS3, Jinja2 Template Engine
- **Server / Environment**: Werkzeug WSGI

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites
- **Python 3.10+** installed
- **MySQL Server** installed and running
- **Git** installed

### 2. Clone the Repository
```bash
git clone https://github.com/akilesh2330/Techhub.E-Commerce-platform.git
cd Techhub.E-Commerce-platform
```

### 3. Create & Activate Virtual Environment
On Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure the Database
1. Open your MySQL client (e.g., MySQL Workbench or CLI) and create the database:
   ```sql
   CREATE DATABASE techhub_db;
   ```
2. Update your credentials in `config.py`:
   ```python
   class Config:
       MYSQL_HOST = 'localhost'
       MYSQL_USER = 'your_mysql_username'
       MYSQL_PASSWORD = 'your_mysql_password'
       MYSQL_DB = 'techhub_db'
   ```

### 6. Run the Application
```bash
python run.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 🔒 Security Best Practices
- Never commit actual production database passwords to public repositories.
- Use environment variables (`.env`) for production credentials and Flask `SECRET_KEY`.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

---

## 📝 License
This project is licensed under the MIT License - see the repository for details.