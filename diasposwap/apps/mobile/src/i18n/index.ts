import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { getLocales } from 'expo-localization';

const fr = {
  sim: 'Mode simulation — aucun argent réel',
  slogan: "L'argent circule localement. La valeur voyage.",
  common: { continue: 'Continuer', cancel: 'Annuler', confirm: 'Confirmer', back: 'Retour', soon: 'Bientôt', close: 'Fermer', seeAll: 'Tout voir' },
  onboarding: {
    s1t: 'Des transferts qui se compensent', s1b: 'Votre envoi vers le Cameroun rencontre un envoi du Cameroun vers la France. Chaque argent est payé localement.',
    s2t: 'Transparent avant de confirmer', s2b: 'Taux, frais et montant reçu sont affichés avant chaque ordre. Délais indicatifs, jamais garantis.',
    s3t: 'Équilibre et réciprocité', s3b: 'Inspiré de Maât : chaque flux trouve son contrepoids. Aucune donnée de contrepartie ne vous est montrée.',
    language: 'Langue', start: 'Commencer',
  },
  login: { title: 'Connexion démo', subtitle: 'Choisissez un profil fictif pour explorer DiaspoSwap.', pin: 'Code PIN démo (4 chiffres)', pinError: 'Saisissez 4 chiffres', submit: 'Se connecter', residence: 'Réside en' },
  tabs: { home: 'Accueil', send: 'Envoyer', history: 'Historique', profile: 'Profil' },
  home: {
    hello: 'Bonjour {{name}}', send: "Envoyer de l'argent", sent: 'Envoyé', received: 'Reçu par vos proches', fees: 'Frais payés',
    savings: 'Économies', savingsNA: 'Non affiché : aucune référence de prix documentée', inProgress: 'En cours', done: 'Terminés',
    corridors: 'Disponibilité des corridors (indicatif)', rates: 'Taux indicatifs', recent: 'Activité récente', none: 'Aucun transfert pour l’instant',
    balanced: 'Équilibré', waiting: 'Attente probable', unknown: 'Données insuffisantes', uncertainty: { LOW: 'incertitude faible', MEDIUM: 'incertitude moyenne', HIGH: 'incertitude élevée' },
  },
  send: {
    title: 'Nouveau transfert', from: 'Depuis', to: 'Vers', amount: 'Montant à envoyer', fee: 'Frais DiaspoSwap (0,75 %, hypothèse)',
    total: 'Total à payer', rate: 'Taux appliqué', receive: 'Montant estimé reçu', peg: 'Parité fixe officielle', simulatedRate: 'Taux simulé',
    beneficiary: 'Bénéficiaire', addBeneficiary: 'Ajouter un bénéficiaire', partial: 'Accepter un matching partiel',
    partialHelp: 'Votre ordre peut être compensé par plusieurs envois inverses.', review: 'Vérifier l’ordre', invalid: 'Montant invalide', noBeneficiary: 'Ajoutez un bénéficiaire dans ce pays',
  },
  confirm: {
    title: 'Confirmation', validity: 'Cotation valable jusqu’à {{time}}', delay: 'Délai : dépend de la disponibilité d’ordres inverses (indicatif, non garanti).',
    pay: 'Payer {{amount}} (simulé)', blocked: 'Ordre bloqué par la conformité (simulée)', review: 'Ordre en revue de conformité (simulée)',
  },
  tracking: {
    title: 'Suivi du transfert', matched: 'Compensé', refunded: 'Remboursé', toReceive: 'Reçu par le bénéficiaire', pending: 'En attente de paiement local',
    demo: 'Outils de démonstration', counterparty: 'Simuler un ordre inverse (contrepartie fictive)', half: 'Simuler un ordre inverse partiel (50 %)',
    runMatching: 'Lancer le matching', settle: 'Confirmer les paiements simulés', receipt: 'Voir le reçu', cancel: 'Annuler l’ordre',
    privacy: 'Les informations de la contrepartie ne sont jamais affichées.', timeline: 'Historique des étapes', matches: '{{count}} compensation(s)',
  },
  states: {
    DRAFT: 'Brouillon', QUOTED: 'Coté', PENDING_VERIFICATION: 'Vérification', PENDING_FUNDING: 'En attente de paiement', FUNDED: 'Payé',
    QUEUED: 'En recherche de matching', PARTIALLY_MATCHED: 'Partiellement compensé', MATCHED: 'Compensé', SETTLEMENT_PENDING: 'Paiements locaux en cours',
    SETTLED: 'Terminé', FAILED: 'Échoué', EXPIRED: 'Expiré', CANCELLED: 'Annulé', REFUND_PENDING: 'Remboursement en cours', REFUNDED: 'Remboursé', DISPUTED: 'En litige',
  },
  history: { title: 'Historique', empty: 'Aucune transaction' },
  receipt: { title: 'Reçu', status: 'Statut', disclaimer: 'Document de simulation sans valeur. Aucun paiement réel n’a eu lieu.', order: 'Référence', date: 'Date' },
  profile: {
    title: 'Profil', kyc: 'Niveau de vérification', language: 'Langue', beneficiaries: 'Bénéficiaires', notifications: 'Notifications',
    security: 'Sécurité', securityBody: 'Session stockée de façon chiffrée sur l’appareil (SecureStore). MFA et biométrie : à venir.',
    simulated: 'simulé', pepYes: 'Oui — revue renforcée', pepNo: 'Non', communities: 'Communautés de diaspora', referral: 'Parrainage', help: 'Centre d’assistance', disputes: 'Litiges', logout: 'Se déconnecter', liquidity: 'Liquidité des corridors (démo)',
  },
  beneficiaries: { title: 'Bénéficiaires', name: 'Nom complet', country: 'Pays', account: 'Référence de compte (fictive)', add: 'Ajouter', nameError: 'Nom trop court', accountError: 'Référence requise', verifiedNote: 'Les nouveaux bénéficiaires passent en vérification (simulée).' },
  notifications: { title: 'Notifications', empty: 'Aucune notification' },
};

