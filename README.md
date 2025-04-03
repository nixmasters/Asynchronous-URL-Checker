# Asynchronous-URL-Checker

Koristeći `asyncio` i asinhroni HTTP klijent `httpx`, kreirao sam program koji paralelno provjerava više GET i POST zahtjeva za različite URL-ove.

## Ulazni Podaci

Ulaz za ovaj program je `.txt` fajl pod nazivom `urls.txt`, koji sadrži više GET zahtjeva, POST zahtjeva i jedan GET zahtjev sa autorizacijom koji zahtijeva API ključ.

## Podaci Koji Se Prikupljaju Za Svaki Zahtjev

Za svaki zahtjev, prikupljaju se sljedeći podaci:

1. **URL Adresa**
2. **HTTP Status Kod**
3. **Vrijeme Odgovora** (u sekundama)

Ovi zahtjevi se prikupljaju i čuvaju u nizu pod nazivom `rezultati`, koji se kasnije pakuje u fajl `rezultati.json`.

## Obrada Grešaka

U slučaju grešaka tokom izvršavanja zahtjeva, program ih obrađuje i prikazuje odgovarajuće poruke o greškama. Greške uključuju:

1. **TimeoutException** - Zahtjev nije završen na vrijeme (istekao je vremenski limit).
2. **RequestError** - Mrežna greška ili problem sa serverom koji sprječava izvršenje zahtjeva.
3. **HTTPStatusError** - Greške statusnog koda, kao što su HTTP statusi 4xx ili 5xx koji ukazuju na probleme sa klijentom ili serverom.

Ove greške su vidljive u konzoli, a detaljno su zabilježene u generisanom `.json` fajlu.

