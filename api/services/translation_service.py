import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


# =====================================
# MODEL CONFIG
# =====================================

MODEL_NAME = "facebook/m2m100_418M"
device = torch.device("cpu")


# =====================================
# LAZY SINGLETON MODEL
# =====================================

class TranslationService:

    _model = None
    _tokenizer = None

    @classmethod
    def load_model(cls):

        if cls._model is None:

            print("Loading M2M100 model... (first time only)")

            cls._tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME)
            cls._model = M2M100ForConditionalGeneration.from_pretrained(MODEL_NAME)

            cls._model.to(device)
            cls._model.eval()

            print("Translation model loaded ✔")

        return cls._model, cls._tokenizer


    # =========================
    # Bangla → English
    # =========================
    def translate(self, text: str) -> str:

        if not text:
            return ""

        try:

            model, tokenizer = self.load_model()

            tokenizer.src_lang = "bn"

            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            )

            inputs = {k: v.to(device) for k, v in inputs.items()}

            generated = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.get_lang_id("en"),
                max_length=128
            )

            return tokenizer.decode(
                generated[0],
                skip_special_tokens=True
            )

        except Exception as e:
            print("[BN->EN ERROR]", repr(e))
            return ""


    # =========================
    # English → Bangla
    # =========================
    def translate_en_to_bn(self, text: str) -> str:

        if not text:
            return ""

        try:

            model, tokenizer = self.load_model()

            tokenizer.src_lang = "en"

            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            )

            inputs = {k: v.to(device) for k, v in inputs.items()}

            generated = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.get_lang_id("bn"),
                max_length=128
            )

            return tokenizer.decode(
                generated[0],
                skip_special_tokens=True
            )

        except Exception as e:
            print("[EN->BN ERROR]", repr(e))
            return ""