// JavaScript code can be added here
$(function() {
    const darkModeToggle = $("#darkModeToggle");
    const messageInput = $("#messageInput");
    const messagesContainer = $("#messages");

    darkModeToggle.on("click", function() {
        $("body").toggleClass("dark-mode");
    });

    $("#user_prompt_form").on("submit", function(event) {
        event.preventDefault();
        sendMessage();
    });

    $("#sendBtn").on("click", function(event) {
        event.preventDefault();
        sendMessage();
    });

    messageInput.on("keydown", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = messageInput.val().trim();
        if (message === "") return;

        appendMessage("user", message);
        messageInput.val("");

        const botMessage = appendMessage("bot", $("<span>").addClass("loading-indicator"));

        $.ajax({
            url: "/ai/generate",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ message: message }),
            success: function(data) {
                botMessage.find(".text").html(data.response).addClass("received");
                botMessage.find(".loading-indicator").remove();
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                botMessage.find(".text").html("An error occurred.");
                botMessage.find(".loading-indicator").remove();
            }
        });
    }

    function appendMessage(sender, content) {
        const messageDiv = $("<div>").addClass("message").addClass(sender);
        const icon = $("<img>").addClass("icon").attr("src", sender === "user" ? "/static/images/user-icon.png" : "/static/images/bot-icon.png").attr("alt", sender === "user" ? "User" : "Bot");
        const textDiv = $("<div>").addClass("text").append(content);

        if (sender === "user") {
            messageDiv.append(textDiv).append(icon);
        } else {
            messageDiv.append(icon).append(textDiv);
        }

        messagesContainer.append(messageDiv);
        messagesContainer.scrollTop(messagesContainer[0].scrollHeight);

        return messageDiv;
    }
});

