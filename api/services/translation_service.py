from transformers import MarianMTModel, MarianTokenizer
import torch


class TranslationService:

    def __init__(self):

        model_name = "Helsinki-NLP/opus-mt-bn-en"

        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

        # force CPU
        self.device = torch.device("cpu")
        self.model.to(self.device)

    def translate(self, text: str) -> str:

        if not text:
            return ""

        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)

            outputs = self.model.generate(**inputs)

            translated = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            return translated

        except Exception as e:
            print("[MarianMT Error]", repr(e))
            return ""