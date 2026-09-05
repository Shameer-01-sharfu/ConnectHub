// ===============================
// DARK MODE
// ===============================

const toggle = document.getElementById("theme-toggle");

if(localStorage.getItem("theme") === "dark"){

    document.body.classList.add("dark");

    if(toggle){

        toggle.innerHTML="☀️";

    }

}

if(toggle){

toggle.addEventListener("click",function(){

document.body.classList.toggle("dark");

if(document.body.classList.contains("dark")){

localStorage.setItem("theme","dark");

toggle.innerHTML="☀️";

}else{

localStorage.setItem("theme","light");

toggle.innerHTML="🌙";

}

});

}