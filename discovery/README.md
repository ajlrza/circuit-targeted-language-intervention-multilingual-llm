# Qwen2.5-1.5B EN→ES Circuit Discovery Pilot

This directory contains the first circuit-discovery pilot for
`Qwen/Qwen2.5-1.5B`.

## Language metric

The discovery objective uses an English-vs-Spanish token-set log-probability
metric derived from FLORES-200. On held-out language prefixes, the metric
achieved 97.5% sign accuracy.

## Attribution and exact validation

Attention-head outputs were evaluated at the final prompt position using
clean Spanish vs. corrupted English activation differences.

For the top 30 head-output candidates, attribution scores correlated strongly
with exact activation-patching effects:

- Spearman rho: 0.8412
- p-value: 5.87e-09

## Selected pilot circuit

- L16H9
- L17H7
- L22H6
- L25H10
- L27H6

The machine-readable head set is stored in
`results/qwen25_en_es_heads.json`.

## Held-out validation

The selected circuit was frozen after discovery and evaluated on 50 disjoint
FLORES examples (indices 100–149), against 100 size- and layer-matched random
head sets.

Spanish activations patched into English prompts:

- mean effect: +1.2216
- 95% bootstrap CI: [+1.0542, +1.3983]
- random-control 95th percentile: +0.0989
- percentile vs. random controls: 100%

English activations patched into Spanish prompts:

- mean effect: +0.8613
- 95% bootstrap CI: [+0.4062, +1.3958]
- random-control 95th percentile: +0.1101
- percentile vs. random controls: 100%

Both held-out validation criteria exceed the 95th percentile of the matched
random controls.

This is a single-language-pair pilot and should be treated as an initial
Qwen2.5 circuit candidate pending replication across additional language
pairs and intervention evaluation.
