const menuButton = document.querySelector(".menu-btn");
const menu = document.querySelector(".main-menu");
const backdrop = document.querySelector(".nav-backdrop");
const menuLinks = document.querySelectorAll(".main-menu a");
const flashStack = document.querySelector(".flash-stack");

if (menuButton && menu && backdrop) {
  const setMenuState = (isOpen) => {
    menu.classList.toggle("show", isOpen);
    backdrop.hidden = !isOpen;
    backdrop.classList.toggle("is-visible", isOpen);
    menuButton.setAttribute("aria-expanded", String(isOpen));
    document.body.classList.toggle("nav-open", isOpen);
  };

  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    setMenuState(!isOpen);
  });

  backdrop.addEventListener("click", () => setMenuState(false));

  menuLinks.forEach((link) => {
    link.addEventListener("click", () => setMenuState(false));
  });
}

if (flashStack) {
  window.setTimeout(() => {
    const removeFlash = () => flashStack.remove();
    flashStack.classList.add("is-dismissing");
    flashStack.addEventListener("transitionend", removeFlash, { once: true });
    window.setTimeout(removeFlash, 300);
  }, 5000);
}
