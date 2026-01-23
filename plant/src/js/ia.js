// Attach the predict function to each form input if live updates are required
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
    console.log("Payload sent:", JSON.stringify(data, null, 2));
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
            throw new Error('Request failed');
        }

        const result = await response.json();
        document.getElementById('loading').style.display = 'none';

        document.getElementById('result').innerHTML = `
                    <h4>Results:</h4>
                    <p><strong>Predicted Survival Percentage:</strong> ${result.prediction_result['Predicted Survival Percentage']}</p>
                    <p><strong>Predicted Life Status:</strong> ${result.prediction_result['Predicted Life Status']}</p>
                `;

        document.getElementById('resultGPT').innerHTML = `
                    <p>${result.gpt_response}</p>
                `;

        document.getElementById('resultVariables').innerHTML = `
            <h4>Variable Statuses:</h4>
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(result.prediction_result['Variable Statuses']).map(([key, value]) => `
                        <tr>
                            <td>${key}</td>
                            <td>${value}</td>
                            </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('plantViewer2').style.display = 'block';

        const modelViewer2 = document.getElementById('plantViewer2');
                const statusPlant = `${result.prediction_result['Predicted Life Status']}`;
        let base = null;

        switch(statusPlant) {
                        case "Optimal":
                base = "../src/" + "bean/Frijol_6";
              break;
                        case "Stable":
                base = "../src/" + "bean/Frijol_5";
              break;
            default:
                        case "Dead":
                        case "Poor":
                base = "../src/" + "bean/planta_final_MUERE";
              break;
          }

        modelViewer2.src = base + '.glb';

        leerTexto();


        document.getElementById('content3D').style.display = 'block';
        document.getElementById('contentText').style.display = 'block';

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').innerHTML = 'An error occurred. Please try again later.';
        console.error('Error:', error);
    }
}

function leerTexto() {
    const texto = document.getElementById("resultGPT").innerText;
    const speech = new SpeechSynthesisUtterance(texto);
    speech.lang = 'en-US';  // Set speech language to English
    window.speechSynthesis.speak(speech);

    document.getElementsByName('voicePlay')[0].style.display = 'none';
    document.getElementsByName('voiceStop')[0].style.display = 'inline-flex';

}

function detenerTexto() {
    window.speechSynthesis.cancel();  // Stop the current narration

    document.getElementsByName('voicePlay')[0].style.display = 'inline-flex';
    document.getElementsByName('voiceStop')[0].style.display = 'none';
}

detenerTexto();

document.getElementById("modalEstandar").click();
