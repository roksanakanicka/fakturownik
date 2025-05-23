# Fakturownik App

Aplikacja webowa do generowania faktur, stworzona na potrzeby zajęć z **Analizy Systemów Informatycznych**. Wykorzystuje **Flask** do obsługi backendu oraz **Bootstrap** do stylizacji interfejsu.

## Funkcje

- Generowanie faktur HTML z danymi klienta  
- Automatyczne nadawanie numeru faktury  
- Historia wystawionych faktur z możliwością usuwania  
- Baza klientów z automatycznym uzupełnianiem danych w formularzu  
- Walidacja danych (NIP, kwota netto)  
- Stylizacja interfejsu z użyciem Bootstrap  

## Jak uruchomić projekt?

Aby uruchomić aplikację lokalnie:

```bash
git clone git@github.com:roksanakanicka/fakturownik.git
cd fakturownik
python -m venv .venv
.venv\Scripts\activate   # dla Windows
# lub
source .venv/bin/activate   # dla Linux/Mac
pip install -r requirements.txt
python main.py
```

Po uruchomieniu aplikacja będzie dostępna pod adresem:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Struktura projektu

```
invoices_app/
├── .venv/
├── templates/
│   ├── base.html
│   ├── form.html
│   ├── invoice.html
│   ├── historia.html
│   └── klienci.html
├── main.py
├── klienci.csv
├── historia_faktur.csv
├── numer.txt
├── requirements.txt
└── README.md
```

## Autor

Roksana Kanicka, 2025
