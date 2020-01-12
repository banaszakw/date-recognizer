# date-recognizer
Skrypt rozpoznaje datę i godzinę zapisaną w tekście słownie, np. "jedenastego zero trzeciego trzy kwadranse po drugiej" i konwertuje ją do słownika Pythona w postaci `{'day': 1, 'month': 1, 'hour': 12, 'minute': 0}`.

W założeniu skrypt otrzymuje pojedyncze zdania, które zawierają zarówno datę i godzinę (interpretowaną w formacie 24-godzinnym). Jeżeli miesiąc nie jest podany, skrypt uzna, że chodzi o styczeń (styczeń ma indeks 1). Zdania mogą być niepoprawne gramatycznie, ale nie mogą zawierać literówek.’

Przykłady:
"ósmego kwadrans na ósmą" - `{'day': 8, 'month': 1, 'hour': 7, 'minute': 15}`
"zero ósmy zero siódmy o ósmej osiemnaście" - `'day': 8, 'month': 7, 'hour': 8, 'minute': 18})`
"siedemnastego w południe" - `{'day': 17, 'month': 1, 'hour': 12, 'minute': 0}`
"trzydziesty marca za piętnaście południe" - `{'day': 30, 'month': 3, 'hour': 11, 'minute': 45}`
"dwudziesty trzeci za dwadzieścia dwie dwudziesta pierwsza" - `{'day': 23, 'month': 1, 'hour': 20, 'minute': 38}`

