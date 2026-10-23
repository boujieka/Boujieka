# Manifeste des documents sources

Les fichiers listés ici ont été fournis par le commanditaire le 23 octobre 2026. Ils sont conservés **localement et en lecture seule** dans `minigrid-studio/reference/`. Ils ne sont **pas versionnés** (voir `.gitignore`), pour trois raisons :

- ce dépôt GitHub est **public** ;
- aucun des documents ne contient de licence explicite autorisant leur redistribution (voir « Droits » ci-dessous) ;
- la règle 3 du cahier des charges impose de vérifier les droits avant toute redistribution.

Pour reconstituer le dossier, déposez les fichiers sous les noms ci-dessous, puis vérifiez les empreintes avec `sha256sum -c` (bloc en bas de page).

| Fichier (nom local) | Rôle (cahier des charges §2) | Taille (octets) | SHA-256 | Métadonnées internes |
|---|---|---|---|---|
| `CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm` | Moteur de référence | 923 309 | `fe0ecb160b294120e3135dfce6bacf619246bff1ed85944e06b6c44c0c4bb33e` | Créé le 20/02/2014, modifié le 27/10/2023 ; enregistré par Microsoft Excel |
| `Open-Sourcing-Infrastructure-Finance-for-Mini-Grids-FINAL.pdf` | Méthode Isolate / Allocate / Aggregate | 14 320 276 | `ec4b903f2d3314bfb9526a9b33e1041ea93b1e9340a0b7fd14b862fb92dd3301` | 53 pages, PDF 1.4, créé le 01/12/2020 |
| `CrossBoundary-Access-Template-PSA-Term-Sheet-Share-Purchase-Jan2024-vFinal.docx` | PSA — cession de titres d'AssetCo | 124 714 | `f037530d62445373f6f720b773e02659c100e5de62d6a33095bf6e359f15fe6e` | Modifié le 22/01/2024 |
| `CrossBoundary-Access-Template-PSA-Term-Sheet-Asset-Transfer-Jan-2024-vFinal.docx` | PSA — transfert d'actifs par lots | 126 817 | `7d8dba39eef482e55b79f1142c7e242ccfacf96409e8ee4f2423e469d0283d8a` | Modifié le 22/01/2024 |
| `CrossBoundary-Access-Template-OSA-Term-Sheet-Jan-2024-vFinal.docx` | OSA — services d'exploitation | 114 223 | `5b21c30c43bb2224ea0922e480575c9d3fba6a2867552831f629063a51d76de4` | Modifié le 22/01/2024 |
| `CrossBoundary-Access-Open-Source-Environmental-and-Social-Management-System-vFinal.docx` | Gabarit ESMS | 259 069 | `904ad54faf9ac61d9bebd3064ae5747feb5c49ba442fa3555ec5b4a426aa6ca5` | Modifié le 19/06/2024 |
| `Mini_Grid_Financial_Model_Studio_Cahier_des_charges_Claude_Code_v01.docx` | Cahier des charges v0.1 (commanditaire) | 42 280 | `7ac675cb2fc6d9e4c5494da4f462cfedf310e00590662cd630a2b0ce0f88cdd9` | — |

**Doublon.** L'OSA a été téléversé deux fois : `…OSA-Term-Sheet-Jan-2024-vFinal.docx` et `…vFinal_1.docx`. Les deux fichiers ont la même empreinte SHA-256 et sont donc identiques octet pour octet. Une seule copie est conservée.

**Provenance publique.** Une version du modèle est proposée sur `crossboundary.com/mini-grid-financial-model-open-source/` (archive `CrossBoundary-Access-Open-Source-Model-1.0-October-2023.zip`). Nous n'avons **pas** vérifié que le fichier fourni est identique à cette archive, car nous ne l'avons pas téléchargée. Le site indique que le télécharger vaut acceptation de ses avertissements.

## Droits (état au 23/10/2026)

| Document | Ce qui est écrit dans le document | Statut |
|---|---|---|
| Modèle `.xlsm` | Feuille *Disclaimer* : modèle fourni « for informational and educational purposes only », sans garantie, avec décharge de responsabilité au profit des auteurs. **Aucune licence** de réutilisation ni de redistribution. | **Non vérifié.** Autorisation écrite de CrossBoundary requise avant tout usage commercial ou redistribution. |
| Rapport 2020 | Se présente comme « ‘open sources’ the approach » (entre guillemets dans le texte), sans licence formelle. La seule licence citée (CC BY 3.0 IGO) concerne une référence Banque mondiale citée en bibliographie. | **Non vérifié.** |
| PSA ×2, OSA | Section « DISCLAIMER » : « confidential and remains the sole property of Owner ». Modèles diffusés publiquement par CrossBoundary, sans licence. | **Non vérifié.** Ce sont des modèles de référence, pas des contrats prêts à signer. |
| ESMS | Invite les développeurs à l'adopter en insérant leur nom (« Developers are encouraged to adopt this ESMS… »), sans licence formelle. | **Usage interne apparemment prévu.** Redistribution non vérifiée. |

Ce que ce dépôt publie à partir de ces sources, et pourquoi c'est limité :

- **Publié :** des analyses (audit, dictionnaire des variables, carte des dépendances) qui citent des libellés, des valeurs par défaut et des extraits de formules du modèle, ainsi que des valeurs calculées, pour permettre les rapprochements.
- **Non publié :** aucun fichier source, ni aucun texte contractuel au-delà de courtes citations.
- **À trancher :** s'il faut retirer ces analyses de l'espace public, ou les déplacer vers un dépôt privé. Voir `docs/audit.md`, section 9.
