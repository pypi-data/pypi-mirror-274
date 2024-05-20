# jota_os/ai_runner.py
from jpu.api import jpuAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class AIRunner:
    def __init__(self):
        self.api = jpuAPI() 
        self.model_id = "mistralai/Mistral-7B-v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, torch_dtype=torch.float16).to('cuda')

    def load_model(self, model_name):
        """Load a Hugging Face model."""
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def run_inference(self, input_text):
        """Run inference on the loaded model."""
        inputs = self.tokenizer(input_text, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
