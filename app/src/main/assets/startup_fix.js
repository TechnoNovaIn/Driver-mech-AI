(function(){
  'use strict';
  // Mahindra BSVI Driver Guide AI — Safe startup orchestrator
  // Ensures driver troubleshooting features are active and never hidden
  function ensureDriverGuideVisible(){
    try{
      var u = (function(){try{return JSON.parse(localStorage.getItem('mahindra_secure_user_v1')||'null');}catch(e){return null;}})();
      var tok = localStorage.getItem('mahindra_secure_token_v1');
      var role = String(u?.role||'').toUpperCase();
      if(tok && u && (role==='ADMIN'||role==='EMPLOYEE'||role==='MECHANIC')){
        if(typeof window.maDashboard === 'function'){
          window.maDashboard();
          return;
        }
      }
      var screen = document.getElementById('screen');
      if(screen && !screen.classList.contains('hide') && screen.innerHTML.trim()){
        return;
      }
      var home = document.getElementById('home');
      var topIntro = document.getElementById('topIntro');
      var langPanel = document.getElementById('languagePanel');
      if(home) home.classList.remove('hide');
      if(topIntro) topIntro.classList.remove('hide');
      if(langPanel) langPanel.classList.remove('hide');
      if(screen && !screen.innerHTML.trim()) screen.classList.add('hide');
    }catch(e){}
  }

  if(document.readyState === 'complete'){
    ensureDriverGuideVisible();
  } else {
    window.addEventListener('load', ensureDriverGuideVisible);
  }
  setTimeout(ensureDriverGuideVisible, 100);
  setTimeout(ensureDriverGuideVisible, 300);
  setTimeout(ensureDriverGuideVisible, 800);
})();
