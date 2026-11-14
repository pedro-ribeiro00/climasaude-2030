"""Carregamento local e resumo de texto com modelo Hugging Face."""

from functools import lru_cache

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"


@lru_cache(maxsize=1)
def carregar_modelo():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, local_files_only=True, torch_dtype="auto")
    model.eval()
    return tokenizer, model


def resumir_texto(texto: str) -> str:
    import torch

    tokenizer, model = carregar_modelo()
    mensagens = [
        {"role": "system", "content": "Resuma em português usando somente informações presentes no texto. Não invente fatos, números ou recomendações. Se não souber, não acrescente nada. Responda apenas com o resumo."},
        {"role": "user", "content": texto},
    ]
    prompt = tokenizer.apply_chat_template(mensagens, tokenize=False, add_generation_prompt=True)
    entrada = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    with torch.inference_mode():
        saida = model.generate(**entrada, max_new_tokens=160, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(saida[0][entrada["input_ids"].shape[1]:], skip_special_tokens=True).strip()
