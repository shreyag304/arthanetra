export default function Input({
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  icon: Icon,
  helperText,
  maxLength,
  disabled = false,
  className = "",
  name,
}) {
  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors">
          {label}
        </label>
      )}
      <div className="relative rounded-2xl shadow-sm">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
            <Icon className="w-5 h-5" />
          </div>
        )}
        <input
          name={name}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          maxLength={maxLength}
          disabled={disabled}
          className={`w-full rounded-2xl border bg-slate-50/50 py-3.5 ${
            Icon ? "pl-11" : "pl-4"
          } pr-4 text-slate-800 placeholder-slate-400 transition-all duration-200 focus:bg-white focus:outline-none focus:ring-4 ${
            error
              ? "border-rose-300 focus:border-rose-500 focus:ring-rose-500/20 text-rose-900 placeholder-rose-300"
              : "border-slate-200 focus:border-blue-500 focus:ring-blue-500/20 hover:border-slate-300"
          } disabled:bg-slate-100 disabled:text-slate-400`}
        />
      </div>
      {error && (
        <p className="mt-1.5 text-xs font-medium text-rose-500 flex items-center gap-1 animate-fadeIn">
          <span className="inline-block w-1 h-1 rounded-full bg-rose-500"></span>
          {error}
        </p>
      )}
      {!error && helperText && (
        <p className="mt-1.5 text-xs text-slate-500">{helperText}</p>
      )}
    </div>
  );
}
