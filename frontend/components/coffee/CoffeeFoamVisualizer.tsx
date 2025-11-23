"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface Bubble {
  id: number;
  x: number;
  size: number;
  delay: number;
  duration: number;
}

interface CoffeeFoamVisualizerProps {
  isActive?: boolean;
}

export default function CoffeeFoamVisualizer({ isActive = false }: CoffeeFoamVisualizerProps) {
  const [bubbles, setBubbles] = useState<Bubble[]>([]);

  useEffect(() => {
    const newBubbles = Array.from({ length: 12 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      size: Math.random() * 20 + 10,
      delay: Math.random() * 2,
      duration: Math.random() * 3 + 3,
    }));
    setBubbles(newBubbles);
  }, []);

  return (
    <div className="relative w-full max-w-md mx-auto h-64 rounded-2xl overflow-hidden bg-gradient-to-b from-[var(--color-coffee-light)] to-[var(--color-coffee-dark)] shadow-2xl">
      {/* Coffee Cup Container */}
      <div className="absolute inset-0 flex items-end justify-center">
        {/* Coffee Surface */}
        <motion.div
          className="w-full h-3/4 bg-gradient-to-t from-[var(--color-coffee-dark)] via-[var(--color-beans)] to-[var(--color-coffee-light)] relative"
          animate={isActive ? { height: "85%" } : { height: "75%" }}
          transition={{ duration: 1, ease: "easeInOut" }}
        >
          {/* Foam Layer */}
          <div className="absolute top-0 left-0 right-0 h-16 bg-gradient-to-b from-[var(--color-foam)] to-transparent opacity-80" />

          {/* Animated Bubbles */}
          {bubbles.map((bubble) => (
            <motion.div
              key={bubble.id}
              className="absolute bottom-0 rounded-full bg-[var(--color-foam)] opacity-60"
              style={{
                left: `${bubble.x}%`,
                width: `${bubble.size}px`,
                height: `${bubble.size}px`,
              }}
              animate={
                isActive
                  ? {
                      y: [-20, -150, -250],
                      opacity: [0.6, 0.4, 0],
                      scale: [1, 1.2, 0.8],
                    }
                  : {
                      y: [-10, -50],
                      opacity: [0.3, 0],
                    }
              }
              transition={{
                duration: bubble.duration,
                delay: bubble.delay,
                repeat: Infinity,
                ease: "easeOut",
              }}
            />
          ))}

          {/* Steam Effect when active */}
          {isActive && (
            <>
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={`steam-${i}`}
                  className="absolute top-0 w-1 h-12 bg-gradient-to-t from-white/40 to-transparent blur-sm"
                  style={{ left: `${20 + i * 15}%` }}
                  animate={{
                    y: [-20, -80],
                    opacity: [0.5, 0],
                    x: [0, Math.random() * 20 - 10],
                  }}
                  transition={{
                    duration: 2 + Math.random(),
                    delay: i * 0.3,
                    repeat: Infinity,
                    ease: "easeOut",
                  }}
                />
              ))}
            </>
          )}
        </motion.div>
      </div>

      {/* Cup Handle */}
      <div className="absolute right-4 top-1/2 w-12 h-16 border-4 border-[var(--color-coffee-light)] rounded-r-full opacity-60" />

      {/* Active Pulse Effect */}
      {isActive && (
        <motion.div
          className="absolute inset-0 border-4 border-[var(--color-caramel)] rounded-2xl"
          animate={{ opacity: [0.5, 0.8, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      )}
    </div>
  );
}
