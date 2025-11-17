document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";
        activityCard.style.border = "1px solid #e0e0e0";
        activityCard.style.borderRadius = "8px";
        activityCard.style.padding = "16px";
        activityCard.style.marginBottom = "20px";
        activityCard.style.background = "#fafafa";
        activityCard.style.boxShadow = "0 2px 6px rgba(0,0,0,0.04)";

        const spotsLeft = details.max_participants - details.participants.length;

        // Build participants list HTML (styled)
        let participantsHtml = `
          <ul class='participants-list'>
        `;
        if (details.participants.length > 0) {
          details.participants.forEach(email => {
            participantsHtml += `
              <li style="margin-bottom: 4px; color: #333; display: flex; align-items: center;">
                <span style="flex:1;">${email}</span>
                <span class="delete-participant" title="Remove participant" style="cursor:pointer; color:#d32f2f; font-size:18px; margin-left:8px;" data-activity="${name}" data-email="${email}">&#128465;</span>
              </li>
            `;
          });
        } else {
          participantsHtml += `<li style="color: #888;"><em>No participants yet</em></li>`;
        }
        participantsHtml += "</ul>";

        activityCard.innerHTML = `
          <h4 style="margin-top:0; color:#2d6cdf;">${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div style="margin-top:12px;">
            <strong style="color:#2d6cdf;">Participants:</strong>
            <div style="margin-left:10px;">${participantsHtml}</div>
          </div>
        `;

        activitiesList.appendChild(activityCard);
        // Add click event for delete icons
        activityCard.querySelectorAll('.delete-participant').forEach(icon => {
          icon.addEventListener('click', async (e) => {
            const activityName = icon.getAttribute('data-activity');
            const email = icon.getAttribute('data-email');
            if (confirm(`Remove ${email} from ${activityName}?`)) {
              try {
                const response = await fetch(`/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`, {
                  method: 'POST'
                });
                if (response.ok) {
                  fetchActivities(); // Refresh list
                } else {
                  alert('Failed to remove participant.');
                }
              } catch (err) {
                alert('Error removing participant.');
              }
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
  messageDiv.textContent = result.message;
  messageDiv.className = "success";
  signupForm.reset();
  fetchActivities(); // Refresh activities list after signup
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
