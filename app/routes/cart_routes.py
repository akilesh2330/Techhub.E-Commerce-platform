from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from app import mysql


# Create Cart Blueprint
cart_bp = Blueprint("cart", __name__)


# ==========================================================
# ADD PRODUCT TO CART
# ==========================================================
@cart_bp.route(
    "/cart/add/<int:product_id>",
    methods=["POST"]
)
def add_to_cart(product_id):

    # Customer must login before adding products
    if not session.get("customer_logged_in"):

        flash(
            "Please login to add products to your cart.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )

    cur = mysql.connection.cursor()

    # Check whether product exists
    cur.execute(
        """
        SELECT
            product_id,
            product_name,
            stock

        FROM products

        WHERE product_id = %s
        """,
        (product_id,)
    )

    product = cur.fetchone()

    cur.close()

    # Product not found
    if product is None:

        flash(
            "Product not found!",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    # Product is out of stock
    if product[2] <= 0:

        flash(
            "This product is currently out of stock.",
            "danger"
        )

        return redirect(
            url_for(
                "product.product_details",
                product_id=product_id
            )
        )

    # Get cart from session
    cart = session.get(
        "cart",
        {}
    )

    # Session dictionary keys are stored as strings
    product_key = str(product_id)

    # Increase quantity if product already exists
    if product_key in cart:

        # Do not add more than available stock
        if cart[product_key] >= product[2]:

            flash(
                "You cannot add more than the available stock.",
                "warning"
            )

            return redirect(
                url_for(
                    "product.product_details",
                    product_id=product_id
                )
            )

        cart[product_key] += 1

    else:

        cart[product_key] = 1

    # Save cart in session
    session["cart"] = cart

    session.modified = True

    flash(
        f"{product[1]} added to cart!",
        "success"
    )

    return redirect(
        url_for("cart.view_cart")
    )


# ==========================================================
# VIEW CART
# ==========================================================
@cart_bp.route("/cart")
def view_cart():

    # Customer login protection
    if not session.get("customer_logged_in"):

        flash(
            "Please login to view your cart.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )

    cart = session.get(
        "cart",
        {}
    )

    cart_items = []

    grand_total = 0

    cur = mysql.connection.cursor()

    # Get every cart product from database
    for product_id, quantity in cart.items():

        cur.execute(
            """
            SELECT
                product_id,
                product_name,
                price,
                image,
                stock

            FROM products

            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cur.fetchone()

        if product:

            # Prevent quantity from exceeding stock
            quantity = min(
                int(quantity),
                int(product[4])
            )

            subtotal = (
                float(product[2])
                * quantity
            )

            grand_total += subtotal

            cart_items.append(
                {
                    "product_id": product[0],
                    "product_name": product[1],
                    "price": product[2],
                    "image": product[3],
                    "stock": product[4],
                    "quantity": quantity,
                    "subtotal": subtotal
                }
            )

    cur.close()

    return render_template(
        "cart/cart.html",
        cart_items=cart_items,
        grand_total=grand_total
    )


# ==========================================================
# UPDATE CART QUANTITY
# ==========================================================
@cart_bp.route(
    "/cart/update/<int:product_id>",
    methods=["POST"]
)
def update_cart(product_id):

    # Customer login protection
    if not session.get("customer_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )

    quantity = request.form.get(
        "quantity",
        type=int
    )

    # Quantity must be at least 1
    if quantity is None or quantity < 1:

        flash(
            "Quantity must be at least 1.",
            "warning"
        )

        return redirect(
            url_for("cart.view_cart")
        )

    cur = mysql.connection.cursor()

    # Get available product stock
    cur.execute(
        """
        SELECT stock

        FROM products

        WHERE product_id = %s
        """,
        (product_id,)
    )

    product = cur.fetchone()

    cur.close()

    if product is None:

        flash(
            "Product not found!",
            "danger"
        )

        return redirect(
            url_for("cart.view_cart")
        )

    available_stock = product[0]

    # Prevent quantity from exceeding stock
    if quantity > available_stock:

        flash(
            f"Only {available_stock} products are available.",
            "warning"
        )

        return redirect(
            url_for("cart.view_cart")
        )

    cart = session.get(
        "cart",
        {}
    )

    product_key = str(product_id)

    if product_key in cart:

        cart[product_key] = quantity

        session["cart"] = cart

        session.modified = True

        flash(
            "Cart quantity updated successfully!",
            "success"
        )

    return redirect(
        url_for("cart.view_cart")
    )


# ==========================================================
# REMOVE PRODUCT FROM CART
# ==========================================================
@cart_bp.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
def remove_from_cart(product_id):

    # Customer login protection
    if not session.get("customer_logged_in"):

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )

    cart = session.get(
        "cart",
        {}
    )

    product_key = str(product_id)

    # Remove selected product
    if product_key in cart:

        cart.pop(
            product_key
        )

        session["cart"] = cart

        session.modified = True

        flash(
            "Product removed from cart!",
            "success"
        )

    return redirect(
        url_for("cart.view_cart")
    )