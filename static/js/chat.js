document.addEventListener("DOMContentLoaded", () => {
    console.log("JS loaded!"); // test

// Get DOM elements

let selectedFiles = [];
const filePreviewContainer = document.getElementById("file-preview-container");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const dictateBtn = document.getElementById("dictate-btn");
const chatMessages = document.getElementById("chat-messages");
const chatHistory = document.getElementById("chat-history");
const uploadImage = document.getElementById("upload-image");
const uploadPdf = document.getElementById("upload-pdf");
const newChatBtn = document.getElementById("new-chat-btn");
const historySearchInput = document.getElementById("history-search-input");
const clearSearchBtn = document.getElementById("clear-search-btn");


if (newChatBtn) {
    newChatBtn.addEventListener("click", () => {
        window.location.href = `/chat?username=${USERNAME}`;
    });
}

function handleFiles(files) {
    for (let file of files) {
        selectedFiles.push(file);
        renderFilePreview(file);
    }
}

uploadImage.addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

uploadPdf.addEventListener("change", (e) => {
    handleFiles(e.target.files);
});
function renderFilePreview(file) {
    const div = document.createElement("div");
    div.classList.add("file-preview");

    div.innerHTML = `
        <span>${file.name}</span>
        <button class="remove-file">❌</button>
    `;

    div.querySelector(".remove-file").addEventListener("click", () => {
        selectedFiles = selectedFiles.filter(f => f !== file);
        div.remove();
    });

    filePreviewContainer.appendChild(div);
}


// Send message on button click or Enter key
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});
let selectedLanguage = "English";

const langToggle = document.getElementById("lang-toggle");
const langMenu = document.getElementById("lang-menu");

if (langToggle && langMenu) {

    // Toggle dropdown
    langToggle.addEventListener("click", (e) => {
        e.stopPropagation();
        langMenu.classList.toggle("hidden");
    });

    // Select language
    langMenu.querySelectorAll("div").forEach(option => {

        option.addEventListener("click", () => {

            selectedLanguage = option.dataset.lang;
            langToggle.textContent = option.dataset.symbol;

            langMenu.classList.add("hidden");

            console.log("Language selected:", selectedLanguage);
        });

    });

    // Close when clicking outside
    document.addEventListener("click", () => {
        langMenu.classList.add("hidden");
    });

}


function showThinking() {
    removeThinking(); // prevent duplicates

    const thinking = document.createElement("div");
    thinking.id = "thinking-indicator";
    thinking.style.fontSize = "14px";
    thinking.style.color = "gray";
    thinking.style.margin = "6px 0";
    thinking.textContent = "🤖 FinSavvy AI is thinking...";

    chatMessages.appendChild(thinking);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
function removeThinking() {
    const thinking = document.getElementById("thinking-indicator");
    if (thinking) thinking.remove();
}


// Append message to chat
function appendMessage(sender, text) {
    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    if (sender === "bot") {
        msgDiv.innerHTML = marked.parse(text);
    } else {
        msgDiv.textContent = text;
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function loadSessions() {
    console.log("Loading sessions...");

    fetch(`/sessions?username=${USERNAME}`)
        .then(res => res.json())
        .then(data => {
            chatHistory.innerHTML = "";

            data.sessions.forEach(session => {

                const li = document.createElement("li");
                li.classList.add("session-item");

                li.innerHTML = `
                    <span class="session-title">
                        ${session.title || "New Conversation"}
                    </span>
                    <div class="session-menu">
                        <button class="menu-btn">
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                        </button>
                        <div class="menu-dropdown hidden">
                            <button class="rename-btn">Rename</button>
                            <button class="delete-btn">Delete</button>
                        </div>
                    </div>
                `;

                const titleSpan = li.querySelector(".session-title");
                const menuBtn = li.querySelector(".menu-btn");
                const dropdown = li.querySelector(".menu-dropdown");
                const renameBtn = li.querySelector(".rename-btn");
                const deleteBtn = li.querySelector(".delete-btn");

                // ---------------- Open Chat ----------------
                titleSpan.addEventListener("click", () => {
                    window.location.href =
                        `/chat?username=${USERNAME}&session_id=${session.id}`;
                });

                // ---------------- Toggle Menu ----------------
                menuBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    dropdown.classList.toggle("hidden");
                });

                // ---------------- Inline Rename ----------------
                renameBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    dropdown.classList.add("hidden");

                    const currentTitle = titleSpan.textContent;

                    // Create input
                    const input = document.createElement("input");
                    input.type = "text";
                    input.value = currentTitle;
                    input.classList.add("rename-input"); 
                    
                    titleSpan.replaceWith(input);
                    input.focus();
                    input.select();

                    // Save on Enter
                    input.addEventListener("keydown", async (event) => {
                        if (event.key === "Enter") {

                            const newTitle = input.value.trim();
                            if (!newTitle) return;

                            await fetch("/rename_session", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify({
                                    session_id: session.id,
                                    title: newTitle
                                })
                            });

                            loadSessions();
                        }

                        // Cancel on ESC
                        if (event.key === "Escape") {
                            loadSessions();
                        }
                    });

                    // Save on blur (click outside)
                    input.addEventListener("blur", async () => {
                        const newTitle = input.value.trim();
                        if (!newTitle) {
                            loadSessions();
                            return;
                        }

                        await fetch("/rename_session", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                session_id: session.id,
                                title: newTitle
                            })
                        });

                        loadSessions();
                    });
                });

                // ---------------- Delete ----------------
                deleteBtn.addEventListener("click", async (e) => {
                    e.stopPropagation();

                    if (!confirm("Delete this chat permanently?")) return;

                    await fetch("/delete_session", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            session_id: session.id
                        })
                    });

                    loadSessions();
                });

                chatHistory.appendChild(li);
            });
        });
}

