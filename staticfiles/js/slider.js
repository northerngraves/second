document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide-image');
  const indicators = document.querySelectorAll('.indicator');
  let currentIndex = 0;
  const slideInterval = 5000; // Интервал в миллисекундах (3000 мс = 3 секунды)

  function setActiveSlide(index) {
      slides.forEach((slide, idx) => {
          slide.style.opacity = '0'; // Сброс видимости всех слайдов
          indicators[idx].classList.replace('opacity-100', 'opacity-50'); // Сброс всех индикаторов
          if (idx === index) {
              slide.style.opacity = '1'; // Активный слайд делаем видимым
              indicators[idx].classList.replace('opacity-50', 'opacity-100'); // Подсветка активного индикатора
          }
      });
  }

  function moveToNextSlide() {
      currentIndex = (currentIndex < slides.length - 1) ? currentIndex + 1 : 0;
      setActiveSlide(currentIndex);
  }

  indicators.forEach((indicator, idx) => {
      indicator.addEventListener('click', () => {
          currentIndex = idx;
          setActiveSlide(currentIndex);
          restartAutoSlide(); // Перезапуск автопереключения после ручного управления
      });
  });

  document.querySelector('.prev').addEventListener('click', () => {
      currentIndex = currentIndex > 0 ? currentIndex - 1 : slides.length - 1;
      setActiveSlide(currentIndex);
      restartAutoSlide(); // Перезапуск автопереключения после ручного управления
  });

  document.querySelector('.next').addEventListener('click', () => {
      moveToNextSlide();
      restartAutoSlide(); // Перезапуск автопереключения после ручного управления
  });

  let autoSlide = setInterval(moveToNextSlide, slideInterval);

  function restartAutoSlide() {
      clearInterval(autoSlide);
      autoSlide = setInterval(moveToNextSlide, slideInterval);
  }

  setActiveSlide(currentIndex); // Показ первого слайда при загрузке
});

  document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide-image-2');
    const indicators = document.querySelectorAll('.indicator-2');
    let currentIndex = 0;
  
    function setActiveSlide(index) {
      slides.forEach((slide, idx) => {
        slide.style.opacity = '0'; // Сброс видимости всех слайдов
        indicators[idx].classList.replace('opacity-100', 'opacity-50'); // Сброс всех индикаторов
        if (idx === index) {
          slide.style.opacity = '1'; // Активный слайд делаем видимым
          indicators[idx].classList.replace('opacity-50', 'opacity-100'); // Подсветка активного индикатора
        }
      });
    }
  
    indicators.forEach((indicator, idx) => {
      indicator.addEventListener('click', () => {
        currentIndex = idx;
        setActiveSlide(currentIndex);
      });
    });
  
    document.querySelector('.prev-2').addEventListener('click', () => {
      currentIndex = currentIndex > 0 ? currentIndex - 1 : slides.length - 1;
      setActiveSlide(currentIndex);
    });
  
    document.querySelector('.next-2').addEventListener('click', () => {
      currentIndex = currentIndex < slides.length - 1 ? currentIndex + 1 : 0;
      setActiveSlide(currentIndex);
    });
  
    setActiveSlide(currentIndex); // Показ первого слайда при загрузке
  });