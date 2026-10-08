/* Reading controls only: examples are never executed. */
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  // Footnotes stay in the current document, including local previews whose
  // origin differs from the configured public site URL.
  document.querySelectorAll('main a.footnote-ref, main a.footnote-back').forEach(link => {
    const target = new URL(link.href, location.href);
    if (target.origin === location.origin && target.pathname === location.pathname && target.search === location.search && target.hash) {
      link.setAttribute('href', target.hash);
      link.removeAttribute('target');
    }
  });
  const shade = document.querySelector('.book-shade');
  const sidebar = document.querySelector('#quarto-sidebar');
  const menu = sidebar?.querySelector('.sidebar-menu-container');
  const chapter = sidebar?.querySelector('[data-current-chapter]');
  const sectionLinks = [...(chapter?.querySelectorAll('[data-book-target]') || [])];
  const locations = sectionLinks.map(link => ({link, target:document.getElementById(link.dataset.bookTarget)})).filter(item => item.target);
  const manuallyClosed = new Set();
  let currentLink = null;
  // Native details also work without JavaScript. Keep links and disclosure
  // clicks separate, and do not undo a reader's explicit collapse on scroll.
  sidebar?.querySelectorAll('summary').forEach(summary => {
    summary.addEventListener('click', event => {
      if (event.target.closest('a')) return;
      const details = summary.parentElement;
      if (details.open) manuallyClosed.add(details); else manuallyClosed.delete(details);
    });
  });
  function expandLocation(link, force = false) {
    for (let parent = link?.parentElement; parent && parent !== sidebar; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS' && (force || !manuallyClosed.has(parent))) {
        parent.open = true;
        if (force) manuallyClosed.delete(parent);
      }
    }
  }
  function keepLocationVisible(link) {
    if (!menu || !link?.getClientRects().length || !menu.getClientRects().length) return;
    const item = link.getBoundingClientRect(), box = menu.getBoundingClientRect();
    if (item.top < box.top + 12) menu.scrollTop += item.top - box.top - 12;
    else if (item.bottom > box.bottom - 12) menu.scrollTop += item.bottom - box.bottom + 12;
  }
  function markLocation(link, force = false) {
    if (link !== currentLink) {
      sectionLinks.forEach(item => { item.classList.remove('is-active', 'is-active-parent'); item.removeAttribute('aria-current'); });
      currentLink = link;
      if (link) {
        link.classList.add('is-active'); link.setAttribute('aria-current', 'location');
        const group = link.closest('.book-section');
        const parentLink = group?.querySelector(':scope > summary > a');
        if (parentLink && parentLink !== link) parentLink.classList.add('is-active-parent');
        expandLocation(link);
        // Update the marker while readers browse the menu without moving it.
        if (!sidebar.matches(':hover') && !sidebar.contains(document.activeElement)) keepLocationVisible(link);
      }
    }
    if (force) { expandLocation(link, true); keepLocationVisible(link); }
  }
  function locateHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return null; }
    let target = document.getElementById(id);
    while (target && target !== document.body) {
      const match = locations.find(item => item.target === target);
      if (match) return match.link;
      target = target.parentElement;
    }
    return null;
  }
  let pendingScroll = false;
  let followingLink = false;
  let scrollEndTimer;
  function finishLinkScroll() {
    followingLink = false;
    updateLocation();
  }
  function followLocation(link) {
    if (!link) { updateLocation(); return; }
    followingLink = true;
    markLocation(link, true);
    clearTimeout(scrollEndTimer);
    scrollEndTimer = setTimeout(finishLinkScroll, 1200);
  }
  function updateLocation() {
    pendingScroll = false;
    let active = null;
    for (const item of locations) {
      if (item.target.getBoundingClientRect().top <= 130) active = item.link;
      else break;
    }
    markLocation(active);
  }
  function scheduleLocation() {
    // A long smooth jump should not expand every section passed on the way.
    if (followingLink) {
      clearTimeout(scrollEndTimer);
      scrollEndTimer = setTimeout(finishLinkScroll, 150);
      return;
    }
    if (!pendingScroll) { pendingScroll = true; requestAnimationFrame(updateLocation); }
  }
  window.addEventListener('scroll', scheduleLocation, {passive:true});
  window.addEventListener('hashchange', () => followLocation(locateHash()));
  window.addEventListener('pageshow', () => { updateLocation(); if (location.hash) followLocation(locateHash()); });
  window.addEventListener('load', () => { updateLocation(); if (location.hash) followLocation(locateHash()); });
  document.fonts?.ready.then(scheduleLocation);
  updateLocation();
  if (location.hash) followLocation(locateHash());
  else keepLocationVisible(sidebar?.querySelector('[aria-current="page"]'));
  sectionLinks.forEach(link => link.addEventListener('click', () => followLocation(link)));
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
  document.querySelectorAll('.book-menu-button').forEach(trigger => {
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
      if (currentLink) markLocation(currentLink, true);
      else {
        const currentChapter = sidebar.querySelector('[aria-current="page"]');
        expandLocation(currentChapter, true); keepLocationVisible(currentChapter);
      }
    });
    panel.addEventListener('click', event => { if (event.target.closest('a[href]')) closeDrawer(); });
  });
  shade?.addEventListener('click', closeDrawer);
  window.addEventListener('resize', closeDrawer);
  document.addEventListener('keydown', event => {
    if (!activeDrawer) return;
    if (event.key === 'Escape') { event.preventDefault(); closeDrawer(); }
    if (event.key === 'Tab') {
      const items = [...activeDrawer.querySelectorAll('a[href],button,input,summary,[tabindex="0"]')].filter(el => {
        if (!el.getClientRects().length || getComputedStyle(el).visibility === 'hidden') return false;
        for (let parent = el.parentElement; parent && parent !== activeDrawer; parent = parent.parentElement) {
          if (parent.tagName === 'DETAILS' && !parent.open && !parent.querySelector(':scope > summary')?.contains(el)) return false;
        }
        return true;
      });
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
