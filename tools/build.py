#!/usr/bin/env python3
"""Generator stron wskazani.pl. Bez zależności (tylko biblioteka standardowa).

Uruchomienie z katalogu repozytorium:   python3 tools/build.py

Menu, stopka, baner zgody i dolny pasek są wspólne (jedno źródło), a wynikiem są gotowe pliki .html
w katalogu głównym repozytorium. Pytania FAQ i oferty są trzymane jako dane, z których powstaje
i widoczny HTML, i JSON-LD, więc zawsze są identyczne.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://wskazani.pl'
LASTMOD = '2026-10-30'
OG_ALT = 'Wskazani: AI poleca Twoją firmę, nie konkurencję'


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- elementy graficzne
def logo(size, bg='#13233A', fg='#FAF8F4'):
    return ('<svg aria-hidden="true" width="%d" height="%d" viewBox="0 0 64 64" style="flex:0 0 auto">'
            '<circle cx="32" cy="32" r="31" fill="%s"></circle>'
            '<path d="M14 26L21.5 41.5L29.5 30L37.5 41.5" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"></path>'
            '<path d="M37.5 41.5L50.5 18.5" fill="none" stroke="#F0743A" stroke-width="6" stroke-linecap="round"></path></svg>') % (size, size, bg, fg)


def tick(color='#15803D', size=20, width='2.6'):
    return ('<svg class="check" aria-hidden="true" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"></path></svg>') % (size, size, color, width)


def bang(size=22):
    return ('<svg class="check" aria-hidden="true" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2.4" '
            'stroke-linecap="round"><path d="M12 7v6"></path><path d="M12 17h.01"></path></svg>') % (size, size)


CHEV = ('<svg class="chev" aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"></path></svg>')
BURGER = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2.2" '
          'stroke-linecap="round"><path d="M4 7h16"></path><path d="M4 12h16"></path><path d="M4 17h16"></path></svg>')
ICO_BANK = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round"><path d="M3 10l9-6 9 6"></path><path d="M5 10v8"></path><path d="M9.5 10v8"></path><path d="M14.5 10v8"></path>'
            '<path d="M19 10v8"></path><path d="M3 20h18"></path></svg>')
ICO_PHONE = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="2"></rect><path d="M11 18h2"></path></svg>')
ICO_CARD = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#13233A" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"></rect><path d="M2 10h20"></path></svg>')

# ---------------------------------------------------------------- nawigacja
NAV = [('/cennik', 'Cennik'), ('/pozycjonowanie-w-ai', 'Pozycjonowanie w AI'), ('/wspolpraca', 'Dla firm'), ('/faq', 'FAQ')]
FOOT = [('/', 'Strona główna'), ('/cennik', 'Cennik'), ('/pozycjonowanie-w-ai', 'Pozycjonowanie w AI'), ('/wspolpraca', 'Dla firm'),
        ('/faq', 'FAQ'), ('/o-nas', 'O nas')]

CONSENT_HEAD = (
    '<script>\n'
    "document.documentElement.classList.add('js');\n"
    "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\n"
    "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});\n"
    "gtag('set','ads_data_redaction',true);\n"
    "try{if(localStorage.getItem('zgoda-marketing')==='tak')gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}catch(e){}\n"
    '</script>\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18503882283"></script>\n'
    "<script>gtag('js',new Date());gtag('config','AW-18503882283');gtag('config','G-ENH7LJ2YW2');</script>\n"
)

NOSCRIPT_HEAD = '<noscript><style>.nav-toggle{display:none}.nav-panel{display:flex!important}.cmp-wrap{display:block!important}.cmp-mobile{display:none!important}</style></noscript>\n'

CONSENT_BOX = (
    '<div class="consent" id="consent" hidden role="dialog" aria-labelledby="consent-t">\n'
    '  <strong id="consent-t">Pliki cookies marketingowe</strong>\n'
    '  <p>Za Twoją zgodą strona uruchomi narzędzia Google (Google Ads i Google Analytics), żeby mierzyć skuteczność reklam. '
    'Bez zgody strona działa tak samo. Szczegóły: <a class="link" href="/polityka-prywatnosci">polityka prywatności</a>.</p>\n'
    '  <div class="btns"><button class="yes" id="c-yes" type="button">Zgadzam się</button><button class="no" id="c-no" type="button">Nie zgadzam się</button></div>\n'
    '</div>\n'
)


def head(title, desc, path, jsonld=(), robots=None, og_type='website'):
    url = SITE + path
    out = ['<!DOCTYPE html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n',
           CONSENT_HEAD,
           '<title>%s</title>\n' % esc(title),
           '<meta name="description" content="%s">\n' % attr(desc)]
    if robots:
        out.append('<meta name="robots" content="%s">\n' % robots)
    out.append('<meta name="author" content="Filip Szmel">\n<meta name="theme-color" content="#13233A">\n')
    if not (robots and 'noindex' in robots and path in ('/dziekuje', '/404')):
        out.append('<link rel="canonical" href="%s">\n' % url)
    out.append('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
               '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
    out.append('<meta property="og:type" content="%s">\n<meta property="og:locale" content="pl_PL">\n<meta property="og:site_name" content="Wskazani">\n'
               '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
               '<meta property="og:image" content="%s/og-image.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
               '<meta property="og:image:alt" content="%s">\n'
               '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
               '<meta name="twitter:image" content="%s/og-image.png">\n'
               % (og_type, attr(title), attr(desc), url, SITE, attr(OG_ALT), attr(title), attr(desc), SITE))
    out.append('<link rel="preload" href="/fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>\n')
    out.append('<link rel="stylesheet" href="/style.css">\n')
    out.append(NOSCRIPT_HEAD)
    for j in jsonld:
        out.append('<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(j, ensure_ascii=False, indent=1))
    out.append('</head>\n')
    return ''.join(out)


def site_header(active, audyt_href, sticky):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else '', t) for h, t in NAV)
    return (
        '<header class="site-header%s">\n<nav class="nav" aria-label="Menu główne">\n'
        '<a class="brand" href="/" aria-label="Wskazani — strona główna"%s>%s<span>wskazani</span></a>\n'
        '<span class="nav-spacer"></span>\n'
        '<button class="nav-toggle" id="nav-toggle" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="nav-panel">%s</button>\n'
        '<div class="nav-panel" id="nav-panel">\n<div class="nav-links">%s</div>\n'
        '<a class="btn btn-primary btn-sm" href="%s">Sprawdź, kogo AI poleca</a>\n</div>\n</nav>\n</header>\n'
        % (' sticky' if sticky else '', ' aria-current="page"' if active == '/' else '', logo(34), BURGER, links, audyt_href))


def subbar(title, anchors, btn_label, btn_href):
    a = ''.join('<a href="%s">%s</a>' % (h, t) for h, t in anchors)
    return ('<div class="subbar"><div class="in"><strong>%s</strong><div class="links">%s<a class="btn btn-primary btn-sm" href="%s">%s</a></div></div></div>\n'
            % (esc(title), a, btn_href, esc(btn_label)))


def site_footer(active):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else '', t) for h, t in FOOT)
    return (
        '<footer>\n<div class="site-footer foot-links">\n'
        '<span class="logo">%s<span>wskazani</span></span>\n%s\n'
        '<a href="tel:+48502890686">502 890 686</a>\n<a href="mailto:szmelfilip.business@gmail.com">szmelfilip.business@gmail.com</a>\n'
        '<a href="/polityka-prywatnosci">Polityka prywatności</a>\n<a href="#" id="cookie-settings">Ustawienia cookies</a>\n'
        '<span class="t">Płatność: przelew · BLIK · karta</span>\n<span class="t">Kwoty końcowe, bez VAT</span>\n</div>\n</footer>\n'
        % (logo(22), links))


def page(path, title, desc, main_html, active=None, audyt_href='/#audyt', sticky=False, bar=None, jsonld=(), robots=None,
         mobile_cta=True, extra_foot=''):
    h = head(title, desc, path, jsonld, robots)
    b = ['<body>\n<a class="skip" href="#tresc">Przejdź do treści</a>\n', site_header(active, audyt_href, sticky)]
    if bar:
        b.append(subbar(*bar))
    b.append('<main id="tresc">\n%s</main>\n' % main_html)
    b.append(site_footer(active))
    if mobile_cta:
        b.append('<div class="mobile-cta"><a class="btn btn-primary" href="%s">Diagnostyka AI: 19 zł</a></div>\n' % audyt_href)
    b.append(CONSENT_BOX)
    b.append(extra_foot)
    b.append('<script src="/site.js" defer></script>\n</body>\n</html>\n')
    return h + ''.join(b)


# ---------------------------------------------------------------- wspólne bloki
def faq_details(items, cls='faq'):
    out = ['<div class="%s">' % cls]
    for q, a in items:
        out.append('<details><summary><span>%s</span>%s</summary><p>%s</p></details>' % (esc(q), CHEV, esc(a)))
    out.append('</div>')
    return '\n'.join(out)


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def cta_band(h2, p, primary, secondary, note):
    ptxt = '<p class="s">%s</p>' % esc(p) if p else ''
    return ('<section class="band-navy cta-band" aria-label="Następny krok"><div class="in">\n<h2>%s</h2>\n%s\n<div class="btn-row">%s%s</div>\n'
            '<p class="n3">%s</p>\n</div></section>\n'
            % (esc(h2), ptxt, '<a class="btn btn-primary btn-lg" href="%s">%s</a>' % (primary[1], esc(primary[0])),
               '<a class="btn btn-ghost-white btn-lg" href="%s">%s</a>' % (secondary[1], esc(secondary[0])), esc(note)))


TILES = [('mini', 'Pełna diagnostyka pozycjonowania w AI', '19 zł'), ('wdrozenie', 'Wdrożenie pozycjonowania', 'od 990 zł'),
         ('strona', 'Nowa strona', 'od 1990 zł'), ('opieka', 'Opieka lub marketing', 'od 199 zł / mies.')]
BRANZE = ['Biuro rachunkowe', 'Kancelaria', 'Doradca finansowy lub kredytowy', 'Biuro nieruchomości', 'Usługi lokalne', 'Inna']
NEWS_TEXT = 'Chcę dostawać „Wskazówki”: bezpłatne poradniki o AI w firmie, mniej więcej co 2 tygodnie. Mogę się wypisać w każdej chwili.'


def audit_form(legend, calm, rodo):
    tiles = ''.join(
        '<label class="tile%s"><input type="radio" name="kafelek" value="%s"%s><span class="n">%s</span><span class="p%s">%s</span></label>'
        % (' on' if i == 0 else '', v, ' checked' if i == 0 else '', esc(n), '', esc(p))
        for i, (v, n, p) in enumerate(TILES))
    opts = ''.join('<option value="%s">%s</option>' % (attr(b), esc(b)) for b in BRANZE)
    return f'''<form class="form" id="audit-form" action="https://api.web3forms.com/submit" method="POST" novalidate>
<input type="hidden" name="access_key" value="7003f878-52e8-4f95-ac90-3dbadec662c6">
<input type="hidden" name="subject" value="Zamówienie: pełna diagnostyka pozycjonowania w AI (19 zł)">
<input type="hidden" name="from_name" value="Wskazani — strona">
<div class="field" id="f-url"><label for="site-url">Adres strony firmy</label>
<input id="site-url" name="site" type="text" inputmode="url" placeholder="np. mojafirma.pl" autocomplete="url" spellcheck="false" autocapitalize="off" required>
<div class="err" id="e-url" aria-live="polite"></div></div>
<div class="frow">
<div class="field" id="f-email"><label for="email">E-mail</label>
<input id="email" name="email" type="email" placeholder="imie@firma.pl" autocomplete="email" spellcheck="false" autocapitalize="off" required>
<div class="err" id="e-email" aria-live="polite"></div></div>
<div class="field"><label for="tel">Telefon <span class="optional">(opcjonalnie)</span></label>
<input id="tel" name="telefon" type="tel" placeholder="np. 600 000 000" autocomplete="tel"></div>
</div>
<div class="field" id="f-branza"><label for="branza">Branża</label>
<select id="branza" name="branza" required aria-describedby="e-branza"><option value="" selected disabled>Wybierz branżę</option>{opts}</select>
<div class="err" id="e-branza" aria-live="polite"></div></div>
<fieldset class="field"><legend>{esc(legend)}</legend>
<div class="tiles">{tiles}</div>
<p class="chosen" aria-live="polite">Wybrany pakiet: <strong id="chosen-name">Pełna diagnostyka pozycjonowania w AI</strong></p></fieldset>
<div class="field" id="f-firma"><label class="chk dark" for="firma"><input type="checkbox" id="firma" name="prowadze_firme" value="Tak" required aria-describedby="e-firma"><span>Prowadzę firmę lub odpowiadam za jej stronę</span></label>
<div class="err" id="e-firma" aria-live="polite"></div></div>
<label class="chk" for="newsletter"><input type="checkbox" id="newsletter" name="newsletter" value="tak"><span>{esc(NEWS_TEXT)}</span></label>
<div class="field" id="f-captcha"><div class="h-captcha captcha" data-captcha="true" data-theme="light"></div><div class="err" id="e-captcha" aria-live="polite"></div></div>
<div class="hp" aria-hidden="true"><label for="botcheck">Nie wypełniaj tego pola</label><input type="checkbox" id="botcheck" name="botcheck" tabindex="-1"></div>
<button class="btn-submit" id="submit-btn" type="submit">Zamawiam diagnostykę: 19 zł</button>
<p class="calm">{esc(calm)}</p>
<p class="rodo">{rodo}</p>
</form>
<script src="https://web3forms.com/client/script.js" async defer></script>
<div class="result" id="result" hidden aria-live="polite">
<div id="r-sending"><div class="status">Wysyłanie…</div></div>
<div id="r-ok" hidden><div class="status">Zgłoszenie przyjęte</div><p>Dziękuję! Przechodzę do strony z potwierdzeniem…</p></div>
<div id="r-fail" hidden>
<div class="status bad">Nie udało się wysłać automatycznie</div>
<p>Kliknij poniżej, żeby otworzyć pocztę z gotową wiadomością. Jeśli się nie otworzy, skopiuj treść i wyślij ją na szmelfilip.business@gmail.com.</p>
<p><a class="btn btn-outline" id="mail-link" href="mailto:szmelfilip.business@gmail.com">Otwórz e-mail</a></p>
<div class="copy-box" id="copy-box"></div>
<p><button class="btn btn-outline btn-sm" id="copy-btn" type="button">Kopiuj treść</button></p>
</div></div>'''


RODO_MAIN = ('Wysyłając formularz, zgadzasz się na kontakt w sprawie zamówienia. Administrator danych: Filip Szmel. '
             'Szczegóły w <a class="link" href="/polityka-prywatnosci">polityce prywatności</a>.')
RODO_CENNIK = ('Wysyłając formularz, zgadzasz się na kontakt w sprawie zgłoszenia. Administrator danych: Filip Szmel. '
               'Szczegóły w <a class="link" href="/polityka-prywatnosci">polityce prywatności</a>.')

ORG_ID = SITE + '/#firma'
PERSON_ID = SITE + '/#filip'
PROVIDER = {'@type': 'Organization', '@id': ORG_ID, 'name': 'Wskazani', 'url': SITE + '/'}

# ---------------------------------------------------------------- dane: oferta
OFFERS = [  # (nazwa, cena, "od", co miesiąc, opis)
    ('Pełna diagnostyka pozycjonowania w AI', 19, False, False, '20 pytań Twoich klientów w ChatGPT, Gemini, Perplexity i Claude: kogo AI poleca, gdzie Ciebie brakuje i co zmienić. Wynik w 3 dni robocze, rozmowa 20 min. Kwota odliczana od Wdrożenia.'),
    ('Wdrożenie pozycjonowania', 990, True, False, 'Wszystkie poprawki z audytu, dane o firmie dla Google i AI, pytania i odpowiedzi na stronie, test przed i po 30 dniach.'),
    ('Nowa strona widoczna w AI', 1990, True, False, 'Strona 4–6 podstron, gotowa pod Google i AI od pierwszego dnia, test przed i po 30 dniach.'),
    ('Opieka i monitoring AI', 199, True, True, 'Co miesiąc sprawdzam, czy AI poleca Twoją firmę, wysyłam krótki raport i robię drobne poprawki.'),
    ('Opieka+', 490, True, True, 'Wszystko z Opieki, do 2 nowych treści miesięcznie, większe zmiany na stronie i rozmowa raz w miesiącu.'),
    ('Marketing na zlecenie', 1490, True, True, 'Social media, Google Ads i treści. Zakres ustalamy w rozmowie. Budżet na reklamy płacisz osobno, bezpośrednio Google lub Meta.'),
]


def offer_ld(name, price, od, monthly, desc):
    spec = {'@type': 'UnitPriceSpecification', 'priceCurrency': 'PLN'}
    if od:
        spec['minPrice'] = price
    else:
        spec['price'] = price
    if monthly:
        spec['unitCode'] = 'MON'
        spec['unitText'] = 'miesiąc'
    return {'@type': 'Offer', 'name': name, 'description': desc + ' Kwota końcowa, bez VAT.', 'priceCurrency': 'PLN',
            'priceSpecification': spec, 'itemOffered': {'@type': 'Service', 'name': name}}


def service_ld(path, name, desc, offers):
    return {'@context': 'https://schema.org', '@type': 'Service', '@id': SITE + path + '#usluga', 'name': name, 'description': desc,
            'url': SITE + path, 'serviceType': 'Pozycjonowanie firmy w AI (GEO)', 'areaServed': {'@type': 'Country', 'name': 'Polska'},
            'provider': PROVIDER, 'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': name, 'itemListElement': [offer_ld(*o) for o in offers]}}


# ================================================================= STRONA GŁÓWNA (v2 GEO, 30.10.2026)
DIAG_NAME = 'Pełna diagnostyka pozycjonowania w AI'
MAIN_FAQ = [
    ('Czym to się różni od SEO?', 'SEO walczy o miejsce na liście wyników Google. My walczymy o to, żeby AI wymieniło Cię z nazwy, kiedy listy w ogóle nie ma. Część pracy jest wspólna: porządna strona pomaga w obu.'),
    ('Gwarantujecie, że ChatGPT zacznie mnie polecać?', 'Nikt nie steruje odpowiedziami AI. Kto mówi inaczej, kłamie. My ustawiamy wszystko, z czego AI buduje odpowiedź, i co miesiąc mierzymy wynik na tych samych pytaniach. Jeśli 90 dni po wdrożeniu test nie pokaże postępu, czyli więcej odpowiedzi z Twoją firmą, pracujemy dalej bez dopłaty, aż pokaże.'),
    ('Ile to trwa?', 'Diagnostyka: 3 dni robocze od wpłaty. Wdrożenie: 2–4 tygodnie. Każde narzędzie AI aktualizuje wiedzę we własnym tempie, dlatego wynik mierzymy co miesiąc, a nie raz.'),
    ('Ile kosztuje?', 'Diagnostyka 19 zł, odliczane od ceny wdrożenia. Wdrożenie od 990 zł. Opieka i pomiar od 199 zł miesięcznie. Dokładną kwotę wdrożenia dostajesz po diagnostyce, zanim cokolwiek zlecisz. Kwoty końcowe, bez VAT.'),
    ('Dlaczego diagnostyka jest płatna?', 'Bo to ręczna praca: 20 pytań w czterech narzędziach AI, sprawdzonych i opisanych. Za 19 zł dostajesz wynik, który zostaje u Ciebie, nawet jeśli nie zlecisz nic więcej.'),
    ('A jeśli AI już mnie poleca?', 'To dowiesz się o tym czarno na białym i będziesz wiedzieć, czego pilnować. Nie sprzedajemy wdrożenia, którego nie potrzebujesz.'),
    ('Muszę coś robić?', 'Dać dostęp do strony i wizytówki Google oraz odpowiedzieć na kilka pytań o firmę. Tekstami, kodem, wizytówką i katalogami zajmujemy się my.'),
    ('Kto to robi?', 'Filip Szmel, Warszawa. Pracujesz z jedną osobą od diagnostyki do raportu, bez działu obsługi i przekazywania sprawy dalej.'),
]

AI_NAMES = ['ChatGPT', 'Gemini', 'Perplexity', 'Claude']


def ai_chat(label, question, rows, foot, tone):
    r = ''.join('<li class="%s"><span class="ai-nm">%s</span>%s</li>' % (c, esc(n), ('<span class="ai-why">%s</span>' % esc(w)) if w else '') for c, n, w in rows)
    return ('<div class="ai-chat %s"><div class="ai-top"><span class="dot"></span><span>%s</span></div>'
            '<p class="ai-q">%s</p><ol class="ai-a">%s</ol><p class="ai-f">%s</p></div>' % (tone, esc(label), esc(question), r, esc(foot)))


def build_main():
    q = '„Polecisz dobre biuro rachunkowe w Warszawie dla małej firmy?”'
    hero_chat = ai_chat('Asystent AI · ilustracja', q,
                        [('c', 'Firma A', 'specjalizacja w JDG, dużo opinii'), ('c', 'Firma B', 'blisko centrum, księgowość online'),
                         ('c', 'Firma C', 'stałe ceny, szybki kontakt'), ('miss', 'Twoja firma', 'brak w odpowiedzi')],
                        'Klient dzwoni do jednej z trzech. Do Ciebie nie.', 'bad')
    before = ai_chat('Bez nas', q,
                     [('c', 'Firma A', 'AI opisuje ją jej słowami'), ('c', 'Firma B', 'z opiniami i lokalizacją'),
                      ('c', 'Firma C', 'z linkiem do strony')],
                     'Twojej firmy nie ma. Nie wiesz nawet, że ten klient istniał.', 'bad')
    after = ai_chat('Z nami: cel', q,
                    [('you', 'Twoja firma', 'z powodem, dla którego AI ją wybiera'), ('c', 'Firma A', ''), ('c', 'Firma B', '')],
                    'AI opisuje Cię Twoimi słowami. Wiesz, przy których pytaniach jesteś, a przy których jeszcze nie.', 'good')
    faq = faq_details(MAIN_FAQ)
    ais = ' · '.join(AI_NAMES)
    return f'''<section id="top" class="wrap hero">
<div class="hero-l">
<p class="eyebrow">Pozycjonowanie w AI · {ais}</p>
<h1 class="display xl">Klient pyta ChatGPT o firmę z Twojej branży. AI wymienia konkurencję. Ciebie nie.</h1>
<p class="lead">I właśnie straciłeś klienta, o którym nawet nie wiedziałeś, że go miałeś.</p>
<div class="btn-row"><a class="btn btn-primary btn-lg" href="#audyt" data-pakiet="mini">Sprawdź, kogo AI poleca zamiast Ciebie</a></div>
<p class="note" style="margin-top:18px">{esc(DIAG_NAME)} · 19 zł · wynik w 3 dni robocze</p>
<p style="margin-top:14px;font-size:17px">Wolisz od razu porozmawiać? <a class="link" href="tel:+48502890686">502 890 686</a></p>
</div>
<figure class="hero-r" aria-label="Ilustracja odpowiedzi asystenta AI">{hero_chat}</figure>
</section>

<section class="band" aria-label="Obietnica"><div class="wrap sec promise">
<h2 class="h2 lg">Robimy tak, że AI zaczyna Cię polecać.</h2>
<div class="grid g-280" style="margin-top:32px">
<div class="pp"><strong>Konkretnie</strong><p>Przy pytaniach, które zadają Twoi klienci, a nie przy hasłach z narzędzia SEO.</p></div>
<div class="pp"><strong>Mierzalnie</strong><p>Co miesiąc te same pytania, te same narzędzia i jeden wynik: w ilu odpowiedziach już jesteś.</p></div>
</div></div></section>

<section id="porownanie" class="wrap sec" aria-label="To samo pytanie, inna odpowiedź">
<h2 class="h2 lg">To samo pytanie. Inna odpowiedź.</h2>
<p class="sub">Tak wygląda odpowiedź AI, kiedy klient szuka firmy w Twojej branży.</p>
<div class="vs">{before}{after}</div>
<p class="note" style="margin-top:18px">Ilustracja układu odpowiedzi, nie wynik klienta. W diagnostyce dostajesz prawdziwe odpowiedzi dla swojej branży i miasta, ze zrzutami i datą testu.</p>
</section>

<section id="google" class="band" aria-label="Dlaczego Google to za mało"><div class="wrap sec">
<h2 class="h2 lg" style="max-width:780px">Google pokazywał listę. AI pokazuje trzy nazwy.</h2>
<div class="wrap-0 stats s4 grid g-240" style="margin-top:36px;gap:32px">
<div><p class="n">68%</p><p class="t">wyszukiwań w Google kończy się bez kliknięcia w żadną stronę.<sup>1</sup></p></div>
<div><p class="n">−58%</p><p class="t">o tyle spada klikalność wyniku nr 1, gdy nad nim pojawia się odpowiedź AI.<sup>2</sup></p></div>
<div><p class="n">900 mln</p><p class="t">ludzi co tydzień korzysta z ChatGPT.<sup>3</sup></p></div>
<div><p class="n">81%</p><p class="t">Polaków w wieku 18–24 używało AI w ostatnich 3 miesiącach. Wśród wszystkich dorosłych: 36%.<sup>4</sup></p></div>
</div>
<p class="lead" style="margin-top:36px;max-width:760px">Pierwsze miejsce w Google nie znaczy już, że klient do Ciebie trafi. Kiedy AI odpowiada za Google, liczy się jedno: czy jesteś w tej odpowiedzi.</p>
</div></section>

<section id="jak" class="wrap sec" aria-label="Co dokładnie robimy">
<h2 class="h2 lg">Co dokładnie robimy</h2>
<ol class="steps3 s4">
<li><span class="num">1</span><strong>Diagnostyka</strong><span class="d">20 pytań, które zadają Twoi klienci, w {ais}. Wiesz, kogo AI poleca, kogo pomija i dlaczego.</span></li>
<li><span class="num">2</span><strong>Strona, którą AI rozumie</strong><span class="d">Treść i kod ustawione tak, żeby AI wiedziało, co robisz, gdzie i dla kogo: odpowiedzi na pytania klientów, dane strukturalne, llms.txt.</span></li>
<li><span class="num">3</span><strong>Źródła, którym AI wierzy</strong><span class="d">Wizytówka Google, katalogi branżowe, opinie, wzmianki. Jedne dane wszędzie, bez trzech adresów i dwóch numerów telefonu.</span></li>
<li><span class="num">4</span><strong>Pomiar co miesiąc</strong><span class="d">Te same pytania, ta sama metoda. Raport na jednej stronie: gdzie byłeś, gdzie jesteś, co robimy dalej.</span></li>
</ol>
</section>

<section id="dla-kogo" class="band" aria-label="Dla kogo"><div class="wrap sec">
<h2 class="h2 lg">Dla kogo to jest. Dla kogo nie.</h2>
<div class="fit">
<div class="yes"><h3>To jest dla Ciebie, jeśli:</h3><ul>
<li>{tick()}<span>klienci wybierają Cię z polecenia: kancelaria, biuro rachunkowe, klinika, gabinet, wykonawca, firma usługowa B2B,</span></li>
<li>{tick()}<span>masz działającą firmę, stronę i choć kilka opinii,</span></li>
<li>{tick()}<span>decyzję podejmujesz sam, bez przetargu i trzech zebrań,</span></li>
<li>{tick()}<span>chcesz wyniku, a nie kolejnego raportu do szuflady.</span></li></ul></div>
<div class="no"><h3>To nie jest dla Ciebie, jeśli:</h3><ul>
<li><span class="x" aria-hidden="true">×</span><span>oczekujesz efektu w tydzień. AI aktualizuje wiedzę we własnym tempie,</span></li>
<li><span class="x" aria-hidden="true">×</span><span>chcesz dostać PDF i wdrażać sam,</span></li>
<li><span class="x" aria-hidden="true">×</span><span>masz agencję na abonamencie i szukasz tańszego wykonawcy na sztuki,</span></li>
<li><span class="x" aria-hidden="true">×</span><span>nie zamierzasz prosić klientów o opinie.</span></li></ul></div>
</div></div></section>

<section id="wspolpraca" class="wrap sec" aria-label="Jak wygląda współpraca">
<h2 class="h2 lg">Robimy wszystko za Ciebie.</h2>
<p class="sub">Twój czas: około godziny w pierwszym miesiącu, potem 15 minut miesięcznie.</p>
<ol class="steps3">
<li><span class="num">1</span><strong>Diagnostyka: 19 zł</strong><span class="d">W 3 dni robocze dostajesz wynik: kogo AI poleca w Twojej branży, gdzie Ciebie brakuje i co trzeba zmienić. Omawiamy go w 20-minutowej rozmowie. 19 zł odliczamy od wdrożenia.</span></li>
<li><span class="num">2</span><strong>Wdrożenie: od 990 zł</strong><span class="d">Dajesz dostęp do strony i wizytówki, odpowiadasz na kilka pytań o firmę. Resztę robimy my, w 2–4 tygodnie.</span></li>
<li><span class="num">3</span><strong>Opieka i pomiar: od 199 zł / mies.</strong><span class="d">Co miesiąc ten sam test i raport. Wypowiedzenie z miesięcznym okresem, bez kar. Wszystko, co wdrożyliśmy, zostaje u Ciebie.</span></li>
</ol>
<div class="guarantee"><strong>Gwarancja 90 dni.</strong> Jeśli 90 dni po wdrożeniu test na tych samych pytaniach nie pokaże postępu, pracujemy dalej bez dopłaty, aż pokaże.</div>
<div class="btn-row" style="margin-top:28px"><a class="btn btn-primary btn-lg" href="#audyt" data-pakiet="mini">Zamawiam diagnostykę</a><a class="btn btn-outline btn-lg" href="/cennik">Pełny cennik</a></div>
</section>

<section id="omnie" class="band" aria-label="Kto to robi"><div class="wrap sec"><div class="who">
<div class="who-logo">{logo(128, '#FAF8F4', '#13233A').replace('aria-hidden="true"', 'role="img" aria-label="Logo Wskazani"', 1)}<span>wskazani</span></div>
<div class="who-txt">
<p class="k">Kto to robi</p>
<h2>Filip Szmel, Warszawa</h2>
<p class="p">W USA agencje GEO działają od dwóch lat. W Polsce prawie nikt nie robi tego dobrze, a Twoi klienci już pytają AI. Pracujesz ze mną od diagnostyki do raportu: bez działu obsługi, bez przekazywania sprawy dalej, bez umowy na lata.</p>
<p class="p"><a class="link" href="/o-nas">Więcej o nas i o tym, jak pracujemy →</a></p>
<div class="contact-row"><a class="link" href="tel:+48502890686">Zadzwoń: 502 890 686</a><a class="link" href="mailto:szmelfilip.business@gmail.com">Napisz: szmelfilip.business@gmail.com</a><a class="link" href="https://www.linkedin.com/in/filip-szmel-b2993a439/" rel="me noopener" target="_blank">LinkedIn</a></div>
</div></div></div></section>

<section id="faq" class="wrap-900 sec" aria-label="Pytania" style="padding-bottom:72px">
<h2 class="h2 lg">Pytania</h2>
<div style="margin-top:24px">{faq}</div>
<a class="link" href="/faq" style="margin-top:16px;font-size:17px">Wszystkie pytania i słowniczek →</a>
</section>

<section id="audyt" class="band-navy on-navy" aria-label="Zamów diagnostykę"><div class="wrap sec"><div class="audit">
<div class="audit-l">
<h2 class="h2 lg" style="line-height:1.08;text-wrap:balance">Twoi klienci już pytają AI. Sprawdź, co słyszą.</h2>
<p class="p">{esc(DIAG_NAME)}: Twoja branża, Twoje miasto, {ais}. 19 zł, odliczane od wdrożenia.</p>
<ul class="ticks"><li>{tick('#86EFAC')}<span>20 pytań Twoich klientów w 4 narzędziach AI</span></li><li>{tick('#86EFAC')}<span>Wynik w 3 dni robocze od wpłaty + rozmowa 20 min</span></li><li>{tick('#86EFAC')}<span>Po zgłoszeniu dostajesz link do płatności online</span></li></ul>
<p class="p" style="margin-top:20px">Albo zadzwoń: <a class="link" href="tel:+48502890686" style="color:#fff">502 890 686</a></p>
</div>
<div class="formbox">
{audit_form('Czego potrzebujesz?', 'Odpowiadam w ciągu 24 h roboczych z linkiem do płatności.', RODO_MAIN)}
</div></div></div></section>

<section id="przypisy" class="wrap foot-notes" aria-label="O Wskazani i przypisy">
<h2>O Wskazani</h2>
<p>Wskazani to agencja GEO (Generative Engine Optimization) dla firm z Warszawy i całej Polski. Sprawdzamy i poprawiamy to, jak ChatGPT, Gemini, Perplexity i Claude opisują i polecają Twoją firmę. Pełna diagnostyka pozycjonowania w AI kosztuje 19 zł i obejmuje 20 pytań klientów w czterech narzędziach AI. Wdrożenie od 990 zł: treść i dane strukturalne (schema.org) na stronie, plik llms.txt, wizytówka Google, katalogi i opinie. Opieka i comiesięczny pomiar od 199 zł miesięcznie, bez umowy na lata. Wskazani prowadzi Filip Szmel.</p>
<h2 class="src">Źródła danych</h2>
<ol>
<li>SparkToro na danych Similarweb, wyszukiwania w Google w USA, styczeń–kwiecień 2026 (68,01% wyszukiwań bez kliknięcia).</li>
<li>Ahrefs, luty 2026, ponad 300 tys. słów kluczowych: klikalność wyniku nr 1 przy obecności AI Overview niższa o 58%.</li>
<li>OpenAI, luty 2026: ponad 900 mln aktywnych użytkowników ChatGPT tygodniowo.</li>
<li>CBOS, komunikat „Korzystanie ze sztucznej inteligencji”, czerwiec 2026, badanie z maja 2026, N=1041 dorosłych mieszkańców Polski.</li>
<li>Kwoty końcowe, bez VAT (działalność nierejestrowana). Ceny aktualne: październik 2026.</li>
</ol>
</section>
'''


def main_ld():
    return [{
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'WebSite', '@id': SITE + '/#strona', 'url': SITE + '/', 'name': 'Wskazani', 'inLanguage': 'pl-PL',
             'publisher': {'@id': ORG_ID}},
            {'@type': 'Organization', '@id': ORG_ID, 'name': 'Wskazani', 'url': SITE + '/', 'logo': SITE + '/icon-512.png',
             'image': SITE + '/og-image.png', 'email': 'szmelfilip.business@gmail.com', 'telephone': '+48502890686',
             'description': 'Agencja GEO: sprawiamy, że ChatGPT, Gemini, Perplexity i Claude polecają polskie firmy. Diagnostyka, wdrożenie i comiesięczny pomiar.',
             'founder': {'@id': PERSON_ID}, 'areaServed': {'@type': 'Country', 'name': 'Polska'},
             'address': {'@type': 'PostalAddress', 'addressLocality': 'Warszawa', 'addressCountry': 'PL'},
             'knowsAbout': ['Generative Engine Optimization', 'pozycjonowanie w AI', 'ChatGPT', 'Gemini', 'Perplexity', 'Claude'],
             'contactPoint': {'@type': 'ContactPoint', 'contactType': 'obsługa klienta', 'telephone': '+48502890686',
                              'email': 'szmelfilip.business@gmail.com', 'availableLanguage': 'pl'},
             'sameAs': ['https://www.linkedin.com/in/filip-szmel-b2993a439/']},
            {'@type': 'Person', '@id': PERSON_ID, 'name': 'Filip Szmel', 'url': SITE + '/',
             'email': 'szmelfilip.business@gmail.com', 'telephone': '+48502890686', 'worksFor': {'@id': ORG_ID},
             'homeLocation': {'@type': 'Place', 'name': 'Warszawa'},
             'sameAs': ['https://www.linkedin.com/in/filip-szmel-b2993a439/']},
            dict({'@id': SITE + '/#faq'}, **faq_ld(MAIN_FAQ)),
        ]}]



# ================================================================= CENNIK
CMP_ROWS = [
    ('Test 20 pytań klientów w 4 narzędziach AI', '✓', '✓', '✓'),
    ('Kogo AI poleca zamiast Ciebie i dlaczego', '✓', '✓', '✓'),
    ('Rozmowa 20 min o wyniku', '✓', '✓', '✓'),
    ('Poprawki wdrożone za Ciebie', '—', 'Wszystkie', 'W nowej stronie'),
    ('Dane o firmie dla Google i AI', '—', '✓', '✓'),
    ('Pytania i odpowiedzi na stronie', '—', '✓', '✓'),
    ('Gwarancja 90 dni', '—', '✓', '✓'),
    ('Nowa strona 4–6 podstron', '—', '—', '✓'),
    ('Cena', '19 zł', 'od 990 zł', 'od 1990 zł'),
]
CENNIK_FAQ = [
    ('Co dostaję za 19 zł?', '20 pytań, które zadają Twoi klienci, sprawdzonych w ChatGPT, Gemini, Perplexity i Claude: kogo AI poleca, gdzie Ciebie brakuje i co trzeba zmienić. Wynik w 3 dni robocze i rozmowa 20 min. 19 zł odliczamy od Wdrożenia.'),
    ('Czy po diagnostyce muszę coś kupić?', 'Nie. Wynik zostaje u Ciebie, nawet jeśli nie zlecisz nic więcej.'),
    ('Gwarantujecie, że ChatGPT zacznie mnie polecać?', 'Nikt nie steruje odpowiedziami AI. Ustawiamy wszystko, z czego AI buduje odpowiedź, i mierzymy wynik co miesiąc. Jeśli 90 dni po wdrożeniu test nie pokaże postępu, pracujemy dalej bez dopłaty, aż pokaże.'),
    ('Czy do ceny dochodzi VAT?', 'Nie. Kwoty na stronie są końcowe, nie doliczam VAT.'),
]
STEPS7 = [('Zamawiasz diagnostykę', '19 zł'), ('Wynik w 3 dni robocze', ''), ('20 min rozmowy', 'w cenie'), ('Wybierasz pakiet', 'od 990 zł'),
          ('Potwierdzenie mailem i płatność', ''), ('Wdrażam poprawki', ''), ('Test po 30 dniach', '')]
QUIZ = [
    ('q1', '1. Czy Twoja firma ma stronę internetową?', [('aktualna', 'Tak, aktualną'), ('stara', 'Tak, ale starą'), ('brak', 'Nie mam')]),
    ('q2', '2. Czego potrzebujesz teraz?', [('sprawdzic', 'Tylko sprawdzić'), ('naprawic', 'Naprawić najważniejsze'), ('komplet', 'Mieć to zrobione kompleksowo')]),
    ('q3', '3. Jednorazowo czy na stałe?', [('raz', 'Jednorazowo'), ('pilnowac', 'Chcę, żeby ktoś tego pilnował'), ('marketing', 'Potrzebuję całego marketingu')]),
]


def build_cennik():
    quiz = ''.join(
        '<fieldset><legend>%s</legend><div class="opts">%s</div></fieldset>' % (
            esc(label), ''.join('<button class="opt" type="button" data-q="%s" data-v="%s" aria-pressed="false">%s</button>' % (k, v, esc(t)) for v, t in opts))
        for k, label, opts in QUIZ)
    head_cells = ''.join(
        '<th scope="col" data-k="%s" data-n="%s">%s</th>' % (k, n, extra) for k, n, extra in [
            ('mini', 'Diagnostyka', 'Diagnostyka'),
            ('wdrozenie', 'Wdrożenie', 'Wdrożenie <span class="rec-tag">Polecany</span>'), ('strona', 'Nowa strona', 'Nowa strona')])
    body_rows = ''.join('<tr><th scope="row">%s</th><td>%s</td><td class="rec">%s</td><td>%s</td></tr>' % tuple(esc(x) for x in r) for r in CMP_ROWS)
    steps = ''.join(
        '<li><span class="n">%d</span><strong>%s</strong>%s</li>' % (i + 1, esc(t), ('<span class="tag%s">%s</span>' % (' free' if tag == '0 zł' else '', esc(tag))) if tag else '<span class="tag"></span>')
        for i, (t, tag) in enumerate(STEPS7))
    return f'''<section id="top" class="wrap center" style="padding-block:88px 32px">
<h1 class="eyebrow">Cennik · ile kosztuje pozycjonowanie w AI</h1>
<p class="display md">Jasne ceny. Zaczynasz od diagnostyki za 19 zł.</p>
<p style="margin:22px auto 0;font-size:18px;line-height:1.6;max-width:760px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 22px;text-align:left"><strong>W skrócie:</strong> pełna diagnostyka pozycjonowania w AI 19 zł (odliczane od wdrożenia) · wdrożenie od 990 zł · nowa strona od 1990 zł · stała opieka od 199 zł / miesiąc. Kwoty końcowe, bez VAT.</p>
<p class="note" style="margin-top:10px">Ceny aktualne: październik 2026</p>
<p class="note" style="margin-top:14px">Bez umowy na lata · Przelew, BLIK lub karta · Wynik w 3 dni robocze</p>
</section>

<section class="quiz" id="quiz" aria-label="Który pakiet dla Ciebie"><div class="quiz-box">
<h2>Który pakiet pozycjonowania w AI wybrać?</h2>
<p>Nie wiesz, co wybrać? Odpowiedz na 3 pytania.</p>
{quiz}
<div class="result-box"><div class="rt"><p class="l" id="quiz-label" aria-live="polite">Twój wynik pojawi się tutaj</p><p class="x" id="quiz-text">Odpowiedz na 3 pytania powyżej.</p><p class="s" id="quiz-note" hidden>Dokładną kwotę podam po diagnostyce.</p></div>
<a class="btn btn-primary" id="quiz-pick" href="#audyt" hidden style="min-height:48px;padding:14px 24px">Wybieram ten zestaw</a></div>
</div></section>

<section class="wrap" aria-label="Pakiety jednorazowe" style="padding-block:88px 24px">
<h2 class="h2">Pakiety jednorazowe: diagnostyka, wdrożenie, nowa strona</h2>
<div class="grid g-240" style="gap:18px;margin-top:32px;align-items:stretch">
<article class="price-card big"><h3>Pełna diagnostyka pozycjonowania w AI</h3><p class="price"><span class="num">19 zł</span><span class="post">jednorazowo</span></p><p class="quote">„Chcę wiedzieć, kogo AI poleca zamiast mnie”</p>
<ul><li>20 pytań Twoich klientów w ChatGPT, Gemini, Perplexity i Claude</li><li>Wynik w 3 dni robocze + rozmowa 20 min</li><li>Kwota odliczana od Wdrożenia</li></ul>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=mini#audyt" data-pakiet="mini">Zamawiam diagnostykę</a></article>
<article class="price-card big pick"><span class="badge">Polecany na start</span><h3>Wdrożenie pozycjonowania</h3><p class="price"><span class="pre">od</span><span class="num">990 zł</span></p><p class="quote">„Chcę mieć to zrobione porządnie”</p>
<ul><li>Wszystkie poprawki z diagnostyki</li><li>Dane o firmie dla Google i AI</li><li>Pytania i odpowiedzi na stronie</li><li>Gwarancja 90 dni</li></ul>
<a class="btn btn-primary btn-block" href="/cennik?pakiet=wdrozenie#audyt" data-pakiet="wdrozenie">Wybierz Wdrożenie</a></article>
<article class="price-card big"><h3>Nowa strona</h3><p class="price"><span class="pre">od</span><span class="num">1990 zł</span></p><p class="quote">„Strona jest stara albo jej nie ma”</p>
<ul><li>4–6 podstron</li><li>Gotowa pod Google i AI od pierwszego dnia</li><li>Test przed i po 30 dniach</li><li>Płatność: 50% na start, 50% przed publikacją</li></ul>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=strona#audyt" data-pakiet="strona">Zapytaj o stronę</a></article>
</div>
<div class="dep">
<div class="all"><h3>Od czego zależy cena?</h3><p>Dokładną kwotę znasz po diagnostyce, zanim cokolwiek zlecisz.</p></div>
<div class="c"><strong>Liczba podstron</strong><p>Więcej podstron to więcej miejsc do poprawienia.</p></div>
<div class="c"><strong>Stan strony</strong><p>Aktualna strona wymaga mniej pracy niż taka sprzed kilku lat.</p></div>
<div class="c"><strong>System strony</strong><p>Każdy system (WordPress, Wix, strona pisana ręcznie) wymaga innego podejścia.</p></div>
</div>
<div class="big-firms on-navy" id="duze-firmy" aria-label="Dla dużych firm"><div class="t"><span class="k">Dla dużych firm</span>
<p>Masz kilka oddziałów, wiele usług albo stronę z setkami podstron? Zaczynamy tak samo, od diagnostyki, a zakres i cenę ustalamy indywidualnie, na piśmie, zanim cokolwiek zlecisz.</p></div>
<a class="btn btn-primary" href="#audyt">Zapytaj o wycenę</a></div>
<p class="muted" style="margin-top:18px;font-size:15px">Co musisz zrobić Ty: dać dostęp do strony i poświęcić 10 minut na pytania.</p>
</section>

<section class="wrap" aria-label="Porównaj pakiety" style="padding-block:72px 24px">
<h2 class="h2">Co zawiera każdy pakiet? Porównanie</h2>
<div class="cmp-wrap"><table class="cmp" id="cmp-table"><thead><tr><th scope="col">Co dostajesz</th>{head_cells}</tr></thead><tbody>{body_rows}</tbody></table></div>
<div class="cmp-mobile" id="cmp-mobile"><p class="muted" style="margin-top:16px;font-size:15px">Wybierz 2 pakiety do porównania.</p>
<div class="pick"><div><label for="cmp-a">Pakiet 1</label><select id="cmp-a"></select></div><div><label for="cmp-b">Pakiet 2</label><select id="cmp-b"></select></div></div>
<div class="rows" id="cmp-rows"></div></div>
</section>

<section id="stale" class="wrap" aria-label="Współpraca stała" style="padding-block:72px 24px">
<h2 class="h2">Ile kosztuje stała opieka nad pozycjonowaniem w AI?</h2>
<p class="muted" style="margin-top:12px;font-size:18px">Płatność z góry za miesiąc. Wypowiedzenie miesięczne, bez kar.</p>
<div class="grid g-280" style="gap:18px;margin-top:30px">
<article class="price-card big mo"><h3>Opieka i monitoring AI</h3><p class="price"><span class="pre">od</span><span class="num">199 zł</span><span class="post">/ miesiąc</span></p>
<p class="desc">Co miesiąc sprawdzam, czy AI poleca Twoją firmę, wysyłam krótki raport i robię drobne poprawki.</p>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=opieka#audyt" data-pakiet="opieka">Wybierz Opiekę</a></article>
<article class="price-card big mo pick"><span class="badge">Dla rosnących firm</span><h3>Opieka+</h3><p class="price"><span class="pre">od</span><span class="num">490 zł</span><span class="post">/ miesiąc</span></p>
<p class="desc">Wszystko z Opieki, do 2 nowych treści miesięcznie, większe zmiany na stronie i rozmowa raz w miesiącu.</p>
<a class="btn btn-primary btn-block" style="background:var(--navy);border-color:var(--navy)" href="/cennik?pakiet=opieka-plus#audyt" data-pakiet="opieka-plus">Wybierz Opiekę+</a></article>
<article class="price-card big mo"><h3>Marketing na zlecenie</h3><p class="price"><span class="pre">od</span><span class="num">1490 zł</span><span class="post">/ miesiąc</span></p>
<p class="desc">Social media, Google Ads i treści — taniej niż etat w marketingu. Zakres ustalamy w rozmowie. Budżet na reklamy płacisz osobno, bezpośrednio Google lub Meta.</p>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=marketing#audyt" data-pakiet="marketing">Porozmawiajmy</a></article>
</div></section>

<section class="wrap" aria-label="Dlaczego Wskazani" style="padding-block:72px 24px"><div class="why on-navy">
<h2>Czym Wskazani różni się od agencji GEO?</h2>
<div class="grid g-240">
<div><p>Bez VAT</p><p>Kwota na stronie jest końcowa. Agencje zwykle podają ceny netto.</p></div>
<div><p>Bez umowy na lata</p><p>Wypowiedzenie miesięczne. U części konkurencji umowa na 3–6 miesięcy.</p></div>
<div><p>Diagnostyka za 19 zł</p><p>Zamiast audytu za 790–2000 zł u części agencji. Kwota jest odliczana od Wdrożenia.</p></div>
<div><p>Jedna osoba</p><p>Rozmawiasz z tym, kto robi poprawki. Bez pośredników i infolinii.</p></div>
</div>
<p class="foot">Porównanie na podstawie cenników agencji GEO z października 2026.</p>
</div></section>

<section id="rozliczenie" class="wrap" aria-label="Jak płacisz" style="padding-block:72px 24px">
<h2 class="h2">Jak przebiega współpraca i jak płacisz?</h2>
<ol class="steps7">{steps}</ol>
<div class="pay4">
<div><p>Diagnostyka</p><p>100% z góry</p></div>
<div><p>Wdrożenie</p><p>50% przed, 50% do 7 dni po wykonaniu</p></div>
<div><p>Nowa strona</p><p>50% przed, 50% przed publikacją</p></div>
<div><p>Opieka i marketing</p><p>Z góry za miesiąc, wypowiedzenie miesięczne, bez kar</p></div>
</div>
<div class="methods" aria-label="Metody płatności"><span>{ICO_BANK}Przelew</span><span>{ICO_PHONE}BLIK</span><span>{ICO_CARD}Karta</span></div>
<p class="muted" style="margin-top:14px;font-size:15px">Przed płatnością dostajesz mailem potwierdzenie: zakres, kwota i terminy. Link do płatności BLIK-iem lub kartą przychodzi mailem. Do każdej wpłaty dostajesz rachunek (działalność nierejestrowana, bez VAT).</p>
</section>

<section class="wrap-900" aria-label="Pytania" style="padding-block:72px 24px">
<h2 class="h2">Pytania o ceny pozycjonowania w AI</h2>
<div style="margin-top:24px">{faq_details(CENNIK_FAQ, 'faq-cards')}</div>
</section>

<section id="audyt" class="band-navy on-navy" aria-label="Zamówienie" style="margin-top:72px"><span id="formularz"></span><div class="wrap sec"><div class="audit">
<div class="audit-l">
<h2 class="h2 lg" style="line-height:1.08;text-wrap:balance">Pakiet wybrany? Wyślij zgłoszenie.</h2>
<p class="p">Nie wiesz jeszcze? Zacznij od diagnostyki. Po wyniku doradzę, od czego zacząć.</p>
<p class="n2">Bez umowy na lata · Przelew, BLIK lub karta · Wynik w 3 dni robocze</p>
</div>
<div class="formbox">
{audit_form('Wybrany pakiet', 'Przed płatnością dostaniesz mailem zakres, dokładną kwotę i terminy.', RODO_CENNIK)}
</div></div></div></section>

<section id="przypisy" class="wrap foot-notes" aria-label="Źródła danych" style="padding-top:40px">
<h2 class="src" style="margin-top:0">Źródła danych</h2>
<ul>
<li>Publiczne cenniki oraz długość umów czterech firm świadczących usługi GEO w Polsce, sprawdzone 17.10.2026. Te firmy podają kwoty netto, do których dochodzi 23% VAT. Nazw firm nie podajemy.</li>
<li>Kwoty końcowe, bez VAT (działalność nierejestrowana). Dokładną kwotę wdrożenia lub strony podaję po diagnostyce, zanim cokolwiek zlecisz. Ceny aktualne: październik 2026.</li>
</ul>
</section>
'''


# ================================================================= WIDOCZNOŚĆ W AI
AREAS = [
    ('Dostęp botów AI do strony', 'Sprawdzam, czy strona nie blokuje robotów ChatGPT, Perplexity i Google, i otwieram im drogę do ważnych podstron.', 'robots.txt'),
    ('Spójne dane firmy', 'Nazwa, adres, telefon i godziny takie same na stronie, w wizytówce Google i w katalogach firm.', 'NAP, wizytówka Google'),
    ('Opis firmy, który Google czyta bez zgadywania', 'Dodaję do strony uporządkowany opis: kim jesteś, co oferujesz, gdzie działasz.', 'dane strukturalne (schema.org)'),
    ('Odpowiedzi na pytania klientów', 'Pytania, które klienci zadają AI, z odpowiedzią już w pierwszym zdaniu.', 'FAQ'),
    ('Tytuł i opis w wynikach Google', 'Tak, żeby nie były ucinane i od razu mówiły, czym się zajmujesz i gdzie.', 'meta title i description'),
    ('Ściągawka o firmie dla asystentów AI', 'Krótki plik z najważniejszymi informacjami. Opcjonalny: Google go nie wymaga.', 'llms.txt'),
]
GEO_ROWS = [
    ('Pierwszy krok', 'U części agencji płatny audyt, 790–2000 zł', 'Diagnostyka za 19 zł, odliczana od Wdrożenia'),
    ('Ceny', 'Zwykle netto, do tego 23% VAT', 'Kwoty końcowe, bez VAT'),
    ('Umowa', 'U części minimum 3–6 miesięcy', 'Abonament z wypowiedzeniem miesięcznym, bez kar'),
    ('Stały monitoring', 'Od 599 zł / miesiąc netto', 'Od 199 zł / miesiąc'),
    ('Z kim rozmawiasz', 'Zależy od agencji', 'Z osobą, która robi poprawki. Bez pośredników i infolinii.'),
]
GEO_STATS = [
    ('16 mln', 'polskich internautów korzysta z narzędzi AI.'),
    ('6 na 10', 'Polaków pyta AI, zanim wybierze produkt lub usługę.'),
    ('Ponad 2×', 'więcej kliknięć dostają firmy cytowane w odpowiedzi AI Google (badanie z USA).'),
    ('8% vs 15%', 'Gdy Google pokazuje odpowiedź AI, ludzie klikają w wyniki prawie o połowę rzadziej (USA).'),
]


def build_geo():
    areas = ''.join('<div><strong>%s</strong><p>%s</p><span class="term">Termin fachowy: %s</span></div>' % (esc(t), esc(d), esc(term)) for t, d, term in AREAS)
    rows = ''.join('<tr><th scope="row">%s</th><td class="a">%s</td><td class="w">%s</td></tr>' % tuple(esc(x) for x in r) for r in GEO_ROWS)
    stats = ''.join('<div><p class="n">%s</p><p class="t">%s</p></div>' % (esc(n), esc(t)) for n, t in GEO_STATS)
    return f'''<section class="wrap" style="padding-block:88px 64px">
<h1 class="eyebrow">Pozycjonowanie w AI (GEO) dla firm</h1>
<p class="display" style="max-width:900px">Poprawiam to, co ChatGPT, Perplexity i Google czytają o Twojej firmie.</p>
<p style="margin:20px 0 0;font-size:18px;line-height:1.6;max-width:760px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 22px"><strong>Czym jest GEO?</strong> To dbanie o to, żeby asystenci AI, tacy jak ChatGPT, Perplexity i tryb AI Google, rozumieli Twoją firmę i mogli ją wymienić w odpowiedzi. W praktyce: poprawki na stronie i spójne dane firmy w internecie.</p>
<p class="lead" style="margin-top:22px;max-width:660px">Konkretny zakres, jawne ceny i bez umowy na lata. Dla firm, które wiedzą, że klienci pytają AI, i szukają kogoś, kto to uporządkuje.</p>
<div class="btn-row" style="margin-top:32px"><a class="btn btn-primary btn-lg" href="/cennik" data-ga="zobacz_ceny" data-ga-miejsce="pozycjonowanie_hero">Zobacz cennik</a><a class="btn btn-outline btn-lg" href="/#audyt">Zamów diagnostykę</a></div>
<p class="note" style="margin-top:20px">Pierwszy krok za 199 zł · kwoty bez VAT · bez umowy na 6 miesięcy</p>
</section>

<section id="zakres" class="band" aria-label="Zakres usługi"><div class="wrap sec">
<h2 class="h2">Co obejmuje usługa GEO?</h2>
<p class="muted" style="margin-top:12px;font-size:18px;max-width:640px">Sześć obszarów. W diagnostyce dowiesz się, które z nich u Ciebie kuleją.</p>
<div class="areas">{areas}</div>
<p style="margin-top:24px;font-size:17px;font-weight:700">Wszystkie poprawki wprowadzam za Ciebie.</p>
</div></section>

<section id="porownanie" class="wrap sec" aria-label="Porównanie z agencją">
<h2 class="h2">Czym Wskazani różni się od agencji GEO?</h2>
<p class="muted" style="margin-top:12px;font-size:18px;max-width:660px">Na podstawie publicznych cenników czterech agencji GEO w Polsce, sprawdzonych 17.10.2026.</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col" style="width:28%"><span class="sr">Kryterium</span></th><th scope="col" class="a">Agencje GEO (zwykle)</th><th scope="col" class="w">Wskazani</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small" style="margin-top:14px">Porównanie na podstawie cenników agencji GEO z października 2026.</p>
</section>

<section id="ustalenia" class="band" aria-label="Przykładowe ustalenia"><div class="wrap sec">
<h2 class="h2">Co najczęściej blokuje firmy w AI?</h2>
<p class="muted" style="margin-top:12px;font-size:18px;max-width:640px">Prawdziwe ustalenia ze stron firm, które sprawdziłem we wrześniu i październiku 2026. Bez nazw.</p>
<div class="grid g-300" style="margin-top:32px">
<div class="finding"><p class="k">Klinika</p><p class="v">Plik dla robotów blokował stronę „Pierwsza wizyta”, której pacjent szuka najczęściej.</p><p class="o">Obszar: dostęp botów AI</p></div>
<div class="finding"><p class="k">Firma budowlana</p><p class="v">Najnowsze treści na stronie były z 2017 roku, a strona nie miała formularza kontaktowego, mapy ani opisu firmy, który Google czyta bez zgadywania.</p><p class="o">Obszar: dane strukturalne i kontakt</p></div>
<div class="finding"><p class="k">Hotel</p><p class="v">Najmocniejszy argument, darmowy transfer 24 h, nie trafił do opisu, który pokazuje Google.</p><p class="o">Obszar: tytuł i opis w Google</p></div>
</div></div></section>

<section class="wrap sec" aria-label="Dane rynkowe">
<h2 class="h2">Dlaczego pozycjonowanie w AI ma znaczenie?</h2>
<div class="stats s4 grid g-240" style="gap:28px;margin-top:32px">{stats}</div>
</section>

{cta_band('Zacznij od diagnostyki za 19 zł.', 'Kogo AI poleca zamiast Ciebie, w 4 narzędziach. Kwota odliczana od Wdrożenia.',
         ('Zobacz cennik', '/cennik'), ('Zamów diagnostykę', '/#audyt'), 'Bez umowy na lata · Wynik w 3 dni robocze').replace('class="btn btn-primary btn-lg" href="/cennik"', 'class="btn btn-primary btn-lg" href="/cennik" data-ga="zobacz_ceny" data-ga-miejsce="widocznosc_dol"')}
<section id="przypisy" class="wrap foot-notes" aria-label="Źródła danych" style="padding-top:40px">
<h2 class="src" style="margin-top:0">Źródła danych</h2>
<ul>
<li>Publiczne cenniki czterech firm świadczących usługi GEO w Polsce, sprawdzone 17.10.2026: audyt 790–2000 zł, abonament od 599 zł/mies., umowy minimum 3–6 miesięcy; kwoty netto. Nazw firm nie podajemy.</li>
<li>Gemius i PBI (Mediapanel), raport „E-commerce w Polsce 2026”, dane z czerwca 2026, publikacja wrzesień 2026.</li>
<li>On Board Think Kong / SW Research, badanie internetowe, N=830 dorosłych Polaków, kwiecień 2026. 61% badanych w ciągu ostatnich 6 miesięcy użyło AI przy wyborze produktów lub usług.</li>
<li>Seer Interactive, 53 marki, 5,47 mln zapytań, publikacja 24.04.2026, dane głównie z USA. Marki cytowane w odpowiedzi AI Google miały o 120% więcej kliknięć niż marki niecytowane.</li>
<li>Pew Research Center, 900 dorosłych z USA, 68 879 wyszukiwań, publikacja 22.07.2025. Gdy Google pokazywał podsumowanie AI, w wyniki klikano w 8% wyszukiwań, bez podsumowania w 15%.</li>
</ul>
</section>
'''


# ================================================================= WSPÓŁPRACA
PLANS = [
    ('Opieka i monitoring AI', '199', 'Chcesz mieć spokój i wiedzieć, że AI dalej Cię rozumie.', '', False, 'Wybierz Opiekę', 'opieka',
     ['Co miesiąc test „czy AI Cię poleca” na tych samych pytaniach', 'Kontrola, czy nic nie zablokowało botów AI', 'Drobne poprawki, które wprowadzam za Ciebie', 'Krótki raport mailem']),
    ('Opieka+', '490', 'Chcesz, żeby AI polecało Cię coraz częściej, miesiąc po miesiącu.', 'Dla rosnących firm', True, 'Wybierz Opiekę+', 'opieka-plus',
     ['Wszystko z Opieki', 'Do 2 nowych treści miesięcznie, np. odpowiedzi na pytania klientów', 'Większe zmiany na stronie', 'Rozmowa raz w miesiącu']),
    ('Marketing na zlecenie', '1490', 'Potrzebujesz kogoś od marketingu, bez zatrudniania na etat.', '', False, 'Porozmawiajmy o zakresie', 'marketing',
     ['Social media', 'Kampanie Google Ads', 'Treści na stronę', 'Zakres ustalamy w rozmowie, raport co miesiąc']),
]


def build_wsp():
    plans = []
    for name, price, forx, badge, feat, cta, pid, items in PLANS:
        b = '<span>%s</span>' % esc(badge) if badge else ''
        lis = ''.join('<li>%s<span>%s</span></li>' % (tick(), esc(i)) for i in items)
        btn = 'btn-primary' if feat else 'btn-cta-outline'
        plans.append(f'<article class="plan{" feat" if feat else ""}"><div class="bs">{b}</div><h2>{esc(name)}</h2><p class="for">{esc(forx)}</p>'
                     f'<p class="price"><span class="pre">od</span><span class="num">{price}</span><span class="post">zł / miesiąc</span></p><ul>{lis}</ul>'
                     f'<a class="btn {btn} btn-block" href="/?pakiet={pid}#audyt" data-pakiet="{pid}">{esc(cta)}</a></article>')
    plans = '\n'.join(plans)
    qa = [('Co zostaje na stronie po rezygnacji?', 'Wszystko, co poprawiłem. Poprawki i treści zostają na Twojej stronie, przestaję tylko co miesiąc sprawdzać i wysyłać raport.'),
          ('Czy mogę zmienić pakiet?', 'Tak, w górę i w dół. Wystarczy mail, nowy pakiet obowiązuje od kolejnego opłaconego miesiąca.'),
          ('Od kiedy liczy się miesiąc?', 'Od dnia płatności. Przed płatnością dostajesz mailem potwierdzenie: zakres, kwota i terminy.')]
    qas = ''.join('<details class="qa" open><summary><span>%s</span>%s</summary><p>%s</p></details>' % (esc(q), CHEV, esc(a)) for q, a in qa)
    return f'''<section class="wrap" style="padding-block:88px 48px">
<h1 class="eyebrow">Stała opieka i monitoring pozycjonowania w AI</h1>
<p class="display" style="max-width:860px">Bez umowy na lata. Od 199 zł miesięcznie.</p>
<p class="lead" style="margin-top:22px;max-width:640px">Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło. Płacisz z góry za miesiąc i możesz zrezygnować w każdym miesiącu.</p>
<div class="btn-row" style="margin-top:32px"><a class="btn btn-primary btn-lg" href="#pakiety">Wybierz pakiet</a><a class="btn btn-outline btn-lg" href="/#audyt">Zacznij od diagnostyki</a></div>
<p class="note" style="margin-top:20px">Bez kar za rezygnację · Przelew, BLIK lub karta · Raport co miesiąc</p>
</section>

<section id="pakiety" class="wrap" aria-label="Pakiety miesięczne" style="padding-block:24px 88px">
<div class="grid g-300" style="align-items:stretch">
{plans}
</div>
<p class="muted" style="margin-top:22px;font-size:15px">Kwoty końcowe, bez VAT. Budżet reklam w pakiecie Marketing płacisz osobno, bezpośrednio do Google lub Meta.</p>
<p class="muted inline" style="margin-top:8px;font-size:15px">Nie wiesz, od czego zacząć? <a class="link" href="/cennik">Zrób quiz w cenniku</a> albo zacznij od diagnostyki za 19 zł i przejdź na Opiekę później.</p>
<p class="muted inline" style="margin-top:8px;font-size:15px">Masz kilka oddziałów, wiele usług albo stronę z setkami podstron? Zakres i cenę ustalamy indywidualnie, na piśmie, zanim cokolwiek zlecisz. <a class="link" href="/cennik#duze-firmy">Wycena dla dużych firm</a></p>
</section>

<section id="raport" class="band" aria-label="Przykładowy raport"><div class="wrap sec" style="display:flex;flex-wrap:wrap;gap:48px;align-items:center">
<div style="flex:1 1 340px;min-width:0">
<h2 class="h2" style="text-wrap:balance">Co zawiera raport miesięczny?</h2>
<p class="muted" style="margin-top:14px;font-size:18px;line-height:1.55">Jedna strona, bez żargonu. Widzisz, co sprawdziłem, co się zmieniło i co poprawiłem. Raz w miesiącu, mailem.</p>
<p class="note" style="margin-top:14px">Przykład układu. Bez danych żadnego klienta.</p>
</div>
<figure class="rep" aria-label="Przykładowy raport miesięczny">
<div class="top"><span class="t">Raport miesięczny · przykład</span><span class="pill">Opieka</span></div>
<dl>
<div class="row"><dt>Dostęp botów AI</dt><dd class="g">bez zmian, otwarty</dd></div>
<div class="row"><dt>Dane firmy w sieci</dt><dd>spójne na stronie, w wizytówce Google i w katalogach</dd></div>
<div><dt>Co poprawiłem</dt><dd>godziny otwarcia na stronie i w wizytówce Google</dd></div>
<div><dt>Na następny miesiąc</dt><dd>dodać odpowiedź na pytanie o dojazd i parking</dd></div>
</dl>
</figure>
</div></section>

<section id="rezygnacja" class="wrap sec" aria-label="Płatność i rezygnacja">
<h2 class="h2">Jak płacisz i jak zrezygnować?</h2>
<div class="pay3 grid g-260" style="margin-top:32px">
<div class="c"><strong>Płacisz z góry za miesiąc</strong><p>Przelewem, BLIK-iem albo kartą przez link do płatności.</p></div>
<div class="c"><strong>Rezygnujesz jednym mailem</strong><p>Wypowiedzenie miesięczne. Opieka trwa do końca opłaconego miesiąca.</p></div>
<div class="c"><strong>Bez kar i bez minimum</strong><p>Nie wiążę Cię umową na 3 czy 6 miesięcy. Zostajesz, jeśli widzisz sens.</p></div>
</div></section>

<section id="pytania" class="wrap sec-b" aria-label="Pytania o współpracę stałą">
<h2 class="h2">Pytania o współpracę stałą</h2>
<div style="margin-top:24px;border-top:1px solid var(--line)">{qas}</div>
<p class="muted inline" style="margin-top:18px;font-size:15px">Więcej odpowiedzi: <a class="link" href="/faq">FAQ</a></p>
</section>

{cta_band('Najpierw sprawdzę, od czego zacząć.', 'Diagnostyka pokaże, czy wystarczy Ci Opieka, czy najpierw trzeba zrobić Wdrożenie.', ('Zamów diagnostykę', '/#audyt'), ('Porównaj wszystkie pakiety', '/cennik'),
         'Bez umowy na lata · Wynik w 3 dni robocze')}
'''


# ================================================================= FAQ
FAQ_GROUPS = [
    ('g0', 'Diagnostyka', [
        ('Co dostaję w diagnostyce za 19 zł?', '20 pytań, które zadają Twoi klienci, w ChatGPT, Gemini, Perplexity i Claude: kogo AI poleca, gdzie Ciebie brakuje i co zmienić. Wynik w 3 dni robocze, rozmowa 20 min. Kwota odliczana od Wdrożenia.'),
        ('Co dostaję?', 'Krótki raport prostym językiem: czy AI czyta Twoją stronę i 3 najważniejsze rzeczy do poprawy.'),
        ('Ile czekam?', 'Do 48 godzin roboczych od wysłania formularza.'),
    ]),
    ('g1', 'Ceny i rozliczenie', [
        ('Ile to kosztuje?', 'Diagnostyka 19 zł, Wdrożenie od 990 zł, nowa strona od 1990 zł, stała opieka od 199 zł miesięcznie. Kwoty końcowe, bez VAT. Szczegóły i porównanie pakietów są w cenniku.'),
        ('Jak się rozliczasz?', 'Diagnostyka płatna z góry. Wdrożenie: połowa przed startem, połowa do 7 dni po wykonaniu. Nowa strona: połowa przed startem, połowa przed publikacją. Abonament z góry za każdy miesiąc.'),
        ('Jak mogę zapłacić?', 'Przelewem albo BLIK-iem lub kartą przez link do płatności, który dostajesz mailem.'),
        ('Czy wystawiasz fakturę?', 'Teraz do każdej wpłaty dostajesz rachunek. Kwoty są końcowe, bez VAT. Gdy będę wystawiać faktury, napiszę o tym przed płatnością.'),
        ('Od czego zależy cena?', 'Od liczby podstron, stanu strony i systemu, na którym działa. Dokładną kwotę znasz po diagnostyce, zanim cokolwiek zlecisz.'),
        ('Czy jest umowa?', 'Każde zlecenie potwierdzam mailem: zakres, kwota i terminy płatności. Abonament możesz wypowiedzieć w każdym miesiącu, bez kar.'),
        ('Mam kilka oddziałów albo stronę z setkami podstron. Jak wyceniasz?', 'Zaczynamy tak samo, od diagnostyki, a zakres i cenę ustalamy indywidualnie, na piśmie, zanim cokolwiek zlecisz.'),
    ]),
    ('g2', 'Współpraca', [
        ('Co muszę zrobić ja?', 'Dać dostęp do strony i znaleźć 10 minut na kilka pytań. Resztę robię ja.'),
        ('Czy mogę zacząć od małego kroku?', 'Tak. Diagnostyka za 19 zł: mała kwota, konkretny wynik, a kwota wraca w cenie Wdrożenia.'),
        ('Gwarantujecie, że AI zacznie polecać moją firmę?', 'Nikt nie steruje odpowiedziami AI. Ustawiamy wszystko, z czego AI buduje odpowiedź, i co miesiąc mierzymy wynik na tych samych pytaniach. Jeśli 90 dni po wdrożeniu test nie pokaże postępu, pracujemy dalej bez dopłaty, aż pokaże.'),
        ('Co, jeśli efekt mnie nie przekona?', 'Widzisz wynik przed i po. Przy Wdrożeniu drugą połowę płacisz do 7 dni po wykonaniu, przy nowej stronie dopiero przed publikacją, a abonament kończysz w dowolnym miesiącu.'),
        ('Od kiedy liczy się miesiąc abonamentu?', 'Od dnia płatności. Przed płatnością dostajesz mailem potwierdzenie: zakres, kwota i terminy.'),
        ('Czy mogę zmienić pakiet?', 'Tak, w górę i w dół. Wystarczy mail, nowy pakiet obowiązuje od kolejnego opłaconego miesiąca.'),
        ('Co zostaje na stronie po rezygnacji?', 'Wszystko, co poprawiłem. Poprawki i treści zostają na Twojej stronie, przestaję tylko co miesiąc sprawdzać i wysyłać raport.'),
    ]),
    ('g3', 'Technika', [
        ('Czy muszę mieć plik llms.txt?', 'Nie. Google nie wymaga go do AI Overviews. To opcjonalna ściągawka o firmie dla asystentów AI, którą mogę dodać przy okazji.'),
        ('Na jakim systemie musi działać strona?', 'Na każdym popularnym: WordPress, Wix albo strona pisana ręcznie. Każdy system wymaga innego podejścia, dlatego sprawdzam go w audycie, bo wpływa na zakres i cenę.'),
    ]),
]
FAQ_ALL = [qa for _, _, items in FAQ_GROUPS for qa in items]
TERMS = [
    ('GEO', 'Dbanie o to, żeby asystenci AI rozumieli Twoją firmę i mogli ją wymienić w odpowiedzi.'),
    ('AI Overviews', 'Odpowiedź wygenerowana przez AI, którą Google pokazuje nad zwykłymi wynikami.'),
    ('Tryb AI Google', 'Osobna zakładka Google, w której AI odpowiada na pytanie zamiast listy linków. W Polsce od października 2025.'),
    ('Dane strukturalne', 'Uporządkowany opis firmy w kodzie strony, który Google czyta bez zgadywania.'),
    ('robots.txt', 'Plik z instrukcją dla robotów: które części strony mogą czytać.'),
    ('llms.txt', 'Opcjonalna ściągawka o firmie dla asystentów AI; nie jest standardem Google.'),
]


def build_faq():
    groups = ''.join('<section id="%s" aria-label="%s"><h2>%s</h2>%s</section>' % (gid, attr(name), esc(name), faq_details(items)) for gid, name, items in FAQ_GROUPS)
    terms = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(t), esc(d)) for t, d in TERMS)
    return f'''<section class="wrap-900" style="padding-block:88px 32px">
<h1 class="eyebrow">Pytania o pozycjonowanie w AI i audyt</h1>
<p class="display">Masz pytanie? Tu jest krótka odpowiedź.</p>
<p class="lead" style="margin-top:18px">Jeśli czegoś brakuje, zadzwoń: <a class="link" href="tel:+48502890686">502 890 686</a>.</p>
</section>
<div class="wrap-900 faq-groups" style="padding-bottom:72px">{groups}</div>
<section id="slowniczek" class="band" aria-label="Słowniczek"><div class="wrap-900" style="padding-block:80px">
<h2 class="h2 sm">Słowniczek</h2>
<p class="muted" style="margin-top:10px;font-size:17px">Każde trudne słowo w jednym zdaniu.</p>
<dl class="gloss">{terms}</dl>
</div></section>
{cta_band('Masz jeszcze pytanie? Zadzwoń: 502 890 686.', '', ('Zamów diagnostykę', '/#audyt'), ('Zobacz cennik', '/cennik'), 'Bez umowy na lata · Wynik w 3 dni robocze').replace('<div class="in">', '<div class="in" style="padding-block:80px">')}
'''



# ================================================================= O NAS
def build_onas():
    return f'''<section class="wrap-900" style="padding-block:88px 32px">
<p class="eyebrow">O nas</p>
<h1 class="display">Wskazani: agencja GEO z Warszawy</h1>
<p class="lead" style="margin-top:18px">Sprawdzamy i poprawiamy to, jak ChatGPT, Gemini, Perplexity i Claude opisują i polecają Twoją firmę. Pracujemy dla firm z Warszawy i całej Polski.</p>
</section>

<section class="wrap-900" style="padding-bottom:56px" aria-label="Dlaczego to robimy">
<h2 class="h2 sm">Dlaczego to robimy</h2>
<p class="p" style="margin-top:14px">Klienci coraz częściej pytają AI zamiast wpisywać hasło w Google. W USA agencje GEO działają od dwóch lat. W Polsce prawie nikt nie robi tego dobrze, a firmy nawet nie wiedzą, że AI wymienia ich konkurencję. Chcemy, żeby AI polecało Ciebie.</p>
</section>

<section class="band" aria-label="Jak pracujemy"><div class="wrap-900" style="padding-block:72px">
<h2 class="h2 sm">Jak pracujemy</h2>
<ul class="ticks" style="margin-top:18px">
<li>{tick()}<span><strong>Jeden opiekun od początku do końca.</strong> Rozmawiasz z tym, kto robi poprawki. Bez infolinii i bez przekazywania sprawy dalej.</span></li>
<li>{tick()}<span><strong>Ręczna praca, nie automat.</strong> 20 pytań Twoich klientów sprawdzamy w czterech narzędziach AI i opisujemy wynik.</span></li>
<li>{tick()}<span><strong>Jawne ceny.</strong> Kwoty na stronie są końcowe, bez VAT. Zakres i cenę wdrożenia dostajesz na piśmie, zanim cokolwiek zlecisz.</span></li>
<li>{tick()}<span><strong>Bez umowy na lata.</strong> Opieka z miesięcznym wypowiedzeniem, bez kar.</span></li>
<li>{tick()}<span><strong>Pomiar i gwarancja 90 dni.</strong> Test przed i po wdrożeniu. Jeśli po 90 dniach nie widać postępu, pracujemy dalej bez dopłaty, aż będzie widać.</span></li>
</ul>
<p class="p" style="margin-top:22px">Szczegóły pakietów: <a class="link" href="/cennik">cennik</a> i <a class="link" href="/pozycjonowanie-w-ai">pozycjonowanie w AI</a>.</p>
</div></section>

<section class="wrap-900" style="padding-block:64px" aria-label="Kontakt">
<h2 class="h2 sm">Kontakt</h2>
<div class="contact-row" style="margin-top:18px"><a class="link" href="tel:+48502890686">Zadzwoń: 502 890 686</a><a class="link" href="mailto:szmelfilip.business@gmail.com">Napisz: szmelfilip.business@gmail.com</a><a class="link" href="https://www.linkedin.com/in/filip-szmel-b2993a439/" rel="me noopener" target="_blank">LinkedIn</a></div>
<p class="muted" style="margin-top:14px;font-size:16px">Warszawa, praca zdalna dla firm z całej Polski. Odpowiadamy w ciągu 24 h roboczych.</p>
</section>
{cta_band('Zacznij od diagnostyki za 19 zł.', '', ('Zamów diagnostykę', '/#audyt'), ('Zobacz cennik', '/cennik'), 'Bez umowy na lata · Wynik w 3 dni robocze').replace('<div class="in">', '<div class="in" style="padding-block:80px">')}
'''


def onas_ld():
    return [{'@context': 'https://schema.org', '@type': 'AboutPage', '@id': SITE + '/o-nas#strona', 'url': SITE + '/o-nas',
             'name': 'O nas: Wskazani', 'inLanguage': 'pl-PL', 'about': {'@id': ORG_ID}, 'isPartOf': {'@id': SITE + '/#strona'}}]


# ================================================================= POZOSTAŁE: polityka, dziękuję, 404
def build_polityka():
    body = open(os.path.join(ROOT, 'src', 'polityka-body.html'), encoding='utf8').read()
    return '<article class="doc">\n<p class="eyebrow" style="margin:0">RODO</p>\n<h1>Polityka prywatności</h1>\n%s</article>\n' % body


def build_dziekuje():
    return '''<section class="doc" id="thanks">
<p class="eyebrow" style="margin:0">Zgłoszenie przyjęte</p>
<h1>Zgłoszenie wysłane</h1>
<div id="t-audyt">
<p class="lead"><span id="t-pakiet"></span>Odpowiem na podany e-mail w ciągu 24 h roboczych, z linkiem do płatności. Jeśli chcesz coś dodać, napisz na <a class="link" href="mailto:szmelfilip.business@gmail.com">szmelfilip.business@gmail.com</a> lub zadzwoń: <a class="link" href="tel:+48502890686">502 890 686</a>.</p>
</div>
<div id="t-check" hidden>
<p class="lead">Pełna wersja checklisty jest gotowa do pobrania.</p>
<p style="margin-top:20px"><a class="btn btn-primary btn-lg" href="/checklista-widocznosc-w-ai.pdf" download>Pobierz checklistę (PDF)</a></p>
<p style="margin-top:16px">Jeśli plik się nie otworzy, napisz na <a class="link" href="mailto:szmelfilip.business@gmail.com">szmelfilip.business@gmail.com</a>. Chcesz, żebym sprawdził Twoją stronę? <a class="link" href="/#audyt">Zamów diagnostykę</a>.</p>
</div>
<noscript><p style="margin-top:20px"><a class="btn btn-primary btn-lg" href="/checklista-widocznosc-w-ai.pdf" download>Pobierz checklistę (PDF), jeśli o nią prosiłeś</a></p></noscript>
<p style="margin-top:32px"><a class="btn btn-outline" href="/">Wróć na stronę główną</a></p>
</section>
'''


def build_404():
    return '''<section class="doc">
<p class="eyebrow" style="margin:0">Błąd 404</p>
<h1>Tej strony tu nie ma</h1>
<p>Adres mógł się zmienić albo zawierać literówkę. Wszystko, czego szukasz, jest na stronie głównej.</p>
<div class="btn-row" style="margin-top:24px"><a class="btn btn-primary btn-lg" href="/">Wróć na stronę główną</a><a class="btn btn-outline btn-lg" href="/#audyt">Zamów diagnostykę</a></div>
</section>
'''


# ================================================================= MONTAŻ
def write(name, content):
    with open(os.path.join(ROOT, name), 'w', encoding='utf8') as f:
        f.write(content)
    print('zapisano', name, len(content))


def main():
    write('index.html', page(
        '/', 'Agencja GEO: AI poleca Twoją firmę, nie konkurencję | Wskazani',
        'Kiedy klient pyta ChatGPT o firmę z Twojej branży, AI wymienia konkurencję. Robimy tak, że zaczyna polecać Ciebie. Diagnostyka 19 zł, wynik w 3 dni robocze.',
        build_main(), active='/', audyt_href='#audyt', sticky=True, jsonld=main_ld()))
    write('cennik.html', page(
        '/cennik', 'Cennik: ile kosztuje pozycjonowanie w AI | Wskazani',
        'Jasne ceny: diagnostyka pozycjonowania w AI 19 zł, wdrożenie od 990 zł, nowa strona od 1990 zł, stała opieka od 199 zł miesięcznie. Kwoty końcowe, bez VAT.',
        build_cennik(), active='/cennik', audyt_href='#audyt', sticky=True,
        jsonld=[service_ld('/cennik', 'Pozycjonowanie w AI (GEO): pakiety i ceny',
                           'Diagnostyka pozycjonowania w AI, Wdrożenie, nowa strona oraz stała opieka i monitoring. Kwoty końcowe, bez VAT.', OFFERS)]))
    write('pozycjonowanie-w-ai.html', page(
        '/pozycjonowanie-w-ai', 'Pozycjonowanie w AI (GEO) dla firm | Wskazani',
        'Poprawiam to, co ChatGPT, Perplexity i Google czytają o Twojej firmie. Konkretny zakres, jawne ceny i bez umowy na lata. Diagnostyka za 19 zł.',
        build_geo(), active='/pozycjonowanie-w-ai',
        bar=('Pozycjonowanie w AI (GEO)', [('#zakres', 'Zakres'), ('#porownanie', 'Porównanie'), ('#ustalenia', 'Ustalenia')], 'Zobacz cennik', '/cennik')))
    write('wspolpraca.html', page(
        '/wspolpraca', 'Stała opieka i monitoring pozycjonowania w AI | Wskazani',
        'Bez umowy na lata, od 199 zł miesięcznie. Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło.',
        build_wsp(), active='/wspolpraca',
        bar=('Współpraca stała', [('#pakiety', 'Pakiety'), ('#raport', 'Raport'), ('#rezygnacja', 'Rezygnacja')], 'Zamów audyt', '/#audyt'),
        jsonld=[service_ld('/wspolpraca', 'Stała opieka i monitoring pozycjonowania w AI',
                           'Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło. Bez umowy na lata.', OFFERS[3:])]))
    write('faq.html', page(
        '/faq', 'Pytania o pozycjonowanie w AI i audyt | Wskazani',
        'Krótkie odpowiedzi o diagnostyce, cenach, rozliczeniu, współpracy i technice, plus słowniczek: GEO, AI Overviews, llms.txt.',
        build_faq(), active='/faq',
        bar=('Pytania i słowniczek', [('#g0', 'Audyt'), ('#g1', 'Rozliczenie'), ('#g2', 'Współpraca'), ('#g3', 'Technika'), ('#slowniczek', 'Słowniczek')], 'Zamów audyt', '/#audyt'),
        jsonld=[dict({'@context': 'https://schema.org'}, **faq_ld(FAQ_ALL))]))
    write('o-nas.html', page(
        '/o-nas', 'O nas: agencja GEO Wskazani z Warszawy',
        'Wskazani to agencja GEO z Warszawy. Sprawdzamy i poprawiamy, jak ChatGPT, Gemini, Perplexity i Claude polecają polskie firmy. Jawne ceny, bez umowy na lata.',
        build_onas(), active='/o-nas', jsonld=onas_ld()))
    write('polityka-prywatnosci.html', page(
        '/polityka-prywatnosci', 'Polityka prywatności | Wskazani',
        'Jak przetwarzam dane z formularzy: administrator, cel, podstawa prawna, odbiorcy, okres przechowywania i Twoje prawa.',
        build_polityka(), robots='noindex, follow', mobile_cta=False))
    write('dziekuje.html', page(
        '/dziekuje', 'Dziękuję za zgłoszenie | Wskazani', 'Zgłoszenie zostało wysłane.', build_dziekuje(), robots='noindex', mobile_cta=False))
    write('404.html', page(
        '/404', 'Nie znaleziono strony | Wskazani', 'Ta strona nie istnieje. Wróć na stronę główną i zamów diagnostykę pozycjonowania firmy w AI.',
        build_404(), robots='noindex', mobile_cta=False))

    urls = ['/', '/cennik', '/pozycjonowanie-w-ai', '/wspolpraca', '/faq', '/o-nas']
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, u, LASTMOD))
    sm.append('</urlset>\n')
    write('sitemap.xml', '\n'.join(sm))


if __name__ == '__main__':
    main()
