# Reproduction log: AIAS 2.0 per-brand scores from the public OSF files

Independent checker, cloud session, 2026-11-13 (US Central times). I had not worked on this study. Inputs: only the 64 files in table A. No model or API calls and no contact with anyone. Network use: the 64 osf.io download links, nothing else (PyPI was not needed; numpy and scipy were already installed). Every number in this log is copied from the run artifacts by `work/make_log.py`, not retyped.

## 0. Outcome in brief

- **As deposited** (no options; run A with `--check-only`, run A2 writing to `--out`), the builder runs (exit 0). It passes the v0.41 gates P1–P4 and parity A1–A5, and prints and writes t1/t2 only: `status: pre-t3`, Stage 2 `pending`. The Stage-2 gate needs the prereg tags to be externally anchored: `git ls-remote` against GitHub, or OSF git-anchor JSON files plus a local git tag. Here this cannot pass. Contacting GitHub is outside the allowed network, so git's https transport was blocked with `GIT_ALLOW_PROTOCOL=file`. The anchor files `osf/v41/anchor/git_anchor_v0_41.json` and `osf/methodology/v1_9/anchor/git_anchor_v1_9.json` are not among the 64 public files, and there is no git repository. So, as deposited, it produces **no t3 values**.
- **With the builder's documented test-only option** `--skip-origin` (which the script requires to be paired with `--out DIR`; run B), the Stage-2 gate only checks that `osf/v41/v41_verdicts.json` and `osf/methodology/v1_9/v1_9_verdicts.json` exist (they do: files 25 and 24). It then completes: `status: complete`, class **A** (H_Dissociation_t3 CONFIRMED, H_Consistency_Reliability CONFIRMED), flags []. All t3 numbers in results.csv come from this run.
- **No code was changed** (no diffs). The only adjustments were environment variables (section 1). Full precision was obtained by calling the builder's own `build()` in-process from a wrapper (`work/extract_full_precision.py`), because the builder's CSV rounds P and C* to 6 decimals.
- Computed: **1008 of 1,008** per-brand values (173 of the 336 C* values are `not rated`) and **55 of 55** table-B quantities. Nothing was left uncomputed.
- Python 3.13.18, numpy 2.5.3, scipy 1.18.1 (pandas 3.0.5 used only in my cross-check), git 2.43.0.

## 1. Environment and folders

- Python: `3.13.18 (main, Oct 26 2026, 14:08:19) [Clang 23.1.3 ]`; numpy `2.5.3`; scipy `1.18.1`; pandas `3.0.5` (cross-check only); git `2.43.0`. All were preinstalled in the standard locations (`/usr/local/bin/python3`). No `pip install` was run.
- Root folder (`AIAS_ROOT`): `/home/claude/reproduction/files/`. Each table-A file is at its "Place at" path under it.
- My scripts: `/home/claude/reproduction/work/`. Outputs: `/home/claude/reproduction/out/`. Builder outputs, unchanged: `/home/claude/reproduction/out/builder/` (run B, the complete run). The as-deposited run A2 wrote to `/home/claude/reproduction/out/builder/default_mode_pre_t3/`.
- Environment variables for every builder run: `AIAS_ROOT=/home/claude/reproduction/files`, `HOME=/home/claude/reproduction/work/home` (an empty folder), `TMPDIR=/home/claude/reproduction/work/tmp`, `GIT_ALLOW_PROTOCOL=file`. Why:
  - `score_v41.py` (docstring, `_bootstrap_root`): when `~/aias` is not `AIAS_ROOT`, it re-executes the entry script with `HOME` pointing at a temp folder whose `aias` entry links to `AIAS_ROOT`. That is because `score_v0_31`, `score_v33` and `score_v20/21/22` hard-code `~/aias`. Pointing `HOME` at an empty folder inside the reproduction folder lets this documented shim run, and setting `TMPDIR` puts the shim's temp folder inside the reproduction folder too, so the run never looks at the real home folder. The shim was active (`_V41_HOME_SHIM` set; HOME during run C: `/home/claude/reproduction/work/tmp/v41_home_j15_hsbg`). It is not cleaned up by the script, so the folders `work/tmp/v41_home_*` were left, one per run (4 in total).
  - `GIT_ALLOW_PROTOCOL=file` makes git refuse the https transport before any connection. The default Stage-2 gate otherwise calls `git ls-remote https://github.com/...`, which the network rules do not allow. This was tested first against a loopback URL (step 7): `fatal: transport 'https' not allowed`, exit 128.

## 2. Steps and commands, in order

`$R` = `/home/claude/reproduction`. `env ...` = `env HOME=$R/work/home TMPDIR=$R/work/tmp AIAS_ROOT=$R/files GIT_ALLOW_PROTOCOL=file`.

1. **12:52**: Check the time and create the folders.
   ```
   TZ=America/Chicago date; mkdir -p /home/claude/reproduction/files /home/claude/reproduction/work /home/claude/reproduction/out/builder
   ```
2. **12:52**: Write the table-A manifest (number, link, path, bytes, SHA-256) to `work/manifest.tsv`, and a download script `work/download.sh`.
   ```
   (Write tool)
   ```
3. **12:53–12:58**: Download all 64 files to their "Place at" paths with `curl -sSL -o <file> <link>` (up to 3 tries each), then record bytes and SHA-256 against table A in `work/download_check.tsv`.
   ```
   bash /home/claude/reproduction/work/download.sh
   ```
4. **12:58**: Read the builder and the modules it imports (Read tool): `scripts/aias_2_0_synthesis_data.py`, `osf/methodology/v1_9/scripts/score_v1_9.py`, `osf/v41/scripts/score_v41.py`, `scripts/score_v0_31.py`, `scripts/score_v33.py`. Grep the import lines of `score_v20/21/22.py`, the prereg modules and the acquisition scripts. The acquisition scripts are only hashed (gate P4) and never imported, so no API client is loaded.
   ```
   grep -nE '^(import|from) |Path.home|subprocess|urllib|...' <files>
   ```
5. **12:59**: Check the interpreter and packages.
   ```
   which python3 git; python3 --version; python3 -c 'import numpy, scipy; ...'
   ```
6. **13:00**: Inspect the data-file structure in all three waves (own code).
   ```
   python3 -I -c '<csv header check>' ...; python3 -I /home/claude/reproduction/work/inspect_t3.py /home/claude/reproduction/files
   ```
7. **13:01**: Test that `GIT_ALLOW_PROTOCOL=file` blocks git's https transport before connecting (loopback URL only).
   ```
   NO_PROXY=127.0.0.1 no_proxy=127.0.0.1 GIT_ALLOW_PROTOCOL=file timeout 20 git ls-remote https://127.0.0.1:9/x.git refs/tags/test   # -> fatal: transport 'https' not allowed (exit 128)
   ```
8. **13:01**: Run A: the builder as deposited, default gate, check-only (writes nothing).
   ```
   env HOME=$R/work/home TMPDIR=$R/work/tmp AIAS_ROOT=$R/files GIT_ALLOW_PROTOCOL=file python3 $R/files/scripts/aias_2_0_synthesis_data.py --check-only
   ```
9. **13:01**: Run A2: the builder as deposited, default gate, writing its outputs (to `--out`, to keep them out of the downloaded tree).
   ```
   env ... python3 $R/files/scripts/aias_2_0_synthesis_data.py --out $R/out/builder/default_mode_pre_t3
   ```
10. **13:01**: Run B: the builder with its documented test-only option `--skip-origin` (requires `--out`).
   ```
   env ... python3 $R/files/scripts/aias_2_0_synthesis_data.py --skip-origin --out $R/out/builder
   ```
11. **13:02**: Print the run-B JSON for inspection: summaries, parity, the computed parts of stage2, inputs_sha256 and the lineage verdict strings.
   ```
   python3 -I -c 'import json; d=json.load(open("$R/out/builder/aias_2_0_synthesis_data.json")); ...'
   ```
12. **13:02**: Run C: full-precision extraction. My wrapper loads the deposited builder as a module and calls its own `build()` with the run-B options (`skip_origin=True`, t3/v41/v19 at defaults). It dumps every per-brand row unrounded and calls `score_v41.run_gates()` once more to record the P1–P4 details.
   ```
   env ... python3 $R/work/extract_full_precision.py $R/work/full_precision.json
   ```
13. **13:03**: Assemble `out/results.csv`. This verifies that the wrapper rows equal the builder CSV at 6 dp and that the wrapper's summaries, parity, stage2 and lineage equal the builder JSON; builds the ids; makes my own t3 response counts and below-6 counts.
   ```
   python3 -I $R/work/make_results.py $R/files $R/work/full_precision.json $R/out/builder $R/out/results.csv $R/work/results_report.json
   ```
14. **13:04**: Independent cross-check (own code). Recompute k, C_P, P, C* and n from the data files, with my own aggregation and the deposited text matchers for v0.20–v0.22 only. Recompute the 8 correlations with pandas ranks and `numpy.corrcoef`.
   ```
   env HOME=$R/work/home python3 -I $R/work/crosscheck.py $R/files $R/work/full_precision.json $R/work/crosscheck_report.json
   ```
15. **13:05**: Compare the run-A2 and run-B outputs; count JSON leaves; hash the outputs.
   ```
   python3 -I -c '...'; sha256sum $R/out/builder/*.* $R/out/builder/default_mode_pre_t3/*
   ```
16. **13:05**: List the key structure only (no values) of the copied `stage2.v19_verdicts`, `stage2.v41_verdicts` and `stage2.v41_manipulation_checks` sections, so they can be labelled in the log.
   ```
   python3 -I -c '... print(list(keys)) ...'
   ```
17. **13:06–13:09**: Write this log and the appendix, then proofread them (Read tool) and regenerate after small wording fixes.
   ```
   python3 -I $R/work/make_log.py
   ```

## 3. Files used, with SHA-256 (all 64 match table A in bytes and SHA-256)

