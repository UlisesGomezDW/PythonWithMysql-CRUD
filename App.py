from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST'] = 'bzmnlqfbzcwpkyatgaqk-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u0or8jlthvzi1zyf'
app.config['MYSQL_PASSWORD'] = 'Uuy0SDPx46x1MFXBYIPH'
app.config['MYSQL_DB'] = 'bzmnlqfbzcwpkyatgaqk'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

#Routes
@app.route('/')
def Index():
    cursorGet = mysql.connection.cursor()
    cursorGet.execute('SELECT * FROM contacts')
    data = cursorGet.fetchall()
    return render_template('index.html', contacts=data)

@app.route('/add/', methods=['POST'])
def addContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash("Contact added successfully!")
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def getContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def updateContact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
