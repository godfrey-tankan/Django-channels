function toggleForm() {
  var signupForm = document.getElementById("signup-container");
  var signinForm = document.getElementById("signin-container");

  signupForm.classList.toggle("hidden");
  signinForm.classList.toggle("hidden");
  document.getElementById("message-container").classList.add("hidden");
}

function showAuthForms() {
  var authForms = document.getElementById("auth-forms");
  authForms.classList.remove("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signup-form");
  const signinForm = document.getElementById("signin-form");
  const signInContainer = document.getElementById("signin-container");
  const signUpContainer = document.getElementById("signup-container");
  const messageContainer = document.getElementById("message-container");
  const passwordOne = document.getElementById("password1");
  const passwordTwo = document.getElementById("password2");
  const profilePictureInput = document.getElementById("profile_picture");
  const formContainer = document.getElementById("form-container");
  const profilePicturePreview = document.getElementById(
    "profile_picture_preview"
  );
  // PREVIEW THE UPLOADED PROF IMG
  profilePictureInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        profilePicturePreview.src = e.target.result;
        profilePicturePreview.style.display = "block";
      };
      reader.readAsDataURL(this.files[0]);
    }
  });
  if (formContainer) {
    formContainer.scrollIntoView({ behavior: "smooth", block: "end" });
  }

  signUpContainer.classList.add("hidden");
  signInContainer.classList.remove("hidden");

  if (!signupForm || !signinForm) {
    console.error("Signup form or Signin form not found.");
    return;
  }

  signupForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(signupForm);
    formData.append("form_type", "signup");

    const passwordOneValue = passwordOne.value;
    const passwordTwoValue = passwordTwo.value;
    const minLength = 5;
    const hasUppercase = /[A-Z]/.test(passwordOneValue);
    const hasNumber = /\d/.test(passwordOneValue);

    if (passwordOneValue.length < minLength) {
      console.log(
        "password is less than 5 characters.",
        passwordOneValue,
        minLength
      );
      displayMessage("Password must be at least 5 characters.", "error");
      return;
    } else if (!hasUppercase) {
      console.log("password does not have uppercase letter.");
      displayMessage(
        "Password must contain at least one uppercase letter.",
        "error"
      );
      return;
    } else if (!hasNumber) {
      console.log("password does not have number.");
      displayMessage("Password must contain at least one number.", "error");
      return;
    } else if (passwordOneValue !== passwordTwoValue) {
      console.log("passwords do not match.");
      displayMessage("Passwords do not match.", "error");
      return;
    }

    axios
      .post("", formData)
      .then((response) => {
        console.log("Signup successful:", response.data);
        displayMessage(response.data.message, "success");
        window.location.reload();
      })
      .catch((error) => {
        console.error("Signup error:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.error
        ) {
          const errors = error.response.data.error;
          let errorMessage = "";
          for (const key in errors) {
            if (errors.hasOwnProperty(key)) {
              errorMessage += `${key}: ${errors[key].join(", ")}\n`;
            }
          }
          displayMessage(errorMessage, "error");
        } else {
          displayMessage(
            "Registration failed. Please check the form.",
            "error"
          );
        }
      });
  });

  signinForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(signinForm);
    formData.append("form_type", "signin");
    axios
      .post("", formData)
      .then((response) => {
        console.log("Login successful:", response.data);
        displayMessage(response.data.message, "success");
        window.history.back();
      })
      .catch((error) => {
        console.error("Login error:", error);
        const errorMessage =
          error.response.data.error || "Invalid credentials!.";
        displayMessage(errorMessage, "error");
      });
  });

  function displayMessage(message, type) {
    messageContainer.textContent = message;
    messageContainer.classList.remove("hidden");
    messageContainer.classList.remove("validation-error", "validation-success");
    messageContainer.classList.add(
      type === "error" ? "validation-error" : "validation-success"
    );
  }
});
