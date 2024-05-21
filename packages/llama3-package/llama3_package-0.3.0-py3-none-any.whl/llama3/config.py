import os

class Config:
    MODEL_NAME = os.getenv("LLAMA3_MODEL_NAME", "llama3")

    @classmethod
    def from_env(cls):
        return cls(
            model_name=os.getenv("LLAMA3_MODEL_NAME", "llama3")
        )
