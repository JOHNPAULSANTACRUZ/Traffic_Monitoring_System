const form = document.getElementById('form')
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const confirmPass = document.getElementById('confirmPass');


form.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs(){
     const usernameValue = username.value.trim();
     const emailValue = email.value.trim();
     const passwordValue = password.value.trim();
     const confirmPassValue = confirmPass.value.trim();

     if (usernameValue == '' || usernameValue== null){
         setErrorFor(username,'Username cannot be blank');
        } else if (!isUsername(usernameValue)) {  
            setErrorFor(username, 'Try again, only lowercase');
        } else {
        setSuccessFor(username);
     }
     
     if(emailValue === ''|| emailValue== null){
		setErrorFor(email, 'Email cannot be blank');
	} else if (!isEmail(emailValue)) {  
		setErrorFor(email, 'Not a valid email');
	} else {
		setSuccessFor(email);
	}
    
    if(passwordValue === '' && confirmPassValue === ''){
		setErrorFor(password, 'Password cannot be blank');
        setErrorFor(confirmPass,'Confirm password connot be blank');
	} else {
		// Add your code here to validate the password length
		if(passwordValue.length <= 7 || passwordValue.length >= 16 ) {
			setErrorFor(password, 'Password must be 8 to 16 characters long');
            setErrorFor(confirmPass, 'Must follow the passoword requirements.');

        }else{
         if(passwordValue !== confirmPassValue) {
            setErrorFor(password, 'Passwords does not match');
                setErrorFor(confirmPass, 'Passwords does not match');

            }else if (passwordValue === confirmPassValue){
                setSuccessFor(password);
                setSuccessFor(confirmPass);
        }
    }
}

function setErrorFor(input,message){
    const formOutline = input.parentElement; //.form-outline
    const small = formOutline.querySelector('small');
    //add error message inside the <small> </small>
    small.innerText= message;
    //add error class
    formOutline.className = 'form-outline error';
};

function setSuccessFor(input){
    const formOutline = input.parentElement;//.form-outline
    // add success class
    formOutline.className = 'form-outline success';
    return input.value;
};


function isEmail(email) {
    //regex for email validation
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
};

function isUsername(username){
    //regex for username validation
    return /^[a-z][a-z]+\d*$|^[a-z]\d\d+$/.test(username);

};

}
