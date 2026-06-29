function LanguageSelector({ language, setLanguage }) {
  const languages = [
    "English",
    "Hindi",
    "Marathi",
    "Gujarati",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Punjabi",
    "Odia",
    "Assamese",
  ];

  return (
    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className="border rounded-lg px-3 py-2 text-sm outline-none"
    >
      {languages.map((lang) => (
        <option key={lang} value={lang}>
          {lang}
        </option>
      ))}
    </select>
  );
}

export default LanguageSelector;