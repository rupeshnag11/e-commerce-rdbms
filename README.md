1. I learned how FastAPI connects to PostgreSQL using SQLAlchemy.

engine → Connects the application to the database
SessionLocal → Creates database sessions
Base → Base class used by SQLAlchemy models
get_db() → Provides a database session to API endpoints

2. Password Hashing

Passwords should not be stored directly in the database and I used bcrypt through passlib to hash passwords.

Password -> hash -> database

When the user logs in, the  password is compared with the stored hash of respective user password.

3. JWT

user login-> verify email and password ->(create access token)(token craeted by server) create jwt token -> send token to cleint ->server verifies token -> (token is stored in client side - cookies)

HS256 is a symmetric signing algorithm.

The secret key is used to sign and verify JWT tokens. the secret key is stored in .env file .

Depends(get_current_user) -> to get user id and verify the user and find user in database.


SQLAlchemy → used to connect to PostgreSQL and work with tables/queries.

psycopg2-binary → PostgreSQL database driver used to  communicates with PostgreSQL