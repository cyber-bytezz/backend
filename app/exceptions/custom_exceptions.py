from fastapi import HTTPException

class ProductNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Product not found")

class OutOfStockException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Product is out of stock")

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")
