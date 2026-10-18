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
LASTMOD = '2026-10-18'
OG_ALT = 'Wskazani: sprawdzę za darmo, czy ChatGPT i Google polecają Twoją firmę'


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
NAV = [('/cennik', 'Cennik'), ('/widocznosc-w-ai', 'Widoczność w AI'), ('/wspolpraca', 'Dla firm'), ('/faq', 'FAQ')]
FOOT = [('/', 'Strona główna'), ('/cennik', 'Cennik'), ('/widocznosc-w-ai', 'Widoczność w AI'), ('/wspolpraca', 'Dla firm'),
        ('/faq', 'FAQ'), ('/#omnie', 'O mnie')]

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
        '<a class="btn btn-primary btn-sm" href="%s">Darmowy audyt</a>\n</div>\n</nav>\n</header>\n'
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
        b.append('<div class="mobile-cta"><a class="btn btn-primary" href="%s">Darmowy audyt</a></div>\n' % audyt_href)
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


TILES = [('mini', 'Darmowy mini-audyt', '0 zł'), ('start', 'Start: test usługi', '199 zł'), ('wdrozenie', 'Wdrożenie widoczności', 'od 990 zł'),
         ('strona', 'Nowa strona', 'od 1990 zł'), ('opieka', 'Opieka lub marketing', 'od 199 zł / mies.')]
BRANZE = ['Biuro rachunkowe', 'Kancelaria', 'Doradca finansowy lub kredytowy', 'Biuro nieruchomości', 'Usługi lokalne', 'Inna']
NEWS_TEXT = 'Chcę dostawać „Wskazówki”: bezpłatne poradniki o AI w firmie, mniej więcej co 2 tygodnie. Mogę się wypisać w każdej chwili.'


def audit_form(legend, calm, rodo):
    tiles = ''.join(
        '<label class="tile%s"><input type="radio" name="kafelek" value="%s"%s><span class="n">%s</span><span class="p%s">%s</span></label>'
        % (' on' if i == 0 else '', v, ' checked' if i == 0 else '', esc(n), ' free' if v == 'mini' else '', esc(p))
        for i, (v, n, p) in enumerate(TILES))
    opts = ''.join('<option value="%s">%s</option>' % (attr(b), esc(b)) for b in BRANZE)
    return f'''<form class="form" id="audit-form" action="https://api.web3forms.com/submit" method="POST" novalidate>
<input type="hidden" name="access_key" value="7003f878-52e8-4f95-ac90-3dbadec662c6">
<input type="hidden" name="subject" value="Zgłoszenie na mini-audyt AI Visibility">
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
<p class="chosen" aria-live="polite">Wybrany pakiet: <strong id="chosen-name">Darmowy mini-audyt</strong></p></fieldset>
<div class="field" id="f-firma"><label class="chk dark" for="firma"><input type="checkbox" id="firma" name="prowadze_firme" value="Tak" required aria-describedby="e-firma"><span>Prowadzę firmę lub odpowiadam za jej stronę</span></label>
<div class="err" id="e-firma" aria-live="polite"></div></div>
<label class="chk" for="newsletter"><input type="checkbox" id="newsletter" name="newsletter" value="tak"><span>{esc(NEWS_TEXT)}</span></label>
<div class="field" id="f-captcha"><div class="h-captcha captcha" data-captcha="true" data-theme="light"></div><div class="err" id="e-captcha" aria-live="polite"></div></div>
<div class="hp" aria-hidden="true"><label for="botcheck">Nie wypełniaj tego pola</label><input type="checkbox" id="botcheck" name="botcheck" tabindex="-1"></div>
<button class="btn-submit" id="submit-btn" type="submit">Zamów darmowy audyt</button>
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


RODO_MAIN = ('Wysyłając formularz, zgadzasz się na kontakt w sprawie audytu. Administrator danych: Filip Szmel. '
             'Szczegóły w <a class="link" href="/polityka-prywatnosci">polityce prywatności</a>.')
RODO_CENNIK = ('Wysyłając formularz, zgadzasz się na kontakt w sprawie zgłoszenia. Administrator danych: Filip Szmel. '
               'Szczegóły w <a class="link" href="/polityka-prywatnosci">polityce prywatności</a>.')

ORG_ID = SITE + '/#firma'
PERSON_ID = SITE + '/#filip'
PROVIDER = {'@type': 'Organization', '@id': ORG_ID, 'name': 'Wskazani', 'url': SITE + '/'}

# ---------------------------------------------------------------- dane: oferta
OFFERS = [  # (nazwa, cena, "od", co miesiąc, opis)
    ('Mini-audyt', 0, False, False, 'Czy AI czyta Twoją stronę i 3 najważniejsze problemy. Raport w 48 h roboczych.'),
    ('Start: test usługi', 199, False, False, 'Plan poprawek krok po kroku i 1–2 szybkie poprawki, które wprowadzam za Ciebie. Kwota odliczana od Wdrożenia.'),
    ('Wdrożenie widoczności', 990, True, False, 'Wszystkie poprawki z audytu, dane o firmie dla Google i AI, pytania i odpowiedzi na stronie, test przed i po 30 dniach.'),
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
            'url': SITE + path, 'serviceType': 'Widoczność firmy w AI (GEO)', 'areaServed': {'@type': 'Country', 'name': 'Polska'},
            'provider': PROVIDER, 'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': name, 'itemListElement': [offer_ld(*o) for o in offers]}}


# ================================================================= STRONA GŁÓWNA
MAIN_CARDS = [
    ('mini', 'Mini-audyt', '', '0 zł', '', 'Czy AI czyta Twoją stronę i 3 najważniejsze problemy. Raport w 48 h roboczych.', 'Zamów za darmo', False),
    ('start', 'Start: test usługi', '', '199 zł', 'jednorazowo', 'Plan poprawek i 1–2 poprawki wdrożone od ręki. Kwota odliczana od Wdrożenia.', 'Wybierz Start', False),
    ('wdrozenie', 'Wdrożenie widoczności', 'od', '990 zł', '', 'Wszystkie poprawki z audytu i test przed i po 30 dniach.', 'Wybierz Wdrożenie', True),
    ('strona', 'Nowa strona', 'od', '1990 zł', '', 'Strona 4–6 podstron, gotowa pod Google i AI od pierwszego dnia.', 'Zapytaj o stronę', False),
]
MAIN_FAQ = [
    ('Czy mini-audyt jest naprawdę darmowy?', 'Tak. Nie płacisz nic i nie musisz potem niczego kupować. Raport jest Twój i do niczego nie zobowiązuje.'),
    ('Czym różni się darmowy mini-audyt od Startu za 199 zł?', 'Mini-audyt mówi, co jest nie tak. Start to naprawia: dostajesz plan poprawek i 1–2 poprawki wdrożone od ręki. Jeśli potem zlecisz Wdrożenie, 199 zł odliczam od jego ceny.'),
    ('Jak się rozliczasz?', 'Start płatny z góry. Wdrożenie: połowa przed startem, połowa do 7 dni po wykonaniu. Nowa strona: połowa przed startem, połowa przed publikacją. Abonament z góry za miesiąc, wypowiedzenie miesięczne.'),
    ('Czy gwarantujesz, że ChatGPT poleci moją firmę?', 'Nie. Asystenci AI sami decydują, kogo wymienić. Poprawiam to, co AI czyta, i pokazuję wynik przed i po 30 dniach.'),
    ('Co muszę zrobić ja?', 'Dać dostęp do strony i znaleźć 10 minut na kilka pytań. Resztę robię ja.'),
]


def build_main():
    cards = []
    for pid, name, pre, price, post, desc, cta, rec in MAIN_CARDS:
        badge = '<span class="badge">Polecany na start</span>' if rec else ''
        btn = 'btn-primary' if rec else 'btn-outline'
        cards.append(
            f'<article class="price-card{" pick" if rec else ""}">{badge}<h3>{esc(name)}</h3>'
            f'<p class="price"><span class="pre">{pre}</span><span class="num{" price-ok" if pid == "mini" else ""}">{price}</span><span class="post">{post}</span></p>'
            f'<p class="desc">{esc(desc)}</p>'
            f'<a class="btn {btn} btn-block" href="/?pakiet={pid}#audyt" data-pakiet="{pid}">{esc(cta)}</a></article>')
    cards = '\n'.join(cards)
    return f'''<section id="top" class="wrap hero">
