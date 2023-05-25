const querySelector = (className) => document.querySelector(className)

const aboutSection = [
  querySelector('.about__content-title'),
  querySelector('.about__content-info'),
]

const testimonialSection = [
  querySelector('.testimonios__cards-card_left'),
  querySelector('.testimonios__cards-card_right'),
]

ScrollReveal().reveal(aboutSection, {
  origin: 'left',
  delay: 500,
  distance: '100px',
  duration: 1500,
  interval: 500,
})

ScrollReveal().reveal(testimonialSection, {
  origin: 'left',
  delay: 500,
  distance: '100px',
  duration: 1500,
  interval: 500,
})

ScrollReveal().reveal(querySelector('.testimonios__cards-card_center'), {
  origin: 'right',
  delay: 500,
  distance: '100px',
  duration: 1500,
  interval: 500,
})
