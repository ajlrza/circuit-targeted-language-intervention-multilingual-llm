# Step 2: intervention and eval harness

How much each intervention reduces code-switching on Qwen2.5-1.5B, and what it costs.

## Interventions (`hooks.py`)
- `ResidualSteer`: steering from Goncharov et al. 2025 (arXiv 2510.13849), same as their code: `h + c ((h - mu) . v) v` on the outputs of layers 26 and 27.
- `HeadSteer`: the same transform through selected heads' `W_O` only. `c = -1` removes `v` from those heads.
- `HeadScale`: scales selected heads.

`v` is PC1 of a per-layer PCA over FLORES-200 dev tokens of both languages. Their code steers layer `l` with the PCA of `hidden_states[l]`, i.e. the previous layer's output. `residual` keeps that, since it reproduces their KL numbers (`kl_check.py`). `resid_own` and the head interventions use each layer's own output. The last layer is read before the final norm, because HF returns it normed.

## Eval (`run_pilot.py`)
- Effect: TED prompts from their repo that start in English and switch to `--lang` halfway. CSI is the share of non-English tokens in the continuation. `csi` is their version (fastText `lid.176`, 5 subword tokens, any label). `csi_pair` uses 5 words and only the two languages, and is the one to read.
- Side effects: CSI on the all-English version of the same prompts, FLORES-200 devtest perplexity in both languages, repeated 4-grams.
- Controls: `random*` takes the same number of heads from the same layers (10 distinct draws), `nearby*` from the layer above or below (5 draws). `summary.json` lists where the selected heads fall among them.

Without `--heads-json` the head set is a stand-in, ranked by how differently each head writes along `v` for the two languages. Since it is picked with the same `v` it is steered with, its edge over the controls is partly built in. Use the step 1 circuit for real runs: `{"heads": {"27": [0, 3]}}`.

## Caveats
- TED prompts end in the switched language, so this measures going back to English, not ignoring an instructed language (LCB would).
- When the selected heads fill most of a layer, same-layer draws overlap; that is what `nearby*` is for.

## Run
```
pip install torch transformers scikit-learn fasttext-wheel
python -m intervention.kl_check --lang es
python -m intervention.run_pilot --lang es --n-eval 50 --head-min-layer 14
```
Data downloads into `CTLI_DATA` (default `.data/`) on first use. Results go to `results/`, written per condition to `rows.jsonl` and `samples.jsonl` and summarized at the end in `summary.json`.

`lid.py` and `metrics.py` are adapted from github.com/fxlrnrpt/language-steering-in-latent-space (MIT).
