// Asocia la función predict al evento input de cada campo del formulario
/*document.querySelectorAll('#plant-form input').forEach(input => {
    input.addEventListener('input', predict);
});*/

const API_BASE_URL = (window.__APP_CONFIG__ && window.__APP_CONFIG__.API_BASE_URL)
    ? window.__APP_CONFIG__.API_BASE_URL.replace(/\/$/, '')
    : (window.location.hostname === 'localhost'
        ? 'http://localhost:5003'
        : `${window.location.origin}`);

const PREDICT_ENDPOINT = `${API_BASE_URL}/predict`;

async function predict() {
    document.getElementById('loading').style.display = 'block';

    document.getElementById('result').innerHTML = '';
    document.getElementById('error').innerHTML = '';

    document.getElementById("plantViewer").style.display="none";
    document.getElementById("factores").style.display="none";
    document.getElementById("menuEtapas").style.display="none";
    document.getElementById("logoUsb").style.width="15%";

    const data = {
        temperatura: parseFloat(document.getElementById('temperatura').value),
        humedad_suelo: parseFloat(document.getElementById('humedad_suelo').value),
        humedad_ambiente: parseFloat(document.getElementById('humedad_ambiente').value),
        luz: parseFloat(document.getElementById('luz').value),
        ph_suelo: parseFloat(document.getElementById('ph_suelo').value),
        co2: parseFloat(document.getElementById('co2').value),
        nitrogeno: parseFloat(document.getElementById('nitrogeno').value),
        fosforo: parseFloat(document.getElementById('fosforo').value),
        potasio: parseFloat(document.getElementById('potasio').value)
    };
    console.log("Datos enviados:", JSON.stringify(data, null, 2));
    try {
        const response = await fetch(PREDICT_ENDPOINT, {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "text/xml",
                "X-PINGOTHER": "pingpong",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }

        const result = await response.json();
        document.getElementById('loading').style.display = 'none';

        document.getElementById('result').innerHTML = `
                    <h4>Resultados:</h4>
                    <p><strong>Porcentaje de Supervivencia Predicho:</strong> ${result.prediction_result['Porcentaje de Supervivencia Predicho']}</p>
                    <p><strong>Estado de Vida Predicho:</strong> ${result.prediction_result['Estado de Vida Predicho']}</p>
                `;

        document.getElementById('resultGPT').innerHTML = `
                    <p>${result.gpt_response}</p>
                `;

        document.getElementById('resultVariables').innerHTML = `
            <h4>Estado de Variables:</h4>
            <table>
                <thead>
                    <tr>
                        <th>Característica</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(result.prediction_result['Estado de Variables']).map(([key, value]) => `
                        <tr>
                            <td>${key.charAt(0).toUpperCase() + key.slice(1)}</td>
                            <td>${value}</td>
                            </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('plantViewer2').style.display = 'block';

        const modelViewer2 = document.getElementById('plantViewer2');
        const statusPlant = `${result.prediction_result['Estado de Vida Predicho']}`;
        let base = null;

        switch(statusPlant) {
            case "Óptimo":
                base = "../src/" + "bean/Frijol_6";
              break;
            case "Estable":
                base = "../src/" + "bean/Frijol_5";
              break;
            default:
            case "Malo":
                base = "../src/" + "bean/planta_final_MUERE";
              break;
          }

        modelViewer2.src = base + '.glb';

        leerTexto();


        document.getElementById('content3D').style.display = 'block';
        document.getElementById('contentText').style.display = 'block';

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').innerHTML = 'Ocurrió un error. Inténtalo de nuevo más tarde.';
        console.error('Error:', error);
    }
}

function leerTexto() {
    const texto = document.getElementById("resultGPT").innerText;
    const speech = new SpeechSynthesisUtterance(texto);
    speech.lang = 'es-ES';  // Establece el idioma (en este caso, español)
    window.speechSynthesis.speak(speech);

    document.getElementsByName('voicePlay')[0].style.display = 'none';
    document.getElementsByName('voiceStop')[0].style.display = 'inline-flex';

}

function detenerTexto() {
    window.speechSynthesis.cancel();  // Detiene la lectura actual

    document.getElementsByName('voicePlay')[0].style.display = 'inline-flex';
    document.getElementsByName('voiceStop')[0].style.display = 'none';
}

detenerTexto();

document.getElementById("modalEstandar").click();