<div class="hero-l">
<h1 class="eyebrow">Darmowy audyt widoczności firmy w AI</h1>
<p class="display xl">Sprawdzę za darmo, czy ChatGPT i Google polecają Twoją firmę.</p>
<p class="lead">Analiza jest bezpłatna. Płacisz tylko, jeśli zlecisz poprawki, od 199 zł.</p>
<div class="btn-row"><a class="btn btn-primary btn-lg" href="#audyt">Zamów darmowy audyt</a><a class="btn btn-outline btn-lg" href="#ceny" data-ga="zobacz_ceny" data-ga-miejsce="glowna_hero">Zobacz ceny</a></div>
<p class="note" style="margin-top:22px">Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych</p>
</div>
<figure class="hero-r report" aria-label="Przykładowy raport z mini-audytu">
<div class="report-top"><span class="t">Mini-audyt · przykład</span><span class="pill">0 zł</span></div>
<p class="q">Czy AI rozumie stronę Twojej firmy?</p>
<div class="rrow ok">{tick('#15803D', 22, '2.4')}<div><strong>Boty AI mają dostęp do strony</strong><div>Nic ich nie blokuje.</div></div></div>
<div class="rrow">{bang()}<div><strong>Brak danych o firmie dla Google</strong><div>AI musi zgadywać, czym się zajmujesz.</div></div></div>
<div class="rrow">{bang()}<div><strong>Tytuł strony ucinany w Google</strong><div>120 znaków, Google pokazuje ok. 60.</div></div></div>
<figcaption>Wynik w 48 h roboczych · bez zobowiązań</figcaption>
</figure>
</section>

<section class="band" aria-label="Dane"><div class="wrap sec stats grid g-240" style="padding-block:44px;gap:32px">
<div><p class="n">16 mln</p><p class="t">polskich internautów korzysta już z narzędzi AI. Twoi klienci też.</p></div>
<div><p class="n">6 na 10</p><p class="t">Polaków pyta AI, zanim wybierze produkt lub usługę.</p></div>
<div><p class="n">2× więcej</p><p class="t">kliknięć dostają firmy cytowane w odpowiedzi AI Google niż te, które AI pomija (badanie z USA).</p></div>
</div></section>

<section id="jak" class="wrap sec" aria-label="Jak to działa" style="padding-bottom:72px">
<h2 class="h2 lg">Jak działa audyt widoczności w AI?</h2>
<p class="sub">Trzy kroki. Bez zobowiązań.</p>
<ol class="steps3">
<li><span class="num">1</span><strong>Podajesz adres strony</strong><span class="d">Formularz na dole tej strony, około minuty. Nie potrzebuję dostępu do niczego.</span></li>
<li><span class="num">2</span><strong>W 48 h roboczych dostajesz raport</strong><span class="d">Co działa, co blokuje AI i co poprawić najpierw. Prostym językiem.</span></li>
<li><span class="num">3</span><strong>Decyzja należy do Ciebie</strong><span class="d">Zlecasz mi poprawki, od 199 zł, albo zostajesz z darmowym raportem. Cenę znasz z góry.</span></li>
</ol>
</section>

<section class="band" aria-label="Przykładowe ustalenia"><div class="wrap sec">
<h2 class="h2 lg" style="max-width:760px">Co najczęściej blokuje firmy w AI?</h2>
<p class="muted" style="margin-top:14px;font-size:18px;max-width:680px">Prawdziwe ustalenia ze stron firm, które sprawdziłem we wrześniu i październiku 2026. Bez nazw.</p>
<div class="grid g-280" style="margin-top:36px">
<div class="finding"><p class="k">Klinika</p><p class="v">Plik dla robotów blokował stronę „Pierwsza wizyta”, której pacjent szuka najczęściej.</p></div>
<div class="finding"><p class="k">Firma budowlana</p><p class="v">Najnowsze treści na stronie były z 2017 roku, a strona nie miała formularza kontaktowego, mapy ani opisu firmy, który Google czyta bez zgadywania.</p></div>
<div class="finding"><p class="k">Hotel</p><p class="v">Najmocniejszy argument, darmowy transfer 24 h, nie trafił do opisu, który pokazuje Google.</p></div>
</div></div></section>

