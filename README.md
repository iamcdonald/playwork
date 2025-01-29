## Debezium Playground

---

### Start Stack
```docker compose up```

- creates postgres, kafka, and debezium connect services
- uses flyway to prep the postgres instance (add a table)
- creates instance of a postgres debezium connector

### Kafka
Check topics:

```docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092```

Watch topic:

```docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic pg_conn.public.things --from-beginning```

### Posgres
Open psql:

```docker compose exec postgres psql -U demo -h postgres -d db```

Run statement:

```docker compose exec postgres psql -U demo -h postgres -d db -c "..."```

---

### _Notes_
I originally tried using a base postgres image but was obviously missing something in terms of:
  - user setup
  - roles
  - anything else needed to allow debezium to create a replication
    - one part being specifying to use `pgoutput` rather than relying on the `decoderbufs` plugin having been installed in postgres

Would like to duck back to that at some point and properly parse what's going on in the [debezium/postgres](https://github.com/debezium/container-images/tree/main/postgres/17-alpine) image.

Kafka now has KRaft for consensus (much like elasticsearch/mongo have internal mechanisms) so Ive set it up for that.
There are some obvious upsides (simplicity for one) but I haven't done a great deal of reading to see what the cons are vs using zookeeper
