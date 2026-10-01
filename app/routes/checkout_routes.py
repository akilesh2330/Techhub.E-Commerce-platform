from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app import mysql


# Create Checkout Blueprint
checkout_bp = Blueprint("checkout", __name__)


# ==========================================================
# CHECKOUT PAGE
# ==========================================================
@checkout_bp.route("/checkout", methods=["GET", "POST"])
def checkout():

    # Customer must be logged in
    if not session.get("customer_logged_in"):

        flash(
            "Please login to continue checkout.",
            "warning"
        )

        return redirect(
            url_for("auth.customer_login")
        )


    # Get cart from session
    cart = session.get("cart", {})


    # Check whether cart is empty
    if not cart:

        flash(
            "Your cart is empty!",
            "warning"
        )

        return redirect(
            url_for("cart.view_cart")
        )


    # Store cart product details
    cart_items = []

    grand_total = 0


    # Create database cursor
    cur = mysql.connection.cursor()


    # ======================================================
    # GET PRODUCTS FROM DATABASE
    # ======================================================

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


        # If product was deleted
        if product is None:

            cur.close()

            flash(
                "One of the products in your cart is no longer available.",
                "danger"
            )

            return redirect(
                url_for("cart.view_cart")
            )


        quantity = int(quantity)

        available_stock = int(product[4])


        # Check whether enough stock is available
        if quantity > available_stock:

            cur.close()

            flash(
                f"Only {available_stock} units of "
                f"{product[1]} are available.",
                "warning"
            )

            return redirect(
                url_for("cart.view_cart")
            )


        # Calculate product subtotal
        subtotal = (
            float(product[2])
            * quantity
        )


        # Add subtotal to total amount
        grand_total += subtotal


        # Add product details to cart list
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


    # ======================================================
    # PLACE ORDER
    # ======================================================

    if request.method == "POST":


        # Get delivery information
        full_name = request.form.get(
            "full_name",
            ""
        ).strip()


        phone = request.form.get(
            "phone",
            ""
        ).strip()


        address = request.form.get(
            "address",
            ""
        ).strip()


        city = request.form.get(
            "city",
            ""
        ).strip()


        state = request.form.get(
            "state",
            ""
        ).strip()


        pincode = request.form.get(
            "pincode",
            ""
        ).strip()


        payment_method = request.form.get(
            "payment_method",
            ""
        )


        # ==================================================
        # VALIDATE CHECKOUT DETAILS
        # ==================================================

        if (
            not full_name
            or not phone
            or not address
            or not city
            or not state
            or not pincode
            or not payment_method
        ):

            cur.close()

            flash(
                "Please fill in all checkout details.",
                "warning"
            )

            return redirect(
                url_for("checkout.checkout")
            )


        # Phone number validation
        if (
            not phone.isdigit()
            or len(phone) != 10
        ):

            cur.close()

            flash(
                "Please enter a valid 10-digit phone number.",
                "warning"
            )

            return redirect(
                url_for("checkout.checkout")
            )


        # Pincode validation
        if (
            not pincode.isdigit()
            or len(pincode) != 6
        ):

            cur.close()

            flash(
                "Please enter a valid 6-digit pincode.",
                "warning"
            )

            return redirect(
                url_for("checkout.checkout")
            )


        try:

            # Get logged-in customer ID
            customer_id = session.get(
                "customer_id"
            )


            # ==============================================
            # SAVE ORDER
            # ==============================================

            cur.execute(
                """
                INSERT INTO orders
                (
                    customer_id,
                    full_name,
                    phone,
                    address,
                    city,
                    state,
                    pincode,
                    payment_method,
                    total_amount,
                    order_status
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    'Pending'
                )
                """,
                (
                    customer_id,
                    full_name,
                    phone,
                    address,
                    city,
                    state,
                    pincode,
                    payment_method,
                    grand_total
                )
            )


            # Get newly created order ID
            order_id = cur.lastrowid


            # ==============================================
            # SAVE ORDER PRODUCTS
            # ==============================================

            for item in cart_items:


                cur.execute(
                    """
                    INSERT INTO order_items
                    (
                        order_id,
                        product_id,
                        product_name,
                        price,
                        quantity,
                        subtotal
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        order_id,
                        item["product_id"],
                        item["product_name"],
                        item["price"],
                        item["quantity"],
                        item["subtotal"]
                    )
                )


                # ==========================================
                # REDUCE PRODUCT STOCK
                # ==========================================

                cur.execute(
                    """
                    UPDATE products

                    SET stock = stock - %s

                    WHERE product_id = %s

                    AND stock >= %s
                    """,
                    (
                        item["quantity"],
                        item["product_id"],
                        item["quantity"]
                    )
                )


                # Stock changed before order was placed
                if cur.rowcount == 0:

                    raise ValueError(
                        "Product stock is no longer available."
                    )


            # Save all database changes
            mysql.connection.commit()


        except Exception as error:


            # Cancel all changes if an error occurs
            mysql.connection.rollback()


            cur.close()


            flash(
                f"Order could not be placed: {error}",
                "danger"
            )


            return redirect(
                url_for("cart.view_cart")
            )


        # Close database cursor
        cur.close()


        # Clear the cart after successful order
        session["cart"] = {}

        session.modified = True


        flash(
            f"Order #{order_id} placed successfully!",
            "success"
        )


        return redirect(
            url_for("main.home")
        )


    # Close cursor for GET request
    cur.close()


    # Display checkout page
    return render_template(
        "checkout/checkout.html",
        cart_items=cart_items,
        grand_total=grand_total
    )