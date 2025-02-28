# **HexaMart - Backend Comprehensive Documentation**  
**Version:** 1.0  
**Prepared By:** Aro Barath Chandru B 
**Date:** 28=02-2025

---

## **Table of Contents**
1. [Introduction](#introduction)  
2. [Tech Stack](#tech-stack)  
3. [Project Structure](#project-structure)  
4. [Environment Setup](#environment-setup)  
5. [Database Schema](#database-schema)  
6. [Authentication System](#authentication-system)  
7. [API Endpoints](#api-endpoints)  
   - Authentication  
   - Product Management  
   - Cart Management  
   - Order Management  
   - Admin Panel  
8. [Middleware and Security](#middleware-and-security)  
9. [Deployment Guide](#deployment-guide)  
10. [Testing and Debugging](#testing-and-debugging)  
11. [Future Enhancements](#future-enhancements)  
12. [Conclusion](#conclusion)  

---

## **1. Introduction**
The **HexaMart Backend** is a robust and scalable RESTful API built using **FastAPI** and **MySQL**. It is designed to handle user authentication, product listings, cart management, and order processing, with an **admin panel** for managing products and orders.  
This documentation provides a **detailed walkthrough** of the backend, covering **architecture, API endpoints, database interactions, and security measures**.

---

## **2. Tech Stack**
- **Language:** Python 3.10+  
- **Framework:** FastAPI (High-performance, async API framework)  
- **Database:** MySQL (With SQLAlchemy ORM)  
- **Authentication:** JWT (JSON Web Token)  
- **Security:** OAuth2 with Password Flow, Password Hashing (bcrypt)  
- **Middleware:** CORS, Exception Handling  
- **Server:** Uvicorn (ASGI Server)  
- **Deployment:** Docker, Nginx (Optional)  

---

## **3. Project Structure**
The backend follows **modular architecture** to ensure separation of concerns.

```
backend/
│── app/
│   ├── database.py         # Database connection and session management
│   ├── models.py           # SQLAlchemy models (User, Product, Cart, Order)
│   ├── routes/
│   │   ├── auth.py         # User authentication routes
│   │   ├── products.py     # Product management routes
│   │   ├── cart.py         # Shopping cart routes
│   │   ├── orders.py       # Order processing routes
│   │   ├── admin.py        # Admin functionalities
│   ├── utils/
│   │   ├── security.py     # JWT authentication, password hashing
│   ├── schemas.py          # Pydantic models for validation
│   ├── main.py             # FastAPI application entry point
│── requirements.txt        # Python dependencies
│── .env                    # Environment variables
│── README.md               # Project documentation
```

---

## **4. Environment Setup**
### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```
### **Step 2: Setup Environment Variables (`.env`)**
```
DATABASE_URL = "mysql+pymysql://username:password@localhost/quitq"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
```
### **Step 3: Run Database Migrations**
```bash
python app/database.py
```
### **Step 4: Start FastAPI Server**
```bash
uvicorn app.main:app --reload
```

---

## **5. Database Schema**
The **SQLAlchemy ORM** is used for database interactions.

### **User Table**
| Column         | Type    | Description |
|---------------|--------|-------------|
| id            | INT    | Primary Key |
| name          | STRING | Full name |
| email         | STRING | Unique email |
| password_hash | STRING | Hashed password |
| is_admin      | BOOLEAN | True for admin |

### **Product Table**
| Column     | Type    | Description |
|-----------|--------|-------------|
| id        | INT    | Primary Key |
| name      | STRING | Product Name |
| price     | FLOAT  | Price |
| category  | STRING | Category |
| stock     | INT    | Stock quantity |
| image_url | STRING | Image link |

### **Cart Table**
| Column    | Type   | Description |
|----------|-------|-------------|
| id       | INT   | Primary Key |
| user_id  | INT   | Foreign Key (User) |
| product_id | INT | Foreign Key (Product) |
| quantity | INT   | Quantity added |

### **Order Table**
| Column     | Type    | Description |
|-----------|--------|-------------|
| id        | INT    | Primary Key |
| user_id   | INT    | Foreign Key (User) |
| total_price | FLOAT | Total price |
| status    | STRING | Pending, Shipped, Delivered |
| created_at | DATETIME | Timestamp |

### **Order Items Table**
| Column     | Type   | Description |
|-----------|-------|-------------|
| id        | INT   | Primary Key |
| order_id  | INT   | Foreign Key (Order) |
| product_id | INT  | Foreign Key (Product) |
| quantity  | INT   | Ordered quantity |

---

## **6. Authentication System**
### **JWT-Based Authentication**
- Users are authenticated using **OAuth2 with Password Flow**.
- Passwords are **hashed using bcrypt**.
- JWT tokens are issued upon login and **stored in headers** for authentication.

### **Authentication Routes**
| Method | Endpoint      | Description |
|--------|-------------|-------------|
| POST   | `/auth/register` | Registers a new user |
| POST   | `/auth/login` | Authenticates user and returns JWT token |

---

## **7. API Endpoints**
### **Product Management**
| Method | Endpoint           | Description |
|--------|--------------------|-------------|
| GET    | `/products/`       | Fetch all products |
| POST   | `/products/`       | Add a new product (Admin only) |
| PUT    | `/products/{id}`   | Update product (Admin only) |
| DELETE | `/products/{id}`   | Delete product (Admin only) |

### **Cart Management**
| Method | Endpoint           | Description |
|--------|--------------------|-------------|
| POST   | `/cart/`           | Add product to cart |
| GET    | `/cart/`           | Fetch cart items |
| PUT    | `/cart/{id}/decrease` | Decrease quantity |
| DELETE | `/cart/{id}`       | Remove item |

### **Order Management**
| Method | Endpoint          | Description |
|--------|------------------|-------------|
| POST   | `/orders/`       | Place an order |
| GET    | `/orders/`       | Fetch user orders |
| PUT    | `/orders/{id}/status` | Update order status (Admin only) |

### **Admin Panel**
| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| GET    | `/admin/dashboard`   | Admin overview |
| GET    | `/admin/products`    | View all products |
| GET    | `/admin/orders`      | View all orders |
| PUT    | `/admin/orders/{id}/status` | Change order status |

---

## **8. Middleware and Security**
- **JWT Authentication** for secure access
- **Role-based access control (RBAC)**
- **CORS Middleware** to prevent unauthorized API access
- **Password hashing with bcrypt**

---

## **9. Deployment Guide**
### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```
### **Step 2: Setup Environment Variables (`.env`)**
```
DATABASE_URL = "mysql+pymysql://username:password@localhost/quitq"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
```
### **Step 3: Start FastAPI Server**
```bash
uvicorn app.main:app --reload
```

---

## **10. Future Enhancements**
- **Payment Gateway Integration**
- **Email Order Confirmation**
- **Real-Time Order Tracking**
- **Admin Analytics Dashboard**

---

## **11. Conclusion**
The HexaMart backend is **secure, scalable, and optimized**. It follows **best practices in authentication, security, and database management**. This documentation serves as a **reference for understanding and modifying the backend as needed**.

---

This **dedicated documentation** covers every aspect of the backend system **A-Z**. Now, let’s move to frontend documentation! 🚀
