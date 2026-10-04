# MODEL 7 guide vidéo : script de la narration en français

Narration de la version française du guide vidéo « Utiliser MODEL 7, pas à pas ». Traduction du script anglais (course/audio/model7_walkthrough/script.md), paragraphe par paragraphe : chaque paragraphe accompagne le même écran que dans la version anglaise. Les écrans montrent le classeur, qui est en anglais ; les noms des feuilles et des libellés sont donc cités en anglais. Les chiffres sont ceux du cas Kasiri par défaut de MODEL 7 v1.0 release candidate 1, écrits tels qu'ils sont prononcés.

## 01. Introduction

Bienvenue dans le guide vidéo de MODEL 7, le modèle de développement et de financement hydroélectrique. Il accompagne le Livre 7, Hydropower Development and Finance, From River to Financial Close.

Pendant les seize prochaines minutes, nous allons parcourir le modèle étape par étape, sur son cas de référence : Kasiri River Hydro, une centrale fictive au fil de l'eau de soixante mégawatts, dans la République fictive de Navaria. À la fin, vous saurez par où commencer, comment vérifier que le modèle est sain, comment lire ses résultats, comment les soumettre à des stress, et comment remplacer le cas par votre propre projet.

Ouvrez maintenant le classeur, et gardez-le à côté de la vidéo. Mettez la vidéo en pause chaque fois que vous voulez essayer une étape vous-même.

## 02. La feuille de garde

Le classeur s'ouvre sur la feuille de garde. En haut, vous voyez le titre et le cadre que le modèle applique : le Hydro Readiness Framework, avec huit questions, vingt-trois portes et une décision de bouclage financier.

En dessous, un bloc appelé Live status donne six réponses qui se mettent à jour à chaque modification. Pour le cas par défaut, elles se lisent ainsi. La décision de bouclage financier est STOP, parce qu'une porte critique n'est pas franchie. Six portes sur vingt-trois sont franchies. L'écran de développement à neuf portes indique non bancable. L'écran budgétaire indique une faible pression budgétaire supplémentaire. Les contrôles d'intégrité du modèle indiquent tout est OK. Et le contrôle de cohérence avec le livre indique que tout passe.

En bas de la feuille de garde, les liens Start here mènent directement aux feuilles principales. Nous les utiliserons dans cet ordre.

## 03. Le Read me et le code couleur

Cliquez sur le lien vers la feuille Read me. Elle explique ce que fait le modèle et comment il est organisé. Trois points comptent avant de toucher à quoi que ce soit.

D'abord, le code couleur. Une police bleue signale une donnée d'entrée que vous pouvez modifier. Une police noire signale une formule ; ne l'écrasez jamais. Une police verte signale un lien depuis une autre feuille. Et une cellule sur fond vert est un résultat clé.

Ensuite, la chronologie. Le modèle est annuel, sur quarante périodes, et tous les montants sont en millions de dollars américains courants, sauf si le libellé indique réel deux mille vingt-six.

Enfin, les deux niveaux de portes. Un écran à neuf portes vous aide à décider s'il faut poursuivre le développement. Les vingt-trois portes, sur la feuille trente A, vérifient si le dossier de preuves permet le bouclage financier. Gardez cette distinction en tête ; nous y reviendrons.

## 04. Le panneau de contrôle

Ouvrez maintenant la feuille zéro un, le panneau de contrôle. C'est la seule feuille dont vous avez besoin pour lancer des scénarios.

La section A fixe le cas. Pour le cas du modèle, choisissez un pour le cas de base, deux pour le cas bas et trois pour le cas haut. Pour le cas de production des flux de trésorerie, choisissez un pour P cinquante, deux pour P soixante-quinze et trois pour P quatre-vingt-dix. Le cas de dimensionnement des prêteurs a quatre options ; la valeur par défaut, quatre, dimensionne la dette sur le P quatre-vingt-dix à dix ans.

La section B fixe la transaction. La structure deux est un producteur d'électricité indépendant privé. En mode de dette un, la dette est dimensionnée par le modèle ; en mode deux, elle est fixée à des montants donnés. La garantie budgétaire, réglée sur un, signifie que l'État couvre tout manque dans les paiements de la compagnie d'électricité au projet.

La section C contient neuf interrupteurs de stress, de la sécheresse au retard de la ligne de transport. Chacun vaut zéro ou un, et ils peuvent être combinés. La section D contient cinq variations de sensibilité, en pourcentage, pour le coût, la production, le tarif, les charges d'exploitation et le taux d'intérêt.

