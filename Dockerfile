FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch first to avoid downloading 2GB of CUDA/GPU libraries
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Now install the rest
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]