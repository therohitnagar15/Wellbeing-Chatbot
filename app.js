

const username = localStorage.getItem("user");
if (!username) window.location.href = "/login";

function logout() {
    localStorage.removeItem("user");
    window.location.href = "/login";
}

async function saveMood() {
    await fetch("/mood", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, mood: mood.value })
    });
    loadChart();
}

async function sendMessage() {
    const msg = document.getElementById("user-input").value;
    if (!msg.trim()) return; // Don't send empty messages

    document.getElementById("chat-box").innerHTML += `<div class="message user-message"><div class="message-content">${msg}</div></div>`;

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, message: msg })
    });
    const data = await res.json();
    document.getElementById("chat-box").innerHTML += `<div class="message bot-message"><div class="message-content">${data.reply}</div></div>`;

    document.getElementById("user-input").value = ""; // Clear input after sending
    document.getElementById("chat-box").scrollTop = document.getElementById("chat-box").scrollHeight; // Auto scroll to bottom
}

// Add event listener for Enter key on user input
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function loadChart() {
    try {
        const res = await fetch(`/moods/${username}`);
        const data = await res.json();

        // Clear any existing chart
        const chartCanvas = document.getElementById("moodChart");
        if (window.moodChartInstance) {
            window.moodChartInstance.destroy();
        }

        if (data.length === 0) {
            // Show message when no data is available
            chartCanvas.style.display = 'none';
            const chartContainer = document.getElementById("chart-container");
            if (!document.getElementById("no-data-message")) {
                const noDataMsg = document.createElement('p');
                noDataMsg.id = 'no-data-message';
                noDataMsg.textContent = 'No mood data available yet. Start logging your moods!';
                noDataMsg.style.textAlign = 'center';
                noDataMsg.style.color = '#666';
                noDataMsg.style.fontStyle = 'italic';
                chartContainer.appendChild(noDataMsg);
            }
            return;
        }

        // Hide no data message if it exists
        const noDataMsg = document.getElementById("no-data-message");
        if (noDataMsg) {
            noDataMsg.remove();
        }
        chartCanvas.style.display = 'block';

        const labels = data.map(d => new Date(d.date).toLocaleDateString());
        const values = data.map(d => {
            const moodIndex = ["Sad","Anxious","Stressed","Calm","Happy"].indexOf(d.mood);
            return moodIndex >= 0 ? moodIndex + 1 : 3; // Default to "Calm" (3) if mood not found
        });

        window.moodChartInstance = new Chart(chartCanvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Mood Level",
                    data: values,
                    borderColor: "#667eea",
                    backgroundColor: "rgba(102, 126, 234, 0.1)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: "#667eea",
                    pointBorderColor: "#fff",
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            callback: function(value) {
                                const moods = ["", "Sad", "Anxious", "Stressed", "Calm", "Happy"];
                                return moods[value] || value;
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const moods = ["", "Sad", "Anxious", "Stressed", "Calm", "Happy"];
                                const mood = moods[context.parsed.y] || context.parsed.y;
                                return `Mood: ${mood}`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading chart:', error);
        const chartCanvas = document.getElementById("moodChart");
        chartCanvas.style.display = 'none';
        const chartContainer = document.getElementById("chart-container");
        if (!document.getElementById("error-message")) {
            const errorMsg = document.createElement('p');
            errorMsg.id = 'error-message';
            errorMsg.textContent = 'Unable to load mood chart. Please try refreshing the page.';
            errorMsg.style.textAlign = 'center';
            errorMsg.style.color = '#e53e3e';
            chartContainer.appendChild(errorMsg);
        }
    }
}

function exportCSV() {
    window.location.href = `/export/csv/${username}`;
}

function exportPDF() {
    window.location.href = `/export/pdf/${username}`;
}

function showSolution(type) {
    const solutions = {
        anxiety: {
            title: "Anxiety Relief",
            content: `
                <h4>Quick Tips for Anxiety Relief:</h4>
                <ul>
                    <li>Practice deep breathing: Inhale for 4 counts, hold for 4, exhale for 4.</li>
                    <li>Ground yourself: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.</li>
                    <li>Progressive muscle relaxation: Tense and release muscle groups from toes to head.</li>
                    <li>Challenge negative thoughts: Ask yourself, "Is this thought based on facts or assumptions?"</li>
                    <li>Physical activity: Take a short walk or do gentle stretching.</li>
                </ul>
                <p>Remember, if anxiety persists, consider speaking with a mental health professional.</p>
            `
        },
        depression: {
            title: "Depression Support",
            content: `
                <h4>Ways to Cope with Depression:</h4>
                <ul>
                    <li>Establish a routine: Set small, achievable daily goals.</li>
                    <li>Stay connected: Reach out to friends or loved ones, even if it's just a text.</li>
                    <li>Physical activity: Exercise releases endorphins that can improve mood.</li>
                    <li>Healthy eating: Focus on balanced meals with fruits, vegetables, and whole grains.</li>
                    <li>Practice self-compassion: Be kind to yourself, as you would to a friend.</li>
                    <li>Limit screen time: Especially before bed, to improve sleep quality.</li>
                </ul>
                <p>Depression is treatable. If you're struggling, professional help can make a significant difference.</p>
            `
        },
        stress: {
            title: "Stress Management",
            content: `
                <h4>Strategies for Managing Stress:</h4>
                <ul>
                    <li>Time management: Prioritize tasks and break them into smaller steps.</li>
                    <li>Mindfulness meditation: Practice being present in the moment.</li>
                    <li>Healthy boundaries: Learn to say no when necessary.</li>
                    <li>Relaxation techniques: Try yoga, tai chi, or listening to calming music.</li>
                    <li>Social support: Talk to someone you trust about your stressors.</li>
                    <li>Self-care: Ensure you're getting enough sleep, eating well, and taking breaks.</li>
                </ul>
                <p>Chronic stress can affect your health. Consider professional support if stress feels overwhelming.</p>
            `
        },
        overwhelm: {
            title: "Overwhelm Help",
            content: `
                <h4>Dealing with Feeling Overwhelmed:</h4>
                <ul>
                    <li>Break it down: Divide large tasks into smaller, manageable steps.</li>
                    <li>Prioritize: Focus on the most important tasks first.</li>
                    <li>Take breaks: Step away for a few minutes to clear your mind.</li>
                    <li>Delegate: Ask for help when possible.</li>
                    <li>Practice acceptance: Remember that it's okay not to do everything perfectly.</li>
                    <li>Grounding techniques: Use the 5-4-3-2-1 method to bring yourself back to the present.</li>
                </ul>
                <p>If overwhelm is frequent, consider talking to a therapist about underlying causes.</p>
            `
        },
        motivation: {
            title: "Motivation Boost",
            content: `
                <h4>Building Motivation:</h4>
                <ul>
                    <li>Set small goals: Start with achievable tasks to build momentum.</li>
                    <li>Find your why: Connect tasks to your values or long-term goals.</li>
                    <li>Reward yourself: Celebrate small wins.</li>
                    <li>Accountability: Share your goals with a friend or use an app.</li>
                    <li>Environment: Create a space conducive to productivity.</li>
                    <li>Self-compassion: Be patient with yourself on difficult days.</li>
                </ul>
                <p>Motivation can fluctuate. Focus on progress, not perfection.</p>
            `
        },
        loneliness: {
            title: "Loneliness Support",
            content: `
                <h4>Addressing Loneliness:</h4>
                <ul>
                    <li>Reach out: Call or text someone you care about.</li>
                    <li>Join communities: Find groups or clubs based on your interests.</li>
                    <li>Volunteer: Helping others can create connections.</li>
                    <li>Pet companionship: Consider adopting a pet if you're able.</li>
                    <li>Professional help: Therapy can help process feelings of loneliness.</li>
                    <li>Online communities: Connect with others who share similar experiences.</li>
                </ul>
                <p>Loneliness is common and doesn't reflect your worth. Building connections takes time.</p>
            `
        }
    };

    const solution = solutions[type];
    if (solution) {
        // Create modal or display area
        const modal = document.createElement('div');
        modal.className = 'solution-modal';
        modal.innerHTML = `
            <div class="solution-content">
                <span class="close-btn" onclick="this.parentElement.parentElement.remove()">&times;</span>
                <h3>${solution.title}</h3>
                ${solution.content}
                <button onclick="sendMessage('I need help with ${type}')">Chat with AI Assistant</button>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

// Feedback modal functions
function openFeedbackModal() {
    document.getElementById('feedback-modal').style.display = 'block';
}

function closeFeedbackModal() {
    document.getElementById('feedback-modal').style.display = 'none';
}

// Handle feedback form submission
document.getElementById('feedback-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const rating = document.querySelector('input[name="rating"]:checked');
    const feedbackText = document.getElementById('feedback-text').value;

    if (!rating) {
        alert('Please select a rating.');
        return;
    }

    const feedbackData = {
        username: username,
        feedback_text: feedbackText,
        rating: parseInt(rating.value)
    };

    try {
        const res = await fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedbackData)
        });

        const data = await res.json();

        if (res.ok) {
            alert('Thank you for your feedback!');
            closeFeedbackModal();
            document.getElementById('feedback-form').reset();
        } else {
            alert('Error submitting feedback: ' + data.error);
        }
    } catch (error) {
        alert('Error submitting feedback. Please try again.');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('feedback-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Add default greeting message
document.getElementById("chat-box").innerHTML += `<div class="message bot-message"><div class="message-content">Hey ${username}, How are you feeling today .</div></div>`;

loadChart();
