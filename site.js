/* wskazani.pl — wspólny skrypt. Bez bibliotek. Konfiguracja formularza, zgody i tagu Google przeniesiona ze starej strony. */
(function(){
  'use strict';

  var EMAIL = 'szmelfilip.business@gmail.com';
  var KEY = '7003f878-52e8-4f95-ac90-3dbadec662c6';
  var GOOGLE_ADS_ID = 'AW-18503882283', GOOGLE_ADS_LABEL = 'DfXmCMW3pZkdEKusq_dE', GA4_ID = 'G-ENH7LJ2YW2';

  function $(id){ return document.getElementById(id); }
  function sget(k){ try{ return sessionStorage.getItem(k); }catch(e){ return null; } }
  function sset(k,v){ try{ sessionStorage.setItem(k,v); }catch(e){} }
  function sdel(k){ try{ sessionStorage.removeItem(k); }catch(e){} }
  function store(k,v){ try{ if(v===undefined) return localStorage.getItem(k); localStorage.setItem(k,v); }catch(e){ return null; } }

  /* ---- Parametry UTM i strona wejścia (tylko sessionStorage, potrzebne do opisania zgłoszenia) ---- */
  var UTM = ['gclid','utm_source','utm_medium','utm_campaign','utm_content','utm_term'];
  (function(){
    var q = new URLSearchParams(location.search);
    UTM.forEach(function(k){ var v = q.get(k); if(v) sset('wsk_'+k, v.slice(0,200)); });
    if(!sget('wsk_wejscie')) sset('wsk_wejscie', location.pathname);
  })();

  /* ---- Zgoda cookies (Consent Mode v2: domyślnie denied, ustawiane w <head> przed gtag.js) ---- */
  function gconsent(v){ if(typeof gtag === 'function') gtag('consent','update',{ad_storage:v,ad_user_data:v,ad_personalization:v,analytics_storage:v}); }
  function consented(){ return store('zgoda-marketing') === 'tak'; }
  var box = $('consent');
  if(box){
    var c = store('zgoda-marketing');
    if(c !== 'tak' && c !== 'nie') box.hidden = false;
    $('c-yes').onclick = function(){ store('zgoda-marketing','tak'); box.hidden = true; gconsent('granted'); };
    $('c-no').onclick = function(){ var had = store('zgoda-marketing') === 'tak'; store('zgoda-marketing','nie'); gconsent('denied'); box.hidden = true; if(had) location.reload(); };
    var cs = $('cookie-settings'); if(cs) cs.onclick = function(ev){ ev.preventDefault(); box.hidden = false; $('c-yes').focus(); };
  }

  /* ---- Zdarzenia GA4: tylko po zgodzie ---- */
  function ev(name, params){
    if(!consented() || typeof gtag !== 'function') return;
    var p = params || {}; p.strona = location.pathname;
    gtag('event', name, p);
  }
  document.addEventListener('click', function(e){
    var el = e.target.closest ? e.target.closest('[data-ga]') : null;
    if(el) ev(el.getAttribute('data-ga'), { miejsce: el.getAttribute('data-ga-miejsce') || '' });
  });

  /* ---- Menu (hamburger na telefonie) ---- */
  var tg = $('nav-toggle'), panel = $('nav-panel');
  if(tg && panel){
    function setNav(open){ panel.classList.toggle('open', open); tg.setAttribute('aria-expanded', open ? 'true' : 'false'); tg.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu'); }
    tg.addEventListener('click', function(){ setNav(!panel.classList.contains('open')); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && panel.classList.contains('open')){ setNav(false); tg.focus(); } });
    panel.addEventListener('click', function(e){ if(e.target.closest('a')) setNav(false); });
  }

  /* ---- Kalkulator (strona główna) ---- */
  var calcBtn = $('calc-toggle'), calcBody = $('calc-body');
  if(calcBtn && calcBody){
    var fmt = function(n){ return Math.round(n).toLocaleString('pl-PL'); };
    var kl = $('k-klienci'), wr = $('k-wartosc'), ud = $('k-udzial'), openedOnce = false;
    function calc(){
      var k = +kl.value, w = +wr.value, u = +ud.value, m = k * w * u / 100;
      $('v-klienci').textContent = k; $('v-wartosc').textContent = fmt(w) + ' zł'; $('v-udzial').textContent = u + '%';
      $('o-mies').textContent = fmt(m) + ' zł'; $('o-rok').textContent = fmt(m * 12) + ' zł';
    }
    function setCalc(open){
      calcBody.hidden = !open; calcBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); calcBtn.textContent = open ? 'Zwiń' : 'Policz';
      if(open && !openedOnce){ openedOnce = true; ev('kalkulator_policz'); }
    }
    [kl, wr, ud].forEach(function(el){ el.addEventListener('input', calc); });
    calcBtn.addEventListener('click', function(){ setCalc(calcBody.hidden); });
    calc();
    if(location.hash === '#kalkulator') setCalc(true);
    window.addEventListener('hashchange', function(){ if(location.hash === '#kalkulator') setCalc(true); });
  }

  /* ---- Pakiety: wybór kafelka, parametr ?pakiet=… ---- */
  var PK = {
    'mini':        { tile: 'mini',      name: 'Darmowy mini-audyt' },
    'start':       { tile: 'start',     name: 'Start: test usługi' },
    'wdrozenie':   { tile: 'wdrozenie', name: 'Wdrożenie widoczności' },
    'strona':      { tile: 'strona',    name: 'Nowa strona' },
    'opieka':      { tile: 'opieka',    name: 'Opieka i monitoring AI' },
    'opieka-plus': { tile: 'opieka',    name: 'Opieka+' },
    'marketing':   { tile: 'opieka',    name: 'Marketing na zlecenie' }
  };
  var form = $('audit-form');
  var current = { id: 'mini', name: 'Darmowy mini-audyt' };
  function setPackage(id){
    var p = PK[id]; if(!p || !form) return false;
    var tiles = form.querySelectorAll('.tile');
    Array.prototype.forEach.call(tiles, function(t){
      var inp = t.querySelector('input'), on = inp.value === p.tile;
      inp.checked = on; t.classList.toggle('on', on);
    });
    current = { id: id, name: p.name };
    var ch = $('chosen-name'); if(ch) ch.textContent = p.name;
    var sb = $('submit-btn'); if(sb) sb.textContent = (p.tile === 'mini') ? 'Zamów darmowy audyt' : 'Wyślij zgłoszenie';
    return true;
  }
  if(form){
    Array.prototype.forEach.call(form.querySelectorAll('.tile input'), function(inp){
      inp.addEventListener('change', function(){
        var label = inp.closest('.tile').querySelector('.n').textContent;
        setPackage(inp.value); current.name = label; var ch = $('chosen-name'); if(ch) ch.textContent = label;
        ev('wybor_pakietu', { pakiet: inp.value });
      });
    });
    var want = new URLSearchParams(location.search).get('pakiet');
    if(want && PK[want]) setPackage(want); else setPackage('mini');
  }
  /* przyciski pakietów: na stronie z formularzem zaznaczają pakiet bez przeładowania */
  document.addEventListener('click', function(e){
    var a = e.target.closest ? e.target.closest('a[data-pakiet]') : null;
    if(!a) return;
    var id = a.getAttribute('data-pakiet');
    ev('wybor_pakietu', { pakiet: id });
    if(form && PK[id] && new URL(a.href, location.href).pathname === location.pathname){
      e.preventDefault(); setPackage(id);
      var t = $('audyt'); if(t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      try{ history.replaceState(null, '', '#audyt'); }catch(x){}
    }
  });

  /* ---- Quiz „Który pakiet?” (cennik) ---- */
  var quiz = $('quiz');
  if(quiz){
    var ans = { q1: null, q2: null, q3: null }, quizSent = false;
    function quizId(){
      if(ans.q2 === 'sprawdzic') return ans.q1 === 'brak' ? 'strona' : 'mini';
      if(ans.q1 === 'brak') return 'strona';
      if(ans.q2 === 'naprawic') return 'start';
      if(ans.q2 === 'komplet') return ans.q1 === 'stara' ? 'strona' : 'wdrozenie';
      return 'mini';
    }
    function quizText(){
      var m = '';
      if(ans.q2 === 'sprawdzic') m = ans.q1 === 'brak' ? 'Nowa strona (od 1990 zł). Zakres i dokładną cenę ustalimy w bezpłatnej rozmowie.' : 'Darmowy mini-audyt (0 zł)';
      else if(ans.q1 === 'brak') m = 'Nowa strona (od 1990 zł)';
      else if(ans.q2 === 'naprawic') m = 'Start (199 zł)';
      else if(ans.q2 === 'komplet') m = ans.q1 === 'stara' ? 'Nowa strona (od 1990 zł)' : 'Wdrożenie (od 990 zł)';
      var x = '';
      if(ans.q3 === 'pilnowac') x = ' + Opieka (od 199 zł/mies.)';
      if(ans.q3 === 'marketing') x = ' + Marketing na zlecenie (od 1490 zł/mies.)';
      return m + x;
    }
    function renderQuiz(){
      Array.prototype.forEach.call(quiz.querySelectorAll('.opt'), function(b){
        b.setAttribute('aria-pressed', ans[b.getAttribute('data-q')] === b.getAttribute('data-v') ? 'true' : 'false');
      });
      var done = ans.q1 && ans.q2 && ans.q3;
      $('quiz-label').textContent = done ? 'Polecam Ci' : 'Twój wynik pojawi się tutaj';
      $('quiz-text').textContent = done ? quizText() : 'Odpowiedz na 3 pytania powyżej.';
      $('quiz-note').hidden = !done; $('quiz-pick').hidden = !done;
      if(done && !quizSent){ quizSent = true; }
      if(done) ev('quiz_pakietu', { wynik: quizId() });
    }
    quiz.addEventListener('click', function(e){
      var b = e.target.closest('.opt'); if(!b) return;
      ans[b.getAttribute('data-q')] = b.getAttribute('data-v'); renderQuiz();
    });
    $('quiz-pick').addEventListener('click', function(e){
      e.preventDefault(); setPackage(quizId());
      $('audyt').scrollIntoView({ behavior: 'smooth', block: 'start' });
      ev('wybor_pakietu', { pakiet: quizId(), zrodlo: 'quiz' });
    });
  }

  /* ---- Porównanie pakietów na telefonie (z tej samej tabeli) ---- */
  var cmp = $('cmp-table'), cmpM = $('cmp-mobile');
  if(cmp && cmpM){
    var names = Array.prototype.map.call(cmp.querySelectorAll('thead th[data-k]'), function(th){ return { k: th.getAttribute('data-k'), n: th.getAttribute('data-n') }; });
    var rows = Array.prototype.map.call(cmp.querySelectorAll('tbody tr'), function(tr){
      var cells = tr.querySelectorAll('td'); return { label: tr.querySelector('th').textContent, v: Array.prototype.map.call(cells, function(c){ return c.textContent; }) };
    });
    var sa = $('cmp-a'), sb2 = $('cmp-b'), out = $('cmp-rows');
    names.forEach(function(n, i){
      [sa, sb2].forEach(function(s){ var o = document.createElement('option'); o.value = i; o.textContent = n.n; s.appendChild(o); });
    });
    sa.value = 1; sb2.value = 2;
    function drawCmp(){
      out.textContent = '';
      rows.forEach(function(r){
        var d = document.createElement('div'), l = document.createElement('div'), t = document.createElement('div');
        l.className = 'lab'; l.textContent = r.label; t.className = 'two';
        [r.v[sa.value], r.v[sb2.value]].forEach(function(x){ var s = document.createElement('span'); s.textContent = x; t.appendChild(s); });
        d.appendChild(l); d.appendChild(t); out.appendChild(d);
      });
    }
    sa.addEventListener('change', drawCmp); sb2.addEventListener('change', drawCmp); drawCmp();
  }

  /* ---- Walidacja i wysyłka (Web3Forms) ---- */
  function setErr(f, el, msg){
    var fld = $(f), ctl = fld.querySelector('input, select');
    fld.classList.toggle('error', !!msg); $(el).textContent = msg || '';
    if(ctl && ctl.type !== 'hidden'){ if(msg){ ctl.setAttribute('aria-invalid','true'); ctl.setAttribute('aria-describedby', el); } else ctl.removeAttribute('aria-invalid'); }
  }
  function norm(v){ v = v.trim(); if(v && !/^https?:\/\//i.test(v)) v = 'https://' + v; return v; }
  function okMail(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); }
  /* mini-audyt: adres musi być domeną firmy, bez spacji, bez linków logowania, banków, poczty i serwisów znanych z niewłaściwych zgłoszeń */
  /* marki i frazy: dopasowanie jako podciąg; słowa ogólne: tylko jako osobny człon adresu (login.x.com, x.pl/login, ale nie doradcabankowy.pl) */
  var BAD_SUB = ['mcafee','norton','avast','kaspersky','allegro','gmail','facebook.com','instagram.com','google.','wp.pl/poczta','onet.pl/poczta'];
  var BAD_TOK = ['login','signin','logowanie','auth','oauth','eset','bank','olx'];
  var BAD_MAIL = ['mailinator','tempmail','10minutemail','guerrillamail','yopmail'];
  var URL_ERR = 'Wpisz adres strony swojej firmy, np. twojafirma.pl. Sprawdzam strony firm, nie bezpieczeństwo linków.';
  function okCompanyUrl(v){
    v = v.trim();
    if(!v || /\s/.test(v)) return false;
    var low = v.toLowerCase();
    try{ low += ' ' + decodeURIComponent(low); }catch(e){}
    var toks = low.split(/[^a-z0-9]+/);
    if(BAD_SUB.some(function(w){ return low.indexOf(w) !== -1; }) || BAD_TOK.some(function(w){ return toks.indexOf(w) !== -1; })) return false;
    var u; try{ u = new URL(norm(v)); }catch(e){ return false; }
    if(u.protocol !== 'https:' && u.protocol !== 'http:') return false;
    if(u.username || u.password || u.port) return false;
    return /^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,23}$/.test(u.hostname.toLowerCase());
  }
  function throwawayMail(v){ var d = v.trim().toLowerCase().split('@').pop(); return BAD_MAIL.some(function(w){ return d.indexOf(w) !== -1; }); }
  function show(s){ ['sending','ok','fail'].forEach(function(k){ $('r-'+k).hidden = (k !== s); }); }
  function trackData(){
    var track = { strona_zgloszenia: location.pathname, strona_wejscia: sget('wsk_wejscie') || location.pathname };
    UTM.forEach(function(k){ var v = sget('wsk_'+k); if(v) track[k] = v; });
    return track;
  }

  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var u = $('site-url').value, m = $('email').value, good = true;
      var brEl = $('branza'), fcEl = $('firma'), capEl = form.querySelector('textarea[name="h-captcha-response"]');
      var branza = brEl.value, capTok = capEl ? capEl.value : '';
      if(!u.trim()){ setErr('f-url','e-url', URL_ERR); good = false; }
      else if(!okCompanyUrl(u)){ setErr('f-url','e-url', URL_ERR); good = false; }
      else setErr('f-url','e-url','');
      if(!m.trim()){ setErr('f-email','e-email','Podaj adres e-mail.'); good = false; }
      else if(!okMail(m)){ setErr('f-email','e-email','To nie wygląda na adres e-mail.'); good = false; }
      else if(throwawayMail(m)){ setErr('f-email','e-email','Podaj stały adres e-mail, nie jednorazowy.'); good = false; }
      else setErr('f-email','e-email','');
      if(!branza){ setErr('f-branza','e-branza','Wybierz branżę.'); good = false; } else setErr('f-branza','e-branza','');
      if(!fcEl.checked){ setErr('f-firma','e-firma','Zaznacz, że prowadzisz firmę lub odpowiadasz za jej stronę.'); good = false; } else setErr('f-firma','e-firma','');
      if(!capTok){ setErr('f-captcha','e-captcha','Potwierdź, że nie jesteś robotem.'); good = false; } else setErr('f-captcha','e-captcha','');
      if(!good){
        var fe = form.querySelector('.field.error input, .field.error select');
        if(fe) fe.focus(); else { var fc2 = form.querySelector('.field.error'); if(fc2) fc2.scrollIntoView({block:'center'}); }
        return;
      }
      if($('botcheck').checked) return;

      var site = norm(u), mail = m.trim(), tel = $('tel').value.trim(), news = $('newsletter').checked;
      var subject = form.querySelector('[name=subject]').value;
      var track = trackData();
      var trackTxt = Object.keys(track).map(function(k){ return k + ': ' + track[k]; }).join('\n');
      var isMini = (PK[current.id] || PK.mini).tile === 'mini';
      var body = 'Strona: ' + site + '\nE-mail kontaktowy: ' + mail + '\n' + (tel ? 'Telefon: ' + tel + '\n' : '') +
        'Branża: ' + branza + '\nProwadzi firmę lub odpowiada za jej stronę: Tak\nPakiet: ' + current.name + '\n' +
        (news ? 'Newsletter „Wskazówki”: zgoda (tak)\n' : '') + trackTxt + '\n\n' +
        (isMini ? 'Proszę o bezpłatny mini-audyt widoczności AI dla powyższej strony.' : 'Proszę o kontakt w sprawie pakietu: ' + current.name + '.');
      $('mail-link').href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var cb = $('copy-box'); cb.textContent = 'Do: ' + EMAIL + '\nTemat: ' + subject + '\n\n' + body;
      $('copy-btn').onclick = function(){
        var b = this; function done(){ b.textContent = 'Skopiowano'; }
        if(navigator.clipboard) navigator.clipboard.writeText(cb.textContent).then(done, done); else done();
      };

      form.hidden = true; $('result').hidden = false; show('sending');
      var payload = { access_key: KEY, subject: subject, from_name: 'Wskazani — strona', site: site, email: mail, message: body,
        botcheck: $('botcheck').checked, branza: branza, prowadze_firme: 'Tak', pakiet: current.name,
        'h-captcha-response': capTok };
      if(tel) payload.telefon = tel;
      if(news) payload.newsletter = 'tak';
      Object.keys(track).forEach(function(k){ payload[k] = track[k]; });
      fetch('https://api.web3forms.com/submit', {
        method: 'POST', headers: {'Content-Type':'application/json','Accept':'application/json'}, body: JSON.stringify(payload)
      }).then(function(r){ return r.json(); }).then(function(d){
        if(d && d.success === true){
          show('ok'); sset('wsk_lead','audyt'); sset('wsk_pakiet', current.name); if(news) sset('wsk_news','1');
          location.href = '/dziekuje?typ=audyt';
        } else show('fail');
      }).catch(function(){ show('fail'); });
    });
  }

  /* ---- Newsletter „Wskazówki” (sam e-mail). Nigdy nie wywołuje konwersji Google Ads ---- */
  var nf = $('news-form');
  if(nf){
    nf.addEventListener('submit', function(e){
      e.preventDefault();
      var m = $('n-email').value, err = $('n-err');
      if(!okMail(m) || throwawayMail(m)){ err.textContent = 'Podaj poprawny adres e-mail.'; $('n-email').setAttribute('aria-invalid','true'); $('n-email').focus(); return; }
      err.textContent = ''; $('n-email').removeAttribute('aria-invalid');
      if($('n-bot').checked) return;
      var track = trackData(), btn = nf.querySelector('button[type=submit]'); btn.disabled = true;
      var payload = { access_key: KEY, subject: 'Zapis na newsletter „Wskazówki”', from_name: 'Wskazani — strona', email: m.trim(), typ: 'newsletter',
        message: 'Zapis na newsletter „Wskazówki”.\nE-mail: ' + m.trim() + '\nstrona_zgloszenia: ' + location.pathname, botcheck: false };
      Object.keys(track).forEach(function(k){ payload[k] = track[k]; });
      fetch('https://api.web3forms.com/submit', {
        method: 'POST', headers: {'Content-Type':'application/json','Accept':'application/json'}, body: JSON.stringify(payload)
      }).then(function(r){ return r.json(); }).then(function(d){
        if(d && d.success === true){ nf.hidden = true; $('news-ok').hidden = false; ev('newsletter_signup', { zrodlo: 'sekcja_wskazowki' }); }
        else { btn.disabled = false; err.textContent = 'Nie udało się zapisać. Spróbuj jeszcze raz albo napisz na ' + EMAIL + '.'; }
      }).catch(function(){ btn.disabled = false; err.textContent = 'Nie udało się zapisać. Spróbuj jeszcze raz albo napisz na ' + EMAIL + '.'; });
    });
  }

  /* ---- Podziękowanie ---- */
  var thanks = $('thanks');
  if(thanks){
    var typ = new URLSearchParams(location.search).get('typ') || sget('wsk_lead') || 'audyt';
    if(typ === 'checklista'){ $('t-audyt').hidden = true; $('t-check').hidden = false; }
    var pk = sget('wsk_pakiet'); if(pk && $('t-pakiet')){ $('t-pakiet').textContent = 'Wybrany pakiet: ' + pk + '. '; }
    var flag = sget('wsk_lead');
    if(flag){
      sdel('wsk_lead'); sdel('wsk_pakiet');
      /* Google: konwersja Ads tylko dla zgłoszenia na audyt, generate_lead do GA4; raz na zgłoszenie (flaga usunięta powyżej, więc odświeżenie nie dubluje); gtag kolejkuje zdarzenia do czasu załadowania gtag.js */
      if(typeof gtag === 'function'){
        if(flag === 'audyt') gtag('event','conversion',{send_to: GOOGLE_ADS_ID + '/' + GOOGLE_ADS_LABEL});
        gtag('event','generate_lead',{lead_type: flag});
      }
      if(sget('wsk_news')){ sdel('wsk_news'); ev('newsletter_signup', { zrodlo: 'formularz_audytu' }); }
    }
  }
})();
