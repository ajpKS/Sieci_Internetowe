// DOM

const przycisk = document.getElementById('wczytaj');
const wyniki = document.getElementById('wyniki');
const ladowanie = document.getElementById('ladowanie');
const blad = document.getElementById('blad');
const brak = document.getElementById('brak');
const filtrGatunek = document.getElementById('filtr-gatunek');
const filtrMulti = document.getElementById('filtr-multi');

function element(tag, tekst, klasa) {
    const el = document.createElement(tag);
    if (tekst !== undefined) el.textContent = tekst;
    if (klasa) el.className = klasa;
    return el;
}

function narysujGre(gra) {
    const li = document.createElement('li');

    const gora = element('div', undefined, 'gora');
    gora.appendChild(element('strong', gra.tytul));
    gora.appendChild(element('span', gra.gatunek, 'gatunek'));
    li.appendChild(gora);

    li.appendChild(element('p', gra.opis));

    const info = [
        'Premiera: ' + gra.data_premiery,
        'Ocena: ' + gra.ocena + '/10',
        gra.wieloosobowa ? 'wieloosobowa' : 'jednoosobowa',
        gra.cena.toFixed(2) + ' zł'
    ];
    li.appendChild(element('div', info.join('  |  '), 'meta'));
    return li;
}

async function wczytajDane() {
    const params = new URLSearchParams();
    if (filtrGatunek.value) params.set('gatunek', filtrGatunek.value);
    if (filtrMulti.value) params.set('wieloosobowa', filtrMulti.value);
    const adres = '/api/gry/' + (params.toString() ? '?' + params.toString() : '');

    wyniki.replaceChildren();
    blad.hidden = true;
    brak.hidden = true;
    ladowanie.hidden = false;
    przycisk.disabled = true;

    // FETCH

    try {
        const response = await fetch(adres);
        if (!response.ok) {
            throw new Error('błąd HTTP ' + response.status);
        }
        const dane = await response.json();

        if (!dane.items || dane.items.length === 0) {
            brak.hidden = false;
        } else {
            dane.items.forEach(gra => wyniki.appendChild(narysujGre(gra)));
        }
    } catch (err) {
        blad.textContent = 'Nie udało się pobrać danych: ' + err.message;
        blad.hidden = false;
    } finally {
        ladowanie.hidden = true;
        przycisk.disabled = false;
    }
}

przycisk.addEventListener('click', wczytajDane);
