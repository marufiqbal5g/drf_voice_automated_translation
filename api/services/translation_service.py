import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
from transformers import MarianMTModel, MarianTokenizer

MODEL_NAME = "Helsinki-NLP/opus-mt-bn-en"


# -----------------------------
# LOAD MODEL ONCE (GLOBAL)
# -----------------------------
print("Loading MarianMT model...")

tokenizer = MarianTokenizer.from_pretrained(
    MODEL_NAME
)

model = MarianMTModel.from_pretrained(
    MODEL_NAME
)

device = torch.device("cpu")

model.to(device)

model.eval()

print("MarianMT ready ✔")


class TranslationService:

    def translate(self, text: str) -> str:

        if not text:
            return ""

        try:

            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            )

            inputs = {
                k: v.to(device)
                for k, v in inputs.items()
            }

            with torch.no_grad():

                outputs = model.generate(
                    **inputs,
                    max_length=128
                )

            return tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

        except Exception as e:

            print("[Marian Error]", repr(e))

            return ""