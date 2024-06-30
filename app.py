from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# MySQL configurations
db = mysql.connector.connect(
    host="127.0.0.1",
    port=8080,
    user="root",
    password="@Work00",
    database="product_db"
)

cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def submit_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        features = request.form['features']
        
        # Handling file uploads
        product_image = request.files['product_image']
        product_table = request.files['product_table']
        product_chart = request.files['product_chart']

        image_url = secure_filename(product_image.filename)
        table_url = secure_filename(product_table.filename)
        chart_url = secure_filename(product_chart.filename)

        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
        product_table.save(os.path.join(app.config['UPLOAD_FOLDER'], table_url))
        product_chart.save(os.path.join(app.config['UPLOAD_FOLDER'], chart_url))

        query = """
            INSERT INTO products (product_name, category, features, image_url, table_url, chart_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (product_name, category, features, image_url, table_url, chart_url))
        db.commit()

        return redirect(url_for('submit_product'))

    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)
