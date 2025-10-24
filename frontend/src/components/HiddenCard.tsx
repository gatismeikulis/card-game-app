interface HiddenCardProps {
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function HiddenCard({ className = "", size = "sm" }: HiddenCardProps) {
  const sizeClasses = {
    sm: "w-4 h-6",
    md: "w-6 h-8",
    lg: "w-8 h-12",
  };

  return (
    <div
      className={`
        ${sizeClasses[size]}
        bg-blue-600 border border-blue-800 rounded
        flex items-center justify-center text-white font-bold text-xs
        shadow-sm
        ${className}
      `}
    >
      ?
    </div>
  );
}
