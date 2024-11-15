import json
import requests
import os
import uuid
import re
import whisper
import cohere
import mimetypes
from odoo import http
from odoo.http import request
from dotenv import load_dotenv
import torch

load_dotenv()


if not torch.cuda.is_available():
    torch.device("cpu")
    torch.set_default_tensor_type(torch.FloatTensor)

model = whisper.load_model("base")

class IAProcessingController(http.Controller):
    
    @http.route('/web/test_endpoint', type='http', auth='public', methods=['GET'], csrf=False)
    def test_endpoint(self):
        return request.make_response(
            '{"message": "Este es un endpoint GET de prueba en Odoo", "status": "success"}',
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/web/generate_image_cover', type='json', auth='public', methods=['POST'], csrf=False)
    def generate_image_cover(self, **kwargs):
        subject = kwargs.get('subject')
        if not subject:
            return {"error": "Falta el parámetro 'subject' para generar la carátula"}, 400

        safe_subject = re.sub(r'[^a-zA-Z0-9_-]', '_', subject)
        
        unique_id = uuid.uuid4().hex  
        
        filename = f"{safe_subject}_{unique_id}_cover.png"
        
        stable_difusion_api_key = os.getenv("STABLE_DIFUSION_API_KEY")
        stable_diffusion_api_url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
        headers = {
            "authorization": f"Bearer {stable_difusion_api_key}",
            "accept": "image/*"
        }
        
        files = {
            "none": ''  
        }
        data = {    
            "prompt": f"Cover for the subject of {subject.upper()}, modern design, detailed and professional background, illustrations related to {subject.upper()}, educational and academic aesthetics, vibrant yet elegant colors, high-quality graphic style, student-oriented.",
            "output_format": "png"
        }

        try:
            response = requests.post(stable_diffusion_api_url, headers=headers, files=files, data=data)
            response.raise_for_status()

            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'img')
            image_path = os.path.join(base_path, filename)

            if not os.path.exists(base_path):
                os.makedirs(base_path)

            with open(image_path, "wb") as file:
                file.write(response.content)

            image_url = f"{request.httprequest.host_url}ia/static/img/{filename}"

            return {
                "message": "Carátula generada exitosamente",
                "image_url": image_url  
            }

        except requests.RequestException as e:
            return {"error": f"Error en la API de Stable Diffusion: {str(e)}"}, 500
        
        
        
    @http.route('/web/generate_audio_quiz', type='http', auth='public', methods=['POST'], csrf=False)
    def process_audio(self, **kwargs):
        try:
            audio_file = request.httprequest.files.get('audio')
            if not audio_file:
                return request.make_response(
                    "Falta el archivo de audio para el procesamiento", 
                    headers={'Content-Type': 'text/plain'},
                    status=400
                )

            extension = mimetypes.guess_extension(audio_file.content_type)
            
            if not extension:
                return request.make_response(
                    "Tipo de archivo no soportado", 
                    headers={'Content-Type': 'text/plain'},
                    status=400
                )
        
        
            filename = f"audio_{uuid.uuid4().hex}{extension}"
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'audio')
            audio_path = os.path.join(base_path, filename)

            if not os.path.exists(base_path):
                os.makedirs(base_path)

            with open(audio_path, "wb") as f:
                f.write(audio_file.read())

            # model = whisper.load_model("small")
            result = model.transcribe(audio_path)
            transcription = result["text"]
            print("Transcripción:", transcription)

            co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
            prompt = (
                "Lee el siguiente texto y genera un cuestionario didáctico de 5 a 10 preguntas sobre los temas mencionados. "
                "Incluye diferentes tipos de preguntas, como selección múltiple, verdadero o falso y preguntas abiertas. "
                "Asegúrate de que las preguntas se enfoquen en los conceptos clave y puntos discutidos en el texto.\n\n"
                + transcription
            )
            
            response = co.chat(
                model="command-r-plus-08-2024",
                messages=[{"role": "user", "content": prompt}],
            )
            
            questions_text = response.message.content[0].text
            print("Texto de preguntas generado:", questions_text)
            
            questions = [q.replace("\n", " ") for q in questions_text.split("\n\n")]
            
            
            response_data = {
                "message": "Audio procesado exitosamente",
                "questions": questions
            }
             
            return request.make_response(
                json.dumps(response_data, indent=4, ensure_ascii=False),
                headers={'Content-Type': 'application/json'},
            )
        except Exception as e:
            print("Error general:", e)
            error_data = {
                "error": f"Error en el procesamiento del audio o generación del cuestionario: {str(e)}"
            }
            return request.make_response(
                json.dumps(error_data, indent=4, ensure_ascii=False),
                headers={'Content-Type': 'application/json'},
                status=500
            )
