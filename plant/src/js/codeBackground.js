    const modelViewer = document.getElementById('plantViewer');
    let time = Date.now();
    
    function oscillate(min, max, duration, elapsed) {
      const range = max - min;
      const halfRange = range / 2;
      return min + halfRange + halfRange * Math.sin((elapsed / duration) * Math.PI * 2);
    }

    function animateExposure() {
      const now = Date.now();
      const elapsed = now - time;
      //modelViewer.environmentImage = '../src/img/hdr/night.jpg';
      modelViewer.exposure = oscillate(0.1, 1, 10000, elapsed);
      requestAnimationFrame(animateExposure);

    }