from flask import Blueprint, render_template
from app import mysql

main_bp = Blueprint("main", __name__)


# ==========================================================
# HOME PAGE
# ==========================================================
@main_bp.route("/")
def home():

    cur = mysql.connection.cursor()

    # Get all categories
    cur.execute(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        ORDER BY category_name ASC
        """
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        "home.html",
        categories=categories
    )


# ==========================================================
# CATEGORY PRODUCTS PAGE
# ==========================================================
@main_bp.route("/category/<int:category_id>")
def category_products(category_id):

    cur = mysql.connection.cursor()

    # Get selected category
    cur.execute(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        WHERE category_id = %s
        """,
        (category_id,)
    )

    category = cur.fetchone()

    # Get products only from the selected category
    cur.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            p.price,
            p.image,
            c.category_name,
            b.brand_name

        FROM products p

        JOIN categories c
            ON p.category_id = c.category_id

        JOIN brands b
            ON p.brand_id = b.brand_id

        WHERE p.category_id = %s

        ORDER BY
            p.price DESC,
            p.product_name ASC
        """,
        (category_id,)
    )

    products = cur.fetchall()

    cur.close()

    return render_template(
        "category_products.html",
        category=category,
        products=products
    )