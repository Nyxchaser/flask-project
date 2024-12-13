import os
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app(): # factory pattern for creating application
    app = Flask(__name__)

    # saves database into application
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog


    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get('content')  # Match the form field name
            formatted_date = datetime.datetime.today().strftime('%m/%d/%Y')
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries = []  # List to store blog entries
        for entry in app.db.entries.find({}):
            content = entry['content']
            original_date = entry['date']
            formatted_date = datetime.datetime.strptime(original_date, '%m/%d/%Y').strftime("%b %d")
            entries.append((content, original_date, formatted_date))

        return render_template('home.html', entries=entries)  # Pass entries to the template

    return app

if __name__ == '__main__':
    app = create_app()  # Create the app instance
    app.run(debug=True)  # Start the Flask development server