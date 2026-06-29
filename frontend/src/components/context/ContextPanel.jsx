import HealthScore from "./HealthScore";
import PersonaCard from "./PersonaCard";
import SchemeCard from "./SchemeCard";
import GoalCard from "./GoalCard";

function ContextPanel({ context }) {
  return (
    <div className="h-full bg-white p-6 overflow-y-auto">

      <h2 className="text-xl font-bold mb-6">
        Live AI Context
      </h2>

      <HealthScore
        score={context.financial_health_score}
      />

      <PersonaCard
        persona={context.persona}
      />

      <SchemeCard
        schemes={context.eligible_schemes}
      />

      <GoalCard
        goal={context.goal}
      />

    </div>
  );
}

export default ContextPanel;