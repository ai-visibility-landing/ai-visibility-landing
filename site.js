/* wskazani.pl — wspólny skrypt. Bez bibliotek. Konfiguracja zgody i tagu Google przeniesiona ze starej strony. */
(function(){
  'use strict';

  var EMAIL = 'szmelfilip.business@gmail.com';
  var GOOGLE_ADS_ID = 'AW-18503882283', GOOGLE_ADS_LABEL = 'DfXmCMW3pZkdEKusq_dE', GA4_ID = 'G-ENH7LJ2YW2';

  function $(id){ return document.getElementById(id); }
  function sget(k){ try{ return sessionStorage.getItem(k); }catch(e){ return null; } }
  function sdel(k){ try{ sessionStorage.removeItem(k); }catch(e){} }
  function store(k,v){ try{ if(v===undefined) return localStorage.getItem(k); localStorage.setItem(k,v); }catch(e){ return null; } }

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
    }
  }
})();
