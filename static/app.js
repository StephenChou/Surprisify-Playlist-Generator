const navSlide = () => {
	const burger = document.querySelector('.burger');
	const nav = document.querySelector('.nav-links');
	const navLinks = document.querySelectorAll('.nav-links li');
	const navbar = document.querySelector('.navbar')
	//Toggle nav

	burger.addEventListener('click', ()=> {
		

		nav.classList.toggle('nav-link-active');
		// navbar.classList.toggle('nav-active');

			//Animate links
		navLinks.forEach((link, index)=>{

			if (link.style.animation) {
				link.style.animation = ''
			} else {
				link.style.animation=`navLinkFade 0.5s ease forwards ${index / 5}s`; 
			}
		});
		//Burger animation
		burger.classList.toggle('toggle');
		navbar.classList.toggle('navbar-background')


	});

	// navLinks.forEach(link => link.addEventListener("click", ()=> {
	// 	nav.classList.remove('nav-link-active');
	// 	burger.classList.remove('toggle');

	// 	}));

	  navLinks.forEach((link) => {
    	link.addEventListener("click", (e) => {
      	navLinks.forEach((link) => {
        link.style.animation = "";
      });
      nav.classList.remove("nav-link-active");
      burger.classList.remove("toggle");
      navbar.classList.remove('navbar-background')

    });
  });

}




navSlide();