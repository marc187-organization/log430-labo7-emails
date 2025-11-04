<div align="center">

<center>
<h1 style="font-size:18pt;">
Labo 07 – Architecture Event-Driven, Event Sourcing et Pub/Sub
</h1>
</center>

<br>
<br>
<br>
<br>

<center>
<h2 style="font-size:16pt;">
PAR
</h2>
</center>

<br>
<br>

<center>
<h2 style="font-size:16pt;">
Marc CHARLEBOIS, CHAM65260301
</h2>
</center>

<br>
<br>
<br>
<br>
<br>
<br>

<center>
<h3 style="font-size:14pt;">
RAPPORT DE LABORATOIRE PRÉSENTÉ À MONSIEUR FABIO PETRILLO DANS LE CADRE DU COURS <em>ARCHITECTURE LOGICIELLE</em> (LOG430-01)
</h3>
</center>

<br>
<br>
<br>
<br>
<br>

<center>
<h3 style="font-size:14pt;">
MONTRÉAL, LE 11 NOVEMBRE 2025
</h3>
</center>

<br>
<br>
<br>
<br>
<br>

<center>
<h3 style="font-size:14pt;">
ÉCOLE DE TECHNOLOGIE SUPÉRIEURE<br>
UNIVERSITÉ DU QUÉBEC
</h3>
</center>

<br>
<br>
<br>
<br>
<br>

</div>

---
## **Tables des matières**
- [**Tables des matières**](#tables-des-matières)
  - [**Question 1**](#question-1)
  - [**Question 2**](#question-2)
  - [**Question 3**](#question-3)
  - [**Question 4**](#question-4)
  - [**Question 5**](#question-5)
  - [**CI/CD**](#cicd)

<br>

---

<div align="justify">

### **Question 1**

> Quelle est la différence entre la communication entre store_manager et coolriel dans ce labo et la communication entre store_manager et payments_api que nous avons implémentée pendant le labo 5 ? Expliquez avec des extraits de code ou des diagrammes et discutez des avantages et des inconvénients.


### **Question 2**

> Quelles méthodes avez-vous modifiées dans src/orders/commands/write_user.py? Illustrez avec des captures d'écran ou des extraits de code.


### **Question 3**

> Comment avez-vous implémenté la vérification du type d'utilisateur ? Illustrez avec des captures d'écran ou des extraits de code.

### **Question 4**

> Comment Kafka utilise-t-il son système de partitionnement pour atteindre des performances de lecture élevées ? Lisez cette section de la documentation officielle à Kafka et résumez les points principaux.

### **Question 5**

> Combien d'événements avez-vous récupérés dans votre historique ? Illustrez avec le fichier JSON généré.


### **CI/CD**

Mon pipeline CI/CD fonctionne ainsi : lors de chaque push ou pull request, mon script CI s’exécute sur GitHub Actions, lance un environnement avec MySQL et Redis, installe les dépendances et exécute les tests pour valider mon code. Si tout est correct, mon script CD se déclenche automatiquement via un runner self-hosted installé sur ma VM, qui récupère le dépôt, génère le fichier .env, construit et démarre les conteneurs avec Docker Compose, puis affiche l’état et les logs pour confirmer le déploiement.

On peut voir ci-dessous que les deux workflows se sont exécutés correctement, ce qui confirme que l’application a été testée puis déployée sans erreur.

![alt text](cicd-1.png)


Le déploiement s’effectue sur mon runner auto-hébergé configuré sur la VM, qui exécute directement les commandes Docker.

![alt text](cicd-2.png)


La commande `docker ps` montre que les conteneurs sont bien lancés sur la VM et que l’application est en fonctionnement.

![alt text](cicd-3.png)