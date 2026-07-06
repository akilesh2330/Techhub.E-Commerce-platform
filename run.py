# run.py
# This is the entry point of our application — the file you actually execute.

from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True gives us auto-reload on code changes + detailed error pages.
    # IMPORTANT: We will turn this OFF before deploying the real project.
    app.run(debug=True)