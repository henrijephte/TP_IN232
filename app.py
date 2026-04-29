from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3, json, io, csv, statistics, math

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT, prenom TEXT, matricule TEXT,
            banque TEXT, faculte TEXT, niveau TEXT,
            montant REAL, raison TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM etudiants').fetchall()
    montants = [r['montant'] for r in rows]
    total_n = len(rows)

    stats = {
        'moyenne': 0, 'mediane': 0, 'ecart_type': 0,
        'min': 0, 'max': 0, 'cv': 0,
        'ic_bas': 0, 'ic_haut': 0
    }
    p_inclusion = 0

    if total_n >= 1:
        moy = statistics.mean(montants)
        stats['moyenne'] = moy
        stats['mediane'] = statistics.median(montants)
        stats['min']     = min(montants)
        stats['max']     = max(montants)

        if total_n > 1:
            sd = statistics.stdev(montants)
            stats['ecart_type'] = sd
            # Coefficient de variation (%)
            stats['cv'] = round((sd / moy) * 100, 1) if moy else 0
            # Intervalle de confiance à 95 % (t ≈ 1.96 pour n > 30, sinon approximation)
            se = sd / math.sqrt(total_n)
            stats['ic_bas']  = moy - 1.96 * se
            stats['ic_haut'] = moy + 1.96 * se

        nb_banc = sum(1 for r in rows if r['banque'] != 'Sans Banque')
        p_inclusion = round((nb_banc / total_n) * 100, 2)

    st_b   = conn.execute('SELECT banque, COUNT(*) as nb FROM etudiants GROUP BY banque').fetchall()
    st_f   = conn.execute('SELECT faculte, COUNT(*) as nb FROM etudiants GROUP BY faculte').fetchall()
    st_niv = conn.execute('SELECT niveau, COUNT(*) as nb FROM etudiants GROUP BY niveau').fetchall()
    # Montant moyen par faculté
    st_moy_f = conn.execute('SELECT faculte, AVG(montant) as moy FROM etudiants GROUP BY faculte').fetchall()
    conn.close()

    return render_template(
        'dashboard.html',
        stats=stats, p_inclusion=p_inclusion, total=total_n,
        l_b=json.dumps([r['banque']  for r in st_b]),
        c_b=json.dumps([r['nb']      for r in st_b]),
        l_f=json.dumps([r['faculte'] for r in st_f]),
        c_f=json.dumps([r['nb']      for r in st_f]),
        l_niv=json.dumps([r['niveau'] for r in st_niv]),
        c_niv=json.dumps([r['nb']     for r in st_niv]),
        l_moy_f=json.dumps([r['faculte']      for r in st_moy_f]),
        c_moy_f=json.dumps([round(r['moy'], 0) for r in st_moy_f]),
    )

@app.route('/nouveau')
def nouveau():
    return render_template('nouveau.html')

@app.route('/donnees')
def donnees():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM etudiants ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('donnees.html', rows=rows)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO etudiants (nom, prenom, matricule, banque, faculte, niveau, montant, raison) VALUES (?,?,?,?,?,?,?,?)',
        (request.form['nom'], request.form['prenom'], request.form['matricule'],
         request.form['banque'], request.form['faculte'], request.form['niveau'],
         request.form['montant'], request.form['raison'])
    )
    conn.commit()
    conn.close()
    return redirect(url_for('donnees'))

@app.route('/exporter')
def exporter():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM etudiants').fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Matricule', 'Nom', 'Banque', 'Faculté', 'Montant'])
    for r in rows:
        writer.writerow([r['matricule'], r['nom'], r['banque'], r['faculte'], r['montant']])
    output.seek(0)
    return Response(
        output.read(), mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=Rapport_UY1.csv"}
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)