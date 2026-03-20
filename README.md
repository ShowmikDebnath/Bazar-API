# 🛒 Bazar API

A simple e-commerce REST API built with FastAPI and PostgreSQL.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **JWT** — authentication
- **Uvicorn** — ASGI server

---

## 📁 Project Structure
```
bazar-api/
├── app/
│   ├── main.py       # API routes
│   ├── models.py     # Database tables
│   ├── schemas.py    # Data validation
│   ├── crud.py       # Database operations
│   ├── auth.py       # JWT authentication
│   └── database.py   # DB connection
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/ShowmikDebnath/Bazar-API.git
cd Bazar-API
```

**2. Create virtual environment**
```bash
python3.11 -m venv myenv
source myenv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create PostgreSQL database**
```bash
psql postgres
CREATE DATABASE bazar;
\q
```

**5. Run the server**
```bash
uvicorn app.main:app --reload
```

**6. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/users/me` | Get current user |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create a product |
| GET | `/products` | Get all products |
| GET | `/products/{id}` | Get single product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cart` | Add item to cart |
| GET | `/cart` | View cart |
| DELETE | `/cart/{id}` | Remove cart item |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Place an order |
| GET | `/orders` | View all orders |

---

## 👨‍💻 Author

**Showmik Debnath**
- GitHub: [@ShowmikDebnath](https://github.com/ShowmikDebnath)
- LinkedIn: [showmikdebnath](https://linkedin.com/in/showmikdebnath)
- Portfolio: [showmikdebnath.github.io/portfolio](https://showmikdebnath.github.io/portfolio)
