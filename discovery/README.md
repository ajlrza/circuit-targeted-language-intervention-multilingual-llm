# Qwen2.5-1.5B EN→ES Circuit Discovery Pilot

This directory contains the first circuit-discovery and validation pilot for
`Qwen/Qwen2.5-1.5B`.

## Language metric

The discovery objective uses an English-vs-Spanish token-set log-probability
metric derived from FLORES-200. The metric achieved 97.5% sign accuracy on
held-out English and Spanish prefixes.

## Head discovery

Attention-head outputs were screened using first-order attribution and then
validated with exact activation patching.

Across the top 30 head-output candidates:

- Spearman rho between attribution and exact effects: 0.8412
- p-value: 5.87e-09

The resulting five-head pilot circuit is:

- L16H9
- L17H7
- L22H6
- L25H10
- L27H6

The intervention-compatible head set is stored in
`results/qwen25_en_es_heads.json`.

## Held-out head-level validation

The five heads were frozen after discovery and evaluated on 50 disjoint
FLORES examples against 100 size- and layer-matched random head sets.

Spanish activations patched into English prompts:

- mean effect: +1.2216
- 95% bootstrap CI: [+1.0542, +1.3983]
- random-control 95th percentile: +0.0989

English activations patched into Spanish prompts:

- mean effect: +0.8613
- 95% bootstrap CI: [+0.4062, +1.3958]
- random-control 95th percentile: +0.1101

Both directions exceeded the 95th percentile of the matched random controls.

## Source-to-destination path validation

Source-head interventions were propagated through the model and the resulting
change in a selected downstream head was isolated with destination-head
patching.

Five candidate paths were frozen after discovery and evaluated on a disjoint
40-example holdout set with source-layer- and destination-layer-matched random
head-pair controls.

Three paths passed all held-out gates:

- L16H9 → L25H10
- L17H7 → L25H10
- L22H6 → L25H10

Their held-out mean effects were +0.0072, +0.0129, and +0.0078 respectively,
with bootstrap confidence intervals excluding zero and effects above the
95th percentile of their matched random controls.

## L25H10 convergence motif

The three validated source paths converge on L25H10. The frozen convergence
motif was evaluated on another disjoint 40-example holdout set.

Combined motif effect:

- mean effect: +0.0146
- 95% bootstrap CI: [+0.0061, +0.0240]

Controls:

- fixed L25H10 destination with randomized source heads:
  95th percentile = +0.0017
- fixed source heads with randomized layer-25 destination heads:
  95th percentile = +0.0047

The selected motif exceeded both control distributions.

The compact circuit description is stored in
`results/qwen25_en_es_circuit.json`.

## Scope

These results establish a held-out EN→ES pilot circuit in Qwen2.5-1.5B.
Replication across additional language pairs and downstream intervention
evaluation are required before making broader claims about multilingual
language-identity circuitry.
