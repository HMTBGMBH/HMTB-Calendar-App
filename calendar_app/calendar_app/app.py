from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from dropbox_integration import upload_to_dropbox, download_from_dropbox

app = Flask(__name__)

# Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect('db/calendar.db')
    conn.row_factory = sqlite3.Row
    return conn

# Startseite mit der Kalenderansicht
@app.route('/')
def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events)

# Termin hinzufügen
@app.route('/add', methods=('GET', 'POST'))
def add_event():
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        customer = request.form['customer']
        other_customer = request.form.get('other_customer')
        location = request.form['location']
        event_type = request.form['event_type']
        comment = request.form['comment']
        confirmation = request.form['confirmation']
        document_type = request.form['document_type']

        if other_customer:
            customer = other_customer

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO events (date, start_time, end_time, customer, location, event_type, comment, confirmation, document_type) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, customer, location, event_type, comment, confirmation, document_type))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_event.html')

# Termin bearbeiten
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_event(id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        customer = request.form['customer']
        other_customer = request.form.get('other_customer')
        location = request.form['location']
        event_type = request.form['event_type']
        comment = request.form['comment']
        confirmation = request.form['confirmation']
        document_type = request.form['document_type']

        if other_customer:
            customer = other_customer

        conn.execute('''
            UPDATE events SET date = ?, start_time = ?, end_time = ?, customer = ?, location = ?, event_type = ?, comment = ?, confirmation = ?, document_type = ?
            WHERE id = ?
        ''', (date, start_time, end_time, customer, location, event_type, comment, confirmation, document_type, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_event.html', event=event)

# Termin löschen
@app.route('/delete/<int:id>', methods=('POST',))
def delete_event(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Dropbox Integration: Termin hochladen
@app.route('/upload_to_dropbox/<int:id>', methods=['POST'])
def upload_event_to_dropbox(id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    # Event als Text speichern und zu Dropbox hochladen
    event_details = f"Date: {event['date']}, Start Time: {event['start_time']}, End Time: {event['end_time']}, ..."
    upload_to_dropbox(event_details, f"event_{id}.txt")
    
    return redirect(url_for('index'))

# Dropbox Integration: Termin herunterladen
@app.route('/download_from_dropbox/<int:id>', methods=['POST'])
def download_event_from_dropbox(id):
    event_details = download_from_dropbox(f"event_{id}.txt")
    return jsonify(event_details)

if __name__ == '__main__':
    app.run(debug=True)
