from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import csv

FIRMA_NIP = "1234567890"

app = Flask(__name__)

@app.route('/')
def home():
    klienci = []
    if os.path.exists("klienci.csv"):
        with open("klienci.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            klienci = list(reader)
    return render_template('form.html', klienci=klienci)

@app.route('/generate', methods=['POST'])
def generate_invoice():
    data = request.form.to_dict()
    zapisz = 'zapisz_fakture' in data

    now = datetime.today()
    numer_faktury = "FV/TEMP"

    if zapisz:
        # Odczyt i aktualizacja numeru faktury
        numer_file = "numer.txt"
        if os.path.exists(numer_file):
            with open(numer_file, "r") as f:
                last_number = int(f.read().strip())
        else:
            last_number = 1
        
        numer_faktury = f"FV/{now.year}/{now.month:02d}/{last_number:03d}"

        with open(numer_file, "w") as f:
            f.write(str(last_number + 1))
        
        # Zapisz fakturę do pliku CSV
        with open("historia_faktur.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([numer_faktury, now.strftime('%Y-%m-%d'), data.get('typ_klienta'),
                             data.get('imie', ''), data.get('nazwisko', ''),
                             data.get('nazwa_firmy', ''), data.get('nip', ''),
                             data.get('opis', ''), data.get('kwota_netto'),
                             data.get('vat', ''), round(float(data.get('kwota_netto', 0)) * (1 + float(data.get('vat', 0)) / 100), 2)])

    # Dane faktury
    typ_klienta = data.get('typ_klienta')
    imie = data.get('imie', '')
    nazwisko = data.get('nazwisko', '')
    nazwa_firmy = data.get('nazwa_firmy', '')
    nip = data.get('nip', '').strip()
    if nip:
        if len(nip) != 10 or not nip.isdigit():
            return "Błąd: NIP klienta musi mieć dokładnie 10 cyfr.", 400
    adres_klienta = data.get('adres_klienta', '')
    opis = data.get('opis', 'Opis niepodany')
    nip_firmy = FIRMA_NIP # stały nr NIP dla firmy

    kwota_netto = float(data.get('kwota_netto', 0))
    if not kwota_netto or float(kwota_netto) <= 0:
        return "Błąd: Musisz wpisać kwotę netto większą niż 0.", 400
    kwota_netto = float(kwota_netto)
    
    vat = float(data.get('vat', 0))
    kwota_brutto = round(kwota_netto * (1 + vat / 100), 2)

    return render_template(
        'invoice.html',
        typ_klienta=typ_klienta,
        imie=imie,
        nazwisko=nazwisko,
        nazwa_firmy=nazwa_firmy,
        nip=nip,
        adres_klienta=adres_klienta,
        nip_firmy=nip_firmy,
        kwota_netto=kwota_netto,
        vat=vat,
        kwota_brutto=kwota_brutto,
        data_wystawienia=now.strftime('%Y-%m-%d'),
        numer_faktury=numer_faktury,
        opis=opis
    )

@app.route('/historia')
def historia():
    faktury = []
    if os.path.exists("historia_faktur.csv"):
        with open("historia_faktur.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            faktury = list(reader)
    
    return render_template("historia.html", faktury=faktury)

@app.route('/usun', methods=['POST'])
def usun_fakture():
    numer_do_usuniecia = request.form.get('numer_faktury')
    nowa_lista = []

    if os.path.exists("historia_faktur.csv"):
        with open("historia_faktur.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            nowa_lista = [row for row in reader if row[0] != numer_do_usuniecia]

        with open("historia_faktur.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(nowa_lista)

    return redirect(url_for('historia'))

@app.route('/klienci')
def klienci():
    lista = []
    if os.path.exists("klienci.csv"):
        with open("klienci.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            lista = list(reader)
        return render_template("klienci.html", klienci=lista)

@app.route('/dodaj_klienta', methods=['POST'])
def dodaj_klienta():
    dane = request.form
    with open("klienci.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([dane.get('typ_klienta'), dane.get('imie'), dane.get('nazwisko'),
                         dane.get('nazwa_firmy'), dane.get('nip'), dane.get('adres')])
    return redirect(url_for('klienci'))

if __name__ == '__main__':
    app.run(debug=True)
