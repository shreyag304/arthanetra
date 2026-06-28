import client from "./client";

export async function login(mobile) {
  const response = await client.post("/auth/login", {
    mobile,
  });

  return response.data;
}