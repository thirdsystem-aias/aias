# Reproduction check from the public files, November 2026: inputs

The 64 files the check uses, with the plan in `plan.md`. Each link opens the file's OSF page; the download link is `https://osf.io/download/<id>/`, with the id at the end of the page link. Files 8 to 10 and 19 were not on OSF when the chain was traced and were deposited with the plan on November 13, 2026, in `program_notes/reproduction_check_2026-11/inputs/`, byte-identical to the repository files last changed in May 2026.

| # | Role | OSF path (osfstorage/…) | Bytes | SHA-256 | Link |
|---|---|---|---|---|---|
| 1 | builder | aias_2_0/scripts/aias_2_0_synthesis_data.py | 22,678 | `45a4e7d46ff9e68556ee5dc6f4d7236486e463e461cd25eb6e4489af13ebe69d` | https://osf.io/ec6wh/files/osfstorage/6af2f0c99c09072501e33163 |
| 2 | scorer | methodology/v1_9/scripts/score_v1_9.py | 15,775 | `71d340c480e09f4549903912960059226da9004413f6072a2c4c7dd209f42e02` | https://osf.io/ec6wh/files/osfstorage/6af1fd1e10cff607527c9201 |
| 3 | scorer | v41/scripts/score_v41.py | 43,627 | `c4231b6805896a077b9b16d8f315bf19ae6297435293deb1de32375d7424dc31` | https://osf.io/ec6wh/files/osfstorage/6af1fc991bfac4d11fb8c47d |
| 4 | scorer | v31/scoring/score_v0_31.py | 14,876 | `193ac0e0c98593d00fe252e4f78674cb212de9124d4e7486a26295880337460b` | https://osf.io/ec6wh/files/osfstorage/6a220530bfcbe456178f960d |
| 5 | scorer | v33/scripts/score_v33.py | 22,214 | `c6b9720496d8abf78450ce297482c27f6e9b1aba76c3452e7964183c7b7fd866` | https://osf.io/ec6wh/files/osfstorage/6a28a5697032ed9e4c878305 |
| 6 | scorer | v31/prereg/v0_31_cpc_baseline_content.py | 7,310 | `e9658c6f77d6e7c44bbf946f29c361ef0e37cc89b82f9bb31c13034f8c970281` | https://osf.io/ec6wh/files/osfstorage/6a22050a06ac7dfb808f99d4 |
| 7 | scorer | v33/prereg/v0_33_provider_asymmetry_content.py | 18,305 | `7f9fa43e169f2c484f09c816416d31822f18a0264805193a8900a3ea3c495a27` | https://osf.io/ec6wh/files/osfstorage/6a28a5524129aa31ed8e6a3d |
| 8 | scorer (mention matcher, skincare) | program_notes/reproduction_check_2026-11/inputs/score_v20.py | 26,002 | `a0b288d5721ebf259e216c7e72af6d85f0e8414e8d3534552bf7c583196b9110` | https://osf.io/ec6wh/files/osfstorage/6af75b4b09c4f77dbf892152 |
| 9 | scorer (mention matcher, cosmetics) | program_notes/reproduction_check_2026-11/inputs/score_v21.py | 26,049 | `993317fcbaf1d64cdd1b7b4cb69bfa602dd675829b2a6fc06bbf1a83252a7e92` | https://osf.io/ec6wh/files/osfstorage/6af75b55a5fa700dcd9cfa7c |
| 10 | scorer (mention matcher, automotive) | program_notes/reproduction_check_2026-11/inputs/score_v22.py | 40,773 | `b03bc55b74cf4aa402412f4313217fa057568365505245cbb0fb25a7f5fccdb9` | https://osf.io/ec6wh/files/osfstorage/6af75b5c381404807d0f0253 |
| 11 | registry | v20/prereg/v0_20_registry.json | 10,584 | `eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782` | https://osf.io/ec6wh/files/osfstorage/6a0fa219bbff4865e867225d |
| 12 | registry | v21/prereg/v0_21_registry.json | 12,574 | `45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3` | https://osf.io/ec6wh/files/osfstorage/6a10b6353c667c5f883862ae |
| 13 | registry | v22/prereg/v0_22_automotive_content.py | 13,665 | `431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9` | https://osf.io/ec6wh/files/osfstorage/6a1488c4d36150eb1c5e3d7b |
| 14 | gate P4 | v19/phase_a_queries.jsonl | 21,946 | `276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e` | https://osf.io/ec6wh/files/osfstorage/6a0ef7e44e20dd5502679d5d |
| 15 | gate P4 | v19/phase_b_queries.jsonl | 9,864 | `75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188` | https://osf.io/ec6wh/files/osfstorage/6a0ef7f755ec681df5679ad9 |
| 16 | gate P4 | v19/thresholds_v0_19.json | 7,178 | `542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61` | https://osf.io/ec6wh/files/osfstorage/6a0ef82d64d8c0792dc9342c |
| 17 | gate P4 | v23/scripts/acquire_v0_23.py | 17,046 | `7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da` | https://osf.io/ec6wh/files/osfstorage/6a160b7c19d8199ca8cc6ddf |
| 18 | gate P4 | v41/prereg/acquisition_manifest_v41.md | 4,174 | `e97d72a14ab8cf9aee9b4589f369db4b0e25375f4faeaf77568bb1351247e59c` | https://osf.io/ec6wh/files/osfstorage/6af167344ad58a60407c9224 |
| 19 | gate P4 (checksum only; not run) | program_notes/reproduction_check_2026-11/inputs/run_acquisition_v22.py | 22,445 | `59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe` | https://osf.io/ec6wh/files/osfstorage/6af75b3fa11280551889213e |
| 20 | gate P1/P2 reference | v41/registries/v1_8_instrument_table.csv | 20,027 | `2d0ea5e83b01a39d1b120fe75b79178b78c85a649837f0d40a473a38f041f6e6` | https://osf.io/ec6wh/files/osfstorage/6af1fcbb9966c813ee53ba3b |
| 21 | gate P2 reference; lineage | v41/registries/v1_8_verdicts.json | 11,522 | `a280385f1868cfdff06d6c3dfae6eb4288fb1a6ad01129d6d23320a3b88b7e78` | https://osf.io/ec6wh/files/osfstorage/6af1fcbe1bfac4d11fb8c48a |
| 22 | gate P3 reference; lineage | v34/v34_verdicts.json | 10,091 | `b838b5352f35d3ae9e95c33dc6f8cb791f6f57eb83f9dfdc29b918649a115ee5` | https://osf.io/ec6wh/files/osfstorage/6a29d9858f5abdf103d14e7f |
| 23 | parity A1-A5 reference; lineage | methodology/v1_9/scoring/v1_9_calibration.json | 9,964 | `4d2ddb982a3372fa4f8c68e5bcf1a9511684186568fb6d37fbc2562b612388bf` | https://osf.io/ec6wh/files/osfstorage/6af1fd30f6aac1b451b31893 |
| 24 | stage 2 record | methodology/v1_9/scoring/v1_9_verdicts.json | 1,574 | `3d838f92821a5ae41c33bdb9a209432e0fdbc505ce7c53f8a17e8c438745967d` | https://osf.io/ec6wh/files/osfstorage/6af1fd380b49671dd5b8c3cb |
| 25 | stage 2 record | v41/scoring/v41_verdicts.json | 13,740 | `0d3f5dfcf0a920e642aa613f5bf45dce66dd155eb6fd4ee054ed4d4bb700d4e2` | https://osf.io/ec6wh/files/osfstorage/6af1fcd071afc7be7e53b9d7 |
| 26 | lineage | v29/data/v29_verdicts.json | 1,493 | `73fdc5e076b0625619f90e6c1038826d60a9e0dd01dda1cfc31d29a78ed23f27` | https://osf.io/ec6wh/files/osfstorage/6a1f4156e59c92d7c46b9ce6 |
| 27 | lineage | v30/v30_cpc_verdicts.json | 5,554 | `61ac89ab2bfff72a757a540f28154cb35a60e5b88e8ad295ed2e70a435956c15` | https://osf.io/ec6wh/files/osfstorage/6a20a11b6e5137c4e7a94e8a |
| 28 | lineage | v31/v31_cpc_verdicts.json | 4,759 | `1124b70dcdbd59737ca843f72b228115b60c7cb25a73d380d174f6bc3953fd5e` | https://osf.io/ec6wh/files/osfstorage/6a22053835701f9e73878a63 |
| 29 | lineage | v32/v32_verdicts.json | 9,706 | `d8591fb8f16a391e3f2584b78b5a042293699898f0644c9e6545d17a7e33620b` | https://osf.io/ec6wh/files/osfstorage/6a272aed593c50bc406d82a1 |
| 30 | lineage | v33/v33_provider_asymmetry_verdicts.json | 5,493 | `9c513273f8c0851b71147b57543664455a801a1279c862b3c642cea2008d096d` | https://osf.io/ec6wh/files/osfstorage/6a28a56e437305380a8e6a24 |
| 31 | lineage | v35/v35_verdicts.json | 15,413 | `68a219607ca615047c55930afc7e12f137698c97d8b50aeb05364ba505797303` | https://osf.io/ec6wh/files/osfstorage/6a2b17455efb8689bc30a3a9 |
| 32 | lineage | aias_2_0/inputs/v36_verdicts.json | 5,314 | `3c41f78a70f02df010c88d3611fb15deae10276bb217eb7a125ec90b90d2fb8b` | https://osf.io/ec6wh/files/osfstorage/6af2f0a818636f6586b8c444 |
| 33 | lineage | methodology/v1_7/v1_7_cpc_verdicts.json | 7,928 | `2ad30dd2ec04dfa1583c44b183ee1caa04a57b35cf3dc7024c1369ad49777742` | https://osf.io/ec6wh/files/osfstorage/6a21a5d06c2aca6d42f92a6b |
| 34 | lineage | v37/v37_verdicts.json | 4,865 | `7f46c853a2395b7f6bf1b4ab83d0786f8afa3c36eb6d41d6e45085a4d3103461` | https://osf.io/ec6wh/files/osfstorage/6a425d20838d727860932f55 |
| 35 | answers t1 | v19/phase_a_results.csv | 2,689 | `5206fe70e5a375b5871e8a7067940065e8bb6b5d98b1b9389a54c2eb9a22d6e3` | https://osf.io/ec6wh/files/osfstorage/6a0ef7f131995da573a7ac9d |
| 36 | answers t1 | v19/phase_b_results.csv | 23,622 | `2542f0e8117a44d02e072b56be24d758f63ede35d700dd163852b720d4739075` | https://osf.io/ec6wh/files/osfstorage/6a0ef802d7337cbee0c93894 |
| 37 | answers t1 | v20/data/phase_a_results.csv | 24,882 | `c8ad6335c982ec95883fffa6c3cb185170b3cdd80b8694377c9fb8afb47d390e` | https://osf.io/ec6wh/files/osfstorage/6a0fb27821da8180b8417914 |
| 38 | answers t1 | v20/data/phase_b_results.csv | 104,769 | `4791113a93b8a25866099fa16ea3a8d14c6f82d6e6c24894609506ad25225828` | https://osf.io/ec6wh/files/osfstorage/6a0fb27c24d5c6fd1d229f3b |
| 39 | answers t1 | v21/scoring/phase_a_results.csv | 24,464 | `d470940aa497f55588588536173a128a3394af2a6f0bb6e94825738622167d0d` | https://osf.io/ec6wh/files/osfstorage/6a10d0402ab9d61126386a07 |
| 40 | answers t1 | v21/scoring/phase_b_results.csv | 105,252 | `45e4c3acca67f8c6d6ddfe94bd08215bf6287e4b5af194b81eef47f427440ee1` | https://osf.io/ec6wh/files/osfstorage/6a10d045b54954f11cf6ca39 |
| 41 | answers t1 | v22/phase_a_results.csv | 21,839 | `93c1b147c44b9031bfad3eb5806d50fd26404cf9c9b7cea95f2fd8a7a00c246a` | https://osf.io/ec6wh/files/osfstorage/6a14e4015e0f559558b76e10 |
| 42 | answers t1 | v22/phase_b_results.csv | 97,446 | `e61dff692ed5eee34a3719067fb07328e4bb3035247c78b703e01d07097fce35` | https://osf.io/ec6wh/files/osfstorage/6a14e4045e0f559558b76e14 |
| 43 | answers t1 | v23/data/v23_phase_a_scored.json | 881,071 | `042188bc876a969e1f87c22bb77b95d6fb819643be7b9c6304e47d6243b7754c` | https://osf.io/ec6wh/files/osfstorage/6a160b2ff5a4474928cc766a |
| 44 | answers t1 | v23/data/v23_phase_b_scored.json | 180,768 | `2fd1400891c4aff0707ff58d11d2e055c2ab5242972512888f3c69b742e7c9e6` | https://osf.io/ec6wh/files/osfstorage/6a160b3e7b1bd8bf217eeffc |
| 45 | answers t2 | v34/data/v19/phase_a_results.csv | 2,689 | `ad566fb46f4652bdab790da3a9db1fdadcc883e230d163c722b555a73ffceb42` | https://osf.io/ec6wh/files/osfstorage/6a29d8ae8f5abdf103d14e1d |
| 46 | answers t2 | v34/data/v19/phase_b_results.csv | 23,616 | `ba751c6cce5c264d37f4cfc0ca19dc1ef37d68570e0eb2e9b4b70429187b6129` | https://osf.io/ec6wh/files/osfstorage/6a29d8ba2db6ade548d14d9b |
| 47 | answers t2 | v34/data/v20/phase_a_results.csv | 25,170 | `382e22ef8e8b4ee808c413031cb179c7cecd53d3cea37e35d494f53e05efcbf4` | https://osf.io/ec6wh/files/osfstorage/6a29d8c28f5abdf103d14e28 |
| 48 | answers t2 | v34/data/v20/phase_b_results.csv | 103,430 | `504dfc5ace742cb27d0d3a764b617b12cb816f607850d165801b64b68fcc8a78` | https://osf.io/ec6wh/files/osfstorage/6a29d8c7dcb8a4e96f733670 |
| 49 | answers t2 | v34/data/v21/phase_a_results.csv | 24,459 | `9bfe8ab018743d2b533b0f1fd8e483a49c738e89091a18cda6ead8c7d0c722d9` | https://osf.io/ec6wh/files/osfstorage/6a29d8d1aa6579b6ba733669 |
| 50 | answers t2 | v34/data/v21/phase_b_results.csv | 107,849 | `f27f4a5f0e2da0b110be2f2e3b85437e391f7354f87ec3e2d9ea5872e6f87ed1` | https://osf.io/ec6wh/files/osfstorage/6a29d8d7727b9dc0bf9ef41e |
| 51 | answers t2 | v34/data/v22/phase_a_results.csv | 21,850 | `9b8e8d49a1be66107af49bcb93ebfcb715fb2992cf7b7ead32f7f511c88445aa` | https://osf.io/ec6wh/files/osfstorage/6a29d8e0cb0e3d86187336cb |
| 52 | answers t2 | v34/data/v22/phase_b_results.csv | 100,091 | `7976de5d76ab5a21729a04bdc3d3f4e12afc7b6e0350dcabcedd99dc329c189a` | https://osf.io/ec6wh/files/osfstorage/6a29d8e6aa6579b6ba73366d |
| 53 | answers t2 | v34/data/v23/v23_phase_a_scored.json | 891,087 | `8f9ca58f81f4b9c6d1aedc4b3395712ed39071d5d5a27db34aae9f3e132d06b1` | https://osf.io/ec6wh/files/osfstorage/6a29d8f6e6800a9fa19ef482 |
| 54 | answers t2 | v34/data/v23/v23_phase_b_scored.json | 178,164 | `f5e7a07e698378d69b08131aa6538748c104fa83e3e4cc4a8f2e2616015dd7cb` | https://osf.io/ec6wh/files/osfstorage/6a29d901395de9f708d14df3 |
| 55 | answers t3 | v41/data/v19/phase_a_results.csv | 2,689 | `370f44409893072492a16647c4fe56c51b2a65994ee96824a9c8d4da34459ce5` | https://osf.io/ec6wh/files/osfstorage/6af1fc4571bf507a257c9389 |
| 56 | answers t3 | v41/data/v19/phase_b_results.csv | 23,621 | `7d49164eab4600b0e97a2d023b47bfc682e7db222fcf7cdf06b371e12ebb07e6` | https://osf.io/ec6wh/files/osfstorage/6af1fc4d75f9fd11047c93aa |
| 57 | answers t3 | v41/data/v20/phase_a_results.csv | 24,613 | `3b0554fd6a0746e7341c5702159b5a6d5e73ea67d385316169e2ab028fd61a55` | https://osf.io/ec6wh/files/osfstorage/6af1fc520da9f493cf53bba0 |
| 58 | answers t3 | v41/data/v20/phase_b_results.csv | 107,419 | `c313569ec31f9789363d863062e56a1a8cd77a4293c75189dc3acd2a1dfcc9c8` | https://osf.io/ec6wh/files/osfstorage/6af1fc56d2a3ca43c17c9243 |
| 59 | answers t3 | v41/data/v21/phase_a_results.csv | 24,452 | `175b16094400375ab4987594abad15875bb7d88bca50d7f39cdb9b2e59b1e6d8` | https://osf.io/ec6wh/files/osfstorage/6af1fc5d75f9fd11047c93b7 |
| 60 | answers t3 | v41/data/v21/phase_b_results.csv | 102,916 | `aeb8a2a2a7846f12467cafaff582a9deb73ddbedacf598f6da23e0e6dff23c69` | https://osf.io/ec6wh/files/osfstorage/6af1fc632df9a4536c7c927c |
| 61 | answers t3 | v41/data/v22/phase_a_results.csv | 22,160 | `40af3d22ef00a5b1ab4e4abf4886ddf9059009d91f5310801e45653b5b91275e` | https://osf.io/ec6wh/files/osfstorage/6af1fc6b9966c813ee53b9b7 |
| 62 | answers t3 | v41/data/v22/phase_b_results.csv | 102,679 | `a5bffb31acfd0d97226e2658001f1adecbf64448b512fd32e037a85d84bde94b` | https://osf.io/ec6wh/files/osfstorage/6af1fc6e1424da87feb8c405 |
| 63 | answers t3 | v41/data/v23/v23_phase_a_scored.json | 876,896 | `13f85accaec51338a67bea95a6169de21a3e84fa2c12b692c88da7f5fa09e99c` | https://osf.io/ec6wh/files/osfstorage/6af1fc781424da87feb8c417 |
| 64 | answers t3 | v41/data/v23/v23_phase_b_scored.json | 175,806 | `2fcff8fb1f7cc57c1ad5056e366a2eccffe8767c1dba95d12cfc0d054e34d52d` | https://osf.io/ec6wh/files/osfstorage/6af1fc81d2a3ca43c17c92fd |
