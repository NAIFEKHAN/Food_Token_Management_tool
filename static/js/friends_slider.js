const friends = [
    { name: "PRAVEEN J", role: "Editor", image: "/static/images/friends/praveen.jpeg" },
    { name: "ANNANGI SRINIVAS", role: "Volunteer", image: "/static/images/friends/srinivas.jpeg" },
    { name: "JALLA BHARGAV", role: "Organizer", image: "/static/images/friends/bhargav.jpeg" },
    { name: "KOTIREDDY", role: "Designer", image: "/static/images/friends/koti.jpeg" },
    { name: "ASHWIN A", role: "Designer", image: "/static/images/friends/ashwin.jpeg" },
    { name: "PRAVEEN V M", role: "Designer", image: "/static/images/friends/cr.jpeg" },
    { name: "DEVDHARSHAN J", role: "Designer", image: "/static/images/friends/dev.jpeg" },
    { name: "GUGAN S", role: "Designer", image: "/static/images/friends/gugan.jpeg" },
    { name: "KAVIPRIYAN M", role: "Designer", image: "/static/images/friends/kavi.jpeg" },
    { name: "KUMARAGURUBARAN", role: "Designer", image: "/static/images/friends/kumaraguru.jpeg" },
    { name: "MUKESH R", role: "Designer", image: "/static/images/friends/mukesh.jpeg" },
    { name: "NAIFE KHAN M", role: "Designer", image: "/static/images/friends/naife.jpeg" },
    { name: "PRAKADESH", role: "Designer", image: "/static/images/friends/pragadeesh.jpeg" },
    { name: "PRAVEEN P", role: "Designer", image: "/static/images/friends/praveenp.jpeg" },
    { name: "SACHIN", role: "Designer", image: "/static/images/friends/sachin.jpeg" },
    { name: "JAYASURIYA G", role: "Designer", image: "/static/images/friends/surya.jpeg" },
    { name: "VIVEK REDDY", role: "Designer", image: "/static/images/friends/vivek.jpeg" },
    { name: "JAYANTH REDDY", role: "Designer", image: "/static/images/friends/jayanth.jpeg"},
    { name: "PRAKASH K", role: "Designer", image: "/static/images/friends/prakash.jpeg"},
    { name: "RAVICHANDRAN J", role: "Designer", image: "/static/images/friends/ravi.jpeg"},
    { name: "SANTHOSH", role: "Designer", image: "/static/images/friends/sandhosh.jpeg"},
    { name: "SANJAI KUMAR C", role: "Designer", image: "/static/images/friends/sanjay.jpeg"}
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
