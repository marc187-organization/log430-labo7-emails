"""
Kafka Historical User Event Consumer (Event Sourcing)
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from logger import Logger
from typing import Optional
from kafka import KafkaConsumer
from handlers.handler_registry import HandlerRegistry

class UserEventHistoryConsumer:
    """A consumer that starts reading Kafka events from the earliest point from a given topic"""

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        registry: HandlerRegistry
    ):

        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.registry = registry
        self.auto_offset_reset = "earliest"
        self.consumer: Optional[KafkaConsumer] = None
        self.logger = Logger.get_instance("UserEventHistoryConsumer")

    def start(self) -> None:
        """Start consuming messages from Kafka"""
        self.logger.info(f"Démarrer un consommateur : {self.group_id}")

        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=self.auto_offset_reset,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True
        )

        try:
            events = []

            for message in self.consumer:
                event = message.value
                events.append(event)

            with open("output/user_events_history.json", "w", encoding="utf-8") as f:
                json.dump(events, f, ensure_ascii=False, indent=4)

            self.logger.info(f"Fichier JSON généré avec {len(events)} événements → output/user_events_history.json")

        except Exception as e:
            self.logger.error(f"Erreur: {e}", exc_info=True)
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the consumer gracefully"""
        if self.consumer:
            self.consumer.close()
            self.logger.info("Arrêter le consommateur!")