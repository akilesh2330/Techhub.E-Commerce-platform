from flask import (Blueprint,render_template,request,redirect,url_for,flash,session)

from app import mysql

# Create Auth Blueprint
auth_bp = Blueprint("auth", __name__)   

# ==========================================================
# CUSTOMER SIGNUP
# ==========================================================
@auth_bp.route("/signup", methods=["GET", "POST"])
def customer_signup():

    # If customer is already logged in
    if session.get("customer_logged_in"):

        return redirect(
            url_for("main.home")
        )

    if request.method == "POST":

        # Get signup form details
        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # Check whether any field is empty
        if (
            not full_name
            or not email
            or not password
            or not confirm_password
        ):

            flash(
                "Please fill in all fields.",
                "warning"
            )

            return redirect(
                url_for("auth.customer_signup")
            )


        # Check whether passwords are the same
        if password != confirm_password:

            flash(
                "Passwords do not match!",
                "danger"
            )

            return redirect(
                url_for("auth.customer_signup")
            )


        # Create database cursor
        cur = mysql.connection.cursor()


        # Check whether email already exists
        cur.execute(
            """
            SELECT user_id

            FROM users

            WHERE LOWER(email) = LOWER(%s)
            """,
            (email,)
        )


        existing_user = cur.fetchone()


        # If email already exists
        if existing_user:

            cur.close()

            flash(
                "An account with this email already exists!",
                "warning"
            )

            return redirect(
                url_for("auth.customer_signup")
            )


        # Add new customer to users table
        cur.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password,
                role
            )

            VALUES
            (
                %s,
                %s,
                %s,
                'customer'
            )
            """,
            (
                full_name,
                email,
                password
            )
        )


        # Save data
        mysql.connection.commit()


        # Close database cursor
        cur.close()


        flash(
            "Account created successfully! Please login.",
            "success"
        )


        return redirect(
            url_for("auth.customer_login")
        )


    return render_template(
        "auth/signup.html"
    )


# ==========================================================
# CUSTOMER LOGIN
# ==========================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def customer_login():

    # If customer is already logged in
    if session.get("customer_logged_in"):

        return redirect(
            url_for("main.home")
        )


    if request.method == "POST":

        # Get login details
        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        # Create database cursor
        cur = mysql.connection.cursor()


        # Check customer email and password
        cur.execute(
            """
            SELECT
                user_id,
                full_name,
                email,
                role

            FROM users

            WHERE email = %s

            AND password = %s

            AND role = 'customer'
            """,
            (
                email,
                password
            )
        )


        customer = cur.fetchone()


        # Close database cursor
        cur.close()


        # If customer details are correct
        if customer:

            # Create customer session
            session["customer_logged_in"] = True

            session["customer_id"] = customer[0]

            session["customer_name"] = customer[1]

            session["customer_email"] = customer[2]


            flash(
                "Login Successful!",
                "success"
            )


            return redirect(
                url_for("main.home")
            )


        # Incorrect login details
        flash(
            "Invalid customer email or password!",
            "danger"
        )


    return render_template(
        "auth/login.html"
    )


# ==========================================================
# CUSTOMER LOGOUT
# ==========================================================
@auth_bp.route("/logout")
def customer_logout():

    # Remove customer login information
    session.pop(
        "customer_logged_in",
        None
    )

    session.pop(
        "customer_id",
        None
    )

    session.pop(
        "customer_name",
        None
    )

    session.pop(
        "customer_email",
        None
    )


    flash(
        "Logged Out Successfully!",
        "success"
    )


    return redirect(
        url_for("auth.customer_login")
    )