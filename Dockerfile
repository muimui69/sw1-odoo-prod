# Usa la imagen base de Odoo versión 17
FROM odoo:17.0

USER root

# Actualiza e instala las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg && apt-get clean

# Actualiza pip e instala las dependencias de Python necesarias
RUN pip3 install --upgrade pip
RUN pip3 install python-dotenv 

# Instala whisper de OpenAI y las dependencias desde el repositorio
RUN pip3 install -U openai-whisper
RUN pip3 install cohere

# Instala PyTorch para CPU
RUN pip3 install torch==2.0.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install "numpy<2"

# Copia el archivo de configuración personalizado de Odoo
COPY ./config_odoo/odoo.conf /etc/odoo/odoo.conf

# Copia los módulos personalizados a la carpeta de addons
COPY ./modules /mnt/extra-addons

# Crea una carpeta para los logs de Odoo y ajusta los permisos
RUN mkdir -p /var/log/odoo && chown -R odoo: /var/log/odoo

# Define variables de entorno necesarias
ENV HOST=db
ENV USER=odoo
ENV PASSWORD=myodootest

# Exponer el puerto de Odoo
EXPOSE 8069

# Comando para iniciar Odoo con la ruta correcta a los módulos
# CMD ["python3", "/usr/bin/odoo", "-r", "odoo", "-w", "myodootest", "--addons-path=/mnt/extra-addons", "-d", "odoo", "-i", "base,ia"]
ENTRYPOINT ["/usr/bin/odoo", "-c", "/etc/odoo/odoo.conf"]