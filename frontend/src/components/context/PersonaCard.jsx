function PersonaCard({ persona }) {
  return (
    <div className="border rounded-xl p-4 mb-4">

      <h3 className="font-semibold">
        Persona
      </h3>

      <p className="mt-2">
        {persona}
      </p>

    </div>
  );
}

export default PersonaCard;