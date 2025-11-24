"use client";

import { motion } from "framer-motion";

interface BeverageVisualizerProps {
  drinkType: string;
  size: string;
  milk?: string;
  extras?: string[];
}

export default function BeverageVisualizer({ 
  drinkType, 
  size, 
  milk, 
  extras = [] 
}: BeverageVisualizerProps) {
  // Size mapping
  const sizeMap = {
    small: { height: 120, width: 80 },
    medium: { height: 160, width: 100 },
    large: { height: 200, width: 120 },
    venti: { height: 200, width: 120 },
  };

  const cupSize = sizeMap[size?.toLowerCase() as keyof typeof sizeMap] || sizeMap.medium;

  // Drink color based on type
  const drinkColors: Record<string, string> = {
    latte: "#d7a877",
    cappuccino: "#c19564",
    espresso: "#4a2c2a",
    americano: "#3d2317",
    mocha: "#6b4423",
    "flat white": "#e8c9a5",
    macchiato: "#d4a574",
    cortado: "#c89968",
    coffee: "#6f4e37",
  };

  const drinkColor = drinkColors[drinkType?.toLowerCase()] || "#8b7355";
  const hasWhippedCream = extras.some(e => e.toLowerCase().includes("whipped") || e.toLowerCase().includes("cream"));
  const hasSyrup = extras.some(e => e.toLowerCase().includes("vanilla") || e.toLowerCase().includes("caramel") || e.toLowerCase().includes("hazelnut"));

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="relative"
        style={{ width: cupSize.width + 40, height: cupSize.height + 60 }}
      >
        {/* Cup */}
        <svg
          width={cupSize.width + 40}
          height={cupSize.height + 40}
          viewBox={`0 0 ${cupSize.width + 40} ${cupSize.height + 40}`}
          className="drop-shadow-xl"
        >
          {/* Cup body */}
          <defs>
            <linearGradient id="cupGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#f5f5f5" />
              <stop offset="100%" stopColor="#e0e0e0" />
            </linearGradient>
            <linearGradient id="drinkGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={drinkColor} stopOpacity="0.9" />
              <stop offset="100%" stopColor={drinkColor} />
            </linearGradient>
          </defs>

          {/* Cup outline (tapered) */}
          <path
            d={`M ${20} ${30} 
                L ${15} ${cupSize.height + 20} 
                Q ${15} ${cupSize.height + 25} ${20} ${cupSize.height + 25}
                L ${cupSize.width + 20} ${cupSize.height + 25}
                Q ${cupSize.width + 25} ${cupSize.height + 25} ${cupSize.width + 25} ${cupSize.height + 20}
                L ${cupSize.width + 20} ${30}
                Z`}
            fill="url(#cupGradient)"
            stroke="#00704A"
            strokeWidth="3"
          />

          {/* Drink fill */}
          <path
            d={`M ${20} ${40} 
                L ${16} ${cupSize.height + 15} 
                L ${cupSize.width + 24} ${cupSize.height + 15}
                L ${cupSize.width + 20} ${40}
                Z`}
            fill="url(#drinkGradient)"
          />

          {/* Foam/Milk layer */}
          {milk && (
            <ellipse
              cx={(cupSize.width + 40) / 2}
              cy={45}
              rx={cupSize.width / 2.5}
              ry={8}
              fill="#f9f6f0"
              opacity="0.8"
            />
          )}

          {/* Whipped cream */}
          {hasWhippedCream && (
            <>
              <ellipse
                cx={(cupSize.width + 40) / 2}
                cy={30}
                rx={cupSize.width / 2.2}
                ry={12}
                fill="#fffef9"
                stroke="#f5f5dc"
                strokeWidth="1"
              />
              <ellipse
                cx={(cupSize.width + 40) / 2 - 10}
                cy={25}
                rx={15}
                ry={10}
                fill="#fffef9"
              />
              <ellipse
                cx={(cupSize.width + 40) / 2 + 10}
                cy={25}
                rx={15}
                ry={10}
                fill="#fffef9"
              />
              <ellipse
                cx={(cupSize.width + 40) / 2}
                cy={20}
                rx={12}
                ry={8}
                fill="#fffef9"
              />
            </>
          )}

          {/* Starbucks logo on cup */}
          <circle
            cx={(cupSize.width + 40) / 2}
            cy={cupSize.height / 2}
            r="18"
            fill="#00704A"
          />
          <circle
            cx={(cupSize.width + 40) / 2}
            cy={cupSize.height / 2}
            r="14"
            fill="white"
          />
        </svg>

        {/* Syrup drizzle indicator */}
        {hasSyrup && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.5, 0.8, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute top-8 left-1/2 -translate-x-1/2 text-xs font-semibold text-amber-600"
          >
            ✨ {extras.find(e => e.toLowerCase().includes("vanilla") || e.toLowerCase().includes("caramel") || e.toLowerCase().includes("hazelnut"))}
          </motion.div>
        )}
      </motion.div>

      {/* Drink details */}
      <div className="text-center">
        <h3 className="text-2xl font-bold text-[#00704A] capitalize">{drinkType}</h3>
        <p className="text-gray-600 capitalize">{size} | {milk || "Regular"} Milk</p>
        {extras.length > 0 && (
          <p className="text-sm text-gray-500 mt-1">+ {extras.join(", ")}</p>
        )}
      </div>
    </div>
  );
}
