(()=>{
 const root=document.documentElement, key='design-document-color-mode', system=matchMedia('(prefers-color-scheme: dark)');
 let saved;try{saved=localStorage.getItem(key)}catch(_){}
 const button=document.querySelector('#themeToggle');
 function apply(mode){root.dataset.theme=mode;button?.setAttribute('aria-label',mode==='dark'?'밝은 화면으로 전환':'어두운 화면으로 전환');button?.setAttribute('title',mode==='dark'?'밝은 화면으로 전환':'어두운 화면으로 전환');}
 apply(saved==='light'||saved==='dark'?saved:system.matches?'dark':'light');
 button?.addEventListener('click',()=>{saved=root.dataset.theme==='dark'?'light':'dark';apply(saved);try{localStorage.setItem(key,saved)}catch(_){}});
 system.addEventListener('change',e=>{if(saved!=='light'&&saved!=='dark')apply(e.matches?'dark':'light')});
 const toggle=document.querySelector('#tocToggle'),nav=document.querySelector('.sidebar'),backdrop=document.querySelector('.toc-backdrop');
 function menu(open,focus=false){document.body.classList.toggle('toc-open',open);toggle?.setAttribute('aria-expanded',String(open));toggle?.setAttribute('aria-label',open?'목차 닫기':'목차 열기');if(innerWidth<=1180&&nav)nav.inert=!open;if(focus)toggle?.focus();}
 toggle?.addEventListener('click',()=>menu(!document.body.classList.contains('toc-open')));
 backdrop?.addEventListener('click',()=>menu(false,true));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('toc-open'))menu(false,true)});
 const links=[...document.querySelectorAll('.sidebar nav a')];
 links.forEach(a=>a.addEventListener('click',()=>{menu(false);const target=document.getElementById(a.hash.slice(1));if(innerWidth<=1180&&target){target.tabIndex=-1;target.focus({preventScroll:true})}}));
 matchMedia('(max-width:1180px)').addEventListener('change',()=>{menu(false);if(nav)nav.inert=innerWidth<=1180});menu(false);if(nav&&innerWidth>1180)nav.inert=false;
 const observer=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){links.forEach(a=>a.removeAttribute('aria-current'));links.find(a=>a.hash==='#'+e.target.id)?.setAttribute('aria-current','true')}})},{rootMargin:'-10% 0px -70% 0px'});
 links.forEach(a=>{const target=document.getElementById(a.hash.slice(1));if(target)observer.observe(target)});
})();
