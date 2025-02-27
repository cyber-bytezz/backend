from fastapi import FastAPI
from app.routes import auth, products, cart, orders, admin, user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="QuitQ E-commerce API")

# Ensure correct token authentication URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# CORS to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Include API routes
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "Welcome to QuitQ API"}