Laissez pour l'instant toutes les valeurs par défaut. La section E, en bas, affiche les principaux résultats pour la sélection en cours.

## 05. Vérifier avant de lire

Avant de lire le moindre résultat, vérifiez que le modèle est sain. Ouvrez la feuille trente-trois, Checks. Elle effectue quatorze tests d'intégrité : les ressources égalent les emplois, la dette est entièrement remboursée, la chaîne énergétique est cohérente, et ainsi de suite. La dernière ligne doit indiquer tout est OK.

Ouvrez ensuite la feuille trente-cinq, Book check. Elle compare le modèle en direct aux vingt-six chiffres de Kasiri imprimés dans le Livre 7. Avec les valeurs par défaut, chaque ligne indique pass. Si vous modifiez une donnée, certaines lignes indiqueront check ; c'est normal, car les chiffres imprimés correspondent au cas par défaut.

La règle est simple : ne vous fiez à aucun résultat tant que les contrôles d'intégrité n'indiquent pas tout est OK.

## 06. Lire le tableau de bord

Ouvrez la feuille trente-deux, le tableau de bord. La ligne quatre donne trois verdicts côte à côte : l'écran à neuf portes, la préparation au bouclage à vingt-trois portes, et l'écran budgétaire.

Le bloc projet décrit la centrale : soixante mégawatts, environ deux cent quatre-vingt-douze gigawattheures par an, en P cinquante, un facteur de charge d'environ cinquante-six pour cent, et un coût de centrale d'environ cent cinquante-sept millions de dollars en valeur deux mille vingt-six.

Le bloc financier montre comment la centrale est financée. La dette senior est d'environ cent quarante-cinq millions de dollars. Le ratio minimal de couverture du service de la dette est de un virgule cinquante-trois. Le rendement des fonds propres privés est de treize virgule huit pour cent, pour un objectif de quinze. Et il reste un besoin de financement non couvert d'environ quatre millions de dollars. Autrement dit, le projet est solide, mais un peu en dessous du tarif dont ses promoteurs ont besoin.

Le bloc développeur montre l'économie du chemin qui y mène. Le budget de développement est d'environ neuf millions de dollars sur six ans, avec environ quinze pour cent de chances d'atteindre le bouclage financier depuis la reconnaissance. En cas de succès, le développeur gagne environ seize pour cent. Mais pondérée par le risque d'échec, sa valeur actuelle nette est d'environ moins un million de dollars. Le projet est attractif une fois qu'il réussit, et ne vaut pas la peine d'être lancé avec ces hypothèses. Le chapitre quatorze du Livre 7 explique pourquoi.

Les blocs compagnie d'électricité et finances publiques montrent l'autre côté de l'opération : l'acheteur peut payer environ six fois la facture, mais l'État et la compagnie d'électricité perdent ensemble environ vingt-huit millions de dollars en valeur actuelle, parce que le tarif est supérieur à ce que la compagnie encaisse auprès de ses clients.

## 07. Pourquoi la décision est STOP

Ouvrez la feuille trente A, Close readiness. Chacune des vingt-trois portes a un statut. Certaines sont testées automatiquement par le modèle ; les autres sont des statuts de preuve que vous saisissez, en anglais dans le classeur : franchie, partielle, non franchie ou sans preuve. Une porte n'est franchie que sur preuve. Un statut vide compte comme sans preuve.

La décision suit une échelle fixe. Une seule porte critique non franchie, et la décision est STOP. Si les portes critiques sont seulement en partie franchies, la décision est not ready. Si toutes les portes critiques sont franchies, la décision est conditional go. Et si les vingt-trois portes sont franchies, la décision est go.

Pour Kasiri, sept portes critiques ne sont pas franchies : la série de débits et sa revue indépendante, la validation de l'étude de faisabilité bancable, l'évaluation environnementale et sociale aux normes des prêteurs, les droits fonciers, six mois de garantie de paiement, un plan de financement entièrement engagé, et un rendement des fonds propres à l'objectif.

En bas de la feuille, les portes sont regroupées sous les huit questions du cadre, et chaque question désigne la partie qui doit l'accepter : le développeur, les prêteurs ou l'État. La feuille trente-quatre, la carte du cadre, indique pour chaque porte où le modèle la teste et quels chapitres du livre la traitent. STOP n'est pas un verdict sur le projet. C'est un programme de travail.

## 08. Le point de vue du développeur

Ouvrez la feuille zéro un A, Development. La section A liste les six étapes du développement, chacune avec une durée, un budget et une probabilité de succès. Ces probabilités relèvent de votre jugement ; aucune donnée publique ne les calibre pour l'hydroélectricité en Afrique.

