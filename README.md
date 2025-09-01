# 📦 FreeLedger API – Backend Django REST Framework

<details>
<summary>📌 Détails du projet</summary>

## Contexte

FreeLedger API est une application REST développée avec Django et Django REST Framework. Elle vise à simplifier la gestion administrative des indépendants et des petites entreprises : création de devis, factures, enregistrement des paiements, gestion des clients et des entreprises, et export comptable.

---

## Entités à modéliser

- **User** : id, email, mot de passe (hashé), nom, prénom, rôle (utilisateur/admin), statut,  
  infos complémentaires (adresse, téléphone…)
- **Company** : id, nom, adresse, numéro de TVA
- **Client** : id, nom, email, téléphone, adresse, société associée
- **Product** : id, nom, description, prix unitaire, stock
- **Quote** : id, référence, date, id_client, statut (brouillon, envoyé, accepté), lignes
- **Invoice** : id, référence, date, id_quote (optionnel), statut (brouillon, envoyé, payé), lignes
- **LineItem** : id, id_invoice ou id_quote, id_product (optionnel), description, quantité, prix unitaire
- **Payment** : id, id_invoice, date, montant

---

## Gestion des rôles & permissions

- **Utilisateur** : création de compte, consultation de son profil et de ses documents  
- **Admin** : gestion des utilisateurs, des entreprises, des clients, des produits, des devis/factures,  
  export comptable

---

### Périmètre du MVP  
1. **Gestion du compte & profil**  
   - Inscription, connexion, déconnexion (JWT)  
   - Complétion et mise à jour du profil utilisateur  
   - Enregistrement des informations d’entreprise  
   - CRUD du carnet d’adresses clients  

2. **Cycle de vente**  
   - Création de devis (lignes manuelles ou catalogue)  
   - Conversion d’un devis accepté en facture  
   - Création directe de facture  
   - Envoi de devis/factures en PDF par email  
   - Consultation de l’historique devis & factures  
   - Enregistrement manuel de paiements  

3. **Export comptable**  
   - Génération d’une archive `.zip` pour une période donnée  
   - Contenu de la ZIP :  
     - PDF de chaque facture  
     - CSV récapitulatif des factures  
     - CSV récapitulatif des paiements 

</details>

<details>
<summary>📌 Architecture du projet</summary>

## Architecture du projet

```
FreeLedger_api/               # Racine du projet
├── apps/                     # Conteneur des bundles métiers
│   ├── authentification/     # JWT, views, serializers, services, tests
│   ├── users/                # Profils et gestion entreprises
│   ├── companies/            # Modèle Company & services
│   ├── clients/              # CRM : clients
│   ├── catalog/              # Articles / produits
│   └── documents/            # Devis, Factures, LineItems, Paiements
│
├── core/                     # Configuration Django + Swagger/OpenAPI
│   └── management/
│   │    └── commands/
│   │         └── startapp_plus.py
│   │
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   └── urls.py               # Routeur principal + doc Swagger
│
├── requirements/             # Fichiers de dépendances Python
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── shared/                   # Code réutilisable (exceptions, utils, validators,...)
│   ├── constants/
│   ├── exceptions/
│   ├── mixins/
│   ├── utils/
│   └── validators/
│
├── manage.py                 # CLI Django
└── README.md                 # Cette documentation
```
</details>

<details>
<summary>📌 Modèle de données</summary>

## 3. Modèle de données

### 3.1 Authentification & profils

| Table             | Colonnes principales                                                                             |
|-------------------|-------------------------------------------------------------------------------------------------|
| **auth_accounts** | id (PK), email (unique), password_hash, created_at, updated_at, last_login                      |
| **user_profiles** | user_id (PK, FK→auth_accounts.id), first_name, last_name, birth_date, phone_number, adresse…    |
| **companies**     | id (PK), owner_id (FK→auth_accounts.id), name, legal_form, reg_number, vat_number, adresse…    |

### 3.2 Données métier

| Table    | Colonnes principales                                                                           |
|----------|-----------------------------------------------------------------------------------------------|
| **clients** | id (PK), company_id (FK→companies.id), name, email, phone, adresse…, vat_number              |
| **items**   | id (PK), company_id (FK→companies.id), name, description, unit_price, vat_rate               |

### 3.3 Documents

| Table        | Colonnes principales                                                                                                                                           |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **quotes**   | id (PK), company_id (FK), client_id (FK), quote_number, status, issue_date, validity_date, total_htva, notes, snapshot client (nom, adresse…), created_at… |
| **invoices** | id (PK), company_id (FK), client_id (FK), quote_id (FK, optionnel), invoice_number, status, issue_date, due_date, total_htva, notes, snapshot client…, created_at… |
| **line_items** | id (PK), quote_id (FK), invoice_id (FK), item_id (FK optionnel), description, quantity, unit_price, vat_rate                                               |
| **payments** | id (PK), invoice_id (FK), payment_date, amount, payment_method, notes, created_at                                                                              |

### 3.4 Relations clés

- auth_accounts.id → user_profiles.user_id  
- auth_accounts.id → companies.owner_id  
- companies.id → clients.company_id  
- companies.id → items.company_id  
- companies.id → quotes.company_id  
- clients.id → quotes.client_id  
- quotes.id → invoices.quote_id  
- quotes.id → line_items.quote_id  
- invoices.id → line_items.invoice_id  
- invoices.id → payments.invoice_id  

</details>
