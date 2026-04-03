# Tableau de bord Inventaire (Inventory Dashboard)

Module Odoo 18 — Dashboard Inventaire dynamique avec KPI en temps réel, vue par types d'operations, filtres interactifs et configuration par societe.

**Auteur :** SOPROMER  
**Version :** 18.0.2.0.0  
**Licence :** LGPL-3  
**Dependance :** `stock`

---

## Fonctionnalites

### KPI en temps reel (8 indicateurs)

| Indicateur | Description |
|---|---|
| **Brouillon** | Nombre de transferts en etat brouillon |
| **En attente** | Transferts en attente de disponibilite |
| **Prets** | Transferts prets a etre traites (composants reserves) |
| **Termines** | Transferts termines sur la periode recente (N derniers jours) |
| **Annules** | Transferts annules |
| **En retard** | Transferts dont la date prevue est depassee (etats actifs uniquement) |
| **Alertes stock min** | Produits dont le stock disponible est inferieur au seuil de reapprovisionnement |
| **Mouvements aujourd'hui** | Nombre de mouvements de stock termines dans la journee |

Chaque carte KPI est **cliquable** et ouvre la liste filtree des transferts ou enregistrements correspondants.

### Types d'operations (fonctionnalite unique)

Le dashboard affiche une **section dediee aux types d'operations** de l'entrepot. Chaque type d'operation (Reception, Expedition, Transfert interne, etc.) est represente par une carte individuelle avec un code couleur distinctif :

| Code operation | Couleur | Exemple |
|---|---|---|
| `incoming` (Receptions) | **Vert** | Receptions fournisseurs |
| `outgoing` (Expeditions) | **Bleu** | Livraisons clients |
| `internal` (Transferts internes) | **Orange** | Transferts inter-entrepots |
| Autre | Gris | Types personnalises |

Chaque carte de type d'operation affiche :

