# Guide d'utilisation — Tableau de bord Inventaire

## Table des matieres

1. [Acceder au dashboard](#1-accéder-au-dashboard)
2. [Comprendre les KPI](#2-comprendre-les-kpi)
3. [Comprendre les types d'operations](#3-comprendre-les-types-dopérations)
4. [Utiliser les filtres](#4-utiliser-les-filtres)
5. [Configurer le rafraichissement automatique](#5-configurer-le-rafraîchissement-automatique)
6. [Naviguer vers les transferts](#6-naviguer-vers-les-transferts)
7. [Lire le graphique des mouvements](#7-lire-le-graphique-des-mouvements)
8. [Surveiller les alertes de stock minimum](#8-surveiller-les-alertes-de-stock-minimum)
9. [Consulter le top produits par mouvement](#9-consulter-le-top-produits-par-mouvement)
10. [Configurer les parametres par defaut](#10-configurer-les-paramètres-par-défaut)
11. [Droits d'acces](#11-droits-daccès)
12. [Cas d'usage courants](#12-cas-dusage-courants)

---

## 1. Acceder au dashboard

1. Ouvrir le menu principal **Inventaire**
2. Cliquer sur **Tableau de bord** (premier element du menu)

Le dashboard se charge et affiche les donnees en temps reel.

> **Note :** Le menu n'apparait que si vous avez le groupe "Utilisateur Dashboard Inventaire" ou "Responsable d'entrepot".

---

## 2. Comprendre les KPI

Les 8 cartes en haut du dashboard affichent les compteurs principaux :

### Cartes d'etat des transferts

- **Brouillon** (gris) — Transferts crees mais pas encore confirmes. Ce sont des operations en preparation.
- **En attente** (bleu clair) — Transferts confirmes mais en attente de disponibilite des produits.
- **Prets** (bleu) — Transferts dont les produits sont reserves et disponibles. Ils peuvent etre traites immediatement.
- **Termines** (vert) — Transferts termines sur la periode recente configurable (par defaut : 30 derniers jours).
- **Annules** (rouge sombre) — Transferts annules.

### Cartes d'alerte

- **En retard** (rouge) — Transferts dont la date prevue est depassee et qui sont toujours en cours (etats : pret, en attente, confirme). Ce sont les **urgences a traiter en priorite**.
- **Alertes stock min** (orange) — Nombre de produits dont le stock disponible en emplacements internes est inferieur au seuil minimum defini dans les regles de reapprovisionnement. Un chiffre eleve signale un risque de rupture.
- **Mouvements aujourd'hui** (turquoise) — Nombre total de mouvements de stock termines dans la journee en cours. Permet de mesurer l'activite quotidienne de l'entrepot.

### Interaction

Cliquer sur n'importe quelle carte ouvre la **liste filtree** des enregistrements correspondants dans une vue standard Odoo :

- Cartes d'etat → liste des transferts (`stock.picking`) filtres par etat
- En retard → liste des transferts en retard
- Alertes stock min → liste des regles de reapprovisionnement (`stock.warehouse.orderpoint`)
- Mouvements aujourd'hui → liste des mouvements de stock (`stock.move`) du jour

---

## 3. Comprendre les types d'operations

La section **Types d'operations** est une fonctionnalite distinctive du dashboard Inventaire. Elle affiche une carte pour chaque type d'operation configure dans l'entrepot.

### Code couleur

Les cartes utilisent un code couleur base sur le type d'operation :

| Type | Code | Couleur | Signification |
|---|---|---|---|
| **Receptions** | `incoming` | **Vert** | Marchandises entrant dans l'entrepot (fournisseurs) |
| **Expeditions** | `outgoing` | **Bleu** | Marchandises sortant de l'entrepot (clients) |
| **Transferts internes** | `internal` | **Orange** | Mouvements entre emplacements ou entrepots |
| **Autre** | autre | **Gris** | Types d'operations personnalises |

### Compteurs par type

Chaque carte affiche des compteurs independants :

- **Brouillon** — transferts en preparation pour ce type
- **En attente** — transferts en attente de disponibilite pour ce type
- **Prets** — transferts prets a traiter pour ce type
- **Termines (7j)** — transferts termines dans les 7 derniers jours pour ce type

### Indicateur de retard

Si des transferts sont en retard pour un type d'operation, un **indicateur d'alerte** (triangle orange avec le nombre) apparait en bas de la carte. Cela permet d'identifier immediatement quel flux logistique est en difficulte.

### Navigation

Cliquer sur une carte de type d'operation ouvre la **liste des transferts actifs** (non termines, non annules) de ce type specifique.

### Exemples de lecture

- Carte "Receptions" verte avec 5 Prets → 5 receptions fournisseurs sont pretes a etre validees
- Carte "Expeditions" bleue avec 2 en retard → 2 livraisons clients sont en retard, action requise
- Carte "Transferts internes" orange avec 3 En attente → 3 mouvements inter-entrepots attendent de la disponibilite

---

## 4. Utiliser les filtres

### Ouvrir le panneau

Cliquer sur le bouton **Filtres** dans l'en-tete du dashboard. Un panneau apparait avec les options suivantes :

### Filtres disponibles

#### Date debut / Date fin
- Permet de restreindre les donnees a une **periode precise**
- Filtre sur la date prevue (`scheduled_date`) des transferts
- Exemple : voir uniquement les transferts de mars 2026

#### Type d'operation
- Liste deroulante contenant tous les types d'operations configures (Receptions, Expeditions, Transferts internes, etc.)
- Permet de focaliser le dashboard sur un **flux logistique specifique**
- "-- Tous --" affiche les donnees de tous les types

#### Partenaire
- Liste deroulante contenant les partenaires (clients et fournisseurs) ayant des transferts dans le systeme (jusqu'a 200 partenaires)
- Permet de suivre les operations d'un **fournisseur ou client particulier**
- "-- Tous --" affiche tous les partenaires

#### Jours graphique
- **7 jours** — vue courte, ideale pour le suivi quotidien
- **14 jours** — vue bi-hebdomadaire
- **30 jours** — vue mensuelle

#### Periode stats
- Determine la periode pour le calcul affiche en haut du graphique ("30j: X transferts / Y mouvements")
- **7 jours** — cette semaine
- **30 jours** — ce mois (par defaut)
- **60 jours** — 2 mois
- **90 jours** — trimestre

### Appliquer les filtres

1. Configurer les filtres souhaites
2. Cliquer sur **Appliquer**
3. Le dashboard se recharge avec les donnees filtrees
4. Un **point bleu** apparait sur le bouton Filtres pour indiquer que des filtres sont actifs

### Reinitialiser

Cliquer sur **Reinitialiser** pour revenir aux valeurs par defaut et recharger toutes les donnees.

> **Note :** Les filtres Type d'operation et Partenaire affectent les cartes KPI et le tableau des transferts actifs. La section Types d'operations affiche toujours tous les types independamment du filtre.

---

## 5. Configurer le rafraichissement automatique

### Depuis le dashboard

Le selecteur **Auto** dans l'en-tete permet de choisir l'intervalle :

| Option | Usage recommande |
|---|---|
| **Off** | Travail ponctuel, consultation rapide |
| **30 secondes** | Suivi en temps reel sur ecran d'entrepot |
| **1 minute** | Supervision active des operations |
| **2 minutes** | Suivi regulier |
| **5 minutes** | Affichage permanent sur ecran mural |

### Depuis la configuration

Le responsable peut definir l'intervalle par defaut dans la configuration (voir section 10).

### Rafraichissement manuel

Le bouton **Actualiser** (icone de rafraichissement) force un rechargement immediat a tout moment.

L'heure de la derniere mise a jour est affichee a gauche des controles.

---

## 6. Naviguer vers les transferts

### Depuis les cartes KPI

Cliquer sur une carte → ouvre la **vue liste** des transferts filtres par cet etat.

- **Brouillon** → tous les transferts brouillon
- **En attente** → tous les transferts en attente
- **Prets** → tous les transferts prets (assigned)
- **Termines** → tous les transferts termines
- **Annules** → tous les transferts annules
- **En retard** → transferts en retard (date prevue depassee, etats actifs)
- **Alertes stock min** → regles de reapprovisionnement
- **Mouvements aujourd'hui** → mouvements de stock du jour

### Depuis les cartes Types d'operations

Cliquer sur une carte de type d'operation → ouvre la **vue liste** des transferts actifs de ce type.

### Depuis le tableau des transferts actifs

Cliquer sur une **ligne du tableau** → ouvre le **formulaire** du transfert directement.

---

## 7. Lire le graphique des mouvements

### Les barres

- Chaque barre represente un jour
- La hauteur indique le **nombre de mouvements de stock termines** ce jour-la
- La valeur exacte est affichee au-dessus de chaque barre
- La date est affichee en dessous (format jj/mm)

### Le resume

En haut a droite du graphique :
- **X transferts** — nombre total de transferts termines sur la periode stats
- **Y mouvements** — nombre total de mouvements de stock sur la periode stats

### Interpreter

- Des barres regulieres indiquent une activite d'entrepot stable
- Des barres a zero signalent des jours sans activite (weekend, fermeture, etc.)
- Une tendance a la hausse peut indiquer une augmentation d'activite a anticiper en ressources
- Des pics isoles peuvent correspondre a des receptions importantes ou des expeditions groupees

---

## 8. Surveiller les alertes de stock minimum

La carte **Alertes stock min** affiche le nombre de produits en situation critique :

### Comment ca fonctionne

1. Le systeme recupere toutes les **regles de reapprovisionnement** (`stock.warehouse.orderpoint`)
2. Pour chaque produit ayant une regle, il compare le **stock disponible** (quantite en emplacements internes) avec le **seuil minimum** defini
3. Si le stock est inferieur au seuil, le produit est compte comme alerte

### Actions recommandees

- Cliquer sur la carte pour ouvrir les regles de reapprovisionnement
- Verifier quels produits sont sous le seuil
- Lancer les commandes de reapprovisionnement necessaires
- Si le compteur est regulierement eleve, envisager d'ajuster les seuils ou les delais fournisseurs

---

## 9. Consulter le top produits par mouvement

La section **Top mouvements par produit** affiche un classement des 20 produits les plus actifs sur la periode stats :

| Colonne | Description |
|---|---|
| **Produit** | Nom du produit |
| **Qte deplacee** | Quantite totale deplacee (somme des mouvements termines) |
| **Nb mouvements** | Nombre de mouvements de stock distincts |

### Utilite

- Identifier les produits a **forte rotation** pour optimiser leur placement en entrepot
- Detecter des **anomalies** (produit avec un nombre anormalement eleve de mouvements)
- Alimenter les decisions de **reamenagement** des zones de stockage

---

## 10. Configurer les parametres par defaut

> Reserve aux **Responsables Dashboard Inventaire** (ou Responsables d'entrepot)

### Acceder a la configuration

**Inventaire > Configuration > Config. Dashboard**

### Creer une configuration

1. Cliquer sur **Nouveau**
2. Remplir les parametres :
   - **Jours graphique mouvements** — nombre de jours par defaut dans le graphique (defaut : 7)
   - **Jours statistiques recentes** — periode de calcul des totaux (defaut : 30)
   - **Limite transferts actifs** — combien de transferts afficher dans le tableau (defaut : 50)
   - **Rafraichissement auto** — intervalle par defaut (Desactive, 30s, 1min, 2min, 5min)
   - **Societe** — la societe concernee (en multi-societe)
3. Cliquer sur **Enregistrer**

### Multi-societe

Si vous gerez plusieurs societes, creez une configuration distincte pour chacune. Le dashboard chargera automatiquement la configuration correspondant a la societe active de l'utilisateur.

### Pas de configuration ?

Si aucune configuration n'existe pour la societe, le dashboard utilise les valeurs par defaut :
- 7 jours pour le graphique
- 30 jours pour les stats
- 50 transferts actifs max
- Pas d'auto-refresh

---

## 11. Droits d'acces

### Groupes disponibles

| Groupe | Acces dashboard | Acces config (lecture) | Acces config (modification) |
|---|---|---|---|
| Utilisateur Dashboard Inventaire | Oui | Oui | Non |
| Responsable Dashboard Inventaire | Oui | Oui | Oui |

### Heritage automatique

- Le groupe **Responsable d'entrepot** (`stock.group_stock_manager`) herite automatiquement du groupe **Responsable Dashboard Inventaire**
- Le groupe **Responsable Dashboard Inventaire** implique automatiquement le groupe **Utilisateur Dashboard Inventaire**
- En consequence, tout responsable d'entrepot a un acces complet sans configuration supplementaire

### Attribuer l'acces a un utilisateur

Pour donner acces au dashboard a un utilisateur qui n'est pas responsable d'entrepot :

1. Aller dans **Parametres > Utilisateurs**
2. Ouvrir la fiche de l'utilisateur
3. Dans la section **Dashboard Inventaire**, selectionner **Utilisateur** ou **Responsable**
4. Enregistrer

### Acces refuse ?

Si un utilisateur voit une erreur "Acces non autorise au dashboard inventaire", il faut lui attribuer le groupe **Utilisateur Dashboard Inventaire** au minimum.

---

## 12. Cas d'usage courants

### Reunion logistique quotidienne

1. Ouvrir le dashboard
2. Verifier les cartes **En retard** et **Alertes stock min** en priorite
3. Parcourir la section **Types d'operations** pour identifier quel flux pose probleme (receptions bloquees ? expeditions en retard ?)
4. Consulter le graphique pour voir l'activite de la veille
5. Parcourir le tableau des transferts actifs pour identifier les blocages

### Suivi des receptions fournisseurs

1. Ouvrir les filtres
2. Selectionner le type d'operation **Receptions** dans la liste deroulante
3. Optionnellement, selectionner un **partenaire** (fournisseur) specifique
4. Cliquer sur **Appliquer**
5. Le dashboard affiche uniquement les donnees relatives aux receptions
6. La carte **Prets** indique combien de receptions sont pretes a etre validees

### Analyse des mouvements de stock

1. Ouvrir les filtres
2. Etendre la **periode stats** a 60 ou 90 jours
3. Mettre les **jours graphique** a 30
4. Cliquer sur **Appliquer**
5. Le graphique montre l'evolution des mouvements sur un mois
6. Le tableau **Top mouvements par produit** revele les articles les plus manipules
7. Utiliser ces donnees pour optimiser le placement en entrepot

### Surveillance du stock minimum

1. Consulter regulierement la carte **Alertes stock min**
2. Si le chiffre augmente, cliquer dessus pour voir les produits concernes
3. Verifier les regles de reapprovisionnement et lancer les commandes necessaires
4. Envisager d'activer l'auto-refresh pour un suivi en continu

### Ecran d'entrepot (affichage permanent)

1. Ouvrir le dashboard sur un ecran dedie dans l'entrepot
2. Configurer l'auto-refresh a **30 secondes** ou **1 minute**
3. Le dashboard se met a jour en continu sans intervention
4. Les operateurs peuvent voir en un coup d'oeil :
   - Combien de transferts sont prets a traiter
   - Quels types d'operations ont des retards
   - L'activite de la journee en cours (mouvements aujourd'hui)
   - Les alertes de stock minimum

---

## Raccourcis clavier

Le dashboard utilise les interactions souris standard d'Odoo :
- **Clic** sur une carte KPI → liste filtree
- **Clic** sur une carte type d'operation → transferts actifs du type
- **Clic** sur une ligne du tableau → formulaire du transfert
- **F5** ou bouton Actualiser → rafraichir les donnees
