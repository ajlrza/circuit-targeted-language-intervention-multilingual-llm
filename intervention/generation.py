import math

import torch


@torch.no_grad()
def generate(model, tok, prompts, max_new_tokens=60, batch_size=32):
    tok.padding_side = "left"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    out = []
    for s in range(0, len(prompts), batch_size):
        batch = tok(prompts[s:s + batch_size], return_tensors="pt", padding=True).to(model.device)
        ids = model.generate(**batch, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tok.pad_token_id)
        out += [[t for t in row if t != tok.pad_token_id] for row in ids[:, batch["input_ids"].shape[1]:].tolist()]
    return out


@torch.no_grad()
def perplexity(model, tok, texts, batch_size=32):
    tok.padding_side = "right"
    nll, n = 0.0, 0
    for s in range(0, len(texts), batch_size):
        batch = tok(texts[s:s + batch_size], return_tensors="pt", padding=True).to(model.device)
        logits = model(**batch).logits[:, :-1].float()
        target, mask = batch["input_ids"][:, 1:], batch["attention_mask"][:, 1:].bool()
        lp = torch.log_softmax(logits, -1).gather(-1, target[..., None])[..., 0]
        nll -= lp[mask].sum().item()
        n += mask.sum().item()
    return math.exp(nll / n)
