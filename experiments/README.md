# Config-driven experiment runner and result aggregation

Runs `intervention.run_pilot` for a grid of models and language pairs from one config file, records exactly what was run,
and aggregates every finished run into one report. `intervention/` and `discovery/` are not modified.

## Run
```
python -m experiments.run experiments/configs/en_es_circuit.yaml --list
python -m experiments.run experiments/configs/en_es_circuit.yaml --dry-run
python -m experiments.run experiments/configs/en_es_circuit.yaml --aggregate
python -m experiments.aggregate results/experiments/en_es_circuit
pytest -q tests/test_experiments.py
```
Options: `--only <substring ...>` runs matching run ids, `--force` ignores the cache, `--stop-on-error` halts at the first failure,
`--root` overrides the output root. The exit code is 1 if any run failed.

## Config
| key | meaning |
|---|---|
| `name` | output folder name under `output_root` |
| `runner` | module (`intervention.run_pilot`) or path to a `.py` file |
| `models` | alias to Hugging Face id |
| `defaults` | any `run_pilot` option (`n_eval`, `head_coefs`, `steer_layers`, `seed`, ...); lists become comma strings |
| `matrix` | cross product of `model`, `lang` and any other key, for example `seed: [0, 1, 2]` |
| `runs` | extra explicit runs; add a `tag` if the model and language repeat |
| `overrides` | `match` / `set` pairs, for example the per-language residual coefficient from the steering paper |
| `heads_json` | path template using `{model}` and `{lang}` |
| `on_missing_heads` | `error` (default), `standin` (let `run_pilot` pick stand-in heads) or `skip` |
| `allow_head_mismatch` | disable the check that a heads file's `model` and `language_pair` match the run |

Run ids look like `qwen25_en_es` and gain `_seed1`-style suffixes for any extra matrix key.

## What is recorded
Each run writes `results/experiments/<name>/<run_id>/manifest.json` with the resolved arguments, the command, git commit, package versions,
head source (`circuit` or `standin`), a fingerprint of arguments and heads file, status, return code and duration, plus `run.log`.
A run is skipped when its manifest says `done` with the same fingerprint and `summary.json` exists. Changing any argument or the heads file re-runs it.

## Aggregation
`aggregate/runs.csv` has one row per run, `aggregate/conditions.csv` one row per run and condition, and `aggregate/report.md` is the table.
Per condition it gives the change in the language-switching metric against no intervention with a paired bootstrap 95% CI,
the English-only side effect, perplexity ratios, and for the selected heads the difference from the mean of the random and nearby control sets
with a one-sided permutation p-value. Every coefficient is reported, not only the best one. Runs with stand-in heads are flagged because the stand-ins
are chosen with the same direction that is steered.

## Adding a model or language
Add the alias under `models`. Set `steer_layers` for models whose depth differs from Qwen2.5-1.5B (28 layers) with an `overrides` entry. `lang` is limited to
`es`, `ru`, `zh`, `hi`, the choices `run_pilot` accepts. Put the circuit's heads file at `discovery/results/<alias>_en_<lang>_heads.json`.
The existing `qwen25_en_es_heads.json` already follows this name.