<section id="ceny" class="wrap sec" aria-label="Ceny" style="padding-bottom:48px">
<h2 class="h2 lg">Ile kosztuje widoczność w AI?</h2>
<p class="sub">Jawne ceny. Zaczynasz od zera złotych.</p>
<p class="muted" style="margin-top:14px;font-size:18px;line-height:1.55;max-width:720px">Audyt 0 zł, pierwszy krok 199 zł, wdrożenie od 990 zł, nowa strona od 1990 zł. Kwoty końcowe, bez VAT. Dokładną kwotę znasz po darmowym audycie, zanim cokolwiek zlecisz.</p>
<p class="note" style="margin-top:8px">Ceny aktualne: październik 2026</p>
<div class="grid g-240" style="gap:18px;margin-top:40px;align-items:stretch">
{cards}
</div>
<div style="display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;margin-top:28px;font-size:16px">
<span class="muted">Stała opieka od 199 zł / miesiąc, bez umowy na lata.</span>
<a class="link" href="/wspolpraca" style="font-size:17px">Współpraca stała →</a>
<a class="link" href="/cennik" style="font-size:17px">Porównaj pakiety i zrób quiz →</a>
</div>
</section>

<section id="kalkulator" class="wrap" aria-label="Kalkulator" style="padding-block:24px 88px">
<div class="calc-box">
<div class="txt"><strong>Ile zarabiasz na klientach, którzy pytają AI?</strong><p>Prosty szacunek z Twoich liczb. Trzy suwaki, 20 sekund.</p></div>
<button class="btn btn-outline" id="calc-toggle" type="button" aria-expanded="false" aria-controls="calc-body" style="min-height:48px;padding:0 24px;font-weight:700">Policz</button>
<div class="calc-body" id="calc-body" hidden>
<div class="calc-in">
<div><label for="k-klienci"><span>Nowi klienci z internetu miesięcznie</span><output id="v-klienci" for="k-klienci">10</output></label><input id="k-klienci" type="range" min="1" max="60" step="1" value="10"></div>
<div><label for="k-wartosc"><span>Średnia wartość klienta</span><output id="v-wartosc" for="k-wartosc">1 500 zł</output></label><input id="k-wartosc" type="range" min="100" max="10000" step="100" value="1500"></div>
<div><label for="k-udzial"><span>Część z nich, która pyta AI</span><output id="v-udzial" for="k-udzial">20%</output></label><input id="k-udzial" type="range" min="5" max="60" step="5" value="20">
<p class="hint">Przyjmij ostrożnie. W badaniu z kwietnia 2026 61% dorosłych Polaków użyło AI przy wyborze produktu lub usługi.</p></div>
</div>
<div class="calc-out on-navy">
<div><p class="l">Przychód od klientów pytających AI, miesięcznie</p><p class="big" id="o-mies" aria-live="polite">3 000 zł</p>
<p class="y">Rocznie: <strong id="o-rok">36 000 zł</strong></p>
<p class="e">Tyle mogą Ci przynosić klienci, którzy przed wyborem firmy pytają AI. Jeśli AI nie rozumie Twojej strony, część z nich wybierze konkurencję.</p></div>
<a class="btn btn-primary btn-block" href="#audyt" style="min-height:48px">Sprawdź swoją stronę za darmo</a>
</div>
</div>
</div>
</section>

<section id="omnie" class="band" aria-label="Kto to robi"><div class="wrap sec"><div class="who">
<div class="who-logo"><svg role="img" aria-label="Logo Wskazani" width="128" height="128" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="#FAF8F4"></circle><path d="M14 26L21.5 41.5L29.5 30L37.5 41.5" fill="none" stroke="#13233A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"></path><path d="M37.5 41.5L50.5 18.5" fill="none" stroke="#F0743A" stroke-width="6" stroke-linecap="round"></path></svg><span>wskazani</span></div>
<div class="who-txt">
<p class="k">Kto to robi</p>
<h2>Filip Szmel, Warszawa</h2>
<p class="p">Klienci coraz częściej pytają AI, komu powierzyć sprawę, a w audytach widzę, że strony wielu firm nie są na to gotowe. Ten rynek dopiero powstaje, dlatego robię to tak, jak sam chciałbym to kupić: konkretnie, z wynikiem przed i po, bez umowy na lata. Rozmawiasz ze mną od pierwszego maila do wyniku po 30 dniach.</p>
<ul>
<li>{tick()}<span>Poprawki wprowadzam za Ciebie, nie dostajesz listy zadań</span></li>
<li>{tick()}<span>Piszę wprost, co sprawdziłem, a czego nie</span></li>
<li>{tick()}<span>Nie obiecuję poleceń AI, pokazuję wynik przed i po</span></li>
</ul>
<div class="contact-row"><a class="link" href="tel:+48502890686">Zadzwoń: 502 890 686</a><a class="link" href="mailto:szmelfilip.business@gmail.com">Napisz: szmelfilip.business@gmail.com</a><a class="link" href="https://www.linkedin.com/in/filip-szmel-b2993a439/" rel="me noopener" target="_blank">LinkedIn</a></div>
</div></div></div></section>

<section class="wrap-900 sec" aria-label="Pytania" style="padding-bottom:72px">
<h2 class="h2 lg">Pytania przed zamówieniem audytu</h2>
<div style="margin-top:24px">{faq_details(MAIN_FAQ)}</div>
<a class="link" href="/faq" style="margin-top:16px;font-size:17px">Wszystkie pytania i słowniczek →</a>
</section>

<section id="audyt" class="band-navy on-navy" aria-label="Darmowy audyt"><div class="wrap sec"><div class="audit">
<div class="audit-l">
<h2 class="h2 lg" style="line-height:1.08;text-wrap:balance">Podaj adres strony. Resztę zrobię ja.</h2>
<p class="p">Raport w 48 h roboczych. Płacisz dopiero, jeśli zlecisz poprawki.</p>
<ul class="ticks"><li>{tick('#86EFAC')}<span>Bez umowy na lata</span></li><li>{tick('#86EFAC')}<span>Przelew, BLIK lub karta</span></li><li>{tick('#86EFAC')}<span>Nie musisz potem niczego kupować</span></li></ul>
</div>
<div class="formbox">
{audit_form('Czego potrzebujesz?', 'Odpowiadam w 48 h roboczych. Bez zobowiązań.', RODO_MAIN)}
</div></div></div></section>

