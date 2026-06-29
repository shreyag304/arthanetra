import client from "./client";

export async function sendMessage(message) {
  const response = await client.post("/chat", {
    message,
  });

  return response.data;
}