| # | path under root | bytes | SHA-256 (downloaded) | matches table A |
|---|---|---|---|---|
| 1 | `scripts/aias_2_0_synthesis_data.py` | 22678 | `45a4e7d46ff9e68556ee5dc6f4d7236486e463e461cd25eb6e4489af13ebe69d` | yes |
| 2 | `osf/methodology/v1_9/scripts/score_v1_9.py` | 15775 | `71d340c480e09f4549903912960059226da9004413f6072a2c4c7dd209f42e02` | yes |
| 3 | `osf/v41/scripts/score_v41.py` | 43627 | `c4231b6805896a077b9b16d8f315bf19ae6297435293deb1de32375d7424dc31` | yes |
| 4 | `scripts/score_v0_31.py` | 14876 | `193ac0e0c98593d00fe252e4f78674cb212de9124d4e7486a26295880337460b` | yes |
| 5 | `scripts/score_v33.py` | 22214 | `c6b9720496d8abf78450ce297482c27f6e9b1aba76c3452e7964183c7b7fd866` | yes |
| 6 | `prereg/v0_31_cpc_baseline_content.py` | 7310 | `e9658c6f77d6e7c44bbf946f29c361ef0e37cc89b82f9bb31c13034f8c970281` | yes |
| 7 | `prereg/v0_33_provider_asymmetry_content.py` | 18305 | `7f9fa43e169f2c484f09c816416d31822f18a0264805193a8900a3ea3c495a27` | yes |
| 8 | `scripts/score_v20.py` | 26002 | `a0b288d5721ebf259e216c7e72af6d85f0e8414e8d3534552bf7c583196b9110` | yes |
| 9 | `scripts/score_v21.py` | 26049 | `993317fcbaf1d64cdd1b7b4cb69bfa602dd675829b2a6fc06bbf1a83252a7e92` | yes |
| 10 | `scripts/score_v22.py` | 40773 | `b03bc55b74cf4aa402412f4313217fa057568365505245cbb0fb25a7f5fccdb9` | yes |
| 11 | `prereg/v0_20_registry.json` | 10584 | `eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782` | yes |
| 12 | `prereg/v0_21_registry.json` | 12574 | `45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3` | yes |
| 13 | `prereg/v0_22_automotive_content.py` | 13665 | `431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9` | yes |
| 14 | `osf/v19/phase_a_queries.jsonl` | 21946 | `276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e` | yes |
| 15 | `osf/v19/phase_b_queries.jsonl` | 9864 | `75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188` | yes |
| 16 | `osf/v19/thresholds_v0_19.json` | 7178 | `542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61` | yes |
| 17 | `scripts/acquire_v0_23.py` | 17046 | `7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da` | yes |
| 18 | `osf/v41/prereg/acquisition_manifest_v41.md` | 4174 | `e97d72a14ab8cf9aee9b4589f369db4b0e25375f4faeaf77568bb1351247e59c` | yes |
| 19 | `scripts/run_acquisition_v22.py` | 22445 | `59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe` | yes |
| 20 | `osf/v41/registries/v1_8_instrument_table.csv` | 20027 | `2d0ea5e83b01a39d1b120fe75b79178b78c85a649837f0d40a473a38f041f6e6` | yes |
| 21 | `osf/v41/registries/v1_8_verdicts.json` | 11522 | `a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78` | yes |
| 22 | `osf/v34/v34_verdicts.json` | 10091 | `b838b5352f35d3ae9e95c33dc6f8cb791f6f57eb83f9dfdc29b918649a115ee5` | yes |
| 23 | `osf/methodology/v1_9/v1_9_calibration.json` | 9964 | `4d2ddb982a3372fa4f8c68e5bcf1a9511684186568fb6d37fbc2562b612388bf` | yes |
| 24 | `osf/methodology/v1_9/v1_9_verdicts.json` | 1574 | `3d838f92821a5ae41c33bdb9a209432e0fdbc505ce7c53f8a17e8c438745967d` | yes |
| 25 | `osf/v41/v41_verdicts.json` | 13740 | `0d3f5dfcf0a920e642aa613f5bf45dce66dd155eb6fd4ee054ed4d4bb700d4e2` | yes |
| 26 | `osf/v29/data/v29_verdicts.json` | 1493 | `73fdc5e076b0625619f90e6c1038826d60a9e0dd01dda1cfc31d29a78ed23f27` | yes |
| 27 | `osf/v30/v30_cpc_verdicts.json` | 5554 | `61ac89ab2bfff72a757a540f28154cb35a60e5b88e8ad295ed2e70a435956c15` | yes |
| 28 | `osf/v31/v31_cpc_verdicts.json` | 4759 | `1124b70dcdbd59737ca843f72b228115b60c7cb25a73d380d174f6bc3953fd5e` | yes |
| 29 | `osf/v32/v32_verdicts.json` | 9706 | `d8591fb8f16a391e3f2584b78b5a042293699898f0644c9e6545d17a7e33620b` | yes |
| 30 | `osf/v33/v33_provider_asymmetry_verdicts.json` | 5493 | `9c513273f8c0851b71147b57543664455a801a1279c862b3c642cea2008d096d` | yes |
| 31 | `osf/v35/v35_verdicts.json` | 15413 | `68a219607ca615047c55930afc7e12f137698c97d8b50aeb05364ba505797303` | yes |
| 32 | `osf/aias_2_0/inputs/v36_verdicts.json` | 5314 | `3c41f78a70f02df010c88d3611fb15deae10276bb217eb7a125ec90b90d2fb8b` | yes |
| 33 | `osf/methodology/v1_7/v1_7_cpc_verdicts.json` | 7928 | `2ad30dd2ec04dfa1583c44b183ee1caa04a57b35cf3dc7024c1369ad49777742` | yes |
| 34 | `osf/v37/v37_verdicts.json` | 4865 | `7f46c853a2395b7f6bf1b4ab83d0786f8afa3c36eb6d41d6e45085a4d3103461` | yes |
| 35 | `osf/v19/phase_a_results.csv` | 2689 | `5206fe70e5a375b5871e8a7067940065e8bb6b5d98b1b9389a54c2eb9a22d6e3` | yes |
| 36 | `osf/v19/phase_b_results.csv` | 23622 | `2542f0e8117a44d02e072b56be24d758f63ede35d700dd163852b720d4739075` | yes |
| 37 | `osf/v20/phase_a_results.csv` | 24882 | `c8ad6335c982ec95883fffa6c3cb185170b3cdd80b8694377c9fb8afb47d390e` | yes |
| 38 | `osf/v20/phase_b_results.csv` | 104769 | `4791113a93b8a25866099fa16ea3a8d14c6f82d6e6c24894609506ad25225828` | yes |
| 39 | `osf/v21/phase_a_results.csv` | 24464 | `d470940aa497f55588588536173a128a3394af2a6f0bb6e94825738622167d0d` | yes |
| 40 | `osf/v21/phase_b_results.csv` | 105252 | `45e4c3acca67f8c6d6ddfe94bd08215bf6287e4b5af194b81eef47f427440ee1` | yes |
| 41 | `osf/v22/phase_a_results.csv` | 21839 | `93c1b147c44b9031bfad3eb5806d50fd26404cf9c9b7cea95f2fd8a7a00c246a` | yes |
| 42 | `osf/v22/phase_b_results.csv` | 97446 | `e61dff692ed5eee34a3719067fb07328e4bb3035247c78b703e01d07097fce35` | yes |
| 43 | `osf/v23/data/v23_phase_a_scored.json` | 881071 | `042188bc876a969e1f87c22bb77b95d6fb819643be7b9c6304e47d6243b7754c` | yes |
| 44 | `osf/v23/data/v23_phase_b_scored.json` | 180768 | `2fd1400891c4aff0707ff58d11d2e055c2ab5242972512888f3c69b742e7c9e6` | yes |
| 45 | `osf/v34/data/v19/phase_a_results.csv` | 2689 | `ad566fb46f4652bdab790da3a9db1fdadcc883e230d163c722b555a73ffceb42` | yes |
| 46 | `osf/v34/data/v19/phase_b_results.csv` | 23616 | `ba751c6cce5c264d37f4cfc0ca19dc1ef37d68570e0eb2e9b4b70429187b6129` | yes |
| 47 | `osf/v34/data/v20/phase_a_results.csv` | 25170 | `382e22ef8e8b4ee808c413031cb179c7cecd53d3cea37e35d494f53e05efcbf4` | yes |
| 48 | `osf/v34/data/v20/phase_b_results.csv` | 103430 | `504dfc5ace742cb27d0d3a764b617b12cb816f607850d165801b64b68fcc8a78` | yes |
| 49 | `osf/v34/data/v21/phase_a_results.csv` | 24459 | `9bfe8ab018743d2b533b0f1fd8e483a49c738e89091a18cda6ead8c7d0c722d9` | yes |
| 50 | `osf/v34/data/v21/phase_b_results.csv` | 107849 | `f27f4a5f0e2da0b110be2f2e3b85437e391f7354f87ec3e2d9ea5872e6f87ed1` | yes |
| 51 | `osf/v34/data/v22/phase_a_results.csv` | 21850 | `9b8e8d49a1be66107af49bcb93ebfcb715fb2992cf7b7ead32f7f511c88445aa` | yes |
| 52 | `osf/v34/data/v22/phase_b_results.csv` | 100091 | `7976de5d76ab5a21729a04bdc3d3f4e12afc7b6e0350dcabcedd99dc329c189a` | yes |
| 53 | `osf/v34/data/v23/v23_phase_a_scored.json` | 891087 | `8f9ca58f81f4b9c6d1aedc4b3395712ed39071d5d5a27db34aae9f3e132d06b1` | yes |
| 54 | `osf/v34/data/v23/v23_phase_b_scored.json` | 178164 | `f5e7a07e698378d69b08131aa6538748c104fa83e3e4cc4a8f2e2616015dd7cb` | yes |
| 55 | `osf/v41/data/v19/phase_a_results.csv` | 2689 | `370f44409893072492a16647c4fe56c51b2a65994ee96824a9c8d4da34459ce5` | yes |
| 56 | `osf/v41/data/v19/phase_b_results.csv` | 23621 | `7d49164eab4600b0e97a2d023b47bfc682e7db222fcf7cdf06b371e12ebb07e6` | yes |
| 57 | `osf/v41/data/v20/phase_a_results.csv` | 24613 | `3b0554fd6a0746e7341c5702159b5a6d5e73ea67d385316169e2ab028fd61a55` | yes |
| 58 | `osf/v41/data/v20/phase_b_results.csv` | 107419 | `c313569ec31f9789363d863062e56a1a8cd77a4293c75189dc3acd2a1dfcc9c8` | yes |
| 59 | `osf/v41/data/v21/phase_a_results.csv` | 24452 | `175b16094400375ab4987594abad15875bb7d88bca50d7f39cdb9b2e59b1e6d8` | yes |
| 60 | `osf/v41/data/v21/phase_b_results.csv` | 102916 | `aeb8a2a2a7846f12467cafaff582a9deb73ddbedacf598f6da23e0e6dff23c69` | yes |
| 61 | `osf/v41/data/v22/phase_a_results.csv` | 22160 | `40af3d22ef00a5b1ab4e4abf4886ddf9059009d91f5310801e45653b5b91275e` | yes |
| 62 | `osf/v41/data/v22/phase_b_results.csv` | 102679 | `a5bffb31acfd0d97226e2658001f1adecbf64448b512fd32e037a85d84bde94b` | yes |
| 63 | `osf/v41/data/v23/v23_phase_a_scored.json` | 876896 | `13f85accaec51338a67bea95a6169de21a3e84fa2c12b692c88da7f5fa09e99c` | yes |
| 64 | `osf/v41/data/v23/v23_phase_b_scored.json` | 175806 | `2fcff8fb1f7cc57c1ad5056e366a2eccffe8767c1dba95d12cfc0d054e34d52d` | yes |

All 64 matched: **True**. Downloaded from the table-A links only. Every file was used: the code files are imported by the builder chain, or hashed in gate P4 (`acquire_v0_23.py`, `run_acquisition_v22.py`, `v0_22_automotive_content.py`, the v0.19 query and threshold files, and the v0.20/v0.21 registries, which are also read). The verdict and calibration JSONs are read by the lineage step, the parity gates and Stage 2. The data files are the three waves.

My own scripts (in `work/`):

- `work/manifest.tsv`  sha256 `42b4589c145800aa0fe48052b30547591017717a4f04a9ef9d34d1c8a1c00877`
- `work/download.sh`  sha256 `cef7e1b06cd1212d01c1ab2973a46a0674f2f983ea6bd09179967db0a62c6683`
- `work/inspect_t3.py`  sha256 `92fe2facaa65e8fb4e510de9a8542f477e5efc0df228c6527e1f894d14675237`
- `work/extract_full_precision.py`  sha256 `fe18b9fae1687c0f5855d88b863475346e11954b12e55cc3a988e0727c390895`
- `work/make_results.py`  sha256 `3a10e1fbfc5563cca878080765fa6b03212fdc20bb080d1651bc6417b8150f95`
- `work/crosscheck.py`  sha256 `d27903dfe2f8770a2333a1f36dcba0aa64460cfed403b044d00bed28def6a512`
- `work/make_log.py`  sha256 `527973896d42fab4879834de63a3044792908ad025a04c0e466b3f2190df20a8`

## 4. What the builder printed (verbatim)

