Vue d'ensemble du Projet

Spotilike est une application web moderne de gestion et de découverte musicale, construite avec une architecture Full-Stack découplée.

Le projet a deux objectifs principaux :
    -Backend (API REST) : Fournir des points d'accès (endpoints) robustes pour gérer les artistes, albums et morceaux.
    -Frontend (Angular) : Offrir une expérience utilisateur immersive et dynamique, caractérisée par un design sombre  et des accents Néon Cyan.

Stack Technique

Le projet repose sur une architecture solide et des technologies modernes :
    -Frontend (Angular/TypeScript) : Développement de l'interface utilisateur SPA (Single Page Application).
    -Styling (CSS Natif & Tailwind CSS) : Design réactif et application du thème Néon Cyan.
    -Backend (Node.js ou équivalent) : Gestion de la logique métier et des requêtes API.
    -Base de Données (Firestore ou Mongo/PostgreSQL) : Stockage des données d'artistes, albums, morceaux et genres.

Instructions d'Installation et de Démarrage

1 installation du front end :
    cd <front-end>
    npm install 
    ng serve 
2 installation et lancement du back-end:
    cd <back-end>
    pip install requirement.txt
    uvicorn app.main:app --reload

Améliorations Futures (Axe d'évolution)

Le projet continuera d'évoluer avec les fonctionnalités suivantes :
    -Playlists : Fonctionnalité permettant aux utilisateurs de créer et gérer leurs propres playlists.
    -Fonctionnalité de Lecture : Intégration d'un lecteur audio fonctionnel.
    -Optimisation : Amélioration des performances de l'API et du chargement initial de l'application