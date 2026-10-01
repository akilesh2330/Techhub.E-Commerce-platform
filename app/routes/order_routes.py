from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from app import mysql


# Create Order Blueprint
order_bp = Blueprint("order", __name__)


# ==========================================================
# CUSTOMER - MY ORDERS
# ==========================================================
@order_bp.route("/my-orders")
def my_orders():

    # Customer must be logged in
    if not session.get("customer_logged_in"):

        flash(
            "Please login to view your orders.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )


    # Get logged-in customer ID
    customer_id = session.get("customer_id")


    # Create database cursor
    cur = mysql.connection.cursor()


    # Get only the logged-in customer's orders
    cur.execute(
        """
        SELECT
            order_id,
            order_date,
            total_amount,
            payment_method,
            order_status

        FROM orders

        WHERE customer_id = %s

        ORDER BY order_date DESC
        """,
        (customer_id,)
    )


    # Store all customer orders
    orders = cur.fetchall()


    # Close database cursor
    cur.close()


    # Display My Orders page
    return render_template(
        "orders/my_orders.html",
        orders=orders
    )


# ==========================================================
# CUSTOMER - ORDER DETAILS
# ==========================================================
@order_bp.route("/order/<int:order_id>")
def order_details(order_id):

    # Customer must be logged in
    if not session.get("customer_logged_in"):

        flash(
            "Please login to view order details.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )


    # Get logged-in customer ID
    customer_id = session.get("customer_id")


    # Create database cursor
    cur = mysql.connection.cursor()


    # Get the selected order
    # customer_id check prevents customers
    # from viewing another customer's order
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

        AND customer_id = %s
        """,
        (
            order_id,
            customer_id
        )
    )


    order = cur.fetchone()


    # If order does not belong to this customer
    if order is None:

        cur.close()

        flash(
            "Order not found!",
            "danger"
        )

        return redirect(
            url_for("order.my_orders")
        )


    # Get all products from the selected order
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


    # Display Order Details page
    return render_template(
        "orders/order_details.html",
        order=order,
        order_items=order_items
    )