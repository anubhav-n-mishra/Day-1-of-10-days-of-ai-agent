"use client";

import { Coffee, Mic, Clock } from "lucide-react";
import { motion } from "framer-motion";

interface BaristaStatusProps {
  status: "idle" | "listening" | "brewing";
}

export default function BaristaStatus({ status }: BaristaStatusProps) {
  const statusConfig = {
    idle: {
      icon: Clock,
      text: "Ready to take your order",
      color: "text-[var(--color-coffee-light)]",
      bgColor: "bg-[var(--color-coffee-light)]/10",
    },
    listening: {
      icon: Mic,
      text: "Listening to your order",
      color: "text-[var(--color-matcha)]",
      bgColor: "bg-[var(--color-matcha)]/10",
    },
    brewing: {
      icon: Coffee,
      text: "Brewing your perfect cup",
      color: "text-[var(--color-caramel)]",
      bgColor: "bg-[var(--color-caramel)]/10",
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-center gap-3 px-6 py-3 rounded-full ${config.bgColor} border border-current/20`}
    >
      <motion.div
        animate={status === "listening" ? { scale: [1, 1.2, 1] } : {}}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        <Icon className={`w-5 h-5 ${config.color}`} />
      </motion.div>
      <span className={`font-medium ${config.color}`}>{config.text}</span>
      {status === "listening" && (
        <motion.div
          className={`w-2 h-2 rounded-full ${config.color.replace("text-", "bg-")}`}
          animate={{ opacity: [1, 0.3, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      )}
    </motion.div>
  );
}
