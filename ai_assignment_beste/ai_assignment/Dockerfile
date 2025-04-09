# Use an official Jupyter Notebook base image
FROM jupyter/base-notebook

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your project folder to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Jupyter Notebook
EXPOSE 8888

# Default command: Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