<section id="wskazowki" class="band" aria-label="Newsletter Wskazówki" style="border-top:0"><div class="wrap news" style="padding-block:64px">
<div class="news-l"><h2>„Wskazówki”: poradniki o AI dla firm</h2><p>Co 2 tygodnie jedna praktyczna porada, jedna zmiana na rynku i jedno narzędzie. Bezpłatnie, bez spamu.</p></div>
<div class="news-r">
<div id="news-ok" role="status" hidden><p style="font-size:18px;font-weight:700">Dzięki! Pierwsze „Wskazówki” dostaniesz mailem.</p><p class="muted" style="margin-top:8px;font-size:15px">Wypisać się możesz w każdej chwili.</p></div>
<form class="news-form" id="news-form" novalidate>
<div class="r"><label class="sr" for="n-email">E-mail do zapisu na „Wskazówki”</label>
<input id="n-email" type="email" name="email" required placeholder="Twój e-mail" autocomplete="email" autocapitalize="off" spellcheck="false">
<button class="btn-submit" type="submit">Zapisz się</button></div>
<div class="err" id="n-err" aria-live="polite"></div>
<label class="chk" for="n-zgoda"><input id="n-zgoda" type="checkbox" required><span>{esc(NEWS_TEXT)}</span></label>
<div class="hp" aria-hidden="true"><label for="n-bot">Nie wypełniaj tego pola</label><input type="checkbox" id="n-bot" tabindex="-1"></div>
</form>
</div></div></section>

<section id="przypisy" class="wrap foot-notes" aria-label="O Wskazani i przypisy">
<h2>O Wskazani</h2>
<p>Wskazani to audyt i wdrożenie widoczności w AI (GEO) dla firm z Warszawy i całej Polski, od jednoosobowych działalności po większe przedsiębiorstwa. Sprawdzam, czy ChatGPT, Perplexity, Gemini i tryb AI Google rozumieją stronę Twojej firmy i mogą ją polecić klientom. Darmowy mini-audyt widoczności w AI pokazuje w 48 godzin roboczych, czy roboty AI mają dostęp do strony, czy dane firmy są spójne w Google i w katalogach firm oraz czego brakuje w opisie usług. Poprawki wprowadzam za Ciebie: dostęp botów AI, dane strukturalne (schema.org), odpowiedzi na pytania klientów, tytuły i opisy w Google, wizytówkę Google i plik llms.txt. Pracuję z biurami rachunkowymi, kancelariami, biurami nieruchomości, doradcami finansowymi i lokalnymi firmami usługowymi. Pierwszy płatny krok kosztuje 199 zł, wdrożenie od 990 zł, nowa strona widoczna w AI od 1990 zł, a stała opieka i monitoring widoczności w AI od 199 zł miesięcznie, bez umowy na lata. Wskazani prowadzi Filip Szmel.</p>
<h2 class="src">Źródła danych</h2>
<ul>
<li>Gemius i PBI (Mediapanel), raport „E-commerce w Polsce 2026”, dane z czerwca 2026, publikacja wrzesień 2026.</li>
<li>On Board Think Kong / SW Research, badanie internetowe, N=830 dorosłych Polaków, kwiecień 2026. 61% badanych w ciągu ostatnich 6 miesięcy użyło AI przy wyborze produktów lub usług.</li>
<li>Seer Interactive, 53 marki, 5,47 mln zapytań, publikacja 24.04.2026, dane głównie z USA. Marki cytowane w odpowiedzi AI Google (AI Overview) miały o 120% więcej kliknięć niż marki niecytowane.</li>
<li>Kwoty końcowe, bez VAT (działalność nierejestrowana). Dokładną kwotę wdrożenia podaję po darmowym audycie, zanim cokolwiek zlecisz. Ceny aktualne: październik 2026.</li>
<li>Ustalenia ze stron firm sprawdzonych we wrześniu i październiku 2026. Nazwy firm pominięte.</li>
</ul>
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
             'description': 'Audyt i wdrożenie widoczności firmy w AI (GEO) dla firm z Warszawy i całej Polski.',
             'founder': {'@id': PERSON_ID}, 'areaServed': {'@type': 'Country', 'name': 'Polska'},
             'address': {'@type': 'PostalAddress', 'addressLocality': 'Warszawa', 'addressCountry': 'PL'},
             'contactPoint': {'@type': 'ContactPoint', 'contactType': 'obsługa klienta', 'telephone': '+48502890686',
                              'email': 'szmelfilip.business@gmail.com', 'availableLanguage': 'pl'},
             'sameAs': ['https://www.linkedin.com/in/filip-szmel-b2993a439/']},
            {'@type': 'Person', '@id': PERSON_ID, 'name': 'Filip Szmel', 'url': SITE + '/#omnie',
             'email': 'szmelfilip.business@gmail.com', 'telephone': '+48502890686', 'worksFor': {'@id': ORG_ID},
             'homeLocation': {'@type': 'Place', 'name': 'Warszawa'},
             'sameAs': ['https://www.linkedin.com/in/filip-szmel-b2993a439/']},
        ]}]


