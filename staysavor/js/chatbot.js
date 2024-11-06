// Get a reference to the chatbot iframe and the toggle button
const chatbotFrame = document.getElementById('chatbot-frame');
const toggleButton = document.getElementById('toggle-chatbot');

// Add event listener to the toggle button
toggleButton.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent the default anchor click behavior
    chatbotFrame.classList.toggle('show-chatbot'); // Toggle the 'show-chatbot' class
});