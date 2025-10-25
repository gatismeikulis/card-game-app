interface HiddenCardProps {
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function HiddenCard({ className = "", size = "sm" }: HiddenCardProps) {
  const sizeClasses = {
    sm: "w-3 h-4.5 sm:w-4 sm:h-6",
    md: "w-4 h-6 sm:w-6 sm:h-8",
    lg: "w-6 h-9 sm:w-8 sm:h-12",
  };

  return (
    <div
      className={`
        ${sizeClasses[size]}
        bg-blue-600 border border-blue-800 rounded
        flex items-center justify-center text-white font-bold text-[8px] sm:text-xs
        shadow-sm
        ${className}
      `}
    >
      ?
    </div>
  );
}
