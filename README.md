# Daro Market Server

## Get Start :

#### **1. git clone https://gitlab.margay.ir/Ticksy/ticksy_server.git** (terminal)

#### **2. pip install -r requirements.txt** (terminal, with active virtualenv)

#### **3. create database with this info:**  (mysql)

    'NAME': 'ticksy_db'
    
    'USER': 'ticksy'
    
    'PASSWORD': 'ticksy_1234'
    
    - Set the **Charset to utf8mb4**, and **Collaction to utf8mb4_general** when creating database in mysql.

##### **3.1. for convenience :**

    CREATE USER 'ticksy'@'%' IDENTIFIED BY 'ticksy_1234';
    
    GRANT ALL PRIVILEGES ON *.* TO 'ticksy'@'%';
    
    CREATE DATABASE ticksy_db DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_general_ci;


#### **4. python manage.py makemigrations** (terminal)

#### **5. python manage.py migrate** (terminal)

#### **6. python manage.py runserver** (terminal)

- **Admin panel**:
    - http://localhost:8000/admin/ 


## Done!