loadSessions();

if (historySearchInput) {
    historySearchInput.addEventListener("input", () => {
        const searchValue = historySearchInput.value.toLowerCase();

        const sessions = document.querySelectorAll(".session-item");

        sessions.forEach(session => {
            const title = session
                .querySelector(".session-title")
                .textContent
                .toLowerCase();

            if (title.includes(searchValue)) {
                session.style.display = "flex";
            } else {
                session.style.display = "none";
            }
        });
    });
}

// Load previous chat messages (FIX FORMATTING)
CHAT_HISTORY.forEach(([sender, message]) => {
    appendMessage(sender, message);
});

function sendMessage() {
    console.log("SEND FUNCTION CALLED");
    let message = userInput.value.trim();
    if (!message && selectedFiles.length === 0) return;

    appendMessage("user", message || "[Document Uploaded]");
    userInput.value = "";

    showThinking();

    const formData = new FormData();
    formData.append("message", message);
    formData.append("language", selectedLanguage);
    console.log(selectedLanguage);


    selectedFiles.forEach(file => {
        formData.append("files", file);
    });

    fetch(`/chat?username=${USERNAME}&session_id=${SESSION_ID}`, {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        removeThinking();
        appendMessage("bot", data.reply);
        selectedFiles = [];
        filePreviewContainer.innerHTML = "";
    })
    .catch(err => {
        removeThinking();
        appendMessage("bot", "⚠️ Error connecting to server.");
        console.error(err);
    });
}


// ----------------- Speech-to-Text (Mic Dictation) -----------------
let micActive = false;
let recognition;
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
} else if ('SpeechRecognition' in window) {
    recognition = new SpeechRecognition();
} else {
    alert("Your browser does not support Speech Recognition");
}

if (recognition) {
    recognition.continuous = false;       
    recognition.interimResults = false;   
    recognition.lang = 'en-US';           

    dictateBtn.addEventListener("click", () => {
    if (micActive) {
        recognition.stop(); // stop if already listening
        return;
    }

    micActive = true;
    userInput.placeholder = "🎙️ Listening...";
    recognition.start();
    });
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        resetMicUI();
    };

    recognition.onerror = () => {
        resetMicUI();
    };

    recognition.onend = () => {
        resetMicUI();
    };

    function resetMicUI() {
        micActive = false;
        userInput.placeholder = "Type your message...";
    }

}

// ----------------- Other UI elements -----------------
const logoutBtn = document.getElementById("logout-btn");
logoutBtn.addEventListener("click", function() {
    window.location.href = "/logout";
});

const plusBtn = document.getElementById("plus-btn");
const uploadMenu = document.getElementById("upload-menu");
plusBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    uploadMenu.classList.toggle("hidden");
});
document.addEventListener("click", function (e) {
    if (!uploadMenu.classList.contains("hidden") && !plusBtn.contains(e.target) && !uploadMenu.contains(e.target)) {
        uploadMenu.classList.add("hidden");
    }
});
});

