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

J’ai modifié la méthode `add_user` afin d’y ajouter le paramètre `user_type_id`, ce qui permet d’associer chaque utilisateur à un type spécifique (par exemple client, employé ou administrateur). La méthode insère toujours l’utilisateur dans la base MySQL, mais publie maintenant sur Kafka un événement `UserCreated` enrichi avec ce champ supplémentaire, de même manière que pour l'évenement `UserDeleted`  :

```Py
def add_user(name: str, email: str, user_type_id: int):
    """Insert user with items in MySQL"""
    if not name or not email or not user_type_id:
        raise ValueError("Cannot create user. A user must have name, email and a user_type_id.")

    session = get_sqlalchemy_session()

    try:
        new_user = User(name=name, email=email, user_type_id=user_type_id)
        session.add(new_user)
        session.flush()
        session.commit()

        user_event_producer = UserEventProducer()
        user_event_producer.get_instance().send('user-events', value={'event': 'UserCreated',
                                           'id': new_user.id,
                                           'name': new_user.name,
                                           'email': new_user.email,
                                           'user_type_id': new_user.user_type_id,
                                           'datetime': str(datetime.datetime.now())})
        return new_user.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
```


### **Question 3**

> Comment avez-vous implémenté la vérification du type d'utilisateur ? Illustrez avec des captures d'écran ou des extraits de code.

J’ai implémenté la vérification du type d’utilisateur directement dans la méthode `handle()` du `UserCreatedHandler` et du `UserDeletedHandler`. Après avoir récupéré la valeur de `user_type_id` depuis les données de l’événement, j’ai ajouté une condition  pour définir une variable `message` que j'ai ajouté au template HTML. Cette variable est donc différente selon le type d’utilisateur. Par exemple :

```Py
user_type_id = event_data.get('user_type_id')
# Autres variables prises de l'évenement...

message = "Salut et bienvenue dans l'équipe!" # Employee or Manager
if user_type_id == 1: # Client
    message = "Merci d'avoir visité notre magazin. Si vous avez des questions ou des problèmes concernant votre achat, n'hésitez pas à nous contacter."


current_file = Path(__file__)
project_root = current_file.parent.parent
with open(project_root / "templates" / "welcome_client_template.html", 'r') as file:
    html_content = file.read()
    # Autres variables remplacées dans le templates...
    html_content = html_content.replace("{{message}}", message)

```

De même pour `UserDeletedHandler`:
```Py
user_type_id = event_data.get('user_type_id')
# Autres variables prises de l'évenement...

message = ""
if user_type_id == 1: # Client
    message = "Merci d'avoir été Client de notre magasin."
if user_type_id == 1: # Employee
    message = "Merci d'avoir été Employee de notre magasin."
if user_type_id == 1: # Manager
    message = "Merci d'avoir été Manager de notre magasin."


current_file = Path(__file__)
project_root = current_file.parent.parent
with open(project_root / "templates" / "goodbye_client_template.html", 'r') as file:
    html_content = file.read()
    # Autres variables remplacées dans le templates...
    html_content = html_content.replace("{{message}}", message)
```



### **Question 4**

> Comment Kafka utilise-t-il son système de partitionnement pour atteindre des performances de lecture élevées ? Lisez cette section de la documentation officielle à Kafka et résumez les points principaux.

Le système de partitionnement de Apache Kafka permet d’atteindre de hautes performances de lecture en divisant chaque sujet (topic) en plusieurs partitions indépendantes, chacune étant un journal ordonné append-only. Ainsi, plusieurs consommateurs d’un même groupe peuvent lire en parallèle chaque partition différente, ce qui augmente le débit global de lecture. De plus, chaque partition peut être placée sur un noeud (broker) différent, permettant la distribution de la charge (lecture/écriture) entre plusieurs serveurs, et la réplication de partitions garantit la disponibilité et la tolérance aux pannes. Enfin, Kafka assure l’ordre des messages à l’intérieur d’une partition (mais pas entre partitions), ce qui permet de maintenir les garanties d’ordre tout en exploitant la parallélisation.


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