export default function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white/90 backdrop-blur-xl rounded-3xl border border-white/60 shadow-2xl shadow-indigo-950/5 p-8 sm:p-10 transition-all duration-300 ${className}`}
    >
      {children}
    </div>
  );
}
