# app/routes/main_routes.py
# This file defines the "controller" logic for general/main pages like Home.

from flask import Blueprint, render_template

# Create a Blueprint named "main". 
# First argument = blueprint's internal name, second = its import location.
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    This function runs when a user visits the root URL ("/") of our site.
    It returns the rendered home.html template to the browser.
    """
    return render_template('home.html')