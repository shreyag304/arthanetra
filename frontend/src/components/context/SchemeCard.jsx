function SchemeCard({ schemes }) {
  return (
    <div className="border rounded-xl p-4 mb-4">

      <h3 className="font-semibold">
        Eligible Schemes
      </h3>

      <ul className="mt-2 list-disc list-inside">
        {schemes.map((scheme) => (
          <li key={scheme}>
            {scheme}
          </li>
        ))}
      </ul>

    </div>
  );
}

export default SchemeCard;