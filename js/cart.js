(() => {
  if (document.documentElement.dataset.cartInitialized) {
    return;
  }
  document.documentElement.dataset.cartInitialized = 'true';

  const script = document.querySelector('script[data-cart-catalog]');
  const cartLink = document.querySelector('[data-cart-link]');
  const badge = document.querySelector('[data-cart-count]');
  const feedback = document.querySelector('[data-cart-feedback]');
  const cartPage = document.querySelector('[data-cart-page]');
  const itemTemplate = document.querySelector('#cart-item-template');
  const storageKey = 'voila-fragrances.cart.v1';
  const maxQuantity = 99;

  if (!script || !cartLink || !badge) {
    return;
  }

  const siteRoot = new URL(script.dataset.cartRoot || './', document.baseURI);
  const locale = document.documentElement.lang || 'tr';
  const productPrefix = locale === 'tr' ? 'products/' : `${locale}/products/`;
  const wholeFormatter = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
  const decimalSeparator = new Intl.NumberFormat(locale, { minimumFractionDigits: 1 })
    .formatToParts(1).find((part) => part.type === 'decimal').value;
  const currencyParts = new Intl.NumberFormat(locale, {
    style: 'currency', currency: 'TRY',
  }).formatToParts(0);
  const currencySymbol = currencyParts.find((part) => part.type === 'currency').value;
  const currencyBefore = currencyParts.findIndex((part) => part.type === 'currency') <
    currencyParts.findIndex((part) => part.type === 'integer');

  let storage = null;
  let products = new Map();
  let items = [];
  let feedbackTimer;

  function formatMinorUnits(minorUnits) {
    const whole = minorUnits / 100n;
    const fraction = minorUnits % 100n;
    const decimals = fraction === 0n ? '' :
      `${decimalSeparator}${fraction.toString().padStart(2, '0')}`;
    const number = `${wholeFormatter.format(whole)}${decimals}`;
    return currencyBefore ? `${currencySymbol} ${number}` : `${number} ${currencySymbol}`;
  }

  function getStorage() {
    try {
      const candidate = window.localStorage;
      const probe = `${storageKey}.probe`;
      candidate.setItem(probe, '1');
      candidate.removeItem(probe);
      return candidate;
    } catch {
      return null;
    }
  }

  function validatePublicCatalog(data) {
    if (!data || data.schema_version !== 1 || data.locale !== locale ||
        !Array.isArray(data.products)) {
      throw new Error('Invalid public catalog');
    }
    const validated = new Map();
    for (const product of data.products) {
      if (!product || typeof product.id !== 'string' ||
          !/^[a-z][a-z0-9-]*$/.test(product.id) ||
          typeof product.name !== 'string' || !product.name.trim() ||
          typeof product.url !== 'string' ||
          !product.url.startsWith(productPrefix) ||
          !/^[a-z0-9]+(?:-[a-z0-9]+)*\/$/.test(product.url.slice(productPrefix.length)) ||
          typeof product.image !== 'string' ||
          !/^assets\/images\/.+\.(?:webp|png|jpe?g)$/i.test(product.image) ||
          /[\\?#\u0000-\u001f]/.test(product.image) ||
          product.image.split('/').some((part) => !part || part === '.' || part === '..') ||
          validated.has(product.id)) {
        throw new Error('Invalid public product');
      }
      if ('price_minor' in product &&
          (!Number.isSafeInteger(product.price_minor) || product.price_minor < 0 ||
           product.currency !== 'TRY')) {
        throw new Error('Invalid public price');
      }
      validated.set(product.id, product);
    }
    return validated;
  }

  function normalizeItems(raw) {
    if (!raw || raw.version !== 1 || !Array.isArray(raw.items)) {
      return [];
    }
    const merged = new Map();
    for (const entry of raw.items) {
      if (!entry || typeof entry.id !== 'string' || !products.has(entry.id) ||
          !Number.isSafeInteger(entry.quantity) || entry.quantity < 1) {
        continue;
      }
      const quantity = Math.min(maxQuantity, entry.quantity);
      merged.set(entry.id, Math.min(maxQuantity, (merged.get(entry.id) || 0) + quantity));
    }
    return [...merged].map(([id, quantity]) => ({ id, quantity }));
  }

  function readItems() {
    let raw;
    try {
      raw = storage.getItem(storageKey);
    } catch {
      storage = null;
      return [];
    }
    if (!raw) {
      return [];
    }
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch {
      parsed = null;
    }
    const cleaned = normalizeItems(parsed);
    const canonical = JSON.stringify({ version: 1, items: cleaned });
    if (raw !== canonical) {
      try {
        storage.setItem(storageKey, canonical);
      } catch {
        storage = null;
      }
    }
    return cleaned;
  }

  function saveItems(next) {
    if (!storage) {
      return false;
    }
    try {
      storage.setItem(storageKey, JSON.stringify({ version: 1, items: next }));
      items = next;
      updateBadge();
      syncAddButtons();
      renderCart();
      return true;
    } catch {
      storage = null;
      disableCart();
      return false;
    }
  }

  function updateBadge() {
    const count = items.reduce((total, item) => total + item.quantity, 0);
    badge.textContent = String(count);
    badge.hidden = count === 0;
    cartLink.setAttribute('aria-label', `${cartLink.dataset.cartLabel}: ${count}`);
  }

  function syncAddButtons() {
    document.querySelectorAll('[data-cart-add]').forEach((button) => {
      const item = items.find((entry) => entry.id === button.dataset.cartAdd);
      button.disabled = !storage || !products.has(button.dataset.cartAdd) ||
        (item && item.quantity >= maxQuantity);
    });
  }

  function showFeedback(kind) {
    if (!feedback) {
      return;
    }
    clearTimeout(feedbackTimer);
    feedback.hidden = false;
    feedback.textContent = kind === 'added' ? feedback.dataset.addedText :
      feedback.dataset.unavailableText;
    feedbackTimer = setTimeout(() => {
      feedback.hidden = true;
    }, 3500);
  }

  function showPageError(selector) {
    if (!cartPage) {
      return;
    }
    cartPage.querySelector('[data-cart-loading]').hidden = true;
    cartPage.querySelector(selector).hidden = false;
  }

  function disableCart() {
    document.querySelectorAll('[data-cart-add]').forEach((button) => {
      button.disabled = true;
    });
    items = [];
    updateBadge();
    showPageError('[data-cart-storage-error]');
  }

  function fillItem(node, product, quantity) {
    const url = new URL(product.url, siteRoot).href;
    const imageLink = node.querySelector('[data-item-image-link]');
    const nameLink = node.querySelector('[data-item-name-link]');
    imageLink.href = url;
    nameLink.href = url;
    nameLink.textContent = product.name;
    const image = node.querySelector('[data-item-image]');
    image.src = new URL(product.image, siteRoot).href;
    image.alt = product.name;
    node.querySelector('[data-item-quantity]').textContent = String(quantity);
    const decrease = node.querySelector('[data-item-decrease]');
    const increase = node.querySelector('[data-item-increase]');
    const remove = node.querySelector('[data-item-remove]');
    decrease.disabled = quantity === 1;
    increase.disabled = quantity === maxQuantity;
    decrease.setAttribute('aria-label', `${cartPage.dataset.decreaseLabel} ${product.name}`);
    increase.setAttribute('aria-label', `${cartPage.dataset.increaseLabel} ${product.name}`);
    remove.setAttribute('aria-label', `${cartPage.dataset.removeLabel} ${product.name}`);
    node.dataset.productId = product.id;

    const unit = node.querySelector('[data-item-unit-price]');
    const total = node.querySelector('[data-item-total]');
    if ('price_minor' in product) {
      unit.textContent = `${cartPage.dataset.unitPriceLabel} ` +
        formatMinorUnits(BigInt(product.price_minor));
      total.textContent = `${cartPage.dataset.lineTotalLabel} ` +
        formatMinorUnits(BigInt(product.price_minor) * BigInt(quantity));
    } else {
      unit.textContent = cartPage.dataset.priceMissingLabel;
      total.textContent = cartPage.dataset.priceMissingLabel;
    }
  }

  function renderCart() {
    if (!cartPage || !storage || !itemTemplate) {
      return;
    }
    cartPage.querySelector('[data-cart-loading]').hidden = true;
    const empty = cartPage.querySelector('[data-cart-empty]');
    const content = cartPage.querySelector('[data-cart-content]');
    empty.hidden = items.length !== 0;
    content.hidden = items.length === 0;
    if (!items.length) {
      return;
    }

    const list = cartPage.querySelector('[data-cart-items]');
    const fragment = document.createDocumentFragment();
    let subtotal = 0n;
    let complete = true;
    for (const item of items) {
      const product = products.get(item.id);
      const node = itemTemplate.content.firstElementChild.cloneNode(true);
      fillItem(node, product, item.quantity);
      fragment.append(node);
      if ('price_minor' in product) {
        subtotal += BigInt(product.price_minor) * BigInt(item.quantity);
      } else {
        complete = false;
      }
    }
    list.replaceChildren(fragment);
    cartPage.querySelector('[data-cart-subtotal]').textContent = complete ?
      formatMinorUnits(subtotal) : cartPage.dataset.subtotalMissingLabel;
    cartPage.querySelector('[data-cart-subtotal-note]').hidden = complete;
  }

  function changeQuantity(id, delta) {
    const next = items.map((item) => item.id === id ? {
      id, quantity: Math.max(1, Math.min(maxQuantity, item.quantity + delta)),
    } : item);
    saveItems(next);
  }

  function handleClick(event) {
    const add = event.target.closest('[data-cart-add]');
    if (add && !add.disabled && products.has(add.dataset.cartAdd)) {
      const id = add.dataset.cartAdd;
      const existing = items.find((item) => item.id === id);
      const next = existing ? items.map((item) => item.id === id ? {
        id, quantity: Math.min(maxQuantity, item.quantity + 1),
      } : item) : [...items, { id, quantity: 1 }];
      showFeedback(saveItems(next) ? 'added' : 'unavailable');
      return;
    }
    const row = event.target.closest('.cart-item[data-product-id]');
    if (row) {
      const id = row.dataset.productId;
      if (event.target.closest('[data-item-increase]')) {
        changeQuantity(id, 1);
      } else if (event.target.closest('[data-item-decrease]')) {
        changeQuantity(id, -1);
      } else if (event.target.closest('[data-item-remove]')) {
        saveItems(items.filter((item) => item.id !== id));
      }
      return;
    }
    if (event.target.closest('[data-cart-clear]')) {
      saveItems([]);
    }
  }

  async function initialize() {
    storage = getStorage();
    if (!storage) {
      disableCart();
      return;
    }
    try {
      const response = await fetch(script.dataset.cartCatalog, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error('Public catalog unavailable');
      }
      products = validatePublicCatalog(await response.json());
    } catch {
      showPageError('[data-cart-error]');
      return;
    }
    items = readItems();
    if (!storage) {
      disableCart();
      return;
    }
    syncAddButtons();
    updateBadge();
    renderCart();
    document.addEventListener('click', handleClick);
    window.addEventListener('storage', (event) => {
      if (event.key === storageKey && storage) {
        items = readItems();
        if (storage) {
          updateBadge();
          syncAddButtons();
          renderCart();
        } else {
          disableCart();
        }
      }
    });
  }

  initialize().catch(() => {
    showPageError('[data-cart-error]');
  });
})();
