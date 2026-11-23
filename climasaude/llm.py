"""Carregamento local e resumo de texto com modelo Hugging Face."""

from functools import lru_cache
from threading import Lock
import os

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
GERACAO_LOCK = Lock()
LIMITE_ENTRADA = 2048


@lru_cache(maxsize=1)
def carregar_modelo():
    import torch
    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # O caminho local também evita consultas de metadados do tokenizer à rede.
    pasta = snapshot_download(MODEL_ID, local_files_only=True)
    torch.set_num_threads(int(os.getenv("CLIMASAUDE_CPU_THREADS", "2")))
    tokenizer = AutoTokenizer.from_pretrained(pasta, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(pasta, local_files_only=True, torch_dtype="auto")
    model.eval()
    return tokenizer, model


def dividir_texto(texto: str, limite: int = 1400) -> list[str]:
    """Divide pelo tokenizer real, preservando todos os caracteres e sua ordem."""
    tokenizer, _ = carregar_modelo()
    blocos = []
    while texto:
        inicio, fim = 1, len(texto)
        while inicio <= fim:
            meio = (inicio + fim) // 2
            if len(tokenizer.encode(texto[:meio], add_special_tokens=False)) <= limite:
                inicio = meio + 1
            else:
                fim = meio - 1
        if fim < 1:
            raise ValueError("Não foi possível dividir o texto no limite de tokens")
        blocos.append(texto[:fim])
        texto = texto[fim:]
    return blocos


def resumir_bloco(texto: str, *, instrucao: str | None = None, max_tokens: int = 240) -> str:
    import torch

    tokenizer, model = carregar_modelo()
    mensagens = [
        {"role": "system", "content": instrucao or "Resuma em português usando somente informações presentes no texto. Não invente fatos, números ou recomendações. Se não souber, não acrescente nada. Responda apenas com o resumo."},
        {"role": "user", "content": texto},
    ]
    prompt = tokenizer.apply_chat_template(mensagens, tokenize=False, add_generation_prompt=True)
    entrada = tokenizer(prompt, return_tensors="pt", truncation=False)
    if entrada["input_ids"].shape[1] > LIMITE_ENTRADA:
        raise ValueError("Entrada excede o limite de tokens; divida o texto antes da geração")
    with GERACAO_LOCK, torch.inference_mode():
        saida = model.generate(**entrada, max_new_tokens=max_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    finais = model.generation_config.eos_token_id
    finais = finais if isinstance(finais, list) else [finais]
    if saida[0, -1].item() not in finais:
        raise ValueError("O modelo atingiu o limite de saída sem concluir o resumo")
    return tokenizer.decode(saida[0][entrada["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def resumir_texto(texto: str) -> str:
    blocos = dividir_texto(texto)
    return "\n\n".join(resumir_bloco(bloco) for bloco in blocos)


def selecionar_trecho(trechos: list[str], contexto: str) -> str:
    """O Qwen escolhe um índice; só o texto original pode compor a síntese."""
    import torch

    tokenizer, model = carregar_modelo()
    mensagens = [
        {"role": "system", "content": (
            "Selecione o trecho mais relevante sobre calor, saúde e prevenção, "
            "considerando o contexto climático. Prefira orientações gerais a alertas "
            "antigos ou referências bibliográficas. Responda somente com o número do trecho."
        )},
        {"role": "user", "content": f"CONTEXTO:\n{contexto}\n\nTRECHOS:\n" + "\n".join(
            f"{i}: {texto}" for i, texto in enumerate(trechos, 1)
        )},
    ]
    prompt = tokenizer.apply_chat_template(mensagens, tokenize=False, add_generation_prompt=True)
    entrada = tokenizer(prompt, return_tensors="pt", truncation=False)
    if entrada["input_ids"].shape[1] > LIMITE_ENTRADA:
        raise ValueError("Trechos e contexto excedem o limite de tokens")
    opcoes = [tokenizer.encode(str(i), add_special_tokens=False) for i in range(1, len(trechos) + 1)]
    tamanho = entrada["input_ids"].shape[1]

    def permitidos(_, ids):
        prefixo = ids[tamanho:].tolist()
        proximos = {seq[len(prefixo)] for seq in opcoes if seq[:len(prefixo)] == prefixo and len(seq) > len(prefixo)}
        if prefixo in opcoes:
            proximos.add(tokenizer.eos_token_id)
        return sorted(proximos)

    with GERACAO_LOCK, torch.inference_mode():
        saida = model.generate(
            **entrada, do_sample=False, max_new_tokens=max(map(len, opcoes)) + 1,
            prefix_allowed_tokens_fn=permitidos, pad_token_id=tokenizer.eos_token_id,
        )
    indice = int(tokenizer.decode(saida[0][tamanho:], skip_special_tokens=True).strip())
    return trechos[indice - 1]
