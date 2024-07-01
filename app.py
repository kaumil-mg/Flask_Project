from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import mysql.connector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/gallery'
app.secret_key = 'your_secret_key'

# Ensure the uploads and gallery folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL configurations
db = mysql.connector.connect(
    host="127.0.0.1",
    port=8080,
    user="root",
    password="@Work00",
    database="product_db"
)

@app.route('/')
def home():
    return redirect('/add-product')

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        features = request.form['features']

        product_image = request.files['product_image']
        product_table = request.files['product_table']
        product_chart = request.files['product_chart']

        image_url = secure_filename(product_image.filename)
        table_url = secure_filename(product_table.filename)
        chart_url = secure_filename(product_chart.filename)

        product_image.save(os.path.join('uploads', image_url))
        product_table.save(os.path.join('uploads', table_url))
        product_chart.save(os.path.join('uploads', chart_url))

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO products (product_name, category, features, image_url, table_url, chart_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_name, category, features, image_url, table_url, chart_url))
        db.commit()
        cursor.close()

        return redirect('/add-product')

    return render_template('add_product.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        gallery_image = request.files['gallery_image']
        image_url = secure_filename(gallery_image.filename)
        gallery_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO gallery (image_url)
            VALUES (%s)
        """, (image_url,))
        db.commit()
        cursor.close()

        return redirect('/gallery')

    return render_template('gallery.html')

if __name__ == '__main__':
    app.run(debug=True)
