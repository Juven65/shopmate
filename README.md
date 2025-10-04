# 🛒 ShopMate

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django&logoColor=white)](https://docs.djangoproject.com/en/stable/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](#)

![ShopMate Demo](screenshots/demo.gif)

---

## 📖 Overview

**ShopMate** is a full-stack e-commerce web application built using **Django**.  
It allows users to register, browse products, add them to cart, and securely checkout.  
The system includes an **admin dashboard** for managing products, orders, and customers — all within a clean, responsive **Bootstrap UI**.

This project helped me strengthen my understanding of Django’s **Model-View-Template (MVT)** pattern, authentication system, and deployment workflow on Render.

---

## 📚 Table of Contents
- [🚀 Features](#-features)
- [🧪 Tech Stack](#-tech-stack)
- [📸 Screenshots](#-screenshots)
- [⚙️ Setup Instructions](#️-setup-instructions)
- [🚀 Deployment](#-deployment)
- [👨‍💻 Developer](#-developer)
- [💬 Developer’s Note](#-developers-note)
- [📜 License](#-license)

---

## 🚀 Features

### 👤 **User Features**
✅ User Registration with Email Confirmation  
✅ Secure Login and Logout  
✅ Profile Management (Update Name, Email, Password)  
✅ Upload Profile Picture  
✅ Manage Shipping Address (Add/Update)  
✅ Product Listing and Detail Pages  
✅ Add to Cart / Remove / Update Quantity  
✅ Checkout with Name, Address, and Phone  
✅ View Order History (Filtered by Month & Year)  
✅ Export Order History (PDF and CSV)  
✅ Submit, Edit, and Delete Product Reviews  

### 🛠 **Admin Features**
✅ Manage Products (Add/Edit/Delete)  
✅ Upload Product Images via Form (Not Only in Admin Panel)  
✅ View and Manage Orders  
✅ Update Order Status (Processing → Shipped → Delivered)  
✅ Manage Stock (Update Quantity Directly from Dashboard)  
✅ Review Moderation (Approve/Reject Reviews)  
✅ Contact Messages Management  
✅ Admin Activity Logs  

📊 **Enhanced Admin Dashboard Charts**  
- **Orders Per Month** – Gradient bar chart with rounded corners & smooth animations  
- **Monthly Sales** – Peso-formatted chart for revenue visualization  
- **Order Status Overview** – Interactive pie chart with percentage tooltips  
- **Product Stock Table** – Filter products by Low Stock or Out of Stock  

---

## 🧠 What I Learned
- Structuring Django apps with clear separation of models, views, and templates  
- Handling user sessions and cart management  
- Using Django ORM for database queries  
- Integrating static and media files  
- Deploying a Django project on Render  
- Writing maintainable and modular Django code  

---

## 🧪 Tech Stack

- **Backend**: [Django 5+](https://docs.djangoproject.com/en/stable/)  
- **Frontend**: [Bootstrap 5](https://getbootstrap.com/)  
- **Database**: SQLite (default, can switch to PostgreSQL/MySQL)  
- **Charts**: [Chart.js](https://www.chartjs.org/)  
- **PDF Export**: [WeasyPrint](https://weasyprint.org/)  
- **CSV Export**: Python CSV module  
- **Email System**: Django Email + Token System  

---

## 📸 Screenshots

### 🏠 Homepage
![Homepage](screenshots/homepage.png)

### 🛒 Cart Page
![Cart](screenshots/cart.png)

### 📋 Checkout Form
![Checkout](screenshots/checkout.png)

### 📦 Order History
![Order History](screenshots/order-history.png)

### 🧾 PDF Invoice Sample
![PDF](screenshots/pdf-sample.png)

### 📝 Manage Reviews
![Reviews](screenshots/reviews.png)

### 📊 Admin Dashboard (Orders Per Month + Monthly Sales + Order Status)
![Admin Dashboard](screenshots/admin-dashboard.png)

### 📦 Manage Stock (Low Stock & Out of Stock Filters)
![Manage Stock](screenshots/manage-stock.png)


## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Juven65/shopmate.git
cd shopmate

# Create a virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate the database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver

---

## 🚀 Deployment
**Live Demo:** [https://shopmate-3ygr.onrender.com](https://shopmate-3ygr.onrender.com)

---

## 👨‍💻 Developer
**Juven Pinoy**  
🎓 Information Technology Graduate – Carlos Hilado Memorial State University (2025)  
🌐 [GitHub Profile](https://github.com/Juven65)

---

## 💬 Developer’s Note
> “This project was built with the help of ChatGPT for guidance and learning purposes.  
> I customized, studied, and managed every feature to understand how Django works in real-world e-commerce applications.”
