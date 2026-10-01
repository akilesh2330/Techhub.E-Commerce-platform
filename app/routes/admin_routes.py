from flask import (Blueprint,render_template,request,redirect,url_for,flash,session)

from app import mysql


# Create Admin Blueprint
admin_bp = Blueprint("admin", __name__)


# ==========================================================
# ADMIN LOGIN
# ==========================================================
@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    # If admin is already logged in
    if session.get("admin_logged_in"):

        return redirect(
            url_for("admin.admin_dashboard")
        )

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()

        query = """
        SELECT *
        FROM users
        WHERE email = %s
        AND password = %s
        AND role = 'admin'
        """

        cur.execute(
            query,
            (email, password)
        )

        admin = cur.fetchone()

        cur.close()

        if admin:

            # Store admin login information in session
            session["admin_logged_in"] = True
            session["admin_email"] = email

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("admin.admin_dashboard")
            )

        else:

            flash(
                "Invalid Email or Password!",
                "danger"
            )

    return render_template(
        "admin/login.html"
    )

    
# ==========================================================
# ADMIN DASHBOARD
# ==========================================================
@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    # Protect dashboard from users who are not logged in
    if not session.get("admin_logged_in"):

        flash(
            "Please login to access the dashboard.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # Count Products
    cur.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cur.fetchone()[0]

    # Count Categories
    cur.execute(
        "SELECT COUNT(*) FROM categories"
    )

    total_categories = cur.fetchone()[0]

    # Count Brands
    cur.execute(
        "SELECT COUNT(*) FROM brands"
    )

    total_brands = cur.fetchone()[0]

    # Count Users
    cur.execute(
        "SELECT COUNT(*) FROM users"
    )

    total_users = cur.fetchone()[0]


    # Count Orders
    cur.execute(
        "SELECT COUNT(*) FROM orders"
    )

    total_orders = cur.fetchone()[0]


    # Close Cursor
    cur.close()

    cur.close()

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        total_brands=total_brands,
        total_users=total_users,
        total_orders=total_orders
    )


