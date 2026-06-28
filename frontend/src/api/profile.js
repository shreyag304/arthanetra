import client from "./client";

export async function getProfile() {
  const response = await client.get("/profile");

  return response.data;
}