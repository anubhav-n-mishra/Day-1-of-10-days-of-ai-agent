"use client";

import { motion } from "framer-motion";
import { Coffee } from "lucide-react";

interface CoffeeFoamVisualizerProps {
  isActive?: boolean;
}

export default function CoffeeFoamVisualizer({ isActive = false }: CoffeeFoamVisualizerProps) {
  return (
    <div className="flex flex-col items-center gap-8">
      {/* Starbucks-style Coffee Cup Icon */}
      <motion.div
        className="relative"
        animate={isActive ? { scale: [1, 1.08, 1] } : {}}
        transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
      >
        <div className="relative w-40 h-40 bg-gradient-to-br from-white to-[#f9f9f9] rounded-3xl shadow-[0_10px_40px_rgba(0,112,74,0.15)] border-[5px] border-[#00704A] flex items-center justify-center">
          {/* Coffee Icon */}
          <Coffee className="w-20 h-20 text-[#00704A]" strokeWidth={2.5} />
          
          {/* Active Indicator */}
          {isActive && (
            <>
              <motion.div
                className="absolute inset-0 rounded-3xl bg-gradient-to-br from-[#00704A]/10 to-[#00a862]/5"
                animate={{ opacity: [0.2, 0.5, 0.2] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              />
              
              {/* Pulse rings */}
              <motion.div
                className="absolute -inset-3 rounded-3xl border-[3px] border-[#00704A]"
                animate={{ scale: [1, 1.3, 1], opacity: [0.6, 0, 0.6] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <motion.div
                className="absolute -inset-3 rounded-3xl border-[3px] border-[#00a862]"
                animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0, 0.4] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
              />
              
              {/* Steam particles */}
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute top-2 w-3 h-3 bg-gradient-to-t from-[#00704A] to-transparent rounded-full"
                  style={{ left: `${25 + i * 12}%` }}
                  animate={{
                    y: [0, -50],
                    opacity: [0.5, 0],
                    scale: [1, 0.3],
                  }}
                  transition={{
                    duration: 1.8,
                    delay: i * 0.25,
                    repeat: Infinity,
                    ease: "easeOut",
                  }}
                />
              ))}
            </>
          )}
        </div>
        
        {/* Starbucks-style circular badge */}
        <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 bg-[#00704A] text-white px-6 py-2 rounded-full text-xs font-bold uppercase tracking-wider shadow-lg">
          AI Barista
        </div>
      </motion.div>
      
      {/* Order status text */}
      {isActive && (
        <motion.div
          className="flex items-center gap-3 bg-[#f1f8f5] px-6 py-3 rounded-full border-2 border-[#00704A]/20"
          animate={{ opacity: [0.8, 1, 0.8] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <div className="w-2 h-2 bg-[#00704A] rounded-full animate-pulse" />
          <p className="text-base font-semibold text-[#00704A]">
            Listening to your order...
          </p>
        </motion.div>
      )}
    </div>
  );
}
