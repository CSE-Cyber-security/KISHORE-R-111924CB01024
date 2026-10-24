(() => {
  'use strict';
  const STORAGE_KEY = 'todo-list-application-v1';
  const form = document.getElementById('task-form');
  const input = document.getElementById('task-input');
  const list = document.getElementById('task-list');
  const emptyState = document.getElementById('empty-state');
  const emptyTitle = document.getElementById('empty-title');
  const emptyDescription = document.getElementById('empty-description');
  const error = document.getElementById('form-error');
  const clearCompletedButton = document.getElementById('clear-completed');
  const footerSummary = document.getElementById('footer-summary');
  const toast = document.getElementById('toast');
  const countEls = {
    all: document.getElementById('all-count'),
    pending: document.getElementById('pending-count'),
    completed: document.getElementById('completed-count')
  };
  let tasks = loadTasks();
  let currentFilter = 'all';
  let toastTimer;

  function loadTasks() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      if (!Array.isArray(saved)) return [];
      return saved.filter(t => t && typeof t.id === 'string' && typeof t.text === 'string')
        .map(t => ({ id: t.id, text: t.text.slice(0, 160), completed: Boolean(t.completed), createdAt: Number(t.createdAt) || Date.now() }));
    } catch (e) { return []; }
  }

  function saveTasks() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
      document.querySelector('.save-status').innerHTML = '<span class="status-dot"></span> Saved on this device';
    } catch (e) {
      document.querySelector('.save-status').textContent = 'Storage unavailable';
    }
  }

  function makeId() {
    return (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function icon(type) {
    if (type === 'delete') return '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3m-9 0 1 13h10l1-13M10 11v5m4-5v5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    return '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6.5 12.5 3.5 3.5 7.5-8" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }

  function createTaskElement(task) {
    const item = document.createElement('li');
    item.className = `task-item${task.completed ? ' completed' : ''}`;
    item.dataset.id = task.id;

    const checkbox = document.createElement('input');
    checkbox.className = 'task-check'; checkbox.type = 'checkbox'; checkbox.checked = task.completed;
    checkbox.setAttribute('aria-label', `${task.completed ? 'Mark as pending' : 'Mark as completed'}: ${task.text}`);

    const text = document.createElement('span');
    text.className = 'task-text'; text.textContent = task.text;

    const actions = document.createElement('div'); actions.className = 'task-actions';
    const complete = document.createElement('button');
    complete.type = 'button'; complete.className = 'icon-button complete-button';
    complete.setAttribute('aria-label', task.completed ? `Mark ${task.text} as pending` : `Complete ${task.text}`);
    complete.title = task.completed ? 'Mark as pending' : 'Mark as completed';
    complete.innerHTML = icon('complete');

    const remove = document.createElement('button');
    remove.type = 'button'; remove.className = 'icon-button delete-button';
    remove.setAttribute('aria-label', `Delete ${task.text}`); remove.title = 'Delete task';
    remove.innerHTML = icon('delete');

    checkbox.addEventListener('change', () => toggleTask(task.id));
    complete.addEventListener('click', () => toggleTask(task.id));
    remove.addEventListener('click', () => deleteTask(task.id));
    actions.append(complete, remove);
    item.append(checkbox, text, actions);
    return item;
  }

  function render() {
    const completed = tasks.filter(t => t.completed).length;
    const pending = tasks.length - completed;
    countEls.all.textContent = tasks.length;
    countEls.pending.textContent = pending;
    countEls.completed.textContent = completed;
    clearCompletedButton.hidden = completed === 0;
    footerSummary.textContent = tasks.length === 0 ? 'Small steps make big goals.' : `${pending} pending  |  ${completed} completed`;

    document.querySelectorAll('.filter').forEach(button => {
      const active = button.dataset.filter === currentFilter;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    const visibleTasks = tasks.filter(t => currentFilter === 'all' || (currentFilter === 'pending' && !t.completed) || (currentFilter === 'completed' && t.completed));
    list.replaceChildren(...visibleTasks.map(createTaskElement));
    const showEmpty = visibleTasks.length === 0;
    emptyState.classList.toggle('visible', showEmpty);
    if (showEmpty) {
      if (tasks.length === 0) {
        emptyTitle.textContent = 'Your day, organized.';
        emptyDescription.textContent = 'Add a task above to get started.';
      } else if (currentFilter === 'pending') {
        emptyTitle.textContent = 'All caught up!';
        emptyDescription.textContent = 'There are no pending tasks right now.';
      } else if (currentFilter === 'completed') {
        emptyTitle.textContent = 'Nothing completed yet';
        emptyDescription.textContent = 'Check off a task when you finish it.';
      }
    }
  }

  function showToast(message) {
    toast.textContent = message; toast.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
  }

  function addTask(text) {
    tasks.unshift({ id: makeId(), text, completed: false, createdAt: Date.now() });
    currentFilter = 'all'; saveTasks(); render(); showToast('Task added successfully.');
  }

  function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    task.completed = !task.completed; saveTasks(); render();
    showToast(task.completed ? 'Task marked as completed.' : 'Task moved to pending.');
  }

  function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id); saveTasks(); render(); showToast('Task deleted.');
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) { error.textContent = 'Please enter a task before adding it.'; input.focus(); return; }
    if (tasks.some(t => t.text.toLocaleLowerCase() === text.toLocaleLowerCase() && !t.completed)) {
      error.textContent = 'That pending task already exists.'; input.focus(); return;
    }
    error.textContent = ''; addTask(text); input.value = ''; input.focus();
  });
  input.addEventListener('input', () => { if (error.textContent) error.textContent = ''; });
  document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => { currentFilter = button.dataset.filter; render(); }));
  clearCompletedButton.addEventListener('click', () => {
    const count = tasks.filter(t => t.completed).length;
    if (!count) return;
    tasks = tasks.filter(t => !t.completed); saveTasks(); render(); showToast(`${count} completed task${count === 1 ? '' : 's'} cleared.`);
  });

  render();
})();
