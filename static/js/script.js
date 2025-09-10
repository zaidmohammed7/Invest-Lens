/*
    Team-26
    CS 222
    File - script.js
    Description of the file - JS logic.
*/

let timeoutSeconds = Math.floor(sessionTimeoutMs / 1000);
let inactivitySeconds = 300; // Inactivity timer
let isInactive = false; // Track whether the user is inactive
let inactivityInterval;

// Regular timer function
function updateTimer() {
    const minutes = Math.floor(timeoutSeconds / 60);
    const seconds = timeoutSeconds % 60;
    const timerElement = document.getElementById('timeout-timer');
    if (timerElement) {
        timerElement.textContent = `Timeout: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    if (timeoutSeconds > 0) {
        timeoutSeconds--;
    } else {
        clearInterval(timerInterval);
        alert("Your session has expired. You will be logged out.");
        window.location.href = "/logout"; // Redirect to logout
    }
}

// Inactivity timer function
function updateInactivityTimer() {
    const minutes = Math.floor(inactivitySeconds / 60);
    const seconds = inactivitySeconds % 60;
    const timerElement = document.getElementById('timeout-timer');
    if (timerElement) {
        timerElement.textContent = `Inactivity: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    if (inactivitySeconds > 0) {
        inactivitySeconds--;
    } else {
        clearInterval(inactivityInterval);
        alert("Inactivity timer expired. You will be logged out.");
        window.location.href = "/logout";
    }
}

// Switch to inactivity timer
function startInactivityTimer() {
    isInactive = true;
    clearInterval(timerInterval);
    inactivitySeconds = 300; // Reset inactivity timer
    inactivityInterval = setInterval(updateInactivityTimer, 1000);
}

// Resume regular timer on activity
function resumeRegularTimer() {
    if (isInactive) {
        isInactive = false;
        clearInterval(inactivityInterval); // Stop the inactivity timer
        timerInterval = setInterval(updateTimer, 1000); // Resume the regular timer
    }
}

// Detect user activity
document.addEventListener('mousemove', resumeRegularTimer);
document.addEventListener('keypress', resumeRegularTimer);

// Start regular timer
let timerInterval = setInterval(updateTimer, 1000);

// Detect inactivity
let inactivityTimeout = setTimeout(startInactivityTimer, 10000); // 30 seconds inactivity

function resetInactivityTimeout() {
    clearTimeout(inactivityTimeout);
    inactivityTimeout = setTimeout(startInactivityTimer, 30000);
}

// Reset inactivity timer on activity
document.addEventListener('mousemove', resetInactivityTimeout);
document.addEventListener('keypress', resetInactivityTimeout);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.update-ltp').forEach(button => {
        button.addEventListener('click', () => {
            alert('Update LTP clicked!');
        });
    });

    document.querySelectorAll('.square-off').forEach(button => {
        button.addEventListener('click', () => {
            alert('Square-off clicked!');
        });
    });
});

// Sort table function
function sortTable(columnIndex, isNumeric = false) {
    const table = document.querySelector(".data-table tbody");
    const rows = Array.from(table.rows);

    // Sort rows based on the selected column
    const sortedRows = rows.sort((a, b) => {
        const cellA = a.cells[columnIndex].innerText.trim();
        const cellB = b.cells[columnIndex].innerText.trim();

        if (isNumeric) {
            const numA = parseFloat(cellA.replace(/[+%]/g, ""));
            const numB = parseFloat(cellB.replace(/[+%]/g, ""));
            return numA - numB;
        } else {
            return cellA.localeCompare(cellB);
        }
    });

    table.innerHTML = "";
    sortedRows.forEach(row => table.appendChild(row));
}

// Store original table rows on page load
let originalTableRows = [];

document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector(".data-table tbody");
    if (table) {
        originalTableRows = Array.from(table.rows).map(row => row.cloneNode(true));
    }
});

// Reset table to its original order
function resetTable() {
    const table = document.querySelector(".data-table tbody");
    if (table && originalTableRows.length > 0) {
        table.innerHTML = ""; // Clear current rows
        originalTableRows.forEach(row => table.appendChild(row)); // Restore original rows
    }
}
