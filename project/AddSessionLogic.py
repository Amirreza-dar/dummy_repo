from project.models import User
from project.database import db
from werkzeug.security import generate_password_hash

def add_admin_user():
    # Admin user credentials
    admin_email = "admin@example.com"
    admin_password = "admin"  # You should choose a strong password

    # Check if admin user already exists
    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        print("An admin user with this email already exists.")
        return

    # Create an admin user instance
    admin_user = User(
        email=admin_email,
        password=generate_password_hash(admin_password, method='sha256'),
        is_admin=True
    )

    # Add the admin user to the session and commit
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user added successfully.")

# Run the function to add an admin user
add_admin_user()
