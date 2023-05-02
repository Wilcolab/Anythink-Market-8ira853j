// Init the Redis client
const { createClient } = require("redis");

const client = createClient({
  url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`,
});

client.on("error", (err) => {
  console.log("Error " + err);
});

const initRedis = async () => {
  await client.connect();
};

module.exports = {
  initRedis,
};
