const profilePopup = document.getElementById("profile-popup");
const showProfileBtn = document.getElementById("profile-container");
const closeButton = document.querySelector(".close-button");
const profileForm = document.getElementById("profile-form");
const zephyrMenu = document.getElementById("zephyr-menu");
const toggleButton = document.getElementById("navbar-toggler-small");
const mobileNav = document.getElementById("profile-containers");
const buttonEdit = document.getElementById("submit-btn");
const inputFields = document.querySelectorAll(
  "#username, #phone-number, #bio-info, #user-interests"
);
buttonEdit.textContent = "Logout";
buttonEdit.setAttribute("href", "/auth/logout");
try {
  inputFields.forEach((input) => {
    input.addEventListener("input", () => {
      buttonEdit.textContent = "Save";
      buttonEdit.setAttribute("href", "#");
    });
  });

  mobileNav.addEventListener("click", () => {
    openPopup();
  });
  zephyrMenu.addEventListener("click", () => {
    zephyrMenu.classList.remove("show");
  });

  showProfileBtn.addEventListener("click", openPopup);
  closeButton.addEventListener("click", closePopup);
  profileForm.addEventListener("submit", handleFormSubmit);
} catch (error) {
  console.error("Error:", error);
}

function openPopup() {
  profilePopup.style.display = "flex";
  fetchProfileData();
}

function closePopup() {
  profilePopup.style.display = "none";
}

toggleButton.addEventListener("click", () => {
  zephyrMenu.classList.toggle("show");
});
function fetchProfileData() {
  axios
    .get("auth/profile")
    .then((response) => {
      if (response.data.error) {
        console.error(response.data.error);
      } else {
        document.getElementById("username").value = response.data.username;
        document.getElementById("phone-number").value = response.data.phone;
        document.getElementById("bio-info").value = response.data.bio;
        document.getElementById("user-interests").value =
          response.data.interests;
      }
    })
    .catch((error) => console.error("Error:", error));
}

function handleFormSubmit(event) {
  if (buttonEdit.textContent === "Logout") {
    console.log("Logging out user");
    logoutUser();
    window.location.reload();
    return;
  }
  event.preventDefault();

  const formData = new FormData(event.target);
  axios
    .post("auth/profile/", formData, {
      headers: {
        "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]')
          .value,
      },
    })
    .then((response) => {
      if (response.data.success) {
        console.log("Profile updated successfully");
        window.location.reload();
        closePopup();
      } else {
        console.error("Error updating profile:", response.data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}

function logoutUser() {
  axios
    .get("auth/logout")
    .then((response) => {
      if (response.data.success) {
        console.log("User logged out successfully");
        window.location.reload();
      } else {
        console.error("Error logging out user:", response.data.error);
      }
    })
    .catch((error) => console.error("Error:", error));
}
