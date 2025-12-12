// Part C: Robot Parallax Effect
document.addEventListener("mousemove", (e) => {
    const robotContainer = document.querySelector('.robot-container');
    if (robotContainer) {
        const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.01;
        robotContainer.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.015)`;
    }
});
