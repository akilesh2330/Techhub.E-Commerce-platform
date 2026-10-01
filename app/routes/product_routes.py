from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql

product_bp = Blueprint("product", __name__)


# ==========================================
# ADD PRODUCT
# ==========================================

@product_bp.route("/admin/add-product", methods=["GET", "POST"])
def add_product():

    cur = mysql.connection.cursor()

    # Categories
    cur.execute("SELECT category_id, category_name FROM categories")
    categories = cur.fetchall()

    # Brands
    cur.execute("SELECT brand_id, brand_name FROM brands")
    brands = cur.fetchall()

    if request.method == "POST":

        product_name = request.form.get("product_name")
        description = request.form.get("description")
        specifications = request.form.get("specifications")
        price = request.form.get("price")
        stock = request.form.get("stock")
        image = request.form.get("image")
        category = request.form.get("category")
        brand = request.form.get("brand")

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
        (%s,%s,%s,%s,%s,%s,%s,%s)
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

        flash("Product Added Successfully!", "success")

        return redirect(url_for("admin.admin_dashboard"))

    cur.close()

    return render_template(
        "products/add_product.html",
        categories=categories,
        brands=brands
    )
# ==========================================
# PRODUCT DETAILS
# ==========================================

@product_bp.route("/product/<int:product_id>")
def product_details(product_id):

    cur = mysql.connection.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.description,
            p.specifications,
            p.price,
            p.stock,
            p.image,
            c.category_name,
            b.brand_name

        FROM products p

        JOIN categories c
            ON p.category_id = c.category_id

        JOIN brands b
            ON p.brand_id = b.brand_id

        WHERE p.product_id = %s
    """

    cur.execute(
        query,
        (product_id,)
    )

    product = cur.fetchone()

    cur.close()

    # If the product is not found
    if product is None:

        flash(
            "Product not found!",
            "danger"
        )

        return redirect(
            url_for("main.home")
        )

    return render_template(
        "products/product_details.html",
        product=product
    )