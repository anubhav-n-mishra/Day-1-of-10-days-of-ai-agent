"use client";

import { motion } from "framer-motion";
import { Coffee } from "lucide-react";

interface CoffeeFoamVisualizerProps {
  isActive?: boolean;
}

export default function CoffeeFoamVisualizer({ isActive = false }: CoffeeFoamVisualizerProps) {
  return (
    <div className="flex flex-col items-center gap-6">
      {/* Starbucks-style Coffee Cup Icon */}
      <motion.div
        className="relative"
        animate={isActive ? { scale: [1, 1.05, 1] } : {}}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="relative w-32 h-32 bg-white rounded-2xl shadow-2xl border-4 border-[#00704A] flex items-center justify-center">
          {/* Coffee Icon */}
          <Coffee className="w-16 h-16 text-[#00704A]" strokeWidth={2} />
          
          {/* Active Indicator */}
          {isActive && (
            <>
              <motion.div
                className="absolute inset-0 rounded-2xl bg-[#00704A]/10"
                animate={{ opacity: [0.1, 0.3, 0.1] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              
              {/* Pulse rings */}
              <motion.div
                className="absolute -inset-2 rounded-2xl border-2 border-[#00704A]"
                animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              
              {/* Steam particles */}
              {[...Array(3)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute top-0 w-2 h-2 bg-[#00704A] rounded-full opacity-30"
                  style={{ left: `${35 + i * 15}%` }}
                  animate={{
                    y: [0, -40],
                    opacity: [0.3, 0],
                    scale: [1, 0.5],
                  }}
                  transition={{
                    duration: 1.5,
                    delay: i * 0.3,
                    repeat: Infinity,
                    ease: "easeOut",
                  }}
                />
              ))}
            </>
          )}
        </div>
        
        {/* Cup sleeve decoration */}
        <div className="absolute inset-x-4 bottom-8 h-8 bg-[#00704A]/5 rounded-lg" />
      </motion.div>
      
      {/* Order status text */}
      <motion.p
        className="text-sm font-medium text-[#00704A]"
        animate={isActive ? { opacity: [0.7, 1, 0.7] } : {}}
        transition={{ duration: 2, repeat: Infinity }}
      >
        {isActive ? "🎤 Listening..." : "Ready for your order"}
      </motion.p>
    </div>
  );
}