# ==========================================================
# ADD PRODUCT — CREATE
# ==========================================================
@admin_bp.route(
    "/admin/add-product",
    methods=["GET", "POST"]
)
def add_product():

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # Get Categories
    cur.execute(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        """
    )

    categories = cur.fetchall()

    # Get Brands
    cur.execute(
        """
        SELECT
            brand_id,
            brand_name
        FROM brands
        """
    )

    brands = cur.fetchall()

    if request.method == "POST":

        product_name = request.form.get(
            "product_name"
        )

        description = request.form.get(
            "description"
        )

        specifications = request.form.get(
            "specifications"
        )

        price = request.form.get(
            "price"
        )

        stock = request.form.get(
            "stock"
        )

        image = request.form.get(
            "image"
        )

        category = request.form.get(
            "category"
        )

        brand = request.form.get(
            "brand"
        )

        query = """
        INSERT INTO products
        (
            product_name,
            description,
            specifications,
            price,
            stock,
            image,
            category_id,
            brand_id
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(
            query,
            (
                product_name,
                description,
                specifications,
                price,
                stock,
                image,
                category,
                brand
            )
        )

        mysql.connection.commit()

        cur.close()

        flash(
            "Product Added Successfully!",
            "success"
        )

        return redirect(
            url_for("admin.admin_dashboard")
        )

    cur.close()

    return render_template(
        "products/add_product.html",
        categories=categories,
        brands=brands
    )


# ==========================================================
# MANAGE PRODUCTS — READ
# ==========================================================
@admin_bp.route("/admin/manage-products")
def manage_products():

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    query = """
    SELECT
        p.product_id,
        p.product_name,
        b.brand_name,
        c.category_name,
        p.price,
        p.stock
    FROM products p

    JOIN brands b
        ON p.brand_id = b.brand_id

    JOIN categories c
        ON p.category_id = c.category_id

    ORDER BY p.product_id DESC
    """

    cur.execute(query)

    products = cur.fetchall()

    cur.close()

    return render_template(
        "products/manage_products.html",
        products=products
    )


# ==========================================================
# EDIT PRODUCT — UPDATE
# ==========================================================
@admin_bp.route(
    "/admin/edit-product/<int:product_id>",
    methods=["GET", "POST"]
)
def edit_product(product_id):

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # Get Categories
    cur.execute(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        """
    )

    categories = cur.fetchall()

    # Get Brands
    cur.execute(
        """
        SELECT
            brand_id,
            brand_name
        FROM brands
        """
    )

    brands = cur.fetchall()

    # Update product
    if request.method == "POST":

        product_name = request.form.get(
            "product_name"
        )

        description = request.form.get(
            "description"
        )

        specifications = request.form.get(
            "specifications"
        )

        price = request.form.get(
            "price"
        )

        stock = request.form.get(
            "stock"
        )

        image = request.form.get(
            "image"
        )

        category = request.form.get(
            "category"
        )

        brand = request.form.get(
            "brand"
        )

        query = """
        UPDATE products

        SET
            product_name = %s,
            description = %s,
            specifications = %s,
            price = %s,
            stock = %s,
            image = %s,
            category_id = %s,
            brand_id = %s

        WHERE product_id = %s
        """

        cur.execute(
            query,
            (
                product_name,
                description,
                specifications,
                price,
                stock,
                image,
                category,
                brand,
                product_id
            )
        )

        mysql.connection.commit()

        cur.close()

        flash(
            "Product Updated Successfully!",
            "success"
        )

        return redirect(
            url_for("admin.manage_products")
        )

    # Get selected product
    query = """
    SELECT
        product_id,
        product_name,
        description,
        specifications,
        price,
        stock,
        image,
        category_id,
        brand_id

    FROM products

    WHERE product_id = %s
    """

    cur.execute(
        query,
        (product_id,)
    )

    product = cur.fetchone()

    cur.close()

    if product is None:

        flash(
            "Product Not Found!",
            "danger"
        )

        return redirect(
            url_for("admin.manage_products")
        )

    return render_template(
        "products/edit_product.html",
        product=product,
        categories=categories,
        brands=brands
    )


# ==========================================================
# DELETE PRODUCT — DELETE
# ==========================================================
@admin_bp.route(
    "/admin/delete-product/<int:product_id>",
    methods=["POST"]
)
def delete_product(product_id):

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    cur.execute(
        """
        DELETE FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    mysql.connection.commit()

    cur.close()

    flash(
        "Product Deleted Successfully!",
        "success"
    )

    return redirect(
        url_for("admin.manage_products")
    )


# ==========================================================
# ADMIN LOGOUT
# ==========================================================
@admin_bp.route("/admin/logout")
def admin_logout():

    # Remove all stored session information
    session.clear()

    flash(
        "Logged Out Successfully!",
        "success"
    )

    return redirect(
        url_for("admin.admin_login")
    )
# ==========================================================
# MANAGE CATEGORIES
# ==========================================================
@admin_bp.route("/admin/manage-categories", methods=["GET", "POST"])
def manage_categories():

    # Check whether admin is logged in
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # ======================================================
    # ADD NEW CATEGORY
    # ======================================================
    if request.method == "POST":

        category_name = request.form.get(
            "category_name"
        )

        # Remove unwanted spaces
        category_name = category_name.strip()

        # Check whether the input is empty
        if not category_name:

            cur.close()

            flash(
                "Category name cannot be empty!",
                "warning"
            )

            return redirect(
                url_for("admin.manage_categories")
            )

        # Check whether the category already exists
        cur.execute(
            """
            SELECT category_id
            FROM categories
            WHERE LOWER(category_name) = LOWER(%s)
            """,
            (category_name,)
        )

        existing_category = cur.fetchone()

        # If category already exists
        if existing_category:

            cur.close()

            flash(
                "Category already exists!",
                "warning"
            )

            return redirect(
                url_for("admin.manage_categories")
            )

        # Add the new category
        cur.execute(
            """
            INSERT INTO categories
            (
                category_name
            )
            VALUES
            (
                %s
            )
            """,
            (category_name,)
        )

        mysql.connection.commit()

        cur.close()

        flash(
            "Category Added Successfully!",
            "success"
        )

        return redirect(
            url_for("admin.manage_categories")
        )

    # ======================================================
    # DISPLAY ALL CATEGORIES
    # ======================================================

    cur.execute(
        """
        SELECT
            category_id,
            category_name

        FROM categories

        ORDER BY category_id ASC
        """
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        "admin/manage_categories.html",
        categories=categories
    )


# ==========================================================
# DELETE CATEGORY
# ==========================================================
@admin_bp.route(
    "/admin/delete-category/<int:category_id>",
    methods=["POST"]
)
def delete_category(category_id):

    # Check whether admin is logged in
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    try:

        # Delete selected category
        cur.execute(
            """
            DELETE FROM categories
            WHERE category_id = %s
            """,
            (category_id,)
        )

        mysql.connection.commit()

        flash(
            "Category Deleted Successfully!",
            "success"
        )

    except Exception:

        # Undo the delete operation if the category
        # is connected to an existing product
        mysql.connection.rollback()

        flash(
            "This category is used by a product, so it cannot be deleted.",
            "danger"
        )

    finally:

        cur.close()

    return redirect(
        url_for("admin.manage_categories")
    )
# ==========================================================
# MANAGE BRANDS
# ==========================================================
@admin_bp.route("/admin/manage-brands", methods=["GET", "POST"])
def manage_brands():

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash("Please login first.", "warning")

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # Add New Brand
    if request.method == "POST":

        brand_name = request.form.get("brand_name")

        # Remove extra spaces
        brand_name = brand_name.strip()

        # Check empty input
        if not brand_name:

            cur.close()

            flash(
                "Brand name cannot be empty!",
                "warning"
            )

            return redirect(
                url_for("admin.manage_brands")
            )

        # Check whether brand already exists
        cur.execute(
            """
            SELECT brand_id
            FROM brands
            WHERE LOWER(brand_name) = LOWER(%s)
            """,
            (brand_name,)
        )

        existing_brand = cur.fetchone()

        # Duplicate brand
        if existing_brand:

            cur.close()

            flash(
                "Brand already exists!",
                "warning"
            )

            return redirect(
                url_for("admin.manage_brands")
            )

        # Insert new brand
        cur.execute(
            """
            INSERT INTO brands
            (
                brand_name
            )
            VALUES
            (
                %s
            )
            """,
            (brand_name,)
        )

        mysql.connection.commit()

        cur.close()

        flash(
            "Brand Added Successfully!",
            "success"
        )

        return redirect(
            url_for("admin.manage_brands")
        )

    # Display all brands
    cur.execute(
        """
        SELECT
            brand_id,
            brand_name
        FROM brands
        ORDER BY brand_id ASC
        """
    )

    brands = cur.fetchall()

    cur.close()

    return render_template(
        "admin/manage_brands.html",
        brands=brands
    )


# ==========================================================
# DELETE BRAND
# ==========================================================
@admin_bp.route(
    "/admin/delete-brand/<int:brand_id>",
    methods=["POST"]
)
def delete_brand(brand_id):

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash("Please login first.", "warning")

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    try:

        # Delete selected brand
        cur.execute(
            """
            DELETE FROM brands
            WHERE brand_id = %s
            """,
            (brand_id,)
        )

        mysql.connection.commit()

        flash(
            "Brand Deleted Successfully!",
            "success"
        )

    except Exception:

        # Undo if the brand is used by a product
        mysql.connection.rollback()

        flash(
            "This brand is used by a product, so it cannot be deleted.",
            "danger"
        )

    finally:

        cur.close()

    return redirect(
        url_for("admin.manage_brands")
    )
# ==========================================================
# BUYERS LIST
# ==========================================================
@admin_bp.route("/admin/buyers-list")
def buyers_list():

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash("Please login first.", "warning")

        return redirect(
            url_for("admin.admin_login")
        )

    cur = mysql.connection.cursor()

    # Get all registered users
    cur.execute(
        """
        SELECT
            user_id,
            full_name,
            email,
            role
        FROM users
        ORDER BY user_id ASC
        """
    )

    users = cur.fetchall()

    cur.close()

    return render_template(
        "admin/buyers_list.html",
        users=users
    )
# ==========================================================
# MANAGE CUSTOMER ORDERS
# ==========================================================
@admin_bp.route("/admin/manage-orders")
def manage_orders():

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    # Create database cursor
    cur = mysql.connection.cursor()

    # Get all customer orders
    cur.execute(
        """
        SELECT
            order_id,
            full_name,
            order_date,
            total_amount,
            payment_method,
            order_status

        FROM orders

        ORDER BY order_date DESC
        """
    )

    # Store all orders
    orders = cur.fetchall()

    # Close database cursor
    cur.close()

    # Display Manage Orders page
    return render_template(
        "admin/manage_orders.html",
        orders=orders
    )


# ==========================================================
# UPDATE ORDER STATUS
# ==========================================================
@admin_bp.route(
    "/admin/update-order-status/<int:order_id>",
    methods=["POST"]
)
def update_order_status(order_id):

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )

    # Get selected status from the form
    order_status = request.form.get(
        "order_status",
        ""
    ).strip()

    # Allowed order statuses
    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    # Prevent invalid status values
    if order_status not in allowed_statuses:

        flash(
            "Invalid order status!",
            "danger"
        )

        return redirect(
            url_for("admin.manage_orders")
        )

    # Create database cursor
    cur = mysql.connection.cursor()

    # Check whether the order exists
    cur.execute(
        """
        SELECT order_id

        FROM orders

        WHERE order_id = %s
        """,
        (order_id,)
    )

    order = cur.fetchone()

    # Order does not exist
    if order is None:

        cur.close()

        flash(
            "Order not found!",
            "danger"
        )

        return redirect(
            url_for("admin.manage_orders")
        )

    # Update order status
    cur.execute(
        """
        UPDATE orders

        SET order_status = %s

        WHERE order_id = %s
        """,
        (
            order_status,
            order_id
        )
    )

    # Save database changes
    mysql.connection.commit()

    # Close database cursor
    cur.close()

    flash(
        f"Order #{order_id} status updated to {order_status}!",
        "success"
    )

    return redirect(
        url_for("admin.manage_orders")
    )
# ==========================================================
# ADMIN - VIEW ORDER DETAILS
# ==========================================================
@admin_bp.route(
    "/admin/order-details/<int:order_id>"
)
def admin_order_details(order_id):

    # Admin login protection
    if not session.get("admin_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("admin.admin_login")
        )


    # Create database cursor
    cur = mysql.connection.cursor()


    # Get selected order details
    cur.execute(
        """
        SELECT
            order_id,
            full_name,
            phone,
            address,
            city,
            state,
            pincode,
            payment_method,
            total_amount,
            order_status,
            order_date

        FROM orders

        WHERE order_id = %s
        """,
        (order_id,)
    )


    order = cur.fetchone()


    # Check whether order exists
    if order is None:

        cur.close()

        flash(
            "Order not found!",
            "danger"
        )

        return redirect(
            url_for("admin.manage_orders")
        )


    # Get products in the selected order
    cur.execute(
        """
        SELECT
            product_name,
            price,
            quantity,
            subtotal

        FROM order_items

        WHERE order_id = %s

        ORDER BY order_item_id ASC
        """,
        (order_id,)
    )


    order_items = cur.fetchall()


    # Close database cursor
    cur.close()


    # Display admin order details page
    return render_template(
        "admin/order_details.html",
        order=order,
        order_items=order_items
    )