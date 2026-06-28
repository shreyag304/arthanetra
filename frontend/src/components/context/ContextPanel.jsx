import HealthScore from "./HealthScore";
import PersonaCard from "./PersonaCard";
import SchemeCard from "./SchemeCard";
import GoalCard from "./GoalCard";

function ContextPanel() {

    return (

        <div className="h-full bg-white p-6 overflow-y-auto">

            <h2 className="text-xl font-bold mb-6">

                Live AI Context

            </h2>

            <HealthScore />

            <PersonaCard />

            <SchemeCard />

            <GoalCard />

        </div>

    );

}

export default ContextPanel;