**Run A: as deposited, `--check-only`**: exit 0
```
status: pre-t3  parity A1-A5: all passed  v0.41 gates: {'P1': True, 'P2': True, 'P3': True, 'P4': True}
t1: rho(C*,P) 0.073 (n 55), not rated 0.509
t2: rho(C*,P) 0.082 (n 54), not rated 0.518
stage 2: pending  class: None  (Stage 2 not available yet (see reasons))  reasons: ["v0.41-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/v41/anchor/git_anchor_v0_41.json not in this tree (merge the phase branch first)", "v1.9-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/methodology/v1_9/anchor/git_anchor_v1_9.json not in this tree (merge the phase branch first)"]
--- stderr (only the shell's `time` report; run A was wrapped in `( time ... )`) ---

real	0m2.249s
user	0m2.105s
sys	0m0.059s
```
**Run A2: as deposited, `--out .../default_mode_pre_t3`**: exit 0
```
status: pre-t3  parity A1-A5: all passed  v0.41 gates: {'P1': True, 'P2': True, 'P3': True, 'P4': True}
t1: rho(C*,P) 0.073 (n 55), not rated 0.509
t2: rho(C*,P) 0.082 (n 54), not rated 0.518
stage 2: pending  class: None  (Stage 2 not available yet (see reasons))  reasons: ["v0.41-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/v41/anchor/git_anchor_v0_41.json not in this tree (merge the phase branch first)", "v1.9-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/methodology/v1_9/anchor/git_anchor_v1_9.json not in this tree (merge the phase branch first)"]
wrote /home/claude/reproduction/out/builder/default_mode_pre_t3/aias_2_0_synthesis_data.json and aias_2_0_profiles.csv
```
**Run B: `--skip-origin --out .../out/builder`**: exit 0
```
status: complete  parity A1-A5: all passed  v0.41 gates: {'P1': True, 'P2': True, 'P3': True, 'P4': True}
t1: rho(C*,P) 0.073 (n 55), not rated 0.509
t2: rho(C*,P) 0.082 (n 54), not rated 0.518
stage 2: complete  class: A  (H_Dissociation_t3 CONFIRMED, H_Consistency_Reliability CONFIRMED)  reasons: []
wrote /home/claude/reproduction/out/builder/aias_2_0_synthesis_data.json and aias_2_0_profiles.csv
```
**Run C: my wrapper calling `build()` (wrapper's own two lines)**: exit 0
```
wrote /home/claude/reproduction/work/full_precision.json; waves: t1=112, t2=112, t2_panel_t3=None, t3=112
status=complete class={'class': 'A', 'flags': [], 'why': 'H_Dissociation_t3 CONFIRMED, H_Consistency_Reliability CONFIRMED'}
```

Runs A2 and B write identical `parity_builder_vs_stage1`, `lineage` and t1/t2 `summaries` (checked programmatically: True). Run A2's profiles CSV has t1 and t2 only.

Builder output files (SHA-256):

- `/home/claude/reproduction/out/builder/aias_2_0_synthesis_data.json`  137445 bytes  sha256 `896931d9e0f4f6bee500892f77748d0af4972c0aac9fed0f5dbee8ead01f6e39`
- `/home/claude/reproduction/out/builder/aias_2_0_profiles.csv`  16540 bytes  sha256 `022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e`
- `/home/claude/reproduction/out/builder/default_mode_pre_t3/aias_2_0_synthesis_data.json`  125750 bytes  sha256 `5c5b723295446500327fe482b14a43078272d2b276e3d33e358263e858d925c5`
- `/home/claude/reproduction/out/builder/default_mode_pre_t3/aias_2_0_profiles.csv`  11053 bytes  sha256 `07b8145912209838012033e3ecd46cb3b289054bd821ec457ef8e915f5308d31`

## 5. Every check and gate the builder ran, with outcome

Inside `score_v41.run_gates()` (called by `build()`; details from run C's second call, identical code and inputs):

- **Frozen v1.8 reference files** (`check_references`): `v1_8_instrument_table.csv` sha256 `2d0ea5e83b01a39d1b120fe75b79178b78c85a649837f0d40a473a38f041f6e6` match=True; `v1_8_verdicts.json` sha256 `a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78` match=True
- **P1** (t1 phi reproduces the v1.8 instrument table): passed=True, rows_checked=112, max_abs_diff=0.0, k_vector_mismatches_info_only=0, problems=[]
- **P2** (phi t1→t2 Spearman, to 4 dp, n): passed=True, rho=0.6453869683902721, n=83; reference rho=0.6453869683902722, n=83, prereg=[0.6454, 83]
- **P3** (per-substrate CV-CPC t1→t2 rho vs v0.34, tol 1e-9): passed=True, failed=[]
  - v0.19: rho=0.4191691916696407, n=8, ref_rho=0.4191691916696407, ref_n=8, match=True
  - v0.20: rho=0.7833333333333333, n=9, ref_rho=0.7833333333333333, ref_n=9, match=True
  - v0.21: rho=0.8901098901098901, n=13, ref_rho=0.8901098901098902, ref_n=13, match=True
  - v0.22: rho=0.9601793410322754, n=14, ref_rho=0.9601793410322754, ref_n=14, match=True
  - v0.23: rho=0.7615129419677079, n=9, ref_rho=0.7615129419677079, ref_n=9, match=True
- **P4** (8 probe artifacts' SHA-256 equal the constants and appear in `acquisition_manifest_v41.md`): passed=True, failed=[]
  - `osf/v19/phase_a_queries.jsonl` sha256 `276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e` match=True
  - `osf/v19/phase_b_queries.jsonl` sha256 `75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188` match=True
  - `osf/v19/thresholds_v0_19.json` sha256 `542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61` match=True
  - `prereg/v0_20_registry.json` sha256 `eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782` match=True
  - `prereg/v0_21_registry.json` sha256 `45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3` match=True
  - `prereg/v0_22_automotive_content.py` sha256 `431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9` match=True
  - `scripts/run_acquisition_v22.py` sha256 `59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe` match=True
  - `scripts/acquire_v0_23.py` sha256 `7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da` match=True
- all_passed=True. The builder records `parity_gates_v0_41` = {"P1": true, "P2": true, "P3": true, "P4": true}.
- `score_v41.load_wave` assertions (each count vector has length 6 with values 0..6; the frame map agrees with the counts for every brand and model): passed for t1, t2 and t3 (no AssertionError in any run).

**PARITY A1–A5** (`parity_t1_t2`; tolerance 1e-12; the builder's t1/t2 values vs the locked `v1_9_calibration.json` row for spec `C_phi+FLOOR+ADD`):

| check | builder | locked | passed |
|---|---|---|---|
| A1_K1_t1 | 0.07293925573105668, 55 | 0.07293925573105668, 55 | True |
| A2_K1_t2 | 0.08153268408519941, 54 | 0.08153268408519941, 54 | True |
| A3_not_rated | 0.5089285714285714, 0.5178571428571429 | 0.5089285714285714, 0.5178571428571429 | True |
| A4_retest_C | 0.7357486264955685, 53 | 0.7357486264955685, 53 | True |
| A5_retest_P | 0.9695933242098346, 112 | 0.9695933242098346, 112 | True |

**Stage-2 gate** (`stage2_gate`):

- Runs A/A2 (as deposited): status `pending`. Reasons:
  - v0.41-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/v41/anchor/git_anchor_v0_41.json not in this tree (merge the phase branch first)
  - v1.9-prereg-r1 not externally anchored: not on origin (fatal: transport 'https' not allowed); osf/methodology/v1_9/anchor/git_anchor_v1_9.json not in this tree (merge the phase branch first)
  - origin record: `{"v0.41-prereg-r1": {"anchored": false, "how": "not on origin (fatal: transport 'https' not allowed); osf/v41/anchor/git_anchor_v0_41.json not in this tree (merge the phase branch first)"}, "v1.9-prereg-r1": {"anchored": false, "how": "not on origin (fatal: transport 'https' not allowed); osf/methodology/v1_9/anchor/git_anchor_v1_9.json not in this tree (merge the phase branch first)"}}`
- Run B (`--skip-origin`): origin `{"skipped": "test mode (--skip-origin)"}`. Both verdict files present, so status `complete`, reasons [].
- Run B, t3 panel (`panel_used` read from `v1_9_verdicts.json`): ['claude-opus-4-5', 'claude-sonnet-4-5', 'gpt-4o', 'gpt-4o-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite'] (6 models, so `profiles['t2_panel_t3']` = None and the t2→t3 retests use the full-panel t2 rows).
- Run B **consistency check** `rho_Cstar_P_t3_matches_v19` (|builder t3 rho(C*,P) − v1.9 H_Dissociation_t3 rho| ≤ 1e-12): **True**.
- Run B **classify()** (section-5 class): class **A**, flags [], why: "H_Dissociation_t3 CONFIRMED, H_Consistency_Reliability CONFIRMED".
- Argument check: `--skip-origin` without `--out` would exit 3. `--out` was given, so the check did not trigger.

## 6. Every number the builder writes outside the copied lineage records

Flattened from `out/builder/aias_2_0_synthesis_data.json` (run B), in file order. The `stage2.v19_verdicts`, `stage2.v41_verdicts` and `stage2.v41_manipulation_checks` blocks are **copied by the builder from the input files** `osf/methodology/v1_9/v1_9_verdicts.json` and `osf/v41/v41_verdicts.json`. They are not computed by the builder, and I did not recompute or compare them. The `lineage` block holds verbatim copies of the 12 hashed lineage inputs (about 1,400 numeric leaves). Below I list only its verdict strings. The full flattened JSON, every leaf including lineage, is in `out/log_appendix_builder_json_flat.tsv`.

| JSON path | value |
|---|---|
| `phase` | AIAS 2.0 synthesis |
| `outline_tag` | aias-2-0-outline-locked |
| `built_at_utc` | 2026-11-13T19:01:27+00:00 |
| `status` | complete |
| `spec.consistency_score` | C_phi rated at >= 6 total mentions (v1.9 SELECTED_CONSISTENCY) |
| `spec.presence_score` | P = 100*(C_P/6 + 2*pi_hat)/3 (v0.25 presence_composite) |
| `spec.composite` | none (v1.9 Stage 1); A = (P + C*)/2 kept only for the descriptive K2 check |
| `parity_gates_v0_41.P1` | true |
| `parity_gates_v0_41.P2` | true |
| `parity_gates_v0_41.P3` | true |
| `parity_gates_v0_41.P4` | true |
| `parity_builder_vs_stage1.A1_K1_t1.builder[0]` | 0.07293925573105668 |
| `parity_builder_vs_stage1.A1_K1_t1.builder[1]` | 55 |
| `parity_builder_vs_stage1.A1_K1_t1.locked[0]` | 0.07293925573105668 |
| `parity_builder_vs_stage1.A1_K1_t1.locked[1]` | 55 |
| `parity_builder_vs_stage1.A1_K1_t1.passed` | true |
| `parity_builder_vs_stage1.A2_K1_t2.builder[0]` | 0.08153268408519941 |
| `parity_builder_vs_stage1.A2_K1_t2.builder[1]` | 54 |
| `parity_builder_vs_stage1.A2_K1_t2.locked[0]` | 0.08153268408519941 |
| `parity_builder_vs_stage1.A2_K1_t2.locked[1]` | 54 |
| `parity_builder_vs_stage1.A2_K1_t2.passed` | true |
| `parity_builder_vs_stage1.A3_not_rated.builder[0]` | 0.5089285714285714 |
| `parity_builder_vs_stage1.A3_not_rated.builder[1]` | 0.5178571428571429 |
| `parity_builder_vs_stage1.A3_not_rated.locked[0]` | 0.5089285714285714 |
| `parity_builder_vs_stage1.A3_not_rated.locked[1]` | 0.5178571428571429 |
| `parity_builder_vs_stage1.A3_not_rated.passed` | true |
| `parity_builder_vs_stage1.A4_retest_C.builder[0]` | 0.7357486264955685 |
| `parity_builder_vs_stage1.A4_retest_C.builder[1]` | 53 |
| `parity_builder_vs_stage1.A4_retest_C.locked[0]` | 0.7357486264955685 |
| `parity_builder_vs_stage1.A4_retest_C.locked[1]` | 53 |
| `parity_builder_vs_stage1.A4_retest_C.passed` | true |
| `parity_builder_vs_stage1.A5_retest_P.builder[0]` | 0.9695933242098346 |
| `parity_builder_vs_stage1.A5_retest_P.builder[1]` | 112 |
| `parity_builder_vs_stage1.A5_retest_P.locked[0]` | 0.9695933242098346 |
| `parity_builder_vs_stage1.A5_retest_P.locked[1]` | 112 |
| `parity_builder_vs_stage1.A5_retest_P.passed` | true |
| `summaries.t1.per_substrate.v0.19.n_units` | 16 |
| `summaries.t1.per_substrate.v0.19.n_rated` | 8 |
| `summaries.t1.per_substrate.v0.19.share_rated` | 0.5 |
| `summaries.t1.per_substrate.v0.19.mean_P` | 48.726851851851855 |
| `summaries.t1.per_substrate.v0.19.mean_C_rated` | 59.21938635914272 |
| `summaries.t1.per_substrate.v0.20.n_units` | 24 |
| `summaries.t1.per_substrate.v0.20.n_rated` | 10 |
| `summaries.t1.per_substrate.v0.20.share_rated` | 0.4166666666666667 |
| `summaries.t1.per_substrate.v0.20.mean_P` | 45.833333333333336 |
| `summaries.t1.per_substrate.v0.20.mean_C_rated` | 88.72561615590908 |
| `summaries.t1.per_substrate.v0.21.n_units` | 24 |
| `summaries.t1.per_substrate.v0.21.n_rated` | 14 |
| `summaries.t1.per_substrate.v0.21.share_rated` | 0.5833333333333334 |
| `summaries.t1.per_substrate.v0.21.mean_P` | 50.7716049382716 |
| `summaries.t1.per_substrate.v0.21.mean_C_rated` | 83.23343780791843 |
| `summaries.t1.per_substrate.v0.22.n_units` | 24 |
| `summaries.t1.per_substrate.v0.22.n_rated` | 14 |
| `summaries.t1.per_substrate.v0.22.share_rated` | 0.5833333333333334 |
| `summaries.t1.per_substrate.v0.22.mean_P` | 49.84567901234568 |
| `summaries.t1.per_substrate.v0.22.mean_C_rated` | 94.58201787414414 |
| `summaries.t1.per_substrate.v0.23.n_units` | 24 |
| `summaries.t1.per_substrate.v0.23.n_rated` | 9 |
| `summaries.t1.per_substrate.v0.23.share_rated` | 0.375 |
| `summaries.t1.per_substrate.v0.23.mean_P` | 41.82098765432099 |
| `summaries.t1.per_substrate.v0.23.mean_C_rated` | 77.77107637644036 |
| `summaries.t1.n_units` | 112 |
| `summaries.t1.n_rated` | 55 |
| `summaries.t1.share_not_rated` | 0.5089285714285714 |
| `summaries.t1.rho_Cstar_P` | 0.07293925573105668 |
| `summaries.t1.rho_Cstar_P_n` | 55 |
| `summaries.t1.rho_A_P_descriptive` | 0.971220479242514 |
| `summaries.t1.rho_A_P_n` | 112 |
| `summaries.t2.per_substrate.v0.19.n_units` | 16 |
| `summaries.t2.per_substrate.v0.19.n_rated` | 8 |
| `summaries.t2.per_substrate.v0.19.share_rated` | 0.5 |
| `summaries.t2.per_substrate.v0.19.mean_P` | 47.22222222222222 |
| `summaries.t2.per_substrate.v0.19.mean_C_rated` | 63.92420893062382 |
| `summaries.t2.per_substrate.v0.20.n_units` | 24 |
| `summaries.t2.per_substrate.v0.20.n_rated` | 9 |
| `summaries.t2.per_substrate.v0.20.share_rated` | 0.375 |
| `summaries.t2.per_substrate.v0.20.mean_P` | 45.29320987654321 |
| `summaries.t2.per_substrate.v0.20.mean_C_rated` | 90.7543766761707 |
| `summaries.t2.per_substrate.v0.21.n_units` | 24 |
| `summaries.t2.per_substrate.v0.21.n_rated` | 14 |
| `summaries.t2.per_substrate.v0.21.share_rated` | 0.5833333333333334 |
| `summaries.t2.per_substrate.v0.21.mean_P` | 51.388888888888886 |
| `summaries.t2.per_substrate.v0.21.mean_C_rated` | 79.89436226691694 |
| `summaries.t2.per_substrate.v0.22.n_units` | 24 |
| `summaries.t2.per_substrate.v0.22.n_rated` | 14 |
| `summaries.t2.per_substrate.v0.22.share_rated` | 0.5833333333333334 |
| `summaries.t2.per_substrate.v0.22.mean_P` | 50.077160493827165 |
| `summaries.t2.per_substrate.v0.22.mean_C_rated` | 94.11410782454006 |
| `summaries.t2.per_substrate.v0.23.n_units` | 24 |
| `summaries.t2.per_substrate.v0.23.n_rated` | 9 |
| `summaries.t2.per_substrate.v0.23.share_rated` | 0.375 |
| `summaries.t2.per_substrate.v0.23.mean_P` | 41.28086419753087 |
| `summaries.t2.per_substrate.v0.23.mean_C_rated` | 78.97168989186869 |
| `summaries.t2.n_units` | 112 |
| `summaries.t2.n_rated` | 54 |
| `summaries.t2.share_not_rated` | 0.5178571428571429 |
| `summaries.t2.rho_Cstar_P` | 0.08153268408519941 |
| `summaries.t2.rho_Cstar_P_n` | 54 |
| `summaries.t2.rho_A_P_descriptive` | 0.9749692326190192 |
| `summaries.t2.rho_A_P_n` | 112 |
| `summaries.t3.per_substrate.v0.19.n_units` | 16 |
| `summaries.t3.per_substrate.v0.19.n_rated` | 8 |
| `summaries.t3.per_substrate.v0.19.share_rated` | 0.5 |
| `summaries.t3.per_substrate.v0.19.mean_P` | 46.99074074074074 |
| `summaries.t3.per_substrate.v0.19.mean_C_rated` | 64.78204665704665 |
| `summaries.t3.per_substrate.v0.20.n_units` | 24 |
| `summaries.t3.per_substrate.v0.20.n_rated` | 9 |
| `summaries.t3.per_substrate.v0.20.share_rated` | 0.375 |
| `summaries.t3.per_substrate.v0.20.mean_P` | 46.45061728395061 |
| `summaries.t3.per_substrate.v0.20.mean_C_rated` | 88.50210097817583 |
| `summaries.t3.per_substrate.v0.21.n_units` | 24 |
| `summaries.t3.per_substrate.v0.21.n_rated` | 13 |
| `summaries.t3.per_substrate.v0.21.share_rated` | 0.5416666666666666 |
| `summaries.t3.per_substrate.v0.21.mean_P` | 49.922839506172835 |
| `summaries.t3.per_substrate.v0.21.mean_C_rated` | 77.4021070335173 |
| `summaries.t3.per_substrate.v0.22.n_units` | 24 |
| `summaries.t3.per_substrate.v0.22.n_rated` | 14 |
| `summaries.t3.per_substrate.v0.22.share_rated` | 0.5833333333333334 |
| `summaries.t3.per_substrate.v0.22.mean_P` | 49.151234567901234 |
| `summaries.t3.per_substrate.v0.22.mean_C_rated` | 93.08817051059349 |
| `summaries.t3.per_substrate.v0.23.n_units` | 24 |
| `summaries.t3.per_substrate.v0.23.n_rated` | 10 |
| `summaries.t3.per_substrate.v0.23.share_rated` | 0.4166666666666667 |
| `summaries.t3.per_substrate.v0.23.mean_P` | 41.2037037037037 |
| `summaries.t3.per_substrate.v0.23.mean_C_rated` | 74.50871659204992 |
| `summaries.t3.n_units` | 112 |
| `summaries.t3.n_rated` | 54 |
| `summaries.t3.share_not_rated` | 0.5178571428571429 |
| `summaries.t3.rho_Cstar_P` | 0.18949782059932604 |
| `summaries.t3.rho_Cstar_P_n` | 54 |
| `summaries.t3.rho_A_P_descriptive` | 0.969272869350446 |
| `summaries.t3.rho_A_P_n` | 112 |
| `stage2.status` | complete |
| `stage2.reasons` | [] |
| `stage2.origin.skipped` | test mode (--skip-origin) |
| `stage2.panel_used[0]` | claude-opus-4-5 |
| `stage2.panel_used[1]` | claude-sonnet-4-5 |
| `stage2.panel_used[2]` | gpt-4o |
| `stage2.panel_used[3]` | gpt-4o-mini |
| `stage2.panel_used[4]` | gemini-2.5-flash |
| `stage2.panel_used[5]` | gemini-2.5-flash-lite |
| `stage2.v19_verdicts.H_Presence_Score_Reliability.tier` | PRIMARY |
| `stage2.v19_verdicts.H_Presence_Score_Reliability.verdict` | CONFIRMED |
| `stage2.v19_verdicts.H_Presence_Score_Reliability.rho` | 0.9542888066830918 |
| `stage2.v19_verdicts.H_Presence_Score_Reliability.p_perm` | 9.999000099990002e-05 |
| `stage2.v19_verdicts.H_Presence_Score_Reliability.n` | 112 |
| `stage2.v19_verdicts.H_Dissociation_t3.tier` | PRIMARY |
| `stage2.v19_verdicts.H_Dissociation_t3.verdict` | CONFIRMED |
| `stage2.v19_verdicts.H_Dissociation_t3.rho` | 0.18949782059932604 |
| `stage2.v19_verdicts.H_Dissociation_t3.n` | 54 |
| `stage2.v19_verdicts.H_Consistency_Reliability.tier` | PRIMARY |
| `stage2.v19_verdicts.H_Consistency_Reliability.verdict` | CONFIRMED |
| `stage2.v19_verdicts.H_Consistency_Reliability.rho` | 0.6473238536507431 |
| `stage2.v19_verdicts.H_Consistency_Reliability.n` | 52 |
| `stage2.v19_verdicts.H_Consistency_Reliability.frame_structure_null.p_frame` | 0.008099190080991902 |
| `stage2.v19_verdicts.H_Consistency_Reliability.frame_structure_null.null_mean` | 0.43783685713432124 |
| `stage2.v19_verdicts.H_Consistency_Reliability.frame_structure_null.null_p95` | 0.5849157274563637 |
| `stage2.v19_verdicts.H_Consistency_Reliability.frame_structure_null.draws` | 10000 |
| `stage2.v19_verdicts.H_Consistency_Reliability.frame_structure_null.seed` | 190020 |
| `stage2.v19_verdicts.H_NoComposite_t3.tier` | SECONDARY (descriptive) |
| `stage2.v19_verdicts.H_NoComposite_t3.verdict` | DESCRIPTIVE |
| `stage2.v19_verdicts.H_NoComposite_t3.rho_A_P` | 0.969272869350446 |
| `stage2.v19_verdicts.H_NoComposite_t3.n` | 112 |
| `stage2.v19_verdicts.H_NoComposite_t3.k2_line` | 0.95 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.tier` | PRIMARY |
| `stage2.v41_verdicts.H_Phi_LongHorizon.verdict` | CONFIRMED |
| `stage2.v41_verdicts.H_Phi_LongHorizon.rho` | 0.6806643811207408 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.p_mc_se` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n` | 80 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.p_frame` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.null_mean` | 0.35709488073921136 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.null_p95` | 0.5094847360022983 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.null_max` | 0.6607237276546056 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.draws` | 10000 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.frame_structure_null.seed` | 410045 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.rule` | CONFIRMED iff rho >= 0.50 AND p_perm < .05 AND p_frame < .05 (SCORER_NOTES S2); FALSIFIED iff rho < 0.30 OR p_perm >= .05; else MARGINAL |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n_per_substrate.v0.19` | 12 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n_per_substrate.v0.20` | 16 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n_per_substrate.v0.21` | 19 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n_per_substrate.v0.22` | 15 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.n_per_substrate.v0.23` | 18 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.pooled_within_substrate_rank_rho` | 0.6286151995058789 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.leave_one_substrate_out.v0.19` | 0.6541579058741032 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.leave_one_substrate_out.v0.20` | 0.7296036617198862 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.leave_one_substrate_out.v0.21` | 0.6787881885053477 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.leave_one_substrate_out.v0.22` | 0.6371540981959121 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.leave_one_substrate_out.v0.23` | 0.6847405507724452 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.loso_range[0]` | 0.6371540981959121 |
| `stage2.v41_verdicts.H_Phi_LongHorizon.sensitivity.loso_range[1]` | 0.7296036617198862 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.tier` | PRIMARY |
| `stage2.v41_verdicts.H_Presence_LongHorizon.verdict` | CONFIRMED |
| `stage2.v41_verdicts.H_Presence_LongHorizon.n_ge_070` | 5 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.n_lt_050` | 0 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.n_undefined` | 0 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.19.rho` | 0.9439504065480042 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.19.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.19.n` | 16 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.20.rho` | 0.9411548284163881 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.20.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.20.n` | 24 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.21.rho` | 0.9413869294719631 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.21.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.21.n` | 24 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.22.rho` | 0.9764816297124751 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.22.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.22.n` | 24 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.23.rho` | 0.9268276971279107 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.23.p_perm` | 9.999000099990002e-05 |
| `stage2.v41_verdicts.H_Presence_LongHorizon.per_substrate.v0.23.n` | 24 |
| `stage2.v41_verdicts.H_Horizon_Decay.tier` | SECONDARY |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.n` | 80 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.rho_t1_t2` | 0.6563074188904829 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.rho_t1_t3` | 0.6378001341617113 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.D` | 0.01850728472877161 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.ci95[0]` | -0.13234909098437841 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.ci95[1]` | 0.16814289938386334 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.boot_dropped_degenerate` | 0 |
| `stage2.v41_verdicts.H_Horizon_Decay.phi.verdict` | MARGINAL |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.rho_t1_t2` | 0.9653753616072284 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.rho_t1_t3` | 0.9630744176166537 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.D` | 0.0023009439905746776 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.ci95[0]` | -0.025439812488873264 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.ci95[1]` | 0.032393237759366915 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.boot_dropped_degenerate` | 0 |
| `stage2.v41_verdicts.H_Horizon_Decay.pi_hat.verdict` | MARGINAL |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t2.rho` | 0.6453869683902721 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t2.n` | 83 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t2.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t2_t3.rho` | 0.6806643811207408 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t2_t3.n` | 80 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t2_t3.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t3.rho` | 0.6351356004674689 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t3.n` | 81 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.phi.t1_t3.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t2.rho` | 0.9653753616072284 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t2.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t2.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t2_t3.rho` | 0.9484577961604258 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t2_t3.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t2_t3.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t3.rho` | 0.9630744176166537 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t3.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.pi_hat.t1_t3.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t2.rho` | 0.7186990539951229 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t2.n` | 71 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t2.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t2_t3.rho` | 0.8007361066949132 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t2_t3.n` | 69 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t2_t3.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t3.rho` | 0.799588068550369 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t3.n` | 69 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.J.t1_t3.statistic` | pooled Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t2.rho` | 0.9566776162908305 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t2.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t2.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t2_t3.rho` | 0.865220775006494 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t2_t3.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t2_t3.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t3.rho` | 0.8955126958549771 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t3.n` | 112 |
| `stage2.v41_verdicts.H_Horizon_Decay.reported_alongside.C_P.t1_t3.statistic` | pooled within-substrate-rank Spearman |
| `stage2.v41_verdicts.H_Drift_Dissociation.tier` | SECONDARY |
| `stage2.v41_verdicts.H_Drift_Dissociation.verdict` | CONFIRMED |
| `stage2.v41_verdicts.H_Drift_Dissociation.rho` | 0.03239999371046976 |
| `stage2.v41_verdicts.H_Drift_Dissociation.p_perm_two_sided` | 0.7773222677732227 |
| `stage2.v41_verdicts.H_Drift_Dissociation.p_mc_se` | 0.004160436993839914 |
| `stage2.v41_verdicts.H_Drift_Dissociation.n` | 80 |
| `stage2.v41_verdicts.H_Drift_Dissociation.baseline_coupling_t2_rho` | 0.15148228106230816 |
| `stage2.v41_verdicts.H_Drift_Dissociation.baseline_note` | rho(phi_t2, pi_hat_t2) on within-substrate percentile ranks; descriptive, not verdict-bearing |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.tier` | TERTIARY (descriptive) |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.verdict` | DESCRIPTIVE |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.19.t2_phantom` | 8 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.19.retained_t3` | 8 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.19.proportion` | 1.0 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.20.t2_phantom` | 15 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.20.retained_t3` | 15 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.20.proportion` | 1.0 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.21.t2_phantom` | 10 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.21.retained_t3` | 9 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.21.proportion` | 0.9 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.22.t2_phantom` | 10 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.22.retained_t3` | 10 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.22.proportion` | 1.0 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.23.t2_phantom` | 15 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.23.retained_t3` | 14 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.per_substrate.v0.23.proportion` | 0.9333333333333333 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.pooled.t2_phantom` | 58 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.pooled.retained_t3` | 56 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.pooled.proportion` | 0.9655172413793104 |
| `stage2.v41_verdicts.H_Phantom_LongPersistence.v0_34_reference_t1_t2` | 56/57 |
| `stage2.v41_manipulation_checks.MC_ProbeParity.status` | PASS |
| `stage2.v41_manipulation_checks.MC_ProbeParity.source` | PARITY P4 recomputed at scoring |
| `stage2.v41_manipulation_checks.MC_Snapshot.status` | PASS |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-opus-4-5.t2` | claude-opus-4-5-20251101 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-opus-4-5.t3[0]` | claude-opus-4-5-20251101 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-opus-4-5.match` | true |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-sonnet-4-5.t2` | claude-sonnet-4-5-20250929 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-sonnet-4-5.t3[0]` | claude-sonnet-4-5-20250929 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.claude-sonnet-4-5.match` | true |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o.t2` | gpt-4o-2024-08-06 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o.t3[0]` | gpt-4o-2024-08-06 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o.match` | true |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o-mini.t2` | gpt-4o-mini-2024-07-18 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o-mini.t3[0]` | gpt-4o-mini-2024-07-18 |
| `stage2.v41_manipulation_checks.MC_Snapshot.per_model.gpt-4o-mini.match` | true |
| `stage2.v41_manipulation_checks.MC_Snapshot.n_match` | 4 |
| `stage2.v41_manipulation_checks.MC_Snapshot.mismatched` | [] |
| `stage2.v41_manipulation_checks.MC_Completeness.expected_total` | 852 |
| `stage2.v41_manipulation_checks.MC_Completeness.ok_total` | 852 |
| `stage2.v41_manipulation_checks.MC_Completeness.status` | PASS |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.claude-opus-4-5.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.claude-opus-4-5.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.claude-sonnet-4-5.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.claude-sonnet-4-5.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gpt-4o.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gpt-4o.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gpt-4o-mini.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gpt-4o-mini.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gemini-2.5-flash.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gemini-2.5-flash.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gemini-2.5-flash-lite.expected` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.per_model.gemini-2.5-flash-lite.ok` | 142 |
| `stage2.v41_manipulation_checks.MC_Completeness.unavailable_models` | [] |
| `stage2.v41_manipulation_checks.MC_Completeness.partially_failed_models` | [] |
| `stage2.v41_manipulation_checks.MC_Completeness.short_cells` | [] |
| `stage2.v41_manipulation_checks.MC_Truncation.status` | DESCRIPTIVE |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash-lite.calls` | 164 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash-lite.truncated` | 10 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash-lite.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash-lite.share_truncated` | 0.06097560975609756 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-opus-4-5.calls` | 164 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-opus-4-5.truncated` | 18 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-opus-4-5.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-opus-4-5.share_truncated` | 0.10975609756097561 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-sonnet-4-5.calls` | 193 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-sonnet-4-5.truncated` | 1 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-sonnet-4-5.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.claude-sonnet-4-5.share_truncated` | 0.0051813471502590676 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o.calls` | 164 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o.truncated` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o.share_truncated` | 0.0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o-mini.calls` | 164 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o-mini.truncated` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o-mini.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gpt-4o-mini.share_truncated` | 0.0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash.calls` | 164 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash.truncated` | 58 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash.finish_reason_missing` | 0 |
| `stage2.v41_manipulation_checks.MC_Truncation.per_model.gemini-2.5-flash.share_truncated` | 0.35365853658536583 |
| `stage2.v41_manipulation_checks.MC_Truncation.note` | t1/t2 recorded no finish reasons; no wave contrast |
| `stage2.descriptive_retest_t2_t3.C_star[0]` | 0.6473238536507431 |
| `stage2.descriptive_retest_t2_t3.C_star[1]` | 52 |
| `stage2.descriptive_retest_t2_t3.P[0]` | 0.9542888066830918 |
| `stage2.descriptive_retest_t2_t3.P[1]` | 112 |
| `stage2.consistency_check.rho_Cstar_P_t3_matches_v19` | true |
| `stage2.class.class` | A |
| `stage2.class.flags` | [] |
| `stage2.class.why` | H_Dissociation_t3 CONFIRMED, H_Consistency_Reliability CONFIRMED |
| `inputs_sha256.osf/v29/data/v29_verdicts.json` | 73fdc5e076b0625619f90e6c1038826d60a9e0dd01dda1cfc31d29a78ed23f27 |
| `inputs_sha256.osf/v30/v30_cpc_verdicts.json` | 61ac89ab2bfff72a757a540f28154cb35a60e5b88e8ad295ed2e70a435956c15 |
| `inputs_sha256.osf/v31/v31_cpc_verdicts.json` | 1124b70dcdbd59737ca843f72b228115b60c7cb25a73d380d174f6bc3953fd5e |
| `inputs_sha256.osf/v32/v32_verdicts.json` | d8591fb8f16a391e3f2584b78b5a042293699898f0644c9e6545d17a7e33620b |
| `inputs_sha256.osf/v33/v33_provider_asymmetry_verdicts.json` | 9c513273f8c0851b71147b57543664455a801a1279c862b3c642cea2008d096d |
| `inputs_sha256.osf/v34/v34_verdicts.json` | b838b5352f35d3ae9e95c33dc6f8cb791f6f57eb83f9dfdc29b918649a115ee5 |
| `inputs_sha256.osf/v35/v35_verdicts.json` | 68a219607ca615047c55930afc7e12f137698c97d8b50aeb05364ba505797303 |
| `inputs_sha256.osf/aias_2_0/inputs/v36_verdicts.json` | 3c41f78a70f02df010c88d3611fb15deae10276bb217eb7a125ec90b90d2fb8b |
| `inputs_sha256.osf/methodology/v1_7/v1_7_cpc_verdicts.json` | 2ad30dd2ec04dfa1583c44b183ee1caa04a57b35cf3dc7024c1369ad49777742 |
| `inputs_sha256.osf/v41/registries/v1_8_verdicts.json` | a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78 |
| `inputs_sha256.osf/v37/v37_verdicts.json` | 7f46c853a2395b7f6bf1b4ab83d0786f8afa3c36eb6d41d6e45085a4d3103461 |
| `inputs_sha256.osf/methodology/v1_9/v1_9_calibration.json` | 4d2ddb982a3372fa4f8c68e5bcf1a9511684186568fb6d37fbc2562b612388bf |
| `inputs_sha256./home/claude/reproduction/files/osf/v41/v41_verdicts.json` | 0d3f5dfcf0a920e642aa613f5bf45dce66dd155eb6fd4ee054ed4d4bb700d4e2 |
| `inputs_sha256./home/claude/reproduction/files/osf/methodology/v1_9/v1_9_verdicts.json` | 3d838f92821a5ae41c33bdb9a209432e0fdbc505ce7c53f8a17e8c438745967d |

Lineage (per phase: source, era, SSRN id/status, extracted verdict strings):

- **v0.29** `osf/v29/data/v29_verdicts.json`, Presence (carried by citation), SSRN 6870778 (posted): {"result": "CONFIRMED"}
- **v0.30** `osf/v30/v30_cpc_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6875319 (declined): {"F1_H_CPC_Computable": "CONFIRM", "F2_H_CPC_LevelConfound": "UNDETERMINED", "F3_H_CPC_LevelCorrected": "UNDETERMINED", "F4_H_CPC_SubstrateVariation": "CONFIRM"}
- **v0.31** `osf/v31/v31_cpc_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6880959 (withdrawn): {"H_CPC_Computable": "CONFIRM", "H_CPC_CrossCategory": "CONFIRM"}
- **v0.32** `osf/v32/v32_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6898581 (posted): {"PRIMARY_H_ScoreRankStable": "CONFIRMED", "SECONDARY_H_ScoreMagnitudeStable": "FALSIFIED", "TERTIARY_H_EmergingInstability": "FALSIFIED"}
- **v0.33** `osf/v33/v33_provider_asymmetry_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6909019 (posted): {"H_Provider_Asymmetry": "CONFIRMED", "H_Provider_Beyond_Presence": "CONFIRMED", "H_Provider_Ordinal": "UNINFORMATIVE (n.s.; N=5 underpowered)"}
- **v0.34** `osf/v34/v34_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6915458 (posted): {"verdicts.H_CPC_Temporal_Stability": "CONFIRMED", "verdicts.H_CPC_Drift_Beyond_Presence": "MARGINAL", "verdicts.H_Presence_Temporal_Stability": "MARGINAL", "verdicts.H_Phantom_Temporal_Persistence": "DESCRIPTIVE"}
- **v0.35** `osf/v35/v35_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6921758 (declined): {"verdicts.H_Phantom_CPC_Signature": "CONFIRMED", "verdicts.H_Phantom_Beyond_Presence": "UNDETERMINED (control flip)", "verdicts.H_Phantom_Beyond_Presence.control_C_P": "CONFIRMED", "verdicts.H_Phantom_Beyond_Presence.control_recall_mean": "FALSIFIED", "verdicts.H_Phantom_Cross_Substrate": "UNINFORMATIVE (n.s.; underpowered N=4; 4/4 concordant, p=0.125)", "verdicts.H_Phantom_t2_Stability": "DESCRIPTIVE", "sensitivity.loso_raw.per_leftout.v0.19": "CONFIRMED", "sensitivity.loso_raw.per_leftout.v0.20": "CONFIRMED", "sensitivity.loso_raw.per_leftout.v0.21": "CONFIRMED", "sensitivity.loso_raw.per_leftout.v0.22": "CONFIRMED", "sensitivity.loso_raw.per_leftout.v0.23": "CONFIRMED", "sensitivity.loso_gate.per_leftout.v0.19": "UNDETERMINED (control flip)", "sensitivity.loso_gate.per_leftout.v0.20": "UNDETERMINED (control flip)", "sensitivity.loso_gate.per_leftout.v0.21": "UNDETERMINED (control flip)", "sensitivity.loso_gate.per_leftout.v0.22": "UNDETERMINED (control flip)", "sensitivity.loso_gate.per_leftout.v0.23": "UNDETERMINED (control flip)"}
- **v0.36** `osf/aias_2_0/inputs/v36_verdicts.json`, CV-CPC era (lineage; instrument not adopted per v1.7), SSRN 6927958 (declined): {"hypotheses.H_RegimeInheritance": "NOT SUPPORTED", "hypotheses.H_RegimeAutonomy": "NOT SUPPORTED", "hypotheses.H_ResidualStructure": "NOT SUPPORTED", "hypotheses.H_SaturationDegeneracy": "NOT SUPPORTED"}
- **v1.7** `osf/methodology/v1_7/v1_7_cpc_verdicts.json`, CV-CPC falsified (turning point), SSRN 6878818 (posted): {"H_CPC_Defined": "FALSIFIED", "H_CPC_Dissociates": "FALSIFIED", "H_CPC_PhantomNull": "CONFIRM"}
- **v1.8** `osf/v41/registries/v1_8_verdicts.json`, phi instrument (AIAS 2.0 evidence), SSRN 6963359 (posted): {"verdicts.H_CV_Reproduces": "CONFIRMED (|rho| >= 0.50)", "verdicts.H_MeanIndependent": "CONFIRMED (|rho| <= 0.50)", "verdicts.H_LowRecallDefined": "CONFIRMED (full recovery; 100% phi-defined among >=1-surfacing AND phi-defined strictly contains CV-CPC_raw-defined AND non-empty low-recall gain)", "verdicts.H_GradedRecognition": "FORWARD-SPEC (frozen data not re-scorable)", "verdicts.H_PositionalDissociation": "CONFIRMED (non-redundant + discordants exist)", "verdicts.H_PhantomSignature": "NULL"}
- **v0.37** `osf/v37/v37_verdicts.json`, phi (AIAS 2.0 evidence), SSRN None (not yet submitted): {"verdicts.H_IL_Consistency": "FALSIFIED", "verdicts.H_IL_Presence_Robustness": "partial_NULL", "verdicts.H_IL_Cross_Substrate": "DESCRIPTIVE (N=3 substrates; no inferential claim)", "verdicts.H_IL_t2_Stability": "DESCRIPTIVE (walled; no confirmatory threshold)"}
- **v1.9-stage1** `osf/methodology/v1_9/v1_9_calibration.json`, scoring rule (AIAS 2.0 evidence; calibration, not a test), SSRN None (no paper yet): {}

## 7. Table B: the 55 summary quantities (as in results.csv)

| id | value | how |
|---|---|---|
| ps-brands-all | 112 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.n_units (t1 112, t2 112, t3 112); score_v41.N_BRAND_UNITS = 112 |
| ps-categories | 5 | scripts/aias_2_0_synthesis_data.py summarize(): number of per_substrate entries = len(score_v41.OMNI) = 5 ['v0.19', 'v0.20', 'v0.21', 'v0.22', 'v0.23'] |
| ps-brands-v19 | 16 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.<wave>.per_substrate['v0.19'].n_units (same in t1/t2/t3); score_v41.EXPECTED_BRANDS = 16 |
| ps-brands-v20 | 24 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.<wave>.per_substrate['v0.20'].n_units (same in t1/t2/t3); score_v41.EXPECTED_BRANDS = 24 |
| ps-brands-v21 | 24 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.<wave>.per_substrate['v0.21'].n_units (same in t1/t2/t3); score_v41.EXPECTED_BRANDS = 24 |
| ps-brands-v22 | 24 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.<wave>.per_substrate['v0.22'].n_units (same in t1/t2/t3); score_v41.EXPECTED_BRANDS = 24 |
| ps-brands-v23 | 24 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.<wave>.per_substrate['v0.23'].n_units (same in t1/t2/t3); score_v41.EXPECTED_BRANDS = 24 |
| ps-models | 6 | scripts/aias_2_0_synthesis_data.py build(): stage2.panel_used (t3 panel, read from v1_9_verdicts.json) = ['claude-opus-4-5', 'claude-sonnet-4-5', 'gpt-4o', 'gpt-4o-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']; score_v41.M = 6; all three waves' files carry the same 6 models |
| ps-frames | 6 | score_v41.F = 6 (frames per model); own check: every model has 6 distinct recall frames/probes in every category in the t3 files (work/make_results.py) |
| ps-t3-responses | 852 | own count (work/make_results.py) over osf/v41/data: recognition + recall answers present (non-empty, status ok where recorded), 6 panel models; breakdown in log |
| ps-t3-recognition | 672 | own count: Phase A rows (v19 parsed rows per brand x model; v20-v22 non-empty response_text; v23 status ok + non-empty response) |
| ps-t3-recall | 180 | own count: Phase B answers (v19 distinct (model, frame) pairs in the parsed file; v20-v22 non-empty response_text rows; v23 status ok + non-empty response) |
| ps-rated-t1 | 55 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.n_rated (C* not None, n >= 6) |
| ps-rated-t2 | 54 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.n_rated (C* not None, n >= 6) |
| ps-rated-t3 | 54 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.n_rated (C* not None, n >= 6) |
| ps-share-t1 | 0.49107142857142855 | own: n_rated/n_units = 55/112 = 55/112 from scripts/aias_2_0_synthesis_data.py summaries.t1 (builder writes share_not_rated = 0.5089285714285714) |
| ps-share-t2 | 0.48214285714285715 | own: n_rated/n_units = 54/112 = 27/56 from scripts/aias_2_0_synthesis_data.py summaries.t2 (builder writes share_not_rated = 0.5178571428571429) |
| ps-share-t3 | 0.48214285714285715 | own: n_rated/n_units = 54/112 = 27/56 from scripts/aias_2_0_synthesis_data.py summaries.t3 (builder writes share_not_rated = 0.5178571428571429) |
| ps-share-t1-v19 | 0.5 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.per_substrate['v0.19'].share_rated = 8/16 = 1/2 |
| ps-share-t2-v19 | 0.5 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.per_substrate['v0.19'].share_rated = 8/16 = 1/2 |
| ps-share-t3-v19 | 0.5 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.19'].share_rated = 8/16 = 1/2 |
| ps-share-t1-v20 | 0.4166666666666667 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.per_substrate['v0.20'].share_rated = 10/24 = 5/12 |
| ps-share-t2-v20 | 0.375 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.per_substrate['v0.20'].share_rated = 9/24 = 3/8 |
| ps-share-t3-v20 | 0.375 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.20'].share_rated = 9/24 = 3/8 |
| ps-share-t1-v21 | 0.5833333333333334 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.per_substrate['v0.21'].share_rated = 14/24 = 7/12 |
| ps-share-t2-v21 | 0.5833333333333334 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.per_substrate['v0.21'].share_rated = 14/24 = 7/12 |
| ps-share-t3-v21 | 0.5416666666666666 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.21'].share_rated = 13/24 = 13/24 |
| ps-share-t1-v22 | 0.5833333333333334 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.per_substrate['v0.22'].share_rated = 14/24 = 7/12 |
| ps-share-t2-v22 | 0.5833333333333334 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.per_substrate['v0.22'].share_rated = 14/24 = 7/12 |
| ps-share-t3-v22 | 0.5833333333333334 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.22'].share_rated = 14/24 = 7/12 |
| ps-share-t1-v23 | 0.375 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.per_substrate['v0.23'].share_rated = 9/24 = 3/8 |
| ps-share-t2-v23 | 0.375 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.per_substrate['v0.23'].share_rated = 9/24 = 3/8 |
| ps-share-t3-v23 | 0.4166666666666667 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.23'].share_rated = 10/24 = 5/12 |
| ps-rated-t3-v19 | 8 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.19'].n_rated (8 of 16 rated in November) |
| ps-rated-t3-v20 | 9 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.20'].n_rated (9 of 24 rated in November) |
| ps-rated-t3-v21 | 13 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.21'].n_rated (13 of 24 rated in November) |
| ps-rated-t3-v22 | 14 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.22'].n_rated (14 of 24 rated in November) |
| ps-rated-t3-v23 | 10 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.per_substrate['v0.23'].n_rated (10 of 24 rated in November) |
| ps-rhoCP-t1 | 0.07293925573105668 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.rho_Cstar_P = score_v1_9._rho(rows,'C','P') (score_v41.pooled_within_rho: within-substrate average ranks, pooled Pearson) |
| ps-rhoCP-t1-n | 55 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t1.rho_Cstar_P_n |
| ps-rhoCP-t2 | 0.08153268408519941 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.rho_Cstar_P = score_v1_9._rho(rows,'C','P') (score_v41.pooled_within_rho: within-substrate average ranks, pooled Pearson) |
| ps-rhoCP-t2-n | 54 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t2.rho_Cstar_P_n |
| ps-rhoCP-t3 | 0.18949782059932604 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.rho_Cstar_P = score_v1_9._rho(rows,'C','P') (score_v41.pooled_within_rho: within-substrate average ranks, pooled Pearson) |
| ps-rhoCP-t3-n | 54 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.rho_Cstar_P_n |
| ps-retestP-t1t2 | 0.9695933242098346 | scripts/aias_2_0_synthesis_data.py parity_t1_t2(): A5_retest_P builder value = score_v1_9.retest(rows_t1, rows_t2, 'P') |
| ps-retestP-t1t2-n | 112 | scripts/aias_2_0_synthesis_data.py parity_t1_t2(): A5_retest_P builder n |
| ps-retestP-t2t3 | 0.9542888066830918 | scripts/aias_2_0_synthesis_data.py build(): stage2.descriptive_retest_t2_t3.P = score_v1_9.retest(rows_t2(panel_used), rows_t3, 'P') |
| ps-retestP-t2t3-n | 112 | scripts/aias_2_0_synthesis_data.py build(): stage2.descriptive_retest_t2_t3.P n |
| ps-retestC-t1t2 | 0.7357486264955685 | scripts/aias_2_0_synthesis_data.py parity_t1_t2(): A4_retest_C builder value = score_v1_9.retest(rows_t1, rows_t2, 'C') (rated in both) |
| ps-retestC-t1t2-n | 53 | scripts/aias_2_0_synthesis_data.py parity_t1_t2(): A4_retest_C builder n |
| ps-retestC-t2t3 | 0.6473238536507431 | scripts/aias_2_0_synthesis_data.py build(): stage2.descriptive_retest_t2_t3.C_star = score_v1_9.retest(rows_t2(panel_used), rows_t3, 'C') (rated in both) |
| ps-retestC-t2t3-n | 52 | scripts/aias_2_0_synthesis_data.py build(): stage2.descriptive_retest_t2_t3.C_star n |
| ps-rhoAP-t3 | 0.969272869350446 | scripts/aias_2_0_synthesis_data.py summarize(): summaries.t3.rho_A_P_descriptive = score_v1_9._rho(rows_t3,'A','P'), A = composite(P, C*, 'ADD'); n = 112 |
| ps-below6-t2 | 58 | own count over the builder's t2 rows (full 6-model panel): n < 6 |
| ps-below6-t2-still-t3 | 56 | own count: of those t2 brands, builder t3 rows with n < 6 |

t3 responses, my own count from `osf/v41/data` (Phase A = recognition, Phase B = recall):

- v0.19/A: 96
- v0.19/B: 36
- v0.20/A: 144
- v0.20/B: 36
- v0.21/A: 144
- v0.21/B: 36
- v0.22/A: 144
- v0.22/B: 36
- v0.23/A: 144
- v0.23/B: 36
- Recall frames per model at t3 (every category and model): [6]

Definitions I used. v0.19's t3 files are the parsed results, not raw responses. A recognition answer is one row per (brand, model) (96). A recall answer is one distinct (model, frame) pair (36), and each pair is coded for all 16 brands (576 rows). For v0.20–v0.22, an answer is a row with non-empty `response_text`. For v0.23, an answer is a record with `status == 'ok'` and a non-empty `response`. Every file had all its answers present.

Brands under 6 mentions at t2 (58): v0.19/Dan Clark Audio, v0.19/Denon, v0.19/Final Audio, v0.19/Koss, v0.19/Meze, v0.19/Spirit Torino, v0.19/Stax, v0.19/ZMF Headphones, v0.20/Estée Lauder, v0.20/Lancôme, v0.20/Sisley, v0.20/Dior Beauty, v0.20/Chanel Beauty, v0.20/La Prairie, v0.20/Clé de Peau Beauté, v0.20/Rare Beauty, v0.20/Rhode, v0.20/Fenty Skin, v0.20/Goop, v0.20/Glossier, v0.20/Tower 28, v0.20/Eucerin, v0.20/Bioderma, v0.21/Bobbi Brown, v0.21/Giorgio Armani Beauty, v0.21/Hourglass, v0.21/Chantecaille, v0.21/Laura Mercier, v0.21/Haus Labs, v0.21/CoverGirl, v0.21/Revlon, v0.21/Wet n Wild, v0.21/Milani Cosmetics, v0.22/Rivian, v0.22/Lucid, v0.22/Polestar, v0.22/Fisker, v0.22/Nissan, v0.22/Pontiac, v0.22/Oldsmobile, v0.22/Plymouth, v0.22/Mercury, v0.22/Saturn, v0.23/S01, v0.23/S03, v0.23/S06, v0.23/S07, v0.23/S08, v0.23/S09, v0.23/S10, v0.23/S12, v0.23/S14, v0.23/S16, v0.23/S18, v0.23/S21, v0.23/S22, v0.23/S23, v0.23/S24

Of those, still under 6 at t3 (56): v0.19/Dan Clark Audio, v0.19/Denon, v0.19/Final Audio, v0.19/Koss, v0.19/Meze, v0.19/Spirit Torino, v0.19/Stax, v0.19/ZMF Headphones, v0.20/Estée Lauder, v0.20/Lancôme, v0.20/Sisley, v0.20/Dior Beauty, v0.20/Chanel Beauty, v0.20/La Prairie, v0.20/Clé de Peau Beauté, v0.20/Rare Beauty, v0.20/Rhode, v0.20/Fenty Skin, v0.20/Goop, v0.20/Glossier, v0.20/Tower 28, v0.20/Eucerin, v0.20/Bioderma, v0.21/Giorgio Armani Beauty, v0.21/Hourglass, v0.21/Chantecaille, v0.21/Laura Mercier, v0.21/Haus Labs, v0.21/CoverGirl, v0.21/Revlon, v0.21/Wet n Wild, v0.21/Milani Cosmetics, v0.22/Rivian, v0.22/Lucid, v0.22/Polestar, v0.22/Fisker, v0.22/Nissan, v0.22/Pontiac, v0.22/Oldsmobile, v0.22/Plymouth, v0.22/Mercury, v0.22/Saturn, v0.23/S01, v0.23/S03, v0.23/S06, v0.23/S07, v0.23/S08, v0.23/S09, v0.23/S12, v0.23/S14, v0.23/S16, v0.23/S18, v0.23/S21, v0.23/S22, v0.23/S23, v0.23/S24

Of those, rated (6 or more) at t3 (2): v0.21/Bobbi Brown, v0.23/S10

## 8. Per-brand values (1,008 = 112 brands × 3 waves × {P, C*, N})

Ids `pb-<wave>-<vNN>-<nn>-<P|C|N>`. `nn` is the position in Python `sorted()` of the builder's brand key within the category (the `brand` column of `aias_2_0_profiles.csv`). Brand sets are identical across the three waves (checked: True). P and C* are Python `repr()`, i.e. full double precision. N is the total mentions over the 6 models (sum of per-model frame counts, 0–36).

**Note on v0.23.** The builder keys premium-spirits brands by id (`S01`…`S24`), not by name, so `nn` for v23 follows the id order. If ids were instead meant to follow the sorted brand *names*, the positions change. The mapping is below, and the `how` column of every v23 row gives the id and name.

| v23 id | brand name | nn (used: id order) | nn if sorted by name |
|---|---|---|---|
| S01 | Johnnie Walker | 01 | 14 |
| S02 | Hennessy | 02 | 11 |
| S03 | Jack Daniel's | 03 | 12 |
| S04 | Patrón | 04 | 19 |
| S05 | Grey Goose | 05 | 09 |
| S06 | Bacardi | 06 | 01 |
| S07 | Bombay Sapphire | 07 | 02 |
| S08 | Jameson | 08 | 13 |
| S09 | Lagavulin | 09 | 15 |
| S10 | Clase Azul | 10 | 04 |
| S11 | Hendrick's | 11 | 10 |
| S12 | Woodford Reserve | 12 | 24 |
| S13 | Monkey 47 | 13 | 17 |
| S14 | The Balvenie | 14 | 23 |
| S15 | Rémy Martin | 15 | 21 |
| S16 | Casamigos | 16 | 03 |
| S17 | Fortaleza | 17 | 08 |
| S18 | Compass Box | 18 | 05 |
| S19 | Nikka | 19 | 18 |
| S20 | Del Maguey | 20 | 06 |
| S21 | Fernet-Branca | 21 | 07 |
| S22 | Redbreast | 22 | 20 |
| S23 | St. George Spirits | 23 | 22 |
| S24 | Mezcal Vago | 24 | 16 |

### v0.19 (v19)

| nn | brand | P t1 | C* t1 | N t1 | P t2 | C* t2 | N t2 | P t3 | C* t3 | N t3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Audeze | 61.111111111111114 | 81.9047619047619 | 15 | 62.96296296296296 | 82.5 | 16 | 62.96296296296296 | 82.5 | 16 |
| 02 | Audio-Technica | 74.07407407407408 | 35.06493506493506 | 22 | 68.51851851851852 | 72.44582043343654 | 19 | 70.37037037037037 | 63.74999999999999 | 20 |
| 03 | Beyerdynamic | 74.07407407407408 | 62.33766233766234 | 22 | 70.37037037037037 | 63.74999999999999 | 20 | 66.66666666666667 | 77.77777777777779 | 18 |
| 04 | Dan Clark Audio | 42.59259259259259 | not rated | 5 | 35.18518518518518 | not rated | 1 | 40.74074074074074 | not rated | 4 |
| 05 | Denon | 16.666666666666668 | not rated | 0 | 14.814814814814815 | not rated | 2 | 16.666666666666668 | not rated | 0 |
| 06 | Final Audio | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 07 | Focal | 68.51851851851852 | 72.44582043343654 | 19 | 68.51851851851852 | 72.44582043343652 | 19 | 66.66666666666667 | 70.37037037037037 | 18 |
| 08 | Grado | 46.2962962962963 | 85.71428571428571 | 7 | 48.148148148148145 | 80.35714285714286 | 8 | 44.444444444444436 | 86.66666666666667 | 6 |
| 09 | HiFiMan | 57.40740740740741 | 86.2876254180602 | 13 | 59.25925925925926 | 85.71428571428571 | 14 | 62.96296296296296 | 78.75 | 16 |
| 10 | Koss | 11.111111111111109 | not rated | 0 | 11.111111111111109 | not rated | 0 | 11.111111111111109 | not rated | 0 |
| 11 | Meze | 40.74074074074074 | not rated | 4 | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 |
| 12 | Sennheiser | 88.8888888888889 | -2.220446049250313e-14 | 30 | 83.33333333333333 | -2.220446049250313e-14 | 30 | 88.8888888888889 | -2.220446049250313e-14 | 30 |
| 13 | Sony | 66.66666666666667 | 50.000000000000014 | 24 | 59.25925925925926 | 54.18060200668897 | 23 | 51.851851851851855 | 58.44155844155843 | 22 |
| 14 | Spirit Torino | 27.777777777777782 | not rated | 0 | 27.777777777777782 | not rated | 0 | 27.777777777777782 | not rated | 0 |
| 15 | Stax | 35.18518518518518 | not rated | 4 | 37.03703703703704 | not rated | 2 | 33.333333333333336 | not rated | 3 |
| 16 | ZMF Headphones | 35.18518518518518 | not rated | 1 | 37.03703703703704 | not rated | 2 | 35.18518518518518 | not rated | 1 |

### v0.20 (v20)

| nn | brand | P t1 | C* t1 | N t1 | P t2 | C* t2 | N t2 | P t3 | C* t3 | N t3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Augustinus Bader | 46.2962962962963 | 85.71428571428571 | 7 | 46.2962962962963 | 91.62561576354679 | 7 | 50.0 | 81.48148148148148 | 9 |
| 02 | Bioderma | 37.03703703703704 | not rated | 2 | 38.88888888888889 | not rated | 3 | 35.18518518518518 | not rated | 1 |
| 03 | CeraVe | 98.14814814814815 | 85.71428571428572 | 35 | 96.29629629629629 | 88.23529411764706 | 34 | 96.29629629629629 | 70.58823529411767 | 34 |
| 04 | Cetaphil | 48.148148148148145 | 96.42857142857143 | 8 | 44.444444444444436 | 80.0 | 6 | 46.2962962962963 | 91.62561576354679 | 7 |
| 05 | Chanel Beauty | 16.666666666666668 | not rated | 0 | 11.111111111111109 | not rated | 0 | 16.666666666666668 | not rated | 0 |
| 06 | Clé de Peau Beauté | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 07 | Dior Beauty | 16.666666666666668 | not rated | 0 | 11.111111111111109 | not rated | 0 | 16.666666666666668 | not rated | 0 |
| 08 | Drunk Elephant | 88.8888888888889 | 93.33333333333333 | 30 | 88.8888888888889 | 100.0 | 30 | 90.74074074074075 | 96.7741935483871 | 31 |
| 09 | Estée Lauder | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 | 37.03703703703704 | not rated | 2 |
| 10 | Eucerin | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 | 42.59259259259259 | not rated | 5 |
| 11 | Fenty Skin | 40.74074074074074 | not rated | 4 | 42.59259259259259 | not rated | 5 | 37.03703703703704 | not rated | 2 |
| 12 | Glossier | 38.88888888888889 | not rated | 3 | 37.03703703703704 | not rated | 2 | 42.59259259259259 | not rated | 5 |
| 13 | Goop | 12.962962962962962 | not rated | 1 | 18.51851851851852 | not rated | 1 | 22.222222222222218 | not rated | 0 |
| 14 | La Mer | 50.0 | 91.35802469135803 | 9 | 50.0 | 96.2962962962963 | 9 | 50.0 | 96.2962962962963 | 9 |
| 15 | La Prairie | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 16 | La Roche-Posay | 83.33333333333333 | 96.2962962962963 | 27 | 85.18518518518518 | 91.07142857142857 | 28 | 83.33333333333333 | 86.41975308641975 | 27 |
| 17 | Lancôme | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 18 | Paula's Choice | 72.22222222222223 | 70.47619047619047 | 21 | 85.18518518518518 | 80.35714285714286 | 28 | 81.48148148148148 | 87.6923076923077 | 26 |
| 19 | Rare Beauty | 5.5555555555555545 | not rated | 3 | 1.8518518518518519 | not rated | 1 | 0.0 | not rated | 0 |
| 20 | Rhode | 46.2962962962963 | 79.80295566502463 | 7 | 38.88888888888889 | not rated | 3 | 40.74074074074074 | not rated | 4 |
| 21 | Sisley | 37.03703703703704 | not rated | 2 | 35.18518518518518 | not rated | 1 | 37.03703703703704 | not rated | 2 |
| 22 | SkinCeuticals | 83.33333333333333 | 91.35802469135803 | 27 | 77.77777777777777 | 91.66666666666667 | 24 | 81.48148148148148 | 92.3076923076923 | 26 |
| 23 | The Ordinary | 90.74074074074075 | 96.7741935483871 | 31 | 87.03703703703705 | 97.53694581280789 | 29 | 88.8888888888889 | 93.33333333333333 | 30 |
| 24 | Tower 28 | 12.962962962962962 | not rated | 1 | 16.666666666666668 | not rated | 0 | 18.51851851851852 | not rated | 1 |

### v0.21 (v21)

| nn | brand | P t1 | C* t1 | N t1 | P t2 | C* t2 | N t2 | P t3 | C* t3 | N t3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Anastasia Beverly Hills | 57.40740740740741 | 94.31438127090301 | 13 | 55.55555555555555 | 79.16666666666667 | 12 | 61.111111111111114 | 74.28571428571429 | 15 |
| 02 | Bobbi Brown | 48.148148148148145 | 96.42857142857143 | 8 | 42.59259259259259 | not rated | 5 | 48.148148148148145 | 85.71428571428571 | 8 |
| 03 | Chantecaille | 33.333333333333336 | not rated | 0 | 35.18518518518518 | not rated | 1 | 33.333333333333336 | not rated | 0 |
| 04 | Charlotte Tilbury | 87.03703703703705 | 73.89162561576354 | 29 | 90.74074074074075 | 73.54838709677418 | 31 | 92.5925925925926 | 84.375 | 32 |
| 05 | CoverGirl | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 06 | Fenty Beauty | 79.62962962962963 | 85.09090909090908 | 25 | 81.48148148148148 | 69.23076923076923 | 26 | 79.62962962962963 | 85.09090909090908 | 25 |
| 07 | Giorgio Armani Beauty | 35.18518518518518 | not rated | 1 | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 |
| 08 | Haus Labs | 40.74074074074074 | not rated | 4 | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 |
| 09 | Hourglass | 37.03703703703704 | not rated | 2 | 38.88888888888889 | not rated | 3 | 40.74074074074074 | not rated | 4 |
| 10 | Huda Beauty | 53.7037037037037 | 85.0909090909091 | 11 | 53.7037037037037 | 72.00000000000001 | 11 | 53.7037037037037 | 67.63636363636364 | 11 |
| 11 | Kylie Cosmetics | 42.59259259259259 | not rated | 5 | 48.148148148148145 | 91.07142857142857 | 8 | 44.444444444444436 | 93.33333333333333 | 6 |
| 12 | L'Oréal Paris | 46.2962962962963 | 79.80295566502463 | 7 | 50.0 | 76.54320987654322 | 9 | 38.88888888888889 | not rated | 3 |
| 13 | Laura Mercier | 42.59259259259259 | not rated | 5 | 40.74074074074074 | not rated | 4 | 42.59259259259259 | not rated | 5 |
| 14 | MAC Cosmetics | 62.96296296296296 | 90.0 | 16 | 68.51851851851852 | 87.30650154798762 | 19 | 62.96296296296296 | 78.75 | 16 |
| 15 | Maybelline | 55.55555555555555 | 54.16666666666667 | 12 | 61.111111111111114 | 66.66666666666666 | 15 | 50.0 | 46.91358024691359 | 9 |
| 16 | Milani Cosmetics | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 17 | NARS | 87.03703703703705 | 85.71428571428571 | 29 | 81.48148148148148 | 87.6923076923077 | 26 | 81.48148148148148 | 78.46153846153847 | 26 |
| 18 | NYX Professional Makeup | 53.7037037037037 | 63.27272727272728 | 11 | 46.2962962962963 | 73.89162561576354 | 7 | 44.444444444444436 | 73.33333333333334 | 6 |
| 19 | Pat McGrath Labs | 59.25925925925926 | 93.5064935064935 | 14 | 62.96296296296296 | 90.0 | 16 | 62.96296296296296 | 71.24999999999999 | 16 |
| 20 | Rare Beauty | 66.66666666666667 | 96.2962962962963 | 18 | 64.81481481481481 | 94.73684210526316 | 17 | 70.37037037037037 | 93.75 | 20 |
| 21 | Revlon | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 22 | Tom Ford Beauty | 44.444444444444436 | 80.0 | 6 | 44.444444444444436 | 73.33333333333334 | 6 | 35.18518518518518 | not rated | 1 |
| 23 | Wet n Wild | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 24 | e.l.f. Cosmetics | 51.851851851851855 | 87.6923076923077 | 10 | 55.55555555555555 | 83.33333333333334 | 12 | 44.444444444444436 | 73.33333333333334 | 6 |

### v0.22 (v22)

| nn | brand | P t1 | C* t1 | N t1 | P t2 | C* t2 | N t2 | P t3 | C* t3 | N t3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | BMW | 74.07407407407408 | 93.5064935064935 | 22 | 74.07407407407408 | 93.5064935064935 | 22 | 75.92592592592592 | 78.26086956521738 | 23 |
| 02 | Bentley | 55.55555555555555 | 100.0 | 12 | 55.55555555555555 | 100.0 | 12 | 53.7037037037037 | 98.18181818181819 | 11 |
| 03 | Cadillac | 48.148148148148145 | 91.07142857142857 | 8 | 46.2962962962963 | 79.80295566502463 | 7 | 44.444444444444436 | 93.33333333333333 | 6 |
| 04 | Chevrolet | 46.2962962962963 | 97.53694581280789 | 7 | 46.2962962962963 | 97.53694581280789 | 7 | 44.444444444444436 | 93.33333333333333 | 6 |
| 05 | Fisker | 27.777777777777782 | not rated | 0 | 27.777777777777782 | not rated | 0 | 27.777777777777782 | not rated | 0 |
| 06 | Ford | 48.148148148148145 | 96.42857142857143 | 8 | 53.7037037037037 | 93.81818181818183 | 11 | 51.851851851851855 | 83.07692307692308 | 10 |
| 07 | Honda | 66.66666666666667 | 100.0 | 18 | 66.66666666666667 | 100.0 | 18 | 66.66666666666667 | 100.0 | 18 |
| 08 | Hyundai | 62.96296296296296 | 90.0 | 16 | 61.111111111111114 | 89.52380952380952 | 15 | 61.111111111111114 | 97.14285714285714 | 15 |
| 09 | Jaguar | 51.851851851851855 | 92.3076923076923 | 10 | 50.0 | 96.2962962962963 | 9 | 48.148148148148145 | 91.07142857142857 | 8 |
| 10 | Lucid | 33.333333333333336 | not rated | 0 | 35.18518518518518 | not rated | 1 | 27.777777777777782 | not rated | 0 |
| 11 | Mercedes-Benz | 81.48148148148148 | 96.92307692307692 | 26 | 81.48148148148148 | 92.3076923076923 | 26 | 79.62962962962963 | 93.81818181818181 | 25 |
| 12 | Mercury | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 27.777777777777782 | not rated | 0 |
| 13 | Nissan | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 14 | Oldsmobile | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 15 | Plymouth | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 16 | Polestar | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 35.18518518518518 | not rated | 1 |
| 17 | Pontiac | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 18 | Porsche | 92.5925925925926 | 84.375 | 32 | 90.74074074074075 | 89.03225806451613 | 31 | 90.74074074074075 | 89.03225806451613 | 31 |
| 19 | Rivian | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 |
| 20 | Rolls-Royce | 57.40740740740741 | 94.31438127090301 | 13 | 62.96296296296296 | 97.5 | 16 | 64.81481481481481 | 98.45201238390094 | 17 |
| 21 | Saturn | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 22 | Tesla | 57.40740740740741 | 94.31438127090301 | 13 | 61.111111111111114 | 93.33333333333333 | 15 | 55.55555555555555 | 91.66666666666667 | 12 |
| 23 | Toyota | 77.77777777777777 | 95.83333333333334 | 24 | 74.07407407407408 | 97.40259740259741 | 22 | 75.92592592592592 | 98.32775919732441 | 23 |
| 24 | Volkswagen | 46.2962962962963 | 97.53694581280789 | 7 | 46.2962962962963 | 97.53694581280789 | 7 | 46.2962962962963 | 97.53694581280789 | 7 |

### v0.23 (v23)

| nn | brand | P t1 | C* t1 | N t1 | P t2 | C* t2 | N t2 | P t3 | C* t3 | N t3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | S01 (Johnnie Walker) | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 | 37.03703703703704 | not rated | 2 |
| 02 | S02 (Hennessy) | 51.851851851851855 | 87.6923076923077 | 10 | 51.851851851851855 | 83.07692307692308 | 10 | 50.0 | 76.54320987654322 | 9 |
| 03 | S03 (Jack Daniel's) | 42.59259259259259 | not rated | 5 | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 |
| 04 | S04 (Patrón) | 53.7037037037037 | 85.0909090909091 | 11 | 48.148148148148145 | 91.07142857142857 | 8 | 48.148148148148145 | 80.35714285714286 | 8 |
| 05 | S05 (Grey Goose) | 50.0 | 86.41975308641975 | 9 | 51.851851851851855 | 73.84615384615385 | 10 | 51.851851851851855 | 73.84615384615385 | 10 |
| 06 | S06 (Bacardi) | 37.03703703703704 | not rated | 2 | 37.03703703703704 | not rated | 2 | 35.18518518518518 | not rated | 1 |
| 07 | S07 (Bombay Sapphire) | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 35.18518518518518 | not rated | 1 |
| 08 | S08 (Jameson) | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 |
| 09 | S09 (Lagavulin) | 40.74074074074074 | not rated | 4 | 38.88888888888889 | not rated | 3 | 38.88888888888889 | not rated | 3 |
| 10 | S10 (Clase Azul) | 42.59259259259259 | not rated | 5 | 42.59259259259259 | not rated | 5 | 44.444444444444436 | 80.0 | 6 |
| 11 | S11 (Hendrick's) | 50.0 | 46.91358024691359 | 9 | 46.2962962962963 | 62.068965517241395 | 7 | 48.148148148148145 | 48.21428571428571 | 8 |
| 12 | S12 (Woodford Reserve) | 35.18518518518518 | not rated | 1 | 35.18518518518518 | not rated | 1 | 33.333333333333336 | not rated | 0 |
| 13 | S13 (Monkey 47) | 46.2962962962963 | 62.068965517241395 | 7 | 44.444444444444436 | 60.00000000000001 | 6 | 44.444444444444436 | 60.00000000000001 | 6 |
| 14 | S14 (The Balvenie) | 33.333333333333336 | not rated | 0 | 37.03703703703704 | not rated | 2 | 33.333333333333336 | not rated | 0 |
| 15 | S15 (Rémy Martin) | 51.851851851851855 | 83.07692307692307 | 10 | 44.444444444444436 | 93.33333333333333 | 6 | 51.851851851851855 | 83.07692307692307 | 10 |
| 16 | S16 (Casamigos) | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 17 | S17 (Fortaleza) | 50.0 | 76.54320987654322 | 9 | 50.0 | 76.54320987654322 | 9 | 48.148148148148145 | 69.64285714285714 | 8 |
| 18 | S18 (Compass Box) | 33.333333333333336 | not rated | 0 | 35.18518518518518 | not rated | 1 | 33.333333333333336 | not rated | 0 |
| 19 | S19 (Nikka) | 46.2962962962963 | 85.71428571428572 | 7 | 48.148148148148145 | 85.71428571428571 | 8 | 46.2962962962963 | 85.71428571428572 | 7 |
| 20 | S20 (Del Maguey) | 50.0 | 86.41975308641975 | 9 | 53.7037037037037 | 85.0909090909091 | 11 | 51.851851851851855 | 87.6923076923077 | 10 |
| 21 | S21 (Fernet-Branca) | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 | 33.333333333333336 | not rated | 0 |
| 22 | S22 (Redbreast) | 40.74074074074074 | not rated | 4 | 40.74074074074074 | not rated | 4 | 42.59259259259259 | not rated | 5 |
| 23 | S23 (St. George Spirits) | 37.03703703703704 | not rated | 2 | 37.03703703703704 | not rated | 2 | 37.03703703703704 | not rated | 2 |
| 24 | S24 (Mezcal Vago) | 40.74074074074074 | not rated | 4 | 38.88888888888889 | not rated | 3 | 37.03703703703704 | not rated | 2 |

## 9. My own verification of the extraction and statistics

- Wrapper rows vs the builder's `aias_2_0_profiles.csv` (P, C*, rated, n, A at the builder's 6-dp formatting): 336 rows compared, 0 mismatches. Builder CSV waves: ['t1', 't2', 't3'].
- Wrapper `build()` result vs the builder's written JSON (excluding `built_at_utc` and `inputs_sha256`): {"status": true, "spec": true, "parity_gates_v0_41": true, "parity_builder_vs_stage1": true, "summaries": true, "stage2": true, "lineage": true}.
- Independent recomputation of k, C_P, P, C* and n from the data files (own aggregation and formulas; only the v0.20–v0.22 text matcher `detect_mention` is deposited code):
  - t1: units 112, max|ΔP| = 0.0, max|ΔC*| = 0.0, rated-status mismatches 0, n mismatches 0, P bit-identical 112/112, C* bit-identical (incl. not rated) 112/112
  - t2: units 112, max|ΔP| = 0.0, max|ΔC*| = 0.0, rated-status mismatches 0, n mismatches 0, P bit-identical 112/112, C* bit-identical (incl. not rated) 112/112
  - t3: units 112, max|ΔP| = 0.0, max|ΔC*| = 0.0, rated-status mismatches 0, n mismatches 0, P bit-identical 112/112, C* bit-identical (incl. not rated) 112/112
- Independent recomputation of the 8 correlations from the full-precision rows (pandas `groupby().rank('average')` within category, `numpy.corrcoef`). results.csv uses the builder's values. The differences are floating-point rounding only:
  - rhoCP-t1: own 0.07293925573105677 (n 55), builder 0.07293925573105668 (n 55), |Δ| = 8.326672684688674e-17, n equal: True
  - rhoCP-t2: own 0.0815326840851994 (n 54), builder 0.08153268408519941 (n 54), |Δ| = 1.3877787807814457e-17, n equal: True
  - rhoCP-t3: own 0.18949782059932604 (n 54), builder 0.18949782059932604 (n 54), |Δ| = 0.0, n equal: True
  - rhoAP-t3: own 0.9692728693504459 (n 112), builder 0.969272869350446 (n 112), |Δ| = 1.1102230246251565e-16, n equal: True
  - retestP-t1t2: own 0.9695933242098348 (n 112), builder 0.9695933242098346 (n 112), |Δ| = 2.220446049250313e-16, n equal: True
  - retestC-t1t2: own 0.7357486264955682 (n 53), builder 0.7357486264955685 (n 53), |Δ| = 3.3306690738754696e-16, n equal: True
  - retestP-t2t3: own 0.9542888066830922 (n 112), builder 0.9542888066830918 (n 112), |Δ| = 4.440892098500626e-16, n equal: True
  - retestC-t2t3: own 0.647323853650743 (n 52), builder 0.6473238536507431 (n 52), |Δ| = 1.1102230246251565e-16, n equal: True

## 10. Failures, workarounds, changes, ambiguities, and anything not computed

- **Code changes: none.** No deposited file was edited. The SHA-256 of every file under `files/` still matches table A at the end of the run (re-checked by `make_log.py`: True). No diffs to report.
- **Failure as deposited: the Stage-2 external-anchor gate.** With the default options the builder exits 0 but writes status `pre-t3` with no t3 profile, because neither anchoring route is available offline from the public files: (a) `git ls-remote` against GitHub (not an allowed host here; git's https transport was blocked with `GIT_ALLOW_PROTOCOL=file` so no connection was attempted), and (b) the OSF git-anchor JSON files plus a local git tag (the anchor files are not among the 64 public files, and there is no git repository). The OSF-anchor route would also call `api.osf.io`, which is not among the allowed links.
- **Workaround: the documented option `--skip-origin` (with the required `--out`)**, listed in the builder's docstring as a "test-only override" and in `--help` as "tests only: skip the ls-remote anchor check". It skips the whole external-anchor check, so Stage 2 then requires only that the two verdict files exist. All t3 values, the t2→t3 retests, the consistency check and the class come from this mode. Nothing else about the computation differs: runs A2 and B write identical t1/t2 numbers.
- **Environment only:** `HOME`, `TMPDIR`, `AIAS_ROOT` and `GIT_ALLOW_PROTOCOL` (section 1). The builder's own HOME shim did the `~/aias` redirection. It leaves its temp folders behind (`work/tmp/v41_home_*`).
- **Full precision:** the builder's CSV rounds P, C* and A to 6 dp, so the unrounded per-brand values were taken from the same `build()` call in-process (run C), and verified equal to the CSV at 6 dp.
- **Ambiguity, v0.23 ids:** see section 8. The builder's brand key for v0.23 is the id `S01`…`S24`. I sorted those. The name-order alternative is tabulated there.
- **Ambiguity, t3 responses:** the definitions are in section 7. Note that `score_v41.mc_completeness` (not called by the builder) looks for `v19/phase_[ab]_responses.jsonl` and `v23_phase_[ab]_raw.json`, which are not among the public files. It would therefore count only v0.20–v0.22 from these files, so I did not use it. My count uses the files that are present.
- **Shares** are given as decimal fractions (Python float, full precision), with the exact fraction a/b in `how`. The builder itself writes `share_not_rated` (= 1 − share rated) for the pooled share, and `share_rated` per category.
- **`inputs_sha256`** in the builder JSON keys the two Stage-2 verdict files by absolute path (builder behaviour: `str(v41_path)`). This shows my local path `/home/claude/reproduction/files/...`.
- **Not computed:** nothing. All 1,008 per-brand values and all 55 table-B quantities were computed.
- The time box was met (finished before 2:40 pm Central).

