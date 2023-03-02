# TODO: replace FROM
FROM dleongsh/torchaudio:0.11.0

# Install libsndfile1 (linux soundfile package)
RUN apt-get update && apt-get install -y gcc libsndfile1 ffmpeg wget sox \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "src/app.py"]