type Dict = typeof fr;
const en: Dict = {
  sim: 'Simulation mode — no real money',
  slogan: 'Money stays local. Value goes global.',
  common: { continue: 'Continue', cancel: 'Cancel', confirm: 'Confirm', back: 'Back', soon: 'Coming soon', close: 'Close', seeAll: 'See all' },
  onboarding: {
    s1t: 'Transfers that offset each other', s1b: 'Your transfer to Cameroon meets a transfer from Cameroon to France. Each side is paid out locally.',
    s2t: 'Transparent before you confirm', s2b: 'Rate, fees and amount received are shown before every order. Timings are indicative, never guaranteed.',
    s3t: 'Balance and reciprocity', s3b: 'Inspired by Maat: every flow finds its counterweight. Counterparty data is never shown to you.',
    language: 'Language', start: 'Get started',
  },
  login: { title: 'Demo sign-in', subtitle: 'Pick a fictional profile to explore DiaspoSwap.', pin: 'Demo PIN (4 digits)', pinError: 'Enter 4 digits', submit: 'Sign in', residence: 'Lives in' },
  tabs: { home: 'Home', send: 'Send', history: 'History', profile: 'Profile' },
  home: {
    hello: 'Hello {{name}}', send: 'Send money', sent: 'Sent', received: 'Received by your family', fees: 'Fees paid',
    savings: 'Savings', savingsNA: 'Not shown: no documented price reference', inProgress: 'In progress', done: 'Completed',
    corridors: 'Corridor availability (indicative)', rates: 'Indicative rates', recent: 'Recent activity', none: 'No transfers yet',
    balanced: 'Balanced', waiting: 'Likely wait', unknown: 'Not enough data', uncertainty: { LOW: 'low uncertainty', MEDIUM: 'medium uncertainty', HIGH: 'high uncertainty' },
  },
  send: {
    title: 'New transfer', from: 'From', to: 'To', amount: 'Amount to send', fee: 'DiaspoSwap fee (0.75%, assumption)',
    total: 'Total to pay', rate: 'Rate applied', receive: 'Estimated amount received', peg: 'Official fixed parity', simulatedRate: 'Simulated rate',
    beneficiary: 'Beneficiary', addBeneficiary: 'Add a beneficiary', partial: 'Accept partial matching',
    partialHelp: 'Your order may be offset by several opposite transfers.', review: 'Review order', invalid: 'Invalid amount', noBeneficiary: 'Add a beneficiary in this country',
  },
  confirm: {
    title: 'Confirmation', validity: 'Quote valid until {{time}}', delay: 'Timing depends on opposite orders being available (indicative, not guaranteed).',
    pay: 'Pay {{amount}} (simulated)', blocked: 'Order blocked by (simulated) compliance', review: 'Order under (simulated) compliance review',
  },
  tracking: {
    title: 'Transfer tracking', matched: 'Offset', refunded: 'Refunded', toReceive: 'Received by beneficiary', pending: 'Awaiting local payout',
    demo: 'Demo tools', counterparty: 'Simulate an opposite order (fictional counterparty)', half: 'Simulate a partial opposite order (50%)',
    runMatching: 'Run matching', settle: 'Confirm simulated payments', receipt: 'View receipt', cancel: 'Cancel order',
    privacy: 'Counterparty information is never displayed.', timeline: 'Step history', matches: '{{count}} offset(s)',
  },
  states: {
    DRAFT: 'Draft', QUOTED: 'Quoted', PENDING_VERIFICATION: 'Verification', PENDING_FUNDING: 'Awaiting payment', FUNDED: 'Paid',
    QUEUED: 'Looking for a match', PARTIALLY_MATCHED: 'Partially offset', MATCHED: 'Offset', SETTLEMENT_PENDING: 'Local payouts in progress',
    SETTLED: 'Completed', FAILED: 'Failed', EXPIRED: 'Expired', CANCELLED: 'Cancelled', REFUND_PENDING: 'Refund in progress', REFUNDED: 'Refunded', DISPUTED: 'Disputed',
  },
  history: { title: 'History', empty: 'No transactions' },
  receipt: { title: 'Receipt', status: 'Status', disclaimer: 'Simulation document with no value. No real payment took place.', order: 'Reference', date: 'Date' },
  profile: {
    title: 'Profile', kyc: 'Verification level', language: 'Language', beneficiaries: 'Beneficiaries', notifications: 'Notifications',
    security: 'Security', securityBody: 'Session stored encrypted on the device (SecureStore). MFA and biometrics: coming.',
    simulated: 'simulated', pepYes: 'Yes — enhanced review', pepNo: 'No', communities: 'Diaspora communities', referral: 'Referral', help: 'Help centre', disputes: 'Disputes', logout: 'Sign out', liquidity: 'Corridor liquidity (demo)',
  },
  beneficiaries: { title: 'Beneficiaries', name: 'Full name', country: 'Country', account: 'Account reference (fictional)', add: 'Add', nameError: 'Name too short', accountError: 'Reference required', verifiedNote: 'New beneficiaries go through (simulated) verification.' },
  notifications: { title: 'Notifications', empty: 'No notifications' },
};

const device = getLocales()[0]?.languageCode === 'en' ? 'en' : 'fr';
void i18n.use(initReactI18next).init({ resources: { fr: { translation: fr }, en: { translation: en } }, lng: device, fallbackLng: 'fr', interpolation: { escapeValue: false } });
export default i18n;
