// added to let 2nd modal run before form submits
document.getElementById("exampleModalToggle2").addEventListener("focus",function(event){
  setTimeout(function(){document.forms['frm1'].submit();}, 5000);
});


let connection = document.getElementById('connectionModal')
connection.addEventListener('shown.bs.modal', function (event) {
  // click event that triggered the modal
  // let clickedConnectionModal = event.relatedTarget
  // Extract info from data-bs-* attributes
  // let recipient = clickedConnectionModal.getAttribute('data-bs-custom-name')
 
  let temp = getLogin().then(login=> {
    let statusRecorded;
    let userName = login.user;
    let password = login.password;

    if (userName == undefined){
      // console.log("Login Undefined")
      statusRecorded = false
      userName = "zeus";
      password = "zeuspass";
    }
    else {
      // console.log("Login Defined");
      statusRecorded = true
      userName = userName;
      password = password;
    }
    
    // Update the modal's content.
    if (statusRecorded){
      let modalTitle = connection.querySelector('.modal-title');
      modalTitle.textContent = 'You are connected as ' + userName;

      let modalUserName = connection.querySelector('#user-name');
      modalUserName.value = userName;

      let modalPassword = connection.querySelector('#user-password');
      modalPassword.value = password;

    }
    else{
      let modalBodyInput = connection.querySelector('#modalSubmit')
      modalBodyInput.innerText = "Submit"
    }

  });

})


let testStatus = document.getElementById('modalSubmit');
testStatus.addEventListener('click', function (event) {
  let progressWidth = document.getElementById('connectionStatus');
  let selectButtonClose = document.getElementById('updateComplete'); 

  let timerCount = 0;
  const progressCounter = setInterval(waitFunc, 100);

  function waitFunc(){
    if (timerCount <= 100){
      
      progressWidth.style.width = String(timerCount + "%");
      progressWidth.innerText = String(Math.round(timerCount,0) + "%");
      progressWidth.ariaValueNow = timerCount;
      timerCount += 2.5;
    }
    else{
      progressWidth.innerText = "Complete";
      setTimeout(function(){progressWidth.style.width = "0%"; selectButtonClose.click()}, 1000);
      clearInterval(progressCounter);
      progressCounter=null;      
    }
  }
 
});


async function getLogin() {
    let url = 'http://127.0.0.1:5000/api/login';
    try {
        const res = await fetch(url);
        let temp = await res.json()

        let user = temp.username;
        let password = temp.password;

        return {user, password}
    } 
    catch (error) {
        console.log(error);
    }
}
