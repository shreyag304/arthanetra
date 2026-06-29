export async function sendMessage(payload) {
  return new Promise((resolve) => {
    setTimeout(() => {

      const message = payload.message.toLowerCase();

      let reply =
        "I'm here to help you with your financial questions.";

      let context = {
        financial_health_score: 72,
        persona: "Student",
        income_type: "Student",
        language: "English",
        goal: "Increase Savings",
        eligible_schemes: ["PM Scholarship"]
      };

      if (message.includes("loan") || message.includes("scam")) {
        reply =
          "This loan appears risky. Please verify if the lender is RBI registered before proceeding.";
      }

      else if (message.includes("budget") || message.includes("save")) {
        reply =
          "Let's create a monthly budget. First, tell me your monthly income.";
      }

      else if (message.includes("scheme")) {
        reply =
          "Based on your profile, you may be eligible for PM-KISAN and PM Jan Dhan Yojana.";

        context.eligible_schemes = [
          "PM-KISAN",
          "PM Jan Dhan Yojana"
        ];
      }

      else if (message.includes("health score")) {
        reply =
          "Your Financial Health Score is currently 72. Increasing savings and reducing debt can improve it.";
      }

      resolve({
        reply,
        context
      });

    }, 1200);
  });
}