console.log("Main JS Loaded");
document.addEventListener(
"DOMContentLoaded",
function(){


const buttons =
document.querySelectorAll(".like-btn");



buttons.forEach(button=>{


button.addEventListener(
"click",
function(){


let postId =
this.dataset.postId;



fetch(`/posts/like/${postId}/`,{


method:"POST",


headers:{


"X-CSRFToken":
document.querySelector(
"[name=csrfmiddlewaretoken]"
).value


}


})


.then(response=>response.json())


.then(data=>{


let count =
document.getElementById(
`like-count-${postId}`
);


count.innerHTML =
data.likes_count;



if(data.liked){


button.classList.add("liked");

button.classList.add("animate");

setTimeout(()=>{

    button.classList.remove("animate");

},350);




}

else{


button.innerHTML="🤍 Like";

button.classList.remove("liked");


}



});


});


});


});
const saveButtons =
document.querySelectorAll(".save-btn");


saveButtons.forEach(button=>{


button.addEventListener(
"click",
function(){


let postId =
this.dataset.postId;



fetch(`/posts/save/${postId}/`,{


method:"POST",


headers:{


"X-CSRFToken":
document.querySelector(
"[name=csrfmiddlewaretoken]"
).value


}


})


.then(response=>response.json())


.then(data=>{


if(data.saved){


button.innerHTML="✅ Saved";

button.classList.add("saved");

button.classList.add("animate");

setTimeout(()=>{

    button.classList.remove("animate");

},350);

}

else{


button.innerHTML="🔖 Save";

button.classList.remove("saved");


}


});


});


});

/* ===========================
   AJAX COMMENT SYSTEM
=========================== */
console.log(document.querySelectorAll(".comment-form").length);
const commentForms = document.querySelectorAll(".comment-form");

commentForms.forEach(form => {

    form.addEventListener("submit", function(e){

        e.preventDefault();

        const postId = this.dataset.postId;

        const formData = new FormData(this);

        fetch(this.action, {

            method: "POST",

            headers: {

                "X-CSRFToken":
                document.querySelector("[name=csrfmiddlewaretoken]").value

            },

            body: formData

        })

        .then(response => response.json())

        .then(data => {

            if(data.success){

                const commentsDiv =
                document.getElementById(`comments-${postId}`);

                const newComment = document.createElement("div");

                newComment.className =
                "border rounded p-2 mb-2";

                newComment.innerHTML =

                `<strong>${data.username}</strong><br>${data.comment}`;

                commentsDiv.prepend(newComment);

                document.getElementById(
`comment-count-${postId}`
).innerHTML =
`💬 ${data.comments_count} Comments`;

this.reset();

            }

        });

    });

});

/* ===========================
   SHARE BUTTON
=========================== */

document.querySelectorAll(".share-btn").forEach(button => {

    button.addEventListener("click", async function () {

        const shareUrl = window.location.href;

        try {

            if (navigator.share) {

                await navigator.share({

                    title: "ConnectHub",

                    text: "Check out this post on ConnectHub!",

                    url: shareUrl

                });

            }

            else {

                await navigator.clipboard.writeText(shareUrl);

                const oldText = this.innerHTML;

                this.innerHTML = "✅ Copied";

                setTimeout(() => {

                    this.innerHTML = oldText;

                }, 2000);

            }

        }

        catch (err) {

            console.log(err);

        }

    });

});

/* ===========================
POST SHARE
=========================== */

let selectedPost = null;

document.querySelectorAll(".share-btn").forEach(btn=>{

btn.addEventListener("click",function(){

selectedPost=this.dataset.postId;

});

});

document.querySelectorAll(".send-share").forEach(btn=>{

btn.addEventListener("click",function(){

let receiver=this.dataset.user;

fetch(`/posts/share/${selectedPost}/`,{

method:"POST",

headers:{

"X-CSRFToken":
document.querySelector("[name=csrfmiddlewaretoken]").value,

"Content-Type":"application/x-www-form-urlencoded"

},

body:`receiver=${receiver}`

})

.then(r=>r.json())

.then(data=>{

if(data.success){

this.innerHTML="✅ Sent";

this.disabled=true;

setTimeout(()=>{

this.innerHTML="Send";

this.disabled=false;

bootstrap.Modal.getInstance(
document.getElementById("shareModal")
).hide();

},1200);

}

});

});

});