- **Nom** du type d'operation
- **Compteurs par etat** : Brouillon, En attente, Prets, Termines (7 derniers jours)
- **Indicateur de retard** : nombre de transferts en retard pour ce type (avec icone d'alerte)

Cliquer sur une carte ouvre la liste des **transferts actifs** (non termines, non annules) de ce type d'operation.

### Graphique des mouvements de stock

- Graphique en barres des mouvements de stock quotidiens (mouvements termines par jour)
- Periode configurable : **7, 14 ou 30 jours**
- Resume en haut a droite : total transferts termines et total mouvements sur la periode stats

### Tableau des transferts actifs

- Liste des transferts non termines (brouillon, en attente, confirme, pret)
- Colonnes : Reference, Type operation, Partenaire, Date prevue, Etat
- Tri par date prevue croissante
- Cliquer sur une ligne ouvre le formulaire du transfert
- Nombre d'enregistrements configurable (par defaut : 50)

### Top mouvements par produit

- Classement des 20 produits avec le plus de mouvements de stock sur la periode
- Colonnes : Produit, Quantite deplacee, Nombre de mouvements
- Permet d'identifier rapidement les articles les plus actifs

---

## Filtres dynamiques

Le panneau de filtres s'ouvre via le bouton **Filtres** dans l'en-tete du dashboard.

| Filtre | Description |
|---|---|
| **Date debut** | Filtrer les transferts a partir de cette date (date prevue) |
| **Date fin** | Filtrer les transferts jusqu'a cette date (date prevue) |
| **Type d'operation** | Filtrer par type d'operation (Reception, Expedition, Interne, etc.) |
| **Partenaire** | Filtrer par partenaire (client ou fournisseur, liste dynamique) |
| **Jours graphique** | Nombre de jours affiches dans le graphique (7/14/30) |
| **Periode stats** | Periode pour les statistiques recentes (7/30/60/90 jours) |

- Un **point bleu** apparait sur le bouton Filtres quand des filtres sont actifs
- Bouton **Appliquer** pour lancer la recherche
- Bouton **Reinitialiser** pour revenir aux valeurs par defaut

---

## Rafraichissement automatique

Le selecteur dans l'en-tete permet de configurer le rafraichissement automatique :

- **Off** — rafraichissement manuel uniquement
- **30 secondes**
- **1 minute**
- **2 minutes**
- **5 minutes**

L'heure de la derniere mise a jour est affichee a cote des controles.

---

## Installation

### Prerequis

- Odoo 18 Community ou Enterprise
- Module `stock` (Inventaire) installe et configure

### Etapes

1. Copier le dossier `inventory_dashboard` dans le repertoire des addons personnalises :

   ```
   cp -r inventory_dashboard /chemin/vers/odoo18/custom-addons/
   ```

2. Mettre a jour la liste des modules dans Odoo :

   **Applications > Mettre a jour la liste des applications**

3. Rechercher et installer le module :

   **Applications > Rechercher "Tableau de bord Inventaire" > Installer**

4. Ou via la ligne de commande :

   ```bash
   python odoo-bin -d ma_base -u inventory_dashboard --stop-after-init
   ```

### Mise a jour

Pour mettre a jour apres modification :

```bash
python odoo-bin -d ma_base -u inventory_dashboard --stop-after-init
```

---

## Configuration

### Acceder a la configuration

**Inventaire > Configuration > Config. Dashboard**

> Seuls les **Responsables Dashboard Inventaire** (ou les Responsables d'entrepot via l'heritage automatique) peuvent modifier la configuration.

### Parametres disponibles

| Parametre | Par defaut | Description |
|---|---|---|
| Jours graphique mouvements | 7 | Nombre de jours dans le graphique en barres |
| Jours statistiques recentes | 30 | Periode pour le calcul des totaux (transferts termines) |
| Limite transferts actifs | 50 | Nombre max de transferts affiches dans le tableau |
| Rafraichissement auto | Desactive | Intervalle de mise a jour automatique |
| Societe | Societe courante | Configuration par societe (multi-societe) |

### Multi-societe

Chaque societe peut avoir sa propre configuration. Le dashboard charge automatiquement la configuration de la societe active de l'utilisateur.

---

## Droits d'acces

### Groupes dedies

Le module definit ses propres groupes de securite dans la categorie **Dashboard Inventaire** :

| Groupe | Voir le dashboard | Voir la config | Modifier la config |
|---|---|---|---|
| Utilisateur Dashboard Inventaire | Oui | Oui (lecture) | Non |
| Responsable Dashboard Inventaire | Oui | Oui | Oui |

### Heritage automatique

Le groupe **Responsable d'entrepot** (`stock.group_stock_manager`) herite automatiquement du groupe **Responsable Dashboard Inventaire**. Ainsi, tout responsable d'entrepot existant a acces complet au dashboard et a sa configuration sans manipulation supplementaire.

Le groupe **Responsable Dashboard Inventaire** implique automatiquement le groupe **Utilisateur Dashboard Inventaire**.

### Attribuer l'acces manuellement

Pour donner acces au dashboard a un utilisateur qui n'est pas responsable d'entrepot :

1. Aller dans **Parametres > Utilisateurs**
2. Ouvrir la fiche de l'utilisateur
3. Dans la section **Dashboard Inventaire**, selectionner **Utilisateur** ou **Responsable**
4. Enregistrer

---

## Architecture technique

```
inventory_dashboard/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py                          # Endpoints RPC
├── models/
│   ├── __init__.py
│   └── inventory_dashboard_config.py    # Modele de configuration
├── security/
│   ├── ir.model.access.csv              # Droits d'acces
│   └── inventory_dashboard_groups.xml   # Groupes de securite
├── static/src/
│   ├── css/inventory_dashboard.css      # Styles
│   ├── js/inventory_dashboard.js        # Composant OWL
│   └── xml/inventory_dashboard.xml      # Template OWL
├── views/
│   ├── inventory_dashboard_views.xml        # Menu + Action client
│   └── inventory_dashboard_config_views.xml # Vues configuration
├── doc/
│   └── guide_utilisation.md             # Guide detaille
└── README.md
```

### Endpoints API

| Route | Type | Description |
|---|---|---|
| `/inventory_dashboard/data` | JSON (POST) | Donnees du dashboard avec filtres |
| `/inventory_dashboard/filters_data` | JSON (POST) | Listes pour les selecteurs de filtres (types d'operation, partenaires) |

### Parametres de `/inventory_dashboard/data`

```json
{
  "filters": {
    "chart_days": 7,
    "recent_days": 30,
    "active_picking_limit": 50,
    "date_from": "2026-01-01",
    "date_to": "2026-03-31",
    "picking_type_id": 3,
    "partner_id": 15
  }
}
```

### Reponse de `/inventory_dashboard/data`

```json
{
  "state_counts": {
    "draft": 5,
    "waiting": 3,
    "assigned": 12,
    "done": 45,
    "cancel": 2
  },
  "late_count": 4,
  "low_stock_count": 7,
  "moves_today_count": 23,
  "operation_type_stats": [
    {
      "id": 1,
      "name": "Receptions",
      "code": "incoming",
      "draft": 2,
      "waiting": 1,
      "assigned": 5,
      "done": 15,
      "late": 1
    }
  ],
  "daily_moves": [
    {"date": "27/03", "count": 18}
  ],
  "done_pickings_total": 45,
  "done_moves_total": 312,
  "active_pickings": [],
  "top_products": [],
  "config": {}
}
```

### Reponse de `/inventory_dashboard/filters_data`

```json
{
  "picking_types": [
    {"id": 1, "name": "Receptions"},
    {"id": 2, "name": "Expeditions"},
    {"id": 3, "name": "Transferts internes"}
  ],
  "partners": [
    {"id": 10, "name": "Fournisseur A"},
    {"id": 20, "name": "Client B"}
  ]
}
```

### Technologies

- **Frontend :** OWL 2 (framework reactif Odoo), Bootstrap 5
- **Backend :** Odoo 18 HTTP Controllers, ORM
- **Modeles interroges :** `stock.picking`, `stock.move`, `stock.picking.type`, `stock.warehouse.orderpoint`, `stock.quant`

---

## Depannage

| Probleme | Solution |
|---|---|
| Le dashboard ne s'affiche pas | Verifier que le module `stock` est installe. Vider le cache navigateur (Ctrl+Maj+Suppr). |
| Erreur "Acces non autorise" | Verifier que l'utilisateur a le groupe "Utilisateur Dashboard Inventaire" ou "Responsable d'entrepot". |
| Les filtres type operation/partenaire sont vides | Normal si aucun transfert n'existe encore dans le systeme. |
| L'auto-refresh ne fonctionne pas | Verifier que la valeur est differente de "Off" dans le selecteur. |
| Les donnees ne correspondent pas | Cliquer sur "Actualiser" pour forcer un rechargement. |
| La section Types d'operations est vide | Verifier que des types d'operation sont configures dans Inventaire > Configuration > Types d'operations. |
| Le compteur Alertes stock min reste a zero | Verifier que des regles de reapprovisionnement sont definies dans Inventaire > Operations > Reapprovisionnement. |

---

## Licence

Ce module est distribue sous licence [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html).