# ================================================================= CENNIK
CMP_ROWS = [
    ('Raport: co działa, co nie', '✓', '✓', '✓', '✓'),
    ('Plan poprawek krok po kroku', '—', '✓', '✓', '✓'),
    ('Poprawki wdrożone za Ciebie', '—', '1–2 szybkie', 'Wszystkie', 'W nowej stronie'),
    ('Dane o firmie dla Google i AI', '—', '—', '✓', '✓'),
    ('Pytania i odpowiedzi na stronie', '—', '—', '✓', '✓'),
    ('Test przed i po 30 dniach', '—', '—', '✓', '✓'),
    ('Kwota odliczana od Wdrożenia', '—', '✓', '—', '—'),
    ('Nowa strona 4–6 podstron', '—', '—', '—', '✓'),
    ('Cena', '0 zł', '199 zł', 'od 990 zł', 'od 1990 zł'),
]
CENNIK_FAQ = [
    ('Czym różni się darmowy mini-audyt od Startu za 199 zł?', 'Mini-audyt mówi, co jest nie tak. Start to plan poprawek i 1–2 szybkie poprawki, które wprowadzam za Ciebie. Kwota jest odliczana od Wdrożenia.'),
    ('Czy po darmowym audycie muszę coś kupić?', 'Nie. Raport jest Twój i do niczego nie zobowiązuje.'),
    ('Czy gwarantujesz, że ChatGPT poleci moją firmę?', 'Nie. Nikt nie może tego uczciwie obiecać. Poprawiam to, co AI czyta, i pokazuję wynik przed i po 30 dniach (we Wdrożeniu i Nowej stronie).'),
    ('Czy do ceny dochodzi VAT?', 'Nie. Kwoty na stronie są końcowe, nie doliczam VAT.'),
]
STEPS7 = [('Wysyłasz adres strony', '0 zł'), ('Mini-audyt w 48 h roboczych', '0 zł'), ('15 min rozmowy', 'opcjonalnie'), ('Wybierasz pakiet', 'od 199 zł'),
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
            ('mini', 'Mini-audyt', 'Mini-audyt'), ('start', 'Start', 'Start'),
            ('wdrozenie', 'Wdrożenie', 'Wdrożenie <span class="rec-tag">Polecany</span>'), ('strona', 'Nowa strona', 'Nowa strona')])
    body_rows = ''.join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td class="rec">%s</td><td>%s</td></tr>' % tuple(esc(x) for x in r) for r in CMP_ROWS)
    steps = ''.join(
        '<li><span class="n">%d</span><strong>%s</strong>%s</li>' % (i + 1, esc(t), ('<span class="tag%s">%s</span>' % (' free' if tag == '0 zł' else '', esc(tag))) if tag else '<span class="tag"></span>')
        for i, (t, tag) in enumerate(STEPS7))
    return f'''<section id="top" class="wrap center" style="padding-block:88px 32px">
<h1 class="eyebrow">Cennik · ile kosztuje widoczność w AI</h1>
<p class="display md">Jasne ceny. Zaczynasz od 0 zł.</p>
<p style="margin:22px auto 0;font-size:18px;line-height:1.6;max-width:760px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 22px;text-align:left"><strong>W skrócie:</strong> mini-audyt 0 zł · pierwszy krok (Start) 199 zł · wdrożenie od 990 zł · nowa strona od 1990 zł · stała opieka od 199 zł / miesiąc. Kwoty końcowe, bez VAT.</p>
<p class="note" style="margin-top:10px">Ceny aktualne: październik 2026</p>
<p class="note" style="margin-top:14px">Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych</p>
</section>

<section class="quiz" id="quiz" aria-label="Który pakiet dla Ciebie"><div class="quiz-box">
<h2>Który pakiet widoczności w AI wybrać?</h2>
<p>Nie wiesz, co wybrać? Odpowiedz na 3 pytania.</p>
{quiz}
<div class="result-box"><div class="rt"><p class="l" id="quiz-label" aria-live="polite">Twój wynik pojawi się tutaj</p><p class="x" id="quiz-text">Odpowiedz na 3 pytania powyżej.</p><p class="s" id="quiz-note" hidden>Dokładną kwotę podam po darmowym audycie.</p></div>
<a class="btn btn-primary" id="quiz-pick" href="#audyt" hidden style="min-height:48px;padding:14px 24px">Wybieram ten zestaw</a></div>
</div></section>

<section class="wrap" aria-label="Pakiety jednorazowe" style="padding-block:88px 24px">
<h2 class="h2">Pakiety jednorazowe: audyt, wdrożenie, nowa strona</h2>
<div class="grid g-240" style="gap:18px;margin-top:32px;align-items:stretch">
<article class="price-card big"><h3>Mini-audyt</h3><p class="price"><span class="num price-ok">0 zł</span></p><p class="quote">„Chcę sprawdzić”</p>
<ul><li>Czy AI czyta Twoją stronę</li><li>3 najważniejsze problemy</li><li>Raport w 48 h roboczych</li></ul>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=mini#audyt" data-pakiet="mini">Zamów za darmo</a></article>
<article class="price-card big"><h3>Start — test usługi</h3><p class="price"><span class="num">199 zł</span><span class="post">jednorazowo</span></p><p class="quote">„Chcę najpierw spróbować”</p>
<ul><li>Plan poprawek krok po kroku</li><li>1–2 szybkie poprawki, które wprowadzam za Ciebie</li><li>Kwota odliczana od Wdrożenia</li></ul>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=start#audyt" data-pakiet="start">Wybierz Start</a></article>
<article class="price-card big pick"><span class="badge">Polecany na start</span><h3>Wdrożenie widoczności</h3><p class="price"><span class="pre">od</span><span class="num">990 zł</span></p><p class="quote">„Chcę mieć to zrobione porządnie”</p>
<ul><li>Wszystkie poprawki z audytu</li><li>Dane o firmie dla Google i AI</li><li>Pytania i odpowiedzi na stronie</li><li>Test przed i po 30 dniach</li></ul>
<a class="btn btn-primary btn-block" href="/cennik?pakiet=wdrozenie#audyt" data-pakiet="wdrozenie">Wybierz Wdrożenie</a></article>
<article class="price-card big"><h3>Nowa strona</h3><p class="price"><span class="pre">od</span><span class="num">1990 zł</span></p><p class="quote">„Strona jest stara albo jej nie ma”</p>
<ul><li>4–6 podstron</li><li>Gotowa pod Google i AI od pierwszego dnia</li><li>Test przed i po 30 dniach</li><li>Płatność: 50% na start, 50% przed publikacją</li></ul>
<a class="btn btn-outline btn-block" href="/cennik?pakiet=strona#audyt" data-pakiet="strona">Zapytaj o stronę</a></article>
</div>
<div class="dep">
<div class="all"><h3>Od czego zależy cena?</h3><p>Dokładną kwotę znasz po darmowym audycie, zanim cokolwiek zlecisz.</p></div>
<div class="c"><strong>Liczba podstron</strong><p>Więcej podstron to więcej miejsc do poprawienia.</p></div>
<div class="c"><strong>Stan strony</strong><p>Aktualna strona wymaga mniej pracy niż taka sprzed kilku lat.</p></div>
<div class="c"><strong>System strony</strong><p>Każdy system (WordPress, Wix, strona pisana ręcznie) wymaga innego podejścia.</p></div>
</div>
<div class="big-firms on-navy" id="duze-firmy" aria-label="Dla dużych firm"><div class="t"><span class="k">Dla dużych firm</span>
<p>Masz kilka oddziałów, wiele usług albo stronę z setkami podstron? Zaczynamy tak samo, od darmowego audytu, a zakres i cenę ustalamy indywidualnie, na piśmie, zanim cokolwiek zlecisz.</p></div>
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
<h2 class="h2">Ile kosztuje stała opieka nad widocznością w AI?</h2>
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
<div><p>Start za 199 zł</p><p>Zamiast płatnego audytu za 790–2000 zł u części agencji. Kwota jest odliczana od Wdrożenia.</p></div>
<div><p>Jedna osoba</p><p>Rozmawiasz z tym, kto robi poprawki. Bez pośredników i infolinii.</p></div>
</div>
<p class="foot">Porównanie na podstawie cenników agencji GEO z października 2026.</p>
</div></section>

<section id="rozliczenie" class="wrap" aria-label="Jak płacisz" style="padding-block:72px 24px">
<h2 class="h2">Jak przebiega współpraca i jak płacisz?</h2>
<ol class="steps7">{steps}</ol>
<div class="pay4">
<div><p>Start</p><p>100% z góry</p></div>
<div><p>Wdrożenie</p><p>50% przed, 50% do 7 dni po wykonaniu</p></div>
<div><p>Nowa strona</p><p>50% przed, 50% przed publikacją</p></div>
<div><p>Opieka i marketing</p><p>Z góry za miesiąc, wypowiedzenie miesięczne, bez kar</p></div>
</div>
<div class="methods" aria-label="Metody płatności"><span>{ICO_BANK}Przelew</span><span>{ICO_PHONE}BLIK</span><span>{ICO_CARD}Karta</span></div>
<p class="muted" style="margin-top:14px;font-size:15px">Przed płatnością dostajesz mailem potwierdzenie: zakres, kwota i terminy. Link do płatności BLIK-iem lub kartą przychodzi mailem. Do każdej wpłaty dostajesz rachunek (działalność nierejestrowana, bez VAT).</p>
</section>

<section class="wrap-900" aria-label="Pytania" style="padding-block:72px 24px">
<h2 class="h2">Pytania o ceny widoczności w AI</h2>
<div style="margin-top:24px">{faq_details(CENNIK_FAQ, 'faq-cards')}</div>
</section>

<section id="audyt" class="band-navy on-navy" aria-label="Zamówienie" style="margin-top:72px"><span id="formularz"></span><div class="wrap sec"><div class="audit">
<div class="audit-l">
<h2 class="h2 lg" style="line-height:1.08;text-wrap:balance">Pakiet wybrany? Wyślij zgłoszenie.</h2>
<p class="p">Nie wiesz jeszcze? Zostaw „Darmowy mini-audyt”. Po raporcie doradzę, od czego zacząć.</p>
<p class="n2">Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych</p>
</div>
<div class="formbox">
{audit_form('Wybrany pakiet', 'Przed płatnością dostaniesz mailem zakres, dokładną kwotę i terminy.', RODO_CENNIK)}
</div></div></div></section>

<section id="przypisy" class="wrap foot-notes" aria-label="Źródła danych" style="padding-top:40px">
<h2 class="src" style="margin-top:0">Źródła danych</h2>
<ul>
<li>Publiczne cenniki oraz długość umów czterech firm świadczących usługi GEO w Polsce, sprawdzone 17.10.2026. Te firmy podają kwoty netto, do których dochodzi 23% VAT. Nazw firm nie podajemy.</li>
<li>Kwoty końcowe, bez VAT (działalność nierejestrowana). Dokładną kwotę wdrożenia lub strony podaję po darmowym audycie, zanim cokolwiek zlecisz. Ceny aktualne: październik 2026.</li>
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
    ('Pierwszy krok', 'U części agencji płatny audyt, 790–2000 zł', 'Darmowy mini-audyt, potem Start za 199 zł, odliczany od Wdrożenia'),
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
<h1 class="eyebrow">Widoczność w AI (GEO) dla firm</h1>
<p class="display" style="max-width:900px">Poprawiam to, co ChatGPT, Perplexity i Google czytają o Twojej firmie.</p>
<p style="margin:20px 0 0;font-size:18px;line-height:1.6;max-width:760px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 22px"><strong>Czym jest GEO?</strong> To dbanie o to, żeby asystenci AI, tacy jak ChatGPT, Perplexity i tryb AI Google, rozumieli Twoją firmę i mogli ją wymienić w odpowiedzi. W praktyce: poprawki na stronie i spójne dane firmy w internecie.</p>
<p class="lead" style="margin-top:22px;max-width:660px">Konkretny zakres, jawne ceny i bez umowy na lata. Dla firm, które wiedzą, że klienci pytają AI, i szukają kogoś, kto to uporządkuje.</p>
<div class="btn-row" style="margin-top:32px"><a class="btn btn-primary btn-lg" href="/cennik" data-ga="zobacz_ceny" data-ga-miejsce="widocznosc_hero">Zobacz cennik</a><a class="btn btn-outline btn-lg" href="/#audyt">Zamów darmowy audyt</a></div>
<p class="note" style="margin-top:20px">Pierwszy krok za 199 zł · kwoty bez VAT · bez umowy na 6 miesięcy</p>
</section>

<section id="zakres" class="band" aria-label="Zakres usługi"><div class="wrap sec">
<h2 class="h2">Co obejmuje usługa GEO?</h2>
<p class="muted" style="margin-top:12px;font-size:18px;max-width:640px">Sześć obszarów. W darmowym mini-audycie dowiesz się, które z nich u Ciebie kuleją.</p>
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
<h2 class="h2">Dlaczego widoczność w AI ma znaczenie?</h2>
<div class="stats s4 grid g-240" style="gap:28px;margin-top:32px">{stats}</div>
</section>

{cta_band('Zacznij od darmowego audytu albo od Startu za 199 zł.', 'Start: plan poprawek i 1–2 szybkie poprawki, które wprowadzam za Ciebie. Kwota odliczana od Wdrożenia.',
         ('Zobacz cennik', '/cennik'), ('Zamów darmowy audyt', '/#audyt'), 'Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych').replace('class="btn btn-primary btn-lg" href="/cennik"', 'class="btn btn-primary btn-lg" href="/cennik" data-ga="zobacz_ceny" data-ga-miejsce="widocznosc_dol"')}
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
    ('Opieka+', '490', 'Chcesz, żeby widoczność rosła z miesiąca na miesiąc.', 'Dla rosnących firm', True, 'Wybierz Opiekę+', 'opieka-plus',
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
<h1 class="eyebrow">Stała opieka i monitoring widoczności w AI</h1>
<p class="display" style="max-width:860px">Bez umowy na lata. Od 199 zł miesięcznie.</p>
<p class="lead" style="margin-top:22px;max-width:640px">Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło. Płacisz z góry za miesiąc i możesz zrezygnować w każdym miesiącu.</p>
<div class="btn-row" style="margin-top:32px"><a class="btn btn-primary btn-lg" href="#pakiety">Wybierz pakiet</a><a class="btn btn-outline btn-lg" href="/#audyt">Zacznij od darmowego audytu</a></div>
<p class="note" style="margin-top:20px">Bez kar za rezygnację · Przelew, BLIK lub karta · Raport co miesiąc</p>
</section>

<section id="pakiety" class="wrap" aria-label="Pakiety miesięczne" style="padding-block:24px 88px">
<div class="grid g-300" style="align-items:stretch">
{plans}
</div>
<p class="muted" style="margin-top:22px;font-size:15px">Kwoty końcowe, bez VAT. Budżet reklam w pakiecie Marketing płacisz osobno, bezpośrednio do Google lub Meta.</p>
<p class="muted inline" style="margin-top:8px;font-size:15px">Nie wiesz, od czego zacząć? <a class="link" href="/cennik">Zrób quiz w cenniku</a> albo zacznij od Startu za 199 zł i przejdź na Opiekę później.</p>
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

{cta_band('Najpierw sprawdzę, od czego zacząć.', 'Darmowy mini-audyt pokaże, czy wystarczy Ci Opieka, czy najpierw warto zrobić Wdrożenie.', ('Zamów darmowy audyt', '/#audyt'), ('Porównaj wszystkie pakiety', '/cennik'),
         'Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych')}
'''


