/* Reading controls only: examples are never executed. */
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const shade = document.querySelector('.book-shade');
  const toc = document.querySelector('#quarto-margin-sidebar');
  if (!toc?.querySelector('#TOC')) body.classList.add('book-no-toc');
  let activeDrawer = null;
  let drawerTrigger = null;
  function closeDrawer() {
    if (!activeDrawer) return;
    activeDrawer.classList.remove('book-drawer');
    activeDrawer.removeAttribute('aria-modal');
    activeDrawer.removeAttribute('role');
    drawerTrigger?.setAttribute('aria-expanded', 'false');
    body.classList.remove('book-drawer-open');
    shade.hidden = true;
    activeDrawer = null;
    drawerTrigger?.focus();
  }
  document.querySelectorAll('.book-chapters-button, .book-toc-button').forEach(trigger => {
    const panel = document.getElementById(trigger.getAttribute('aria-controls'));
    if (!panel) return;
    const close = document.createElement('button');
    close.type = 'button'; close.className = 'drawer-close'; close.textContent = '关闭目录';
    close.addEventListener('click', closeDrawer); panel.prepend(close);
    trigger.addEventListener('click', () => {
      const same = activeDrawer === panel; closeDrawer(); if (same) return;
      activeDrawer = panel; drawerTrigger = trigger;
      panel.classList.add('book-drawer'); panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true'); panel.setAttribute('aria-label', trigger.textContent);
      trigger.setAttribute('aria-expanded', 'true'); body.classList.add('book-drawer-open');
      shade.hidden = false; close.focus();
    });
    panel.addEventListener('click', event => { if (event.target.closest('a[href]')) closeDrawer(); });
  });
  shade?.addEventListener('click', closeDrawer);
  window.addEventListener('resize', closeDrawer);
  document.addEventListener('keydown', event => {
    if (!activeDrawer) return;
    if (event.key === 'Escape') { event.preventDefault(); closeDrawer(); }
    if (event.key === 'Tab') {
      const items = [...activeDrawer.querySelectorAll('a[href],button,input,[tabindex="0"]')].filter(el => el.getClientRects().length);
      const first = items[0], last = items.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  document.querySelector('.book-search-button')?.addEventListener('click', () => { closeDrawer(); window.quartoOpenSearch?.(); });
  const names = {bash:'Bash / Shell', sh:'Shell', r:'R', python:'Python', julia:'Julia', powershell:'PowerShell', json:'JSON', yaml:'YAML', perl:'Perl'};
  function button(label, action) {
    const el = document.createElement('button'); el.type = 'button'; el.textContent = label;
    el.addEventListener('click', action); return el;
  }
  async function copyText(raw, status) {
    try {
      if (navigator.clipboard) await navigator.clipboard.writeText(raw);
      else {
        const field = document.createElement('textarea'); field.value = raw; field.style.position = 'fixed'; field.style.opacity = '0';
        document.body.append(field); field.select(); const ok = document.execCommand('copy'); field.remove();
        if (!ok) throw new Error('copy');
      }
      status.textContent = '已复制';
    } catch { status.textContent = '复制失败，请选中代码复制'; }
  }
  document.querySelectorAll('main pre').forEach(pre => {
    if (pre.closest('.code-panel')) return;
    const code = pre.querySelector('code'); if (!code) return;
    const source = pre.parentElement.classList.contains('sourceCode') ? pre.parentElement : pre;
    const role = pre.dataset.bookRole || source.dataset.bookRole || 'code';
    const language = [...code.classList, ...pre.classList].find(c => names[c]);
    const label = pre.dataset.codeTitle || source.dataset.codeTitle || ({output:'输出',data:'数据 / 文本',pseudocode:'伪代码'}[role] || names[language] || '代码');
    const raw = pre.dataset.codeText ? JSON.parse(pre.dataset.codeText) : code.textContent;
    const focus = (pre.dataset.focusLines || source.dataset.focusLines || '').split(',').map(Number);
    [...code.children].forEach((line, index) => { if (focus.includes(index + 1)) line.classList.add('book-focus-line'); });
    const panel = document.createElement('div'); panel.className = `code-panel book-${role}`;
    const toolbar = document.createElement('div'); toolbar.className = 'code-toolbar';
    const title = document.createElement('span'); title.className = 'code-label'; title.textContent = label;
    const status = document.createElement('span'); status.className = 'copy-status'; status.setAttribute('aria-live', 'polite');
    toolbar.append(title, status, button('复制', () => copyText(raw, status)));
    const viewport = document.createElement('div'); viewport.className = 'code-viewport'; viewport.tabIndex = 0;
    viewport.setAttribute('role', 'region'); viewport.setAttribute('aria-label', `${label}，可横向滚动`);
    source.replaceWith(panel); viewport.append(source); panel.append(toolbar, viewport);
    const expand = button('展开代码', () => {
      const dialog = document.createElement('dialog'); dialog.className = `code-dialog code-panel book-${role}`; dialog.setAttribute('aria-label', label);
      const header = document.createElement('div'); header.className = 'code-toolbar';
      const name = title.cloneNode(true), copied = status.cloneNode(false); copied.textContent = '';
      header.append(name, copied, button('复制', () => copyText(raw, copied)), button('关闭', () => dialog.close()));
      const content = viewport.cloneNode(true);
      content.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      content.querySelectorAll('a[href^="#cb"]').forEach(el => el.removeAttribute('href'));
      dialog.append(header, content); document.body.append(dialog);
      dialog.addEventListener('close', () => { dialog.remove(); expand.focus(); }); dialog.showModal();
    }); toolbar.append(expand);
  });
});
