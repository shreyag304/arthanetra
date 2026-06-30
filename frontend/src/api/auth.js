import client from "./client";

export async function login(mobile, password) {
  try {
    const response = await client.post("/auth/login", {
      mobile,
      password,
    });

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Login failed. Please try again.";
    throw new Error(message);
  }
}

export async function checkRegistration(mobile) {
  try {
    const response = await client.get("/auth/register", {
      params: { mobile },
    });

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Failed to check registration status.";
    throw new Error(message);
  }
}

export async function register(mobile, password, name = "User", email = null) {
  try {
    let finalName = name;
    let finalEmail = email;
    if (typeof name === "string" && name.includes("@") && !email) {
      finalEmail = name;
      finalName = "User";
    }
    const response = await client.post("/auth/register", {
      mobile,
      password,
      name: finalName || "User",
      ...(finalEmail && { email: finalEmail }),
    });

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Registration failed. Please try again.";
    throw new Error(message);
  }
}