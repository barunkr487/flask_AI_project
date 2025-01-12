/* script.js */

// Flask API URL for TTS and Speech-to-Text
const TTS_URL = "/tts";
const STT_URL = "/speech-to-text";

// Function to speak text using Flask TTS
function speakText(text) {
    if (!text) {
        alert("No text to speak!");
        return;
    }

    axios.post(TTS_URL, { text })
        .then(() => {
            console.log("Text spoken successfully");
        })
        .catch(error => {
            console.error("Error in text-to-speech:", error.response.data || error.message);
        });
}

// Function to handle Speech-to-Text using Flask API
function startSpeechToText(targetInputId) {
    axios.post(STT_URL)
        .then(response => {
            if (response.data.text) {
                document.getElementById(targetInputId).value = response.data.text;
            } else {
                alert("No speech recognized. Please try again.");
            }
        })
        .catch(error => {
            console.error("Speech-to-text error:", error.response?.data?.error || error.message);
            alert("Error in speech-to-text: " + (error.response?.data?.error || error.message));
        });
}

// Fetch weather data from Flask API
function getWeather() {
    const city = document.getElementById('city').value;
    axios.post(`/weather?city=${city}`)
        .then(response => {
            document.getElementById('weatherResult').innerText = `Weather: City:${response.data.city}" ,"temperature:${response.data.temperature}","Description:${response.data.description}`;
        })
        .catch(error => {
            document.getElementById('weatherResult').innerText = `Error: ${error.response.data.message || error.message}`;
        });
}

// Fetch a random joke from Flask API
function getJoke() {
    axios.get('/joke')
        .then(response => {
            document.getElementById('jokeResult').innerText = response.data.setup + ", " + response.data.punchline;
        })
        .catch(error => {
            document.getElementById('jokeResult').innerText = `Error: ${error.response.data.message || error.message}`;
        });
}

// Fetch news from Flask API based on user input
function getNews() {
    const country = document.getElementById('country').value;
    if (!country) {
        alert("Country name is empty!");
        return false;
    }

    axios.post('/news', { message: country })
        .then(response => {
            const articles = response.data.articles;
            if (!Array.isArray(articles) || articles.length === 0) {
                document.getElementById('newsResult').innerHTML = `No news data available for the provided country: "${country}". Please check the news API documentation for valid input.`;
                return;
            }

            const newsList = articles.map(article => `<li>${article.title}</li>`).join('');
            document.getElementById('newsResult').innerHTML = `<ul>${newsList}</ul>`;
        })
        .catch(error => {
            document.getElementById('newsResult').innerText = `Error: ${error.response.data.message || error.message}`;
        });
}

// Chatbot interaction with Flask API
function askChatbot() {
    const userInput = document.getElementById('chatInput').value;
    axios.post('/chatbot', { message: userInput })
        .then(response => {
            document.getElementById('chatResult').innerText = `Bot: ${response.data.reply}`;
        })
        .catch(error => {
            document.getElementById('chatResult').innerText = `Error: ${error.response.data.message || error.message}`;
        });
}

// Toggle Show/Hide for All Sections with Slide effect
$('#toggleButton').click(function() {
    const sections = ['#weatherSection', '#jokeSection', '#newsSection', '#chatbotSection'];
    const allVisible = sections.every(section => $(section).is(':visible'));

    if (allVisible) {
        $(sections.join(', ')).slideUp(1000);  // Slide Up effect for hiding
        $('#toggleButton').text('Show All Sections');
    } else {
        $(sections.join(', ')).slideDown(1000);  // Slide Down effect for showing
        $('#toggleButton').text('Hide All Sections');
    }
});
