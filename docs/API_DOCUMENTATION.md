# E-Commerce API Documentation

URL : http://localhost:8000

1. Authentication APIs
1.1 Register

API: Register a new user

Method: POST

URL: /register

Description:
This API is used to create a new user account.

Input:

Username
Email
Password

Example Input:

{
  "username": "Rahul",
  "email": "rahul@gmail.com",
  "password": "Rahul@123"
}

Success Response:

{
  "status": "User created successfully",
  "user_id": 1,
  "email": "rahul@gmail.com"
}

Error : 1. Email is already registered


1.2 Login

API: Login user

Method: POST

URL: /login

Description:
This API is used to log for existing user.

Input:

Email
Password

Example Input:

{
  "email": "rahul@gmail.com",
  "password": "password123"
}

Success Response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "user_id": 1,
  "username": "Rahul",
  "email": "rahul@gmail.com",
  "status": "login successful"
}

Possible Errors: 1.User not found
                 2.Invalid email/password


1.3 Logout

API: Logout user

Method: POST

URL: /logout

Description:
This API is used to log out already logged-in  user.

Success Response:

{
  "status": "successfully logout"
}



2. Health API
2.1 Health Check

API: Check application health

Method: GET

URL: /health

Description:
This API is used to check whether the application is running or not.

Success Response:

{
  "message": "OK"
}



3. User APIs
3.1 Get User Details

API: Get current user details

Method: GET

URL: /users_details

Description:
This API returns the details of the currently logged-in user.

Authentication: Required

Success Response:

{
  "user_id": 1,
  "username": "Rahul",
  "email": "rahul@gmail.com"
}


3.2 Get User Past Orders

API: Get user's past orders

Method: GET

URL: /get_user_past_n_orders

Description:
This API returns the previous orders of the currently logged-in user.

Authentication: Required

Success Response:

Returns the user's previous order details.



4. Inventory APIs
4.1 Check Inventory

API: Check product inventory

Method: POST

URL: /check_inventory

Description:
This API checks whether the requested quantity of a product is available.

Authentication: Required

Input:

Product ID
Quantity

Example Input:
{
  "product_id": 1,
  "quantity": 2
}

Success Response:

{
  "available": true,
  "product_id": 1,
  "requested_quantity": 2,
  "available_quantity": 10
}

Possible Error:1.Product not found in inventory
               2. product out of stock

4.2 Update Inventory

API: Update product inventory

Method: POST

URL: /inventory_update

Description:
This API updates the inventory quantity for a product.

Authentication: Required

Input:

Product ID
Quantity

Example Input:

{
  "product_id": 1,
  "quantity": 2
}

Success Response:

{
  "status": "inventory updated",
  "product_id": 1,
  "quantity": 2
}

Possible Error: Insufficient stock or product not found


5. Cart APIs
5.1 Create Cart

API: Add product to cart

Method: POST

URL: /create_cart

Description:
This API adds a product to the user's cart.

Authentication: Required

Input:

Product ID
Quantity

Example Input:

{
  "product_id": 1,
  "quantity": 2
}

Success Response:

{
  "cart": true,
  "status": "cart is created",
  "user_id": 1,
  "product_id": 1,
  "quantity": 2,
  "total_amount": 2000
}

Possible Error: Product not found


6. Order APIs
6.1 Purchase Order

API: Purchase a product

Method: POST

URL: /purchase_order

Description:
This API purchases a product, updates the inventory, and creates an order.

Authentication: Required

Input:

Product ID
Quantity

Example Input:

{
  "product_id": 1,
  "quantity": 2
}

Success Response:

{
  "status": "purchase successful",
  "user_id": 1,
  "product_id": 1,
  "quantity": 2,
  "total_amount": 2000,
  "order_id": 10
}

Possible Errors: 1.Product not found
                 2.Insufficient stock


6.2 Create Order

API: Create a new order

Method: POST

URL: /create_order

Description:
This API creates a new order for the currently logged-in user.

Authentication: Required

Input:

Total amount

Example Input:

{
  "total_amount": 2000
}

Success Response:

{
  "order": true,
  "status": "order is created",
  "order_id": 10,
  "user_id": 1,
  "total_amount": 2000
}


For below APIs, authentication is required using the JWT token.

/users_details
/get_user_past_n_orders
/check_inventory
/purchase_order
/create_cart
/create_order
/inventory_update

If the token is invalid or expired(access_token > 30 min), the API returns an authentication error.



HTTP CODES :

1. 200 : Request completed successfully

2. 400 : Bad Request Error(insufficient stock)

3. 401 : unauthorized error (user not found or token is expired/invalid)

4. 404 : NOt Found (product not found)
