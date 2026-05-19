cd /Users/erekofke/Documents/Projects/React Projects/Rekode_Portfolio/Rekode_Training
touch wsgi.py

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()