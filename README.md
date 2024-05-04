# Task manager

## Get Started

### Clone git

```shell
# Clone Repositories
git clone https://github.com/GitarisTWorkSpace/Task-Manager-Backend.git
```

### Create Python venv

```shell
# Open project folder 
cd Task-Manager-Backend

# Create python venv 
# Python version needed 3.11.9
python -m venv venv 

# Activate Python venv
venv\Scripts\activate

# Download all requirements
pip install -r requirements.txt
```

### Create .env file for environment value

1. Create .env file
2. Open file 
3. Write next text

POSTGRES_USER=value
POSTGRES_PASSWORD=value
POSTGRES_DB=value
POSTGRES_HOST=value
POSTGRES_PORT=value

### Create RSA Keys

```shell
# Open src folder
cd src

# Screate certs folder
mkdir certs

# Open certs folder
cd certs

# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048

# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem 
```

### Create DB migrations

```shell
# Back to project foder
cd ..

# Open migrations folder
cd migrations

# Create versions folder 
mkdir versions

# Back to project foder
cd ..

# Python venv should be active
# Create migration file
alembic revision --autogenerate -m "Migration name"

# Apply migrations
alembic upgrade head
```

### Start project

```shell
# Python venv should be active
# Open scr folder
cd src

# Start
uvicorn main:app --reload
```