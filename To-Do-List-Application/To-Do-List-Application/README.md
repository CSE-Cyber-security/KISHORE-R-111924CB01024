# To-Do List Application

A responsive task-management web application built with **HTML, CSS, and vanilla JavaScript**. It allows users to add tasks, mark them as completed, delete them, filter the task list, and keep tasks saved between visits using the browser's `localStorage`.

## Features

- Add new tasks with input validation.
- Mark tasks as completed or return them to pending.
- Delete individual tasks.
- Filter by **All**, **Pending**, and **Completed**.
- View live counts for each task category.
- Clear all completed tasks at once.
- Automatically save tasks in the current browser.
- Responsive layout for desktop, tablet, and mobile screens.
- Accessible labels, keyboard focus indicators, and reduced-motion support.
- Prevents duplicate pending task names (case-insensitive).

## Project files

```text
To-Do-List-Application/
├── index.html       # Page structure and task-manager interface
├── style.css        # Responsive styling and visual design
├── script.js        # Task operations, filters, and local storage
├── README.md        # Project documentation
└── .gitignore       # Files excluded from Git
```

## How to run

1. Download or clone this repository.
2. Open `index.html` in a modern web browser.
3. Enter a task in the input field and select **Add Task** (or press Enter).
4. Use the checkbox or green check button to change a task's completion status.
5. Use the red delete button to remove a task, and the filter buttons to view task categories.

No build tools, server, or package installation are required. For a development workflow, open the folder in Visual Studio Code and use the **Live Server** extension to serve `index.html` locally.

## Data storage

Tasks are stored in the browser's local storage under the key `todo-list-application-v1`. They remain available in the same browser on the same device after refreshing or reopening the page. Clearing the browser's site data or using a different browser/device can remove or hide the saved tasks. This is a front-end demonstration; it does not use a remote database or user accounts.

## GitHub submission

1. Sign in to GitHub and create a public repository named `To-Do-List-Application`.
2. Upload `index.html`, `style.css`, `script.js`, `README.md`, and `.gitignore`.
3. To publish it, open **Settings → Pages**, select the `main` branch and `/ (root)` folder, and save. Wait for GitHub Pages to provide the published site URL.
4. Open the published site, test the features, and capture screenshots for the submission.

## Test checklist

- [ ] Add a task using the button and Enter key.
- [ ] Try submitting an empty task and confirm validation appears.
- [ ] Try adding a duplicate pending task and confirm it is prevented.
- [ ] Complete a task and verify the counters and filters update.
- [ ] Return a completed task to pending.
- [ ] Delete a task.
- [ ] Clear completed tasks.
- [ ] Refresh the page and verify tasks persist.
- [ ] Test the layout on a narrow/mobile screen.

## Technologies used

- **HTML5** for semantic page structure.
- **CSS3** for responsive layout, states, and styling.
- **JavaScript (ES6+)** for DOM manipulation and task logic.
- **Web Storage API** (`localStorage`) for persistence.
- **Git and GitHub** for version control and submission.
