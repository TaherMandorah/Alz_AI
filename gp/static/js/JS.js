function validateLogin ()
        {
          var valid = true;
          //Validate the Username field
           if (document.getElementById("User Email").value.search(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/) != 0)         //name should be at least 6 characters. Not complete regex. Each character should be a-z OR A-Z OR ' or - or  or space
           {
               valid = false;
               document.getElementById("errUEmail").innerHTML = "ERROR: Enter your Email !";
               document.getElementById("errUEmail").style.display = "inline";
           }
           else
           {
               document.getElementById("errUEmail").innerHTML = "";
               document.getElementById("errUEmail").style.display = "none";
            }

           //Validate the password 
          if (document.getElementById("password").value.length < 8)
          {
              valid = false;
              document.getElementById("errPassword").innerHTML = "ERROR: Enter correct Password!";
              document.getElementById("errPassword").style.display = "inline";
          }
          else
          {
              document.getElementById("errPassword").innerHTML = "";
              document.getElementById("errPassword").style.display = "none";
          }
           //i.e.   return valid;
          if (valid == false)
          {
               return false;
          }
          else
          {
               return true;
          }

        }
        const dropArea = document.getElementById("drop-area");
        const inputFile = document.getElementById("input-file");
        const previewImage = document.getElementById("preview-image");
    
        inputFile.addEventListener('change', previewUploadedImage);
    
        // JavaScript file: JS.js

        function previewUploadedImage() {
          const file = inputFile.files[0];
          const reader = new FileReader();

          reader.onload = function(e) {
              previewImage.src = e.target.result;
          };

          if(file) {
              reader.readAsDataURL(file);
          }
        }

        // Add event listener to input file element
        inputFile.addEventListener('change', previewUploadedImage);

    
        dropArea.addEventListener("dragover", function(e){
            e.preventDefault();
        });
    
        dropArea.addEventListener("drop", function(e){
            e.preventDefault();
            inputFile.files = e.dataTransfer.files;
            previewUploadedImage();
        });
    
        document.getElementById("uploadForm").addEventListener("submit", function(e) {
            e.preventDefault();
            // Handle form submission or additional processing here
            console.log("Form submitted!");
        });
        
// Function to open the modal
function openModal() {
    var modal = document.getElementById('modal01');
    modal.style.display = "block"; // Display the modal
  }
  
  // Function to close the modal
  function closeModal() {
    var modal = document.getElementById('modal01');
    modal.style.display = "none"; // Hide the modal
  }