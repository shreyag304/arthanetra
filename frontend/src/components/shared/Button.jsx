import Loader from "./Loader";

export default function Button({
  children,
  onClick,
  type = "button",
  variant = "primary",
  isLoading = false,
  disabled = false,
  className = "",
  icon: Icon = null,
}) {
  const baseStyles =
    "w-full relative inline-flex items-center justify-center gap-2.5 rounded-2xl font-semibold transition-all duration-300 py-4 px-6 focus:outline-none focus:ring-4 disabled:opacity-60 disabled:cursor-not-allowed transform active:scale-[0.98]";

  const variants = {
    primary:
      "bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-700 hover:to-indigo-800 text-white shadow-lg shadow-blue-600/30 hover:shadow-xl hover:shadow-blue-600/40 focus:ring-blue-500/30",
    secondary:
      "bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-200/80 focus:ring-slate-400/30",
    outline:
      "border-2 border-indigo-600/30 hover:border-indigo-600 text-indigo-700 hover:bg-indigo-50/50 focus:ring-indigo-500/20",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`${baseStyles} ${variants[variant] || variants.primary} ${className}`}
    >
      {isLoading ? (
        <>
          <Loader size="sm" />
          <span>Processing...</span>
        </>
      ) : (
        <>
          {Icon && <Icon className="w-5 h-5" />}
          <span>{children}</span>
        </>
      )}
    </button>
  );
}
