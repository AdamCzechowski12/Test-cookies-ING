# Test Python + Playwright – Test_Cookies_ING_Adam_Czechowski

Automatyczny test E2E wykonany przy użyciu [Playwright](https://playwright.dev/python/), sprawdzający zachowanie ciasteczek na stronie [https://www.ing.pl] przed i po akceptacji użycia ciasteczek analitycznych.

# Wymagania
- IDLE Shell 3.13.4 lub kompatybilny
- Python 3.7 lub wyższy
- Playwright dla Pythona

# Uruchomienie

1. Otwórz Idle Shell
2. Kliknij przycisk "File"
3. Z Listy wybierz i kliknij "Open"
4. Wybierz plik: Test_Cookies_ING_Adam_Czechowski i kliknij "Otwórz"
5. W nowo otwartym pliku kliknij "Run" a następnie "Run Module"

Jeżeli użytkownik posiada tylko Python:
pip install playwright
python -m playwright install
python .\Test_Cookies_ING_Adam_Czechowski.py

# Funkcjonalność

- Otwiera stronę ING.pl
- Czyści ciasteczka przed rozpoczęciem testu
- Wchodzi w ustawienia ciasteczek („Dostosuj”)
- Włącza „Ciasteczka analityczne”
- Zatwierdza zaznaczone ustawienia
- Porównuje ciasteczka przed i po akceptacji ciasteczek analitycznych
- Loguje dodane i usunięte ciasteczka

Test uruchamiany jest równolegle w trzech przeglądarkach:
- Chromium
- Firefox
- WebKit
