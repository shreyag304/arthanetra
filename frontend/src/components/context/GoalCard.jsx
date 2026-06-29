function GoalCard({ goal }) {
  return (
    <div className="border rounded-xl p-4">

      <h3 className="font-semibold">
        Current Goal
      </h3>

      <p className="mt-2">
        {goal}
      </p>

    </div>
  );
}

export default GoalCard;