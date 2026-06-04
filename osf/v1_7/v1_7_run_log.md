# v1.7 CPC scoring run log

```
==============================================================================
v1.7 (CPC) verdicts — lock v1.7-prereg-r2  |  trio: skincare / cosmetics / automotive
==============================================================================
  H_CPC_Defined      : FALSIFIED   (pooled defined-rate 57% of 67 in-market)
      v0.20: 10/24 defined (42%)  N/A: ['Estée Lauder', 'Lancôme', 'Sisley', 'Dior Beauty', 'Chanel Beauty', 'La Prairie', 'Clé de Peau Beauté', 'Rare Beauty', 'Fenty Skin', 'Goop', 'Glossier', 'Tower 28', 'Eucerin', 'Bioderma']
      v0.21: 14/24 defined (58%)  N/A: ['Giorgio Armani Beauty', 'Hourglass', 'Chantecaille', 'Laura Mercier', 'Haus Labs', 'Kylie Cosmetics', 'CoverGirl', 'Revlon', 'Wet n Wild', 'Milani Cosmetics']
      v0.22: 14/19 defined (74%)  N/A: ['Rivian', 'Lucid', 'Polestar', 'Fisker', 'Nissan']
  H_CPC_Dissociates  : FALSIFIED   [load-bearing]
      pooled |rho(CPC, Presence_composite)| = 0.766  (rho=0.766, p=2.04e-08, 95% BCa [0.601, 0.885], n=38) vs ceiling 0.5
      pooled |rho| recognition-only=nan  recall-level=0.766
      v0.20: rho=+0.939 |rho|=0.939 (n=10) off-diag brands=0
      v0.21: rho=+0.846 |rho|=0.846 (n=14) off-diag brands=1
      v0.22: rho=+0.637 |rho|=0.637 (n=14) off-diag brands=2
      off-diagonal occupancy (pooled): hiP/loC=["v0.20:Paula's Choice", 'v0.21:MAC Cosmetics', 'v0.22:Hyundai']
                                       loP/hiC=['v0.22:Bentley', 'v0.22:Chevrolet', 'v0.22:Volkswagen']
  H_CPC_PhantomNull  : CONFIRM   (5 Cell-D phantoms; offenders=[])

  reconciliation vs v0.30 cpc_raw: checked 38 brands, max|Δ|=2.22e-16  -> OK
  wrote: /Users/pablou/aias/osf/v1_7/data/v1_7_cpc.csv
  wrote: /Users/pablou/aias/osf/v1_7/v1_7_cpc_verdicts.json
```

## Certified input hashes (SHA256)

- v0.20: phase_a `c8ad6335c982ec95883fffa6c3cb185170b3cdd80b8694377c9fb8afb47d390e`  phase_b `4791113a93b8a25866099fa16ea3a8d14c6f82d6e6c24894609506ad25225828`
- v0.21: phase_a `d470940aa497f55588588536173a128a3394af2a6f0bb6e94825738622167d0d`  phase_b `45e4c3acca67f8c6d6ddfe94bd08215bf6287e4b5af194b81eef47f427440ee1`
- v0.22: phase_a `93c1b147c44b9031bfad3eb5806d50fd26404cf9c9b7cea95f2fd8a7a00c246a`  phase_b `e61dff692ed5eee34a3719067fb07328e4bb3035247c78b703e01d07097fce35`
