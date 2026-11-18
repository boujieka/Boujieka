export function MethodPage() {
  return (
    <div className="page prose">
      <h2>Méthode et limites (phase P1)</h2>
      <p>
        GeoRenew Africa P1 réalise un <strong>screening géospatial préliminaire</strong>. Les résultats sont indicatifs et
        <strong> non bancables</strong>. Ils ne valent ni étude de faisabilité, ni vérification foncière, environnementale
        ou de capacité réseau.
      </p>
      <h3>Calcul des surfaces</h3>
      <ol>
        <li>Projection dans la zone UTM (WGS 84) contenant le centroïde du site ; jamais de mesure en EPSG:4326 ou 3857.</li>
        <li>Recul de limite : buffer intérieur du site.</li>
        <li>Exclusions strictes : union des entités tamponnées ; un chevauchement n'est soustrait qu'une fois.</li>
        <li>Contraintes indicatives : surface affectée dans la surface nette, jamais soustraite.</li>
        <li>Contrôle : surface brute UTM comparée à la surface géodésique sur l'ellipsoïde WGS 84.</li>
        <li>Intervalle de sensibilité uniquement si la précision de position de chaque couche est renseignée.</li>
      </ol>
      <h3>Nature des valeurs</h3>
      <ul>
        <li><strong>Renseigné</strong> : fourni par l'utilisateur.</li>
        <li><strong>Calculé</strong> : produit par le moteur à partir des entrées.</li>
        <li><strong>Hypothétique</strong> : dépend d'une hypothèse (ex. densité MWp/ha).</li>
        <li><strong>Inconnu</strong> : donnée absente ; aucune valeur n'est inventée.</li>
      </ul>
      <h3>Ce que P1 ne fait pas</h3>
      <p>
        Pas de MNT ni de pente calculée, pas de données solaires ou éoliennes, pas de modèle PV horaire, pas de raccordement
        ni de corridor, pas de BESS, pas de modèle financier, pas de rapport PDF/Word/Excel, pas d'authentification.
        Voir <code>docs/P1_RAPPORT.md</code>.
      </p>
    </div>
  );
}
