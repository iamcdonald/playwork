# Debezium Playground

---

## Outline
A Postgres DB with Debezium tracking changes into a Kafka topic.

Python server fronted by Pushpin allowing create, get, list of entries as well as
listening to changes.

Listening to changes uses Pushpin to setup a long lived connection.
A background task is publishing changes from the Kafka topic to the same Pushpin channel allowing Server Side Events.

### Start Stack
```docker compose up```

- creates postgres, kafka, debezium connect, python and pushpin services
- uses flyway to prep the postgres instance (add a table)
- creates instance of a postgres debezium connector

### Usage
_Create Thing_
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"a thing"}' \
  http://localhost:8000/things
```
_Get Thing_
```
> curl localhost:8000/things/:id
```
_List Things_
```
> curl localhost:8000/things
```
_Listen to Thing changes_
```
> curl localhost:8000/things/listen
```

## Debugging
#### **Kafka**
_Check topics:_

```
> docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092
```

_Watch topic:_

```
> docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic pg_conn.public.things --from-beginning
```

#### **Posgres**
_Open psql:_

```
> docker compose exec postgres psql -U demo -h postgres -d db
```

_Run statement:_

```
> docker compose exec postgres psql -U demo -h postgres -d db -c "..."
```

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
