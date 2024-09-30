window.onload = function() {
    setTimeout(function() {
      document.getElementById('loader').style.display = 'none'; 
      document.getElementById('main-content').style.display = 'block'; 
    }, 2000); 
  };
  
  function showLoader() {
    document.getElementById('loader').style.display = 'flex'; 
    setTimeout(function() {
      document.getElementById('loader').style.display = 'none'; 
    }, 2000);
  }

  
  document.getElementById('myButton').addEventListener('click', function(event) {
    event.preventDefault(); 
    showLoader(); 
  });

  document.getElementById('myLink').addEventListener('click', function(event) {
    event.preventDefault(); 
    showLoader(); 
});
function toggleMenu() {
    const mobileNavbar = document.getElementById('mobileNavbar');
    const mobilebtn = document.getElementById('mobile-btn');
    const menuIcon = document.getElementById('menuIcon');
    const closeIcon = document.getElementById('closeIcon');

    mobileNavbar.classList.toggle('active');
    mobilebtn.classList.toggle('active');
    
    menuIcon.classList.toggle('hidden'); 
    closeIcon.classList.toggle('hidden');
}

document.addEventListener("DOMContentLoaded", function() {
    let currentComment = 0;
    const comments = document.querySelectorAll(".comment-container");
    const totalComments = comments.length;

    document.getElementById("next-btn").addEventListener("click", function() {
        comments[currentComment].classList.remove("active");
        currentComment = (currentComment + 1) % totalComments;
        comments[currentComment].classList.add("active");
    });

    document.getElementById("prev-btn").addEventListener("click", function() {
        comments[currentComment].classList.remove("active");
        currentComment = (currentComment - 1 + totalComments) % totalComments;
        comments[currentComment].classList.add("active");
    });
});
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();


    document.getElementById('loader').style.display = 'block';


    document.getElementById('submit-btn').disabled = true;


    setTimeout(function() {
    
        document.getElementById('loginForm').submit();
    }, 1000);
})


  // Function to apply dark mode to all necessary elements
  function applyDarkModeToElements() {
    const elements = document.querySelectorAll(
      '.second-container, .third-container, .quickly-div, .start-div, .flex-div, .person, .second-grouped-div, .sixth-grouped-div, .comment-container, .msg-div, .quickly-look-div, .grps-div, .event-div, .giving-div, .help-container div, .help-container div a, .first-container, .our-story, .service-div.form, .fifth-groupd-div, .cs-div, .faq, .first-div-contact, .first-service-container,.forth-grouped-div ,.form,.form input,.form textarea'
    );

    elements.forEach((el) => {
      el.classList.add('dark-mode');
    });
  }

  // Function to remove dark mode from elements
  function removeDarkModeFromElements() {
    const elements = document.querySelectorAll(
      '.second-container, .third-container, .quickly-div, .start-div, .flex-div, .person, .second-grouped-div, .sixth-grouped-div, .comment-container, .msg-div, .quickly-look-div, .grps-div, .event-div, .giving-div, .help-container div, .help-container div a, .first-container, .our-story, .service-div.form, .fifth-groupd-div, .cs-div, .faq, .first-div-contact, .first-service-container,.forth-grouped-div ,.form,.form input,.form textarea'
    );

    elements.forEach((el) => {
      el.classList.remove('dark-mode');
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Get the theme from localStorage
    const theme = localStorage.getItem('theme') || 'light';

    // Apply dark mode if 'theme' in localStorage is 'dark'
    if (theme === 'dark') {
      document.body.classList.add('dark-mode');
      applyDarkModeToElements(); // Apply dark mode to all relevant elements
    } else {
      document.body.classList.add('light-mode');
    }
  });

  // Function to toggle theme and store preference in localStorage
  function themes() {
    const body = document.body;
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
      body.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light'); // Switch to light mode
      removeDarkModeFromElements(); // Remove dark mode from elements
    } else {
      body.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark'); // Switch to dark mode
      applyDarkModeToElements(); // Apply dark mode to elements
    }
  }

