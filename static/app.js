// ==========================================
// Configuration
// ==========================================
const API_URL = "";

// ==========================================
// DOM Elements
// ==========================================
const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("task-title");
const descriptionInput = document.getElementById("task-description");
const tasksContainer = document.getElementById("tasks-container");

// ==========================================
// Render
// ==========================================
function renderTasks(tasks) {
    if (!tasks || tasks.length === 0) {
        tasksContainer.innerHTML = `
            <p class="empty-state">No tasks yet. Add one above! ✨</p>
        `;
        return;
    }

    tasksContainer.innerHTML = tasks.map(task => `
        <div class="task ${task.completed ? 'completed' : ''}">
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                <div class="task-meta">${formatDate(task.created_at)}</div>
            </div>
            <div class="task-actions">
                ${!task.completed ? `
                    <button class="btn-complete" onclick="completeTask(${task.id})">✓</button>
                ` : ''}
                <button class="btn-delete" onclick="deleteTask(${task.id})">✕</button>
            </div>
        </div>
    `).join('');
}

// ==========================================
// Helpers
// ==========================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(isoString) {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// ==========================================
// API Calls
// ==========================================
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error("Error loading tasks:", error);
        tasksContainer.innerHTML = `
            <p class="empty-state">⚠️ Could not connect to server. Is it running?</p>
        `;
    }
}

async function createTask(title, description) {
    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description }),
        });
        if (!response.ok) throw new Error("Failed to create task");
        await loadTasks();
    } catch (error) {
        console.error("Error creating task:", error);
        alert("Could not create task. Check console.");
    }
}

async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}/complete`, {
            method: "PUT",
        });
        if (!response.ok) throw new Error("Failed to complete task");
        await loadTasks();
    } catch (error) {
        console.error("Error completing task:", error);
    }
}

async function deleteTask(taskId) {
    if (!confirm("Delete this task?")) return;
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE",
        });
        if (!response.ok) throw new Error("Failed to delete task");
        await loadTasks();
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

// ==========================================
// Event Listeners
// ==========================================
taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (!title) return;

    await createTask(title, description);

    // پاک کردن فرم
    titleInput.value = "";
    descriptionInput.value = "";
    titleInput.focus();
});

// ==========================================
// Init
// ==========================================
loadTasks();
