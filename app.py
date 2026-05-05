from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# ==================================================
# DATOS DE TELEGRAM
# ==================================================
BOT_TOKEN = "8765396518:AAHqPOnZ6bnKWaIfh_u5xOm3aNr--IxRNwU"
CHAT_ID = "-5162450661"

# ==================================================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timbre Vecinal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #075E54 0%, #128C7E 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: system-ui, sans-serif;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 48px;
            padding: 50px 40px;
            text-align: center;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
        }
        h1 { color: #075E54; font-size: 32px; margin-bottom: 16px; }
        .sub { color: #666; font-size: 16px; margin-bottom: 30px; }
        button {
            background-color: #25D366;
            color: white;
            border: none;
            padding: 22px 30px;
            font-size: 26px;
            font-weight: bold;
            border-radius: 80px;
            width: 100%;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 10px 25px -5px rgba(37,211,102,0.4);
        }
        button:active { transform: scale(0.97); }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        .mensaje {
            margin-top: 30px;
            padding: 15px;
            border-radius: 24px;
            font-size: 15px;
            display: none;
        }
        .footer { margin-top: 35px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔔 ¿ALGUIEN EN LA PUERTA?</h1>
        <div class="sub">Presiona el botón para avisar a los vecinos</div>
        <button id="botonAvisar">📢 DAR AVISO</button>
        <div id="estado" class="mensaje"></div>
        <div class="footer">Los vecinos recibirán el aviso en Telegram</div>
    </div>

    <script>
        const boton = document.getElementById('botonAvisar');
        const estadoDiv = document.getElementById('estado');

        async function enviarAviso() {
            boton.disabled = true;
            estadoDiv.style.display = 'block';
            estadoDiv.style.background = '#FFF3CD';
            estadoDiv.style.color = '#856404';
            estadoDiv.textContent = '📡 Enviando aviso...';

            try {
                const respuesta = await fetch('/timbre', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const datos = await respuesta.json();

                if (respuesta.ok) {
                    estadoDiv.style.background = '#D4EDDA';
                    estadoDiv.style.color = '#155724';
                    estadoDiv.textContent = datos.mensaje;
                } else {
                    estadoDiv.style.background = '#F8D7DA';
                    estadoDiv.style.color = '#721C24';
                    estadoDiv.textContent = '❌ ' + datos.mensaje;
                }
            } catch (error) {
                estadoDiv.style.background = '#F8D7DA';
                estadoDiv.style.color = '#721C24';
                estadoDiv.textContent = '❌ Error de conexión';
            }

            setTimeout(() => {
                boton.disabled = false;
                setTimeout(() => { estadoDiv.style.display = 'none'; }, 3000);
            }, 3000);
        }

        boton.addEventListener('click', enviarAviso);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/timbre', methods=['POST'])
def timbre():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "🔔 AVISO: Alguien está en la puerta del edificio"
    }
    try:
        respuesta = requests.post(url, data=data, timeout=10)
        if respuesta.status_code == 200:
            return {"mensaje": "✅ Aviso enviado al grupo de Telegram"}
        else:
            return {"mensaje": f"❌ Error {respuesta.status_code}"}, 500
    except Exception as e:
        return {"mensaje": "❌ Error de conexión"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
