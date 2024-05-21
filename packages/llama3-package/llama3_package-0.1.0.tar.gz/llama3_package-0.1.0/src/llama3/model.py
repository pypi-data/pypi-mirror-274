import subprocess
import shutil
import platform
import time
import requests
from .config import Config
from .utils import logger
import atexit

class Llama3Model:
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.ollama_server_process = None
        self.ollama_process = None
        self._install_ollama()
        self._start_ollama_server()
        self._ensure_server_is_running()
        self._pull_model()
        self._start_ollama()
        logger.info(f"Initialized Llama3 model with model name: {self.model_name}")
        atexit.register(self._stop_ollama)

    def _install_ollama(self):
        system = platform.system()
        if system == "Linux":
            install_command = "curl -fsSL https://ollama.com/install.sh | sh"
        elif system == "Darwin":  # macOS
            install_command = "brew install ollama"
        else:
            raise EnvironmentError("Ollama installation is only supported on Linux and macOS.")

        if not shutil.which("ollama"):
            try:
                logger.info(f"Ollama not found. Installing Ollama on {system}...")
                subprocess.run(install_command, shell=True, check=True)
                logger.info("Ollama installed successfully.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing Ollama: {e}")
                raise

    def _start_ollama_server(self):
        try:
            logger.info("Starting Ollama server in the background...")
            self.ollama_server_process = subprocess.Popen(
                ["nohup", "ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info("Ollama server started successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error starting Ollama server: {e.stderr}")
            raise

    def _ensure_server_is_running(self, retries=5, delay=5):
        for attempt in range(retries):
            try:
                response = requests.get("http://127.0.0.1:11434/api/version")
                if response.status_code == 200:
                    logger.info("Ollama server is running.")
                    return True
            except requests.ConnectionError:
                logger.warning(f"Attempt {attempt + 1}/{retries}: Ollama server is not running yet. Retrying in {delay} seconds...")
                time.sleep(delay)
        raise RuntimeError("Ollama server did not start successfully.")

    def _pull_model(self):
        try:
            logger.info(f"Pulling model {self.model_name}...")
            subprocess.run(["ollama", "pull", self.model_name], check=True)
            logger.info(f"Model {self.model_name} pulled successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error pulling model: {e.stderr}")
            raise

    def _start_ollama(self):
        try:
            logger.info(f"Starting Ollama with model {self.model_name}...")
            self.ollama_process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Ollama started with model {self.model_name}.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error starting Ollama: {e.stderr}")
            raise

    def _stop_ollama(self):
        if self.ollama_process:
            logger.info("Stopping Ollama...")
            self.ollama_process.terminate()
            self.ollama_process.wait()
            logger.info("Ollama stopped.")
        if self.ollama_server_process:
            logger.info("Stopping Ollama server...")
            self.ollama_server_process.terminate()
            self.ollama_server_process.wait()
            logger.info("Ollama server stopped.")

    def prompt(self, text):
        try:
            logger.info(f"Sending prompt: {text}")
            process = subprocess.run(["ollama", "run", self.model_name], input=text, text=True, capture_output=True, check=True)
            logger.info(f"Prompt successful: {text}")
            return process.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error in prompt: {e.stderr}")
            raise

    def stream_prompt(self, text):
        try:
            logger.info(f"Starting streaming prompt: {text}")
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            process.stdin.write(text)
            process.stdin.close()
            for line in process.stdout:
                yield line.strip()
            logger.info(f"Streaming prompt successful: {text}")
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    returncode=process.returncode,
                    cmd=process.args,
                    output=process.stdout.read(),
                    stderr=process.stderr.read()
                )
        except subprocess.CalledProcessError as e:
            logger.error(f"Error in stream_prompt: {e.stderr}")
            raise
