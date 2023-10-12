  // This javascript will hide the password hide button when empty
  const password = document.getElementById('password-field');
  const toggle = document.getElementById('toggle');

  // Set up an event listener for the input field
  password.addEventListener("input", function() {
    // Check if the input field is empty
    if (this.value === "") {
      // The input field is empty, so hide the show password eye button
      toggle.style.visibility = "hidden";
    } else {
      // The input field is not empty, so show the show password eye button
      toggle.style.visibility = "visible";
    }
  });

  function showHide(){
  if (password.type ==='password'){
    password.setAttribute('type', 'text');
    toggle.classList.add('hide')

  }
  else {
    password.setAttribute('type', 'password');
    toggle.classList.remove('hide')
  }
  };