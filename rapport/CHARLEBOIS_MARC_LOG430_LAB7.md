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

Dans le Lab 5, la création d’une commande repose sur des appels synchrones REST. Quand on exécute add_order, tout s’enchaîne dans le même flot : insertion en MySQL, mise à jour du stock et appel direct du service de paiements via l’API-Gateway. Par exemple :

```Python
response = requests.post('http://api-gateway:8080/payments-api/payments', json={"user_id": user_id, "order_id": order_id, "total_amount": total_amount})
```
Si ce service est lent ou indisponible, l’ordre échoue et toute la transaction est annulée. C’est donc simple et cohérent immédiatement, mais fortement couplé et peu résilient.

Dans le Lab 7, on adopte une approche asynchrone Event Driven avec Kafka. Lorsqu’un utilisateur est créé, il est d’abord inséré en base, puis un événement est publié :

```Py
UserEventProducer().send('user-events', value={'event':'UserCreated','id':new_user.id})
```
Les autres services, comme le service de notification, écoutent ce topic et réagissent via leurs handlers :

```Python
registry.register(UserCreatedHandler(...))
consumer_service.start()
```
De cette façon, le service `store_manager` reste découplé : il n’attend pas la fin du traitement des autres services (dans ce cas-ci, le service de notification `Coolriel`). C’est plus robuste et extensible, mais la cohérence devient éventuelle et la gestion de Kafka ajoute de la complexité au code.



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