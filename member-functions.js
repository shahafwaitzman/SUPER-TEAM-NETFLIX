// ===== PAGE NAVIGATION =====
function showPage(pageId) {
  // Hide all pages
  document.querySelectorAll('[id$="Page"]').forEach(p => p.classList.add('hidden'));
  document.getElementById('mainContent').classList.add('hidden');
  
  // Show selected page
  if (pageId === 'main') {
    document.getElementById('mainContent').classList.remove('hidden');
  } else {
    document.getElementById(pageId).classList.remove('hidden');
  }
}

// ===== RENDER MEMBERS GRID =====
function renderMembers() {
  const grid = document.getElementById('membersGrid');
  grid.innerHTML = MEMBERS.map(member => `
    <div style="background: var(--bg-card); border-radius: 12px; padding: 24px; text-align: center; border: 1px solid var(--bg-hover); transition: all 0.3s; cursor: pointer;" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 8px 24px rgba(0,0,0,0.5)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
      <div style="width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, var(--red), var(--gold)); margin: 0 auto 16px; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 900; color: var(--white);">
        ${member.name.charAt(0)}
      </div>
      <h3 style="font-size: 16px; font-weight: 700; color: var(--white); margin-bottom: 8px;">${member.name}</h3>
      <p style="color: var(--text-dim); font-size: 13px; word-break: break-all;">${member.email}</p>
    </div>
  `).join('');
}

// ===== NAV BUTTONS FOR PAGES =====
function addPageButtons() {
  const navRight = document.querySelector('.nav-right');
  const membersBtn = document.createElement('button');
  membersBtn.textContent = '👥 חברים';
  membersBtn.className = 'nav-link';
  membersBtn.style.cssText = 'margin: 0; padding: 4px 12px; background: none; border: none; color: var(--text-dim); font-size: 13px; font-weight: 500; cursor: pointer; transition: color 0.2s;';
  membersBtn.onclick = () => { showPage('membersPage'); membersBtn.style.color = 'var(--white)'; membersBtn.nextElementSibling.style.color = 'var(--text-dim)'; };
  
  const awtBtn = document.createElement('button');
  awtBtn.textContent = '🏢 AWT';
  awtBtn.className = 'nav-link';
  awtBtn.style.cssText = 'margin: 0; padding: 4px 12px; background: none; border: none; color: var(--text-dim); font-size: 13px; font-weight: 500; cursor: pointer; transition: color 0.2s;';
  awtBtn.onclick = () => { showPage('awtPage'); awtBtn.style.color = 'var(--white)'; membersBtn.style.color = 'var(--text-dim)'; };
  
  navRight.insertBefore(awtBtn, navRight.firstChild);
  navRight.insertBefore(membersBtn, navRight.firstChild);
}
