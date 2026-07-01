import client from "./client";

export async function calculateFHS(file, currentLiquidBalance = 100000) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("current_liquid_balance", currentLiquidBalance);

  try {
    const response = await client.post("/fhs/calculate", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || "Failed to calculate FHS.";
    throw new Error(message, { cause: error });
  }
}
