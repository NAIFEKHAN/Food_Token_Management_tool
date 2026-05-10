const friends = [
    { name: "PRAVEEN J", role: "Editor", image: "/static/images/friends/praveen.jpeg" },
    { name: "KUMARAGURUBARAN", role: "Designer", image: "/static/images/friends/kumaraguru.jpeg" },
    { name: "NAIFE KHAN M", role: "Editor", image: "/static/images/friends/naife.jpeg" },
    { name: "GUGAN S", role: "Designer", image: "/static/images/friends/gugan.jpeg" },
    { name: "KOTIREDDY", role: "Designer", image: "/static/images/friends/koti.jpeg" },
    { name: "JALLA BHARGAV", role: "Volunteer", image: "/static/images/friends/bhargav.jpeg" },
    { name: "ASHWIN A", role: "Incharge", image: "/static/images/friends/ashwin.jpeg" },
    { name: "PRAVEEN V M", role: "Editor", image: "/static/images/friends/cr.jpeg" },
    { name: "DEVDHARSHAN J", role: "Editor", image: "/static/images/friends/dev.jpeg" },
    { name: "KAVIPRIYAN M", role: "Designer", image: "/static/images/friends/kavi.jpeg" },
    { name: "ANNANGI SRINIVAS", role: "Volunteer", image: "/static/images/friends/srinivas.jpeg" },
    { name: "MUKESH R", role: "Designer", image: "/static/images/friends/mukesh.jpeg" },
    { name: "PRAKADESH", role: "volunteer", image: "/static/images/friends/pragadeesh.jpeg" },
    { name: "PRAVEEN P", role: "Designer", image: "/static/images/friends/praveenp.jpeg" },
    { name: "SACHIN", role: "volunteer", image: "/static/images/friends/sachin.jpeg" },
    { name: "JAYASURIYA G", role: "Incharge", image: "/static/images/friends/surya.jpeg" },
    { name: "VIVEK REDDY", role: "Designer", image: "/static/images/friends/vivek.jpeg" },
    { name: "JAYANTH REDDY", role: "Designer", image: "/static/images/friends/jayanth.jpeg"},
    { name: "PRAKASH K", role: "Incharge", image: "/static/images/friends/prakash.jpeg"},
    { name: "RAVICHANDRAN J", role: "Designer", image: "/static/images/friends/ravi.jpeg"},
    { name: "SANTHOSH", role: "volunteer", image: "/static/images/friends/sandhosh.jpeg"},
    { name: "SANJAI KUMAR C", role: "Volunteer", image: "/static/images/friends/sanjay.jpeg"},
    { name: "SUMANTH REDDY", role: "Volunteer", image: "/static/images/friends/sumanth.jpeg"},
    { name: "SIVASELVAM K", role: "Volunteer", image: "/static/images/friends/selva.jpeg"},
    { name: "RITHIP REDDY", role: "Designer", image: "/static/images/friends/rithip.jpeg"},
    { name: "CHANDRU S", role: "Volunteer", image: "/static/images/friends/chandru.jpeg"},
    { name: "JAIDI AVINASH", role: "Designer", image: "/static/images/friends/avinash.jpeg"},
    { name: "ROHITH REDDY", role: "Volunteer", image: "/static/images/friends/rohith.jpeg"}
];

const track = document.getElementById('friends-track');

if (track) {
    const tripleList = [...friends, ...friends, ...friends];

    tripleList.forEach(friend => {
        const slide = document.createElement('div');
        slide.className = 'friend-card';

        slide.innerHTML = `
            <img src="${friend.image}" alt="${friend.name}">
            <span class="name">${friend.name}</span>
            <span class="role">${friend.role}</span>
        `;

        track.appendChild(slide);
    });
}
