FROM python:3.10-slim

# -----------------------------
# Installation des dépendances système
# -----------------------------
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    bash \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Installation de Google Cloud CLI (inclut bq)
# -----------------------------
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Dossier de travail
# -----------------------------
WORKDIR /app

# -----------------------------
# Dépendances Python
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copier le projet
# -----------------------------
COPY . .

CMD ["bash"]