# ================================================================= FAQ
FAQ_GROUPS = [
    ('g0', 'Darmowy mini-audyt', [
        ('Czy mini-audyt jest naprawdę darmowy?', 'Tak. Nie płacisz nic i nie musisz potem niczego kupować. Płacisz tylko, jeśli zlecisz poprawki.'),
        ('Co dostaję?', 'Krótki raport prostym językiem: czy AI czyta Twoją stronę i 3 najważniejsze rzeczy do poprawy.'),
        ('Ile czekam?', 'Do 48 godzin roboczych od wysłania formularza.'),
        ('Czym różni się darmowy mini-audyt od Startu za 199 zł?', 'Mini-audyt mówi, co jest nie tak. Start to naprawia: dostajesz plan poprawek krok po kroku i 1–2 szybkie poprawki, które wprowadzam za Ciebie. Jeśli potem zlecisz Wdrożenie, 199 zł odliczam od jego ceny.'),
    ]),
    ('g1', 'Ceny i rozliczenie', [
        ('Ile to kosztuje?', 'Mini-audyt 0 zł, Start 199 zł, Wdrożenie od 990 zł, nowa strona od 1990 zł, stała opieka od 199 zł miesięcznie. Kwoty końcowe, bez VAT. Szczegóły i porównanie pakietów są w cenniku.'),
        ('Jak się rozliczasz?', 'Start płatny z góry. Wdrożenie: połowa przed startem, połowa do 7 dni po wykonaniu. Nowa strona: połowa przed startem, połowa przed publikacją. Abonament z góry za każdy miesiąc.'),
        ('Jak mogę zapłacić?', 'Przelewem albo BLIK-iem lub kartą przez link do płatności, który dostajesz mailem.'),
        ('Czy wystawiasz fakturę?', 'Teraz do każdej wpłaty dostajesz rachunek. Kwoty są końcowe, bez VAT. Gdy będę wystawiać faktury, napiszę o tym przed płatnością.'),
        ('Od czego zależy cena?', 'Od liczby podstron, stanu strony i systemu, na którym działa. Dokładną kwotę znasz po darmowym audycie, zanim cokolwiek zlecisz.'),
        ('Czy jest umowa?', 'Każde zlecenie potwierdzam mailem: zakres, kwota i terminy płatności. Abonament możesz wypowiedzieć w każdym miesiącu, bez kar.'),
        ('Mam kilka oddziałów albo stronę z setkami podstron. Jak wyceniasz?', 'Zaczynamy tak samo, od darmowego audytu, a zakres i cenę ustalamy indywidualnie, na piśmie, zanim cokolwiek zlecisz.'),
    ]),
    ('g2', 'Współpraca', [
        ('Co muszę zrobić ja?', 'Dać dostęp do strony i znaleźć 10 minut na kilka pytań. Resztę robię ja.'),
        ('Czy mogę zacząć od małego pakietu?', 'Tak. Start za 199 zł to test usługi: mała kwota, konkretny efekt na Twojej stronie.'),
        ('Czy gwarantujesz, że AI zacznie polecać moją firmę?', 'Nie. Asystenci AI sami decydują, kogo wymienić. Poprawiam to, co AI czyta, i pokazuję wynik przed i po 30 dniach.'),
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
<h1 class="eyebrow">Pytania o widoczność w AI i audyt</h1>
<p class="display">Masz pytanie? Tu jest krótka odpowiedź.</p>
<p class="lead" style="margin-top:18px">Jeśli czegoś brakuje, zadzwoń: <a class="link" href="tel:+48502890686">502 890 686</a>.</p>
</section>
<div class="wrap-900 faq-groups" style="padding-bottom:72px">{groups}</div>
<section id="slowniczek" class="band" aria-label="Słowniczek"><div class="wrap-900" style="padding-block:80px">
<h2 class="h2 sm">Słowniczek</h2>
<p class="muted" style="margin-top:10px;font-size:17px">Każde trudne słowo w jednym zdaniu.</p>
<dl class="gloss">{terms}</dl>
</div></section>
{cta_band('Masz jeszcze pytanie? Sprawdź stronę za darmo.', '', ('Zamów darmowy audyt', '/#audyt'), ('Zobacz cennik', '/cennik'), 'Bez umowy na lata · Przelew, BLIK lub karta · Odpowiedź w 48 h roboczych').replace('<div class="in">', '<div class="in" style="padding-block:80px">')}
'''


# ================================================================= POZOSTAŁE: polityka, dziękuję, 404
def build_polityka():
    body = open(os.path.join(ROOT, 'src', 'polityka-body.html'), encoding='utf8').read()
    return '<article class="doc">\n<p class="eyebrow" style="margin:0">RODO</p>\n<h1>Polityka prywatności</h1>\n%s</article>\n' % body


def build_dziekuje():
    return '''<section class="doc" id="thanks">
<p class="eyebrow" style="margin:0">Zgłoszenie przyjęte</p>
<h1>Zgłoszenie wysłane</h1>
<div id="t-audyt">
<p class="lead"><span id="t-pakiet"></span>Odpowiem na podany e-mail w ciągu 48 h roboczych. Jeśli chcesz coś dodać, napisz na <a class="link" href="mailto:szmelfilip.business@gmail.com">szmelfilip.business@gmail.com</a> lub zadzwoń: <a class="link" href="tel:+48502890686">502 890 686</a>.</p>
</div>
<div id="t-check" hidden>
<p class="lead">Pełna wersja checklisty jest gotowa do pobrania.</p>
<p style="margin-top:20px"><a class="btn btn-primary btn-lg" href="/checklista-widocznosc-w-ai.pdf" download>Pobierz checklistę (PDF)</a></p>
<p style="margin-top:16px">Jeśli plik się nie otworzy, napisz na <a class="link" href="mailto:szmelfilip.business@gmail.com">szmelfilip.business@gmail.com</a>. Chcesz, żebym sprawdził Twoją stronę? <a class="link" href="/#audyt">Zamów bezpłatny mini-audyt</a>.</p>
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
<div class="btn-row" style="margin-top:24px"><a class="btn btn-primary btn-lg" href="/">Wróć na stronę główną</a><a class="btn btn-outline btn-lg" href="/#audyt">Zamów darmowy audyt</a></div>
</section>
'''


# ================================================================= MONTAŻ
def write(name, content):
    with open(os.path.join(ROOT, name), 'w', encoding='utf8') as f:
        f.write(content)
    print('zapisano', name, len(content))


def main():
    write('index.html', page(
        '/', 'Darmowy audyt widoczności firmy w AI | Wskazani',
        'Sprawdzę za darmo, czy ChatGPT i Google polecają Twoją firmę. Analiza jest bezpłatna, płacisz tylko za zlecone poprawki, od 199 zł. Raport w 48 h roboczych.',
        build_main(), active='/', audyt_href='#audyt', sticky=True, jsonld=main_ld()))
    write('cennik.html', page(
        '/cennik', 'Cennik: ile kosztuje widoczność w AI | Wskazani',
        'Jasne ceny: mini-audyt 0 zł, Start 199 zł, wdrożenie od 990 zł, nowa strona od 1990 zł, stała opieka od 199 zł miesięcznie. Kwoty końcowe, bez VAT.',
        build_cennik(), active='/cennik', audyt_href='#audyt', sticky=True,
        jsonld=[service_ld('/cennik', 'Widoczność w AI (GEO): pakiety i ceny',
                           'Mini-audyt widoczności w AI, Start, Wdrożenie, nowa strona oraz stała opieka i monitoring. Kwoty końcowe, bez VAT.', OFFERS)]))
    write('widocznosc-w-ai.html', page(
        '/widocznosc-w-ai', 'Widoczność w AI (GEO) dla firm | Wskazani',
        'Poprawiam to, co ChatGPT, Perplexity i Google czytają o Twojej firmie. Konkretny zakres, jawne ceny i bez umowy na lata. Pierwszy krok za 199 zł.',
        build_geo(), active='/widocznosc-w-ai',
        bar=('Widoczność w AI (GEO)', [('#zakres', 'Zakres'), ('#porownanie', 'Porównanie'), ('#ustalenia', 'Ustalenia')], 'Zobacz cennik', '/cennik')))
    write('wspolpraca.html', page(
        '/wspolpraca', 'Stała opieka i monitoring widoczności w AI | Wskazani',
        'Bez umowy na lata, od 199 zł miesięcznie. Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło.',
        build_wsp(), active='/wspolpraca',
        bar=('Współpraca stała', [('#pakiety', 'Pakiety'), ('#raport', 'Raport'), ('#rezygnacja', 'Rezygnacja')], 'Zamów audyt', '/#audyt'),
        jsonld=[service_ld('/wspolpraca', 'Stała opieka i monitoring widoczności w AI',
                           'Co miesiąc sprawdzam, czy AI dalej rozumie Twoją firmę, i poprawiam to, co się zmieniło. Bez umowy na lata.', OFFERS[4:])]))
    write('faq.html', page(
        '/faq', 'Pytania o widoczność w AI i audyt | Wskazani',
        'Krótkie odpowiedzi o darmowym mini-audycie, cenach, rozliczeniu, współpracy i technice, plus słowniczek: GEO, AI Overviews, llms.txt.',
        build_faq(), active='/faq',
        bar=('Pytania i słowniczek', [('#g0', 'Audyt'), ('#g1', 'Rozliczenie'), ('#g2', 'Współpraca'), ('#g3', 'Technika'), ('#slowniczek', 'Słowniczek')], 'Zamów audyt', '/#audyt'),
        jsonld=[dict({'@context': 'https://schema.org'}, **faq_ld(FAQ_ALL))]))
    write('polityka-prywatnosci.html', page(
        '/polityka-prywatnosci', 'Polityka prywatności | Wskazani',
        'Jak przetwarzam dane z formularzy: administrator, cel, podstawa prawna, odbiorcy, okres przechowywania i Twoje prawa.',
        build_polityka(), robots='noindex, follow', mobile_cta=False))
    write('dziekuje.html', page(
        '/dziekuje', 'Dziękuję za zgłoszenie | Wskazani', 'Zgłoszenie zostało wysłane.', build_dziekuje(), robots='noindex', mobile_cta=False))
    write('404.html', page(
        '/404', 'Nie znaleziono strony | Wskazani', 'Ta strona nie istnieje. Wróć na stronę główną i zamów darmowy audyt widoczności firmy w AI.',
        build_404(), robots='noindex', mobile_cta=False))

    urls = ['/', '/cennik', '/widocznosc-w-ai', '/wspolpraca', '/faq']
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, u, LASTMOD))
    sm.append('</urlset>\n')
    write('sitemap.xml', '\n'.join(sm))


if __name__ == '__main__':
    main()
