# app/__init__.py

from flask import Flask
from flask_mysqldb import MySQL
from config import Config

# Global MySQL object
mysql = MySQL()


def create_app():

    # Create Flask application
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Secret Key
    app.secret_key = "techhub_secret_key"

    # Initialize MySQL
    mysql.init_app(app)

    # ==========================================
    # Register Blueprints
    # ==========================================

    # Home Routes
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # Admin Routes
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    # Product Routes
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp)

    # Authentication Routes (Future)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # Cart Routes (Future)
    from app.routes.cart_routes import cart_bp
    app.register_blueprint(cart_bp)

    from app.routes.checkout_routes import checkout_bp
    app.register_blueprint(checkout_bp)

    # Contact Routes (Future)
    # from app.routes.contact_routes import contact_bp
    # app.register_blueprint(contact_bp)

    # Order Routes (Future)
    from app.routes.order_routes import order_bp
    app.register_blueprint(order_bp)

    # PC Builder Routes (Future)
    # from app.routes.pcbuilder_routes import pcbuilder_bp
    # app.register_blueprint(pcbuilder_bp)

    return app