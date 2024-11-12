import { Kafka } from "kafkajs";

const kafka = new Kafka({
  clientId: "hospital.hospital.patients",
  brokers: ["kafka:9092"],
});

const consumer = kafka.consumer({
  groupId: "consumer-group",
});

await consumer.connect();

await consumer.run({
  eachMessage: async ({ topic, partition, message, heartbeat, pause }) => {
    console.log({
      key: message.key?.toString(),
      value: message.value?.toString(),
      headers: message.headers,
    });
  },
});
