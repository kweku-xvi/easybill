# **EasyBill**

An Invoice App API, built with Django Rest Framework, allows users to securely create, manage, and send invoices to customers

# **Features**
- *User Registration & Authentication:* Anyone can sign up to create invoices.
- *Invoice Management:* Create, update, delete, and view invoices
- *Invoice Items:* Add multiple items with quantity and unit prices

## **Installation**

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/kweku-xvi/easybill>

2. **Change directory:**
   ```bash
    cd easybill

3. **Create a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate  # For Windows

4. **Install dependencies:**
   ```bash
    pip install -r requirements.txt

5. **Apply migrations:**
   ```bash
    python manage.py migrate

6. **Create super user:**
   ```bash
    python manage.py createsuperuser

7. **Run development server:**
   ```bash
    python manage.py runserver


