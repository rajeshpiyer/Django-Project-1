// Generate a random captcha code and update the captcha image
function generateCaptcha() {
    const captcha = Math.random().toString(36).substr(2, 5);
    const captchaImage = document.getElementById('captchaImage');
    captchaImage.src = 'captcha_image.jpg?captcha=' + captcha;
    return captcha;
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    // Generate initial captcha code
    generateCaptcha();
  
    // Form submit event listener
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent form submission
  
      // Get form inputs
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const captchaInput = document.getElementById('captcha').value;
      
      // Validate captcha
      const captcha = generateCaptcha();
      if (captcha !== captchaInput) {
        alert('Captcha verification failed. Please try again.');
        return;
      }
  
      // Perform login or further processing here
      alert('Username: ' + username + ', Password: ' + password);
    });
  });
  