from playwright.sync_api import sync_playwright, TimeoutError
from concurrent.futures import ThreadPoolExecutor
import time

def log(browser, msg):
    print(f"[{browser}] {msg}")
# Uruchomienie testu na 3 przeglądarkach
def run_test(browser_name):
    log(browser_name, "Start testu")
    try:
        with sync_playwright() as p:
            if browser_name == "chromium":
                browser = p.chromium.launch(headless=False)
            elif browser_name == "firefox":
                browser = p.firefox.launch(headless=False)
            elif browser_name == "webkit":
                browser = p.webkit.launch(headless=False)
            else:
                log(browser_name, f"Nieznana przeglądarka: {browser_name}")
                return

            context = browser.new_context()
            page = context.new_page()
# Czyszczenie ciasteczek
            context.clear_cookies()
            log(browser_name, "Ciasteczka wyczyszczone")
# Przejście na stronę ING
            page.goto('https://www.ing.pl/')
            page.wait_for_load_state("load")
            log(browser_name, "Strona załadowana")
# Pobranie ciasteczek przed akceptacją
            cookies_before = context.cookies()
            log(browser_name, f"[Przed akceptacją] Liczba ciasteczek: {len(cookies_before)}")
            for c in cookies_before:
                log(browser_name, f"[Przed] - {c['name']} ({c['domain']})")
# Wybranie opcji "Dostosuj"
            try:
                button = page.wait_for_selector('button:has-text("Dostosuj")', timeout=10000)
                if button.is_visible():
                    log(browser_name, "Przycisk 'Dostosuj' widoczny")
                    if button.is_enabled():
                        log(browser_name, "Przycisk 'Dostosuj' klikalny")
                        button.click()
                        log(browser_name, "Kliknięto 'Dostosuj'")
                    else:
                        log(browser_name, "Przycisk 'Dostosuj' NIE jest klikalny")
                else:
                    log(browser_name, "Przycisk 'Dostosuj' NIE jest widoczny")
            except TimeoutError:
                log(browser_name, "Przycisk 'Dostosuj' nie został znaleziony w czasie oczekiwania")

# Wybranie opcji "Ciasteczka analityczne"
            try:
                toggle = page.wait_for_selector('div.cookie-policy-type:nth-child(2) > div:nth-child(2) > div:nth-child(1)', timeout=10000)

                if toggle.is_visible():
                    log(browser_name, "Przycisk 'Ciasteczka analityczne' widoczny")
                    if toggle.is_enabled():
                        log(browser_name, "Przycisk 'Ciasteczka analityczne' klikalny")
                        toggle.click(force=True)
                        log(browser_name, "Kliknięto 'Ciasteczka analityczne'")
                    else:
                        log(browser_name, "Przycisk 'Ciasteczka analityczne' NIE jest klikalny")
                else:
                    log(browser_name, "Przycisk 'Ciasteczka analityczne' NIE jest widoczny")
            except TimeoutError:
                log(browser_name, "Przycisk 'Ciasteczka analityczne' nie został znaleziony w czasie oczekiwania")
# Kliknięcie opcji Zaakceptuj zaznaczone
            try:
                button = page.wait_for_selector('button:has-text("Zaakceptuj zaznaczone")', timeout=10000)
                if button.is_visible():
                    log(browser_name, "Przycisk 'Zaakceptuj zaznaczone' widoczny")
                    if button.is_enabled():
                        log(browser_name, "Przycisk 'Zaakceptuj zaznaczone' klikalny")
                        button.click()
                        log(browser_name, "Kliknięto 'Zaakceptuj zaznaczone'")
                    else:
                        log(browser_name, "Przycisk 'Zaakceptuj zaznaczone' NIE jest klikalny")
                else:
                    log(browser_name, "Przycisk 'Zaakceptuj zaznaczone' NIE jest widoczny")
            except TimeoutError:
                log(browser_name, "Przycisk 'Zaakceptuj zaznaczone' nie został znaleziony w czasie oczekiwania")
# Pobranie ciasteczek po akceptacji
            cookies_after = context.cookies()
            log(browser_name, f"[Po akceptacji] Liczba ciasteczek: {len(cookies_after)}")
            for c in cookies_after:
                log(browser_name, f" - {c['name']} ({c['domain']})")
# Porównanie zmian
            names_before = set(c['name'] for c in cookies_before)
            names_after = set(c['name'] for c in cookies_after)

            added = [c for c in cookies_after if c['name'] not in names_before]
            removed = [c for c in cookies_before if c['name'] not in names_after]

            log(browser_name, f"[Różnice] Dodano {len(added)} ciasteczek:")
            for c in added:
                log(browser_name, f"[Dodane] - {c['name']} ({c['domain']})")

            log(browser_name, f"[Różnice] Usunięto {len(removed)} ciasteczek:")
            for c in removed:
                log(browser_name, f"[Usunięte] - {c['name']} ({c['domain']})")
# Zamknięcie przeglądarki
            browser.close()
    except Exception as e:
        log(browser_name, f"Błąd testu: {e}")
        

if __name__ == '__main__':
    browsers = ["chromium", "firefox", "webkit"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_test, browsers)
