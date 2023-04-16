from flask import Flask, render_template, request, redirect
import string
import random
import sqlite3

app = Flask(__name__)

# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')

# Define the route to handle form submissions
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    short_url = generate_short_url()
    save_mapping(short_url, long_url)
    return render_template('shortened.html', short_url=short_url)

# Define the route to redirect short URLs
@app.route('/<short_url>')
def redirect_short_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url, code=301)
    else:
        return render_template('not_found.html'), 404

# Helper function to generate a random string for the short URL
def generate_short_url():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))

# Helper function to save the mapping between short and long URLs in a database
def save_mapping(short_url, long_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('INSERT INTO mappings (short_url, long_url) VALUES (?, ?)', (short_url, long_url))
    conn.commit()
    conn.close()

# Helper function to get the long URL from the database using the short URL
def get_long_url(short_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT long_url FROM mappings WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
