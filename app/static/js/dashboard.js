document.addEventListener("DOMContentLoaded", function () {
  // Check for authentication token immediately
  const token = localStorage.getItem("accessToken");
  
  // If no token, redirect to login page immediately
  if (!token) {
    window.location.href = "/login";
    return;
  }

  const queryForm = document.getElementById("query-form");
  const responseContent = document.getElementById("response-content");
  const logoutBtn = document.getElementById("logout-btn");
  const userName = document.getElementById("user-name");

  // Since we have a token, fetch user info
  fetchUserInfo(token);

  if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      // Since we're on the dashboard, we know we have a token
      localStorage.removeItem("accessToken");
      window.location.href = "/";
    });
  }

  async function fetchUserInfo(token) {
    try {
      const response = await fetch("/api/users/me", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        if (userName)
          userName.textContent = userData.full_name || userData.username;
      } else {
        if (response.status === 401) {
          localStorage.removeItem("accessToken");
          window.location.href = "/login";
          return;
        }
        if (userName) userName.textContent = "Guest";
        if (logoutBtn) logoutBtn.textContent = "Login";
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
      // On error, redirect to login to be safe
      localStorage.removeItem("accessToken");
      window.location.href = "/login";
    }
  }

  if (queryForm) {
    queryForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      let query = "";
      const queryElement = document.getElementById("query");
      if (
        queryElement instanceof HTMLInputElement ||
        queryElement instanceof HTMLTextAreaElement
      ) {
        query = queryElement.value;
      }

      if (responseContent) {
        responseContent.innerHTML =
          '<p class="placeholder">Processing your query...</p>';
      }

      try {
        const headers = {
          "Content-Type": "application/json",
        };

        if (token) {
          headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch("/api/secure-query", {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            query: query,
          }),
        });

        const data = await response.json();

        if (response.ok && responseContent) {
          let responseHTML = `<div class="ai-response">${formatResponse(
            data.response
          )}</div>`;

          responseContent.innerHTML = responseHTML;
        } else if (responseContent) {
          responseContent.innerHTML = `<p class="error-message">${
            data.detail || "An error occurred while processing your query."
          }</p>`;

          if (response.status === 401 && token) {
            localStorage.removeItem("accessToken");
            window.location.href = "/login";
            return;
          }
        }
      } catch (error) {
        console.error("Error:", error);
        if (responseContent) {
          responseContent.innerHTML =
            '<p class="error-message">An error occurred. Please try again later.</p>';
        }
      }
    });
  }

  function formatResponse(text) {
    return text.replace(/\n/g, "<br>");
  }
});
