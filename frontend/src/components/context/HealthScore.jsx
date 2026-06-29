function HealthScore({ score }) {
  return (
    <div className="border rounded-xl p-4 mb-4">

      <h3 className="font-semibold">
        Financial Health Score
      </h3>

      <p className="text-3xl font-bold text-blue-600 mt-2">
        {score}
      </p>

    </div>
  );
}

export default HealthScore;