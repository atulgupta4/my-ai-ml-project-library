
const search=document.querySelector('#project-search');
const buttons=[...document.querySelectorAll('[data-filter]')];
const cards=[...document.querySelectorAll('[data-project-card]')];
const empty=document.querySelector('#empty-state');let active='all';
function update(){const q=(search?.value||'').toLowerCase().trim();let count=0;cards.forEach(c=>{const ok=(active==='all'||c.dataset.category===active)&&(!q||c.innerText.toLowerCase().includes(q));c.style.display=ok?'flex':'none';if(ok)count++});if(empty)empty.style.display=count?'none':'block'}
search?.addEventListener('input',update);buttons.forEach(b=>b.addEventListener('click',()=>{active=b.dataset.filter;buttons.forEach(x=>x.classList.toggle('active',x===b));update()}));