La section D donne les rendements du développeur : la valeur actuelle nette pondérée par le risque, la prime de développement d'équilibre et la valeur en cas de succès. La section D deux évalue l'ensemble de la position de développement au début de chaque étape. Utilisez-la pour fixer le prix d'entrée d'un co-développeur : au début des autorisations, la position de Kasiri vaut environ un virgule trois million de dollars.

Essayez une modification. Augmentez la probabilité de l'étape de faisabilité, et observez la valeur pondérée par le risque. Puis remettez la valeur d'origine.

## 09. Stresser la rivière

Revenez au panneau de contrôle et réglez l'interrupteur de sécheresse sur un. Le modèle applique trois années à cinquante-cinq pour cent du débit normal. La dette reste dimensionnée sur le même cas prêteur, donc son montant ne change pas. Mais ouvrez le tableau de bord : le ratio minimal de couverture du service de la dette tombe sous un, à environ zéro virgule sept. Le compte de réserve est mobilisé, et il ne suffit pas.

C'est le stress le plus important pour un tarif rémunérant uniquement l'énergie produite. Un prêteur demanderait une réserve plus grande, un balayage de trésorerie les années humides, ou moins de dette. Remettez l'interrupteur de sécheresse à zéro.

## 10. Stresser l'acheteur

Réglez maintenant le stress sur l'acheteur sur un. Les encaissements de la compagnie d'électricité baissent, les transferts sont réduits et le tarif de détail est gelé. En moins de dix ans, la compagnie ne peut plus payer la facture du projet. Avec la garantie budgétaire activée, le projet est payé intégralement, et le coût passe à l'État : la valeur budgétaire consolidée tombe à environ moins cent vingt-cinq millions de dollars.

Réglez ensuite la garantie sur zéro. La garantie de paiement de douze mois est épuisée, le reste devient des arriérés, et le projet fait défaut : le ratio minimal de couverture devient négatif. C'est la leçon centrale du livre : un projet peut être bancable parce que le risque a été transféré à l'État. Remettez les deux valeurs par défaut.

## 11. Comparer les structures et les contrats

Sur le panneau de contrôle, réglez la structure sur un, puis trois, quatre et cinq, et lisez la feuille dix-sept A, Structures, avec le tableau de bord. La structure un est publique, la trois un partenariat public-privé avec dette concessionnelle, la quatre une structure hybride avec génie civil public, et la cinq un financement mixte. Observez comment le rendement des fonds propres et la valeur budgétaire évoluent ensemble : une subvention qui ne se traduit pas par un tarif plus bas transfère de l'argent public aux actionnaires privés. Remettez la structure sur deux.

Sur la feuille zéro cinq A, Contracting, la structure du contrat de construction peut valoir un, un contrat clés en main unique, deux, des lots séparés, ou trois, des contrats multiples. Comparez le coût et la part des dépassements que conserve le maître d'ouvrage.

## 12. L'appliquer à votre propre projet

Pour appliquer le modèle à un projet réel, remplacez les données bleues dans cet ordre. D'abord, la feuille zéro deux, les données du projet, et la feuille zéro trois, l'hydrologie : débits mensuels, chute, débit d'équipement, longueur et qualité de la série de débits. Ensuite, la feuille zéro cinq, le coût de la centrale. Puis la feuille zéro un A, les étapes de développement, les budgets et les probabilités. Ensuite, les conditions commerciales : la feuille quatorze pour le contrat d'achat d'électricité, et les feuilles onze et douze pour l'acheteur. Ensuite, les conditions de financement, sur les feuilles de la dette et des structures. Enfin, les statuts de preuve des vingt-trois portes, sur la feuille trente A.

Après chaque série de modifications, vérifiez la feuille trente-trois avant de lire le moindre résultat. Attendez-vous à ce que la feuille trente-cinq affiche des lignes check : elle ne s'applique qu'au cas Kasiri. Et gardez une trace de chaque hypothèse et de sa source, car les portes vous la demanderont.

## 13. Conclusion

Voilà tout le parcours : la feuille de garde, les contrôles, le tableau de bord, la décision de bouclage, le point de vue du développeur, les stress et votre propre projet. Le manuel d'utilisation et de méthodologie, MANUAL 7, détaille chaque formule et chaque feuille, et le Livre 7 explique le raisonnement derrière chaque étape.

Rappelez-vous que MODEL 7 est un outil d'aide à la décision, pas un conseil en investissement, et que toutes les valeurs par défaut sont illustratives. Merci de votre attention.
