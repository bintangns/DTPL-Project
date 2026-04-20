document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('chatbotToggle');
    const panel = document.getElementById('chatbotPanel');
    const closeBtn = document.getElementById('chatbotClose');
    const input = document.getElementById('chatbotInput');
    const sendBtn = document.getElementById('chatbotSend');
    const messagesArea = document.getElementById('chatbotMessages');

    if (!toggle || !panel) return;

    // === CSRF Token ===
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // === Toggle Panel ===
    toggle.addEventListener('click', function() {
        panel.classList.toggle('active');
        if (panel.classList.contains('active')) {
            input.focus();
        }
    });

    closeBtn.addEventListener('click', function() {
        panel.classList.remove('active');
    });

    // === Send Message ===
    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message ' + sender;

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';

        // Simple markdown-like formatting for bot messages
        if (sender === 'bot') {
            let formatted = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>');
            bubble.innerHTML = formatted;
        } else {
            bubble.textContent = text;
        }

        msgDiv.appendChild(bubble);
        messagesArea.appendChild(msgDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function showTyping() {
        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.id = 'typingIndicator';
        typing.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
        messagesArea.appendChild(typing);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function removeTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        input.value = '';
        input.style.height = 'auto';

        // Disable input
        input.disabled = true;
        sendBtn.disabled = true;

        // Show typing
        showTyping();

        try {
            const response = await fetch('/destinasi/api/ask-gemini/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ message: message }),
            });

            removeTyping();

            const data = await response.json();

            if (response.ok && data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage(data.error || 'Maaf, terjadi kesalahan. Silakan coba lagi.', 'bot');
            }
        } catch (error) {
            removeTyping();
            addMessage('Maaf, tidak dapat terhubung ke server. Periksa koneksi internet Anda.', 'bot');
        }

        // Re-enable input
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }

    sendBtn.addEventListener('click', sendMessage);

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 80) + 'px';
    });
});
