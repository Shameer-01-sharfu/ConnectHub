// =======================================
// AUTOPLAY REELS
// =======================================

const videos = document.querySelectorAll(".reel-video");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        const video = entry.target;

        if (entry.isIntersecting) {

            video.play().catch(() => {});

        } else {

            video.pause();

        }

    });

}, {

    threshold: 0.7

});

videos.forEach(video => observer.observe(video));


// =======================================
// CSRF TOKEN
// =======================================

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;

            }

        }

    }

    return cookieValue;

}


// =======================================
// LIKE AJAX
// =======================================

document.querySelectorAll(".like-btn").forEach(button => {

    button.addEventListener("click", function () {

        const url = this.dataset.url;

        const reelId = this.dataset.reelId;

        fetch(url, {

            method: "POST",

            headers: {

                "X-CSRFToken": getCookie("csrftoken")

            }

        })

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "like-count-" + reelId
            ).innerHTML = data.likes_count;

            this.innerHTML = data.liked ? "❤️" : "🤍";

        });

    });

});


// =======================================
// SHARE MODAL
// =======================================

let selectedReel = null;

document.querySelectorAll(".share-btn").forEach(button => {

    button.addEventListener("click", function () {

        selectedReel = this.dataset.reel;console.log("Selected Reel:", selectedReel);



        const modal = new bootstrap.Modal(
            document.getElementById("shareModal")
        );

        modal.show();

        document.getElementById("user-search").value = "";

        document.getElementById("user-results").innerHTML = "";

    });

});


// =======================================
// SEARCH USERS
// =======================================

document.addEventListener("input", function (e) {

    if (e.target.id !== "user-search") return;

    const query = e.target.value.trim();

    console.log("Searching:", query);

    if (query === "") {

        document.getElementById("user-results").innerHTML = "";

        return;

    }

    fetch("/reels/search-users/?q=" + encodeURIComponent(query))

    .then(response => response.json())

    .then(users => {

        let html = "";

        users.forEach(user => {

            html += `
                <div class="user-item border rounded p-2 mb-2"
                     data-id="${user.id}"
                     style="cursor:pointer">

                    <strong>${user.username}</strong><br>
                    <small>${user.name}</small>

                </div>
            `;

        });

        document.getElementById("user-results").innerHTML = html;

        attachShareEvents();

    });

});

function attachShareEvents() {

    document.querySelectorAll(".user-item").forEach(item => {

        item.onclick = function () {

            const receiver = this.dataset.id;

            fetch("/reels/share/" + selectedReel + "/", {

                method: "POST",

                headers: {

                    "X-CSRFToken": getCookie("csrftoken"),

                    "Content-Type": "application/x-www-form-urlencoded"

                },

                body: "receiver=" + receiver

            })

            .then(response => response.json())

            .then(data => {

                if (data.success) {

                    alert("✅ Reel Shared Successfully");

                    bootstrap.Modal.getInstance(
                        document.getElementById("shareModal")
                    ).hide();

                }

            });

        };

    });

}

// =======================================
// DOUBLE TAP LIKE
// =======================================

document.querySelectorAll(".reel-video").forEach(video => {

    let lastTap = 0;

    video.addEventListener("click", function () {

        const currentTime = Date.now();

        if (currentTime - lastTap < 300) {

            const reel = video.closest(".reel");

            const likeBtn = reel.querySelector(".like-btn");

            if (likeBtn.innerHTML.trim() === "🤍") {

                likeBtn.click();

            }

            const heart = document.createElement("div");

            heart.className = "heart-animation";

            heart.innerHTML = "❤️";

            reel.appendChild(heart);

            setTimeout(() => {

                heart.remove();

            },700);

        }

        lastTap = currentTime;

    });

});