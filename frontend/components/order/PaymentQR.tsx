"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface PaymentQRProps {
  amount: number;
  orderNumber: string;
}

export default function PaymentQR({ amount, orderNumber }: PaymentQRProps) {
  const [qrGenerated, setQrGenerated] = useState(false);

  useEffect(() => {
    setTimeout(() => setQrGenerated(true), 500);
  }, []);

  // Generate a simple QR-like pattern (for demo purposes)
  // In production, use a real QR code library like qrcode.react
  const generateQRPattern = () => {
    const size = 15;
    const pattern = [];
    
    for (let i = 0; i < size; i++) {
      const row = [];
      for (let j = 0; j < size; j++) {
        // Create a pseudo-random pattern based on order number and position
        const seed = (i * j + orderNumber.charCodeAt(0)) % 3;
        row.push(seed !== 0);
      }
      pattern.push(row);
    }
    return pattern;
  };

  const qrPattern = generateQRPattern();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, type: "spring" }}
      className="w-full max-w-md mx-auto bg-white rounded-2xl shadow-2xl p-8 border-2 border-[#00704A]"
    >
      {/* Header */}
      <div className="text-center mb-6">
        <motion.div
          initial={{ rotate: 0 }}
          animate={{ rotate: qrGenerated ? 360 : 0 }}
          transition={{ duration: 1 }}
        >
          <svg width="60" height="60" viewBox="0 0 60 60" className="mx-auto mb-3">
            <circle cx="30" cy="30" r="28" fill="#00704A" />
            <circle cx="30" cy="30" r="24" fill="white" />
            <path d="M25 25 L25 35 L35 35 L35 25 Z M28 28 L28 32 L32 32 L32 28 Z" fill="#00704A" />
          </svg>
        </motion.div>
        <h2 className="text-2xl font-bold text-[#00704A]">Scan to Pay</h2>
        <p className="text-gray-600 mt-1">Complete your order</p>
      </div>

      {/* QR Code */}
      <div className="bg-white p-6 rounded-xl border-4 border-[#00704A] mb-6">
        <div className="aspect-square bg-white p-4 rounded-lg">
          <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(15, 1fr)` }}>
            {qrPattern.map((row, i) =>
              row.map((cell, j) => (
                <motion.div
                  key={`${i}-${j}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: (i + j) * 0.01 }}
                  className={`aspect-square rounded-sm ${
                    cell ? "bg-[#00704A]" : "bg-white"
                  }`}
                />
              ))
            )}
          </div>
        </div>
      </div>

      {/* Payment details */}
      <div className="bg-[#f1f8f5] rounded-lg p-4 mb-4">
        <div className="flex justify-between items-center mb-2">
          <p className="text-gray-600">Order Number</p>
          <p className="font-mono font-bold text-[#00704A]">{orderNumber}</p>
        </div>
        <div className="flex justify-between items-center">
          <p className="text-gray-600">Amount to Pay</p>
          <p className="text-2xl font-bold text-[#00704A]">${amount.toFixed(2)}</p>
        </div>
      </div>

      {/* Payment methods */}
      <div className="space-y-2 mb-4">
        <p className="text-sm text-gray-600 text-center mb-3">Accepted Payment Methods</p>
        <div className="flex justify-center gap-4">
          {["UPI", "PayPal", "GPay", "Apple Pay"].map((method) => (
            <div
              key={method}
              className="bg-white border-2 border-gray-200 rounded-lg px-3 py-2 text-xs font-semibold text-gray-700"
            >
              {method}
            </div>
          ))}
        </div>
      </div>

      {/* Instructions */}
      <div className="text-center text-sm text-gray-500 space-y-1">
        <p>1. Open your payment app</p>
        <p>2. Scan the QR code above</p>
        <p>3. Complete the payment</p>
      </div>

      {/* Processing indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: [0, 1, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="mt-6 text-center"
      >
        <div className="inline-flex items-center gap-2 text-sm text-[#00704A]">
          <div className="w-2 h-2 bg-[#00704A] rounded-full animate-pulse" />
          <span>Waiting for payment...</span>
        </div>
      </motion.div>
    </motion.div>
  );
}
