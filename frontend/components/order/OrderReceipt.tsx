"use client";

import { motion } from "framer-motion";

interface OrderReceiptProps {
  order: {
    drinkType: string;
    size: string;
    milk: string;
    extras: string[];
    name: string;
  };
  orderNumber?: string;
  timestamp?: string;
}

export default function OrderReceipt({ order, orderNumber, timestamp }: OrderReceiptProps) {
  const prices: Record<string, number> = {
    small: 3.50,
    medium: 4.50,
    large: 5.50,
    venti: 5.50,
  };

  const basePrice = prices[order.size?.toLowerCase()] || 4.50;
  const extrasPrice = order.extras.length * 0.75;
  const subtotal = basePrice + extrasPrice;
  const tax = subtotal * 0.08;
  const total = subtotal + tax;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-md mx-auto bg-white rounded-lg shadow-2xl p-8 border-2 border-[#00704A]"
    >
      {/* Header */}
      <div className="text-center mb-6">
        <div className="flex justify-center mb-3">
          <svg width="60" height="60" viewBox="0 0 60 60">
            <circle cx="30" cy="30" r="28" fill="#00704A" />
            <circle cx="30" cy="30" r="24" fill="white" />
            <circle cx="30" cy="30" r="18" fill="#00704A" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-[#00704A]">Starbucks</h2>
        <p className="text-sm text-gray-600">Order Receipt</p>
        {orderNumber && (
          <p className="text-xs text-gray-500 mt-1">Order #{orderNumber}</p>
        )}
        {timestamp && (
          <p className="text-xs text-gray-400">{new Date(timestamp).toLocaleString()}</p>
        )}
      </div>

      <div className="border-t-2 border-dashed border-gray-300 my-4"></div>

      {/* Customer name */}
      <div className="mb-4 bg-[#f1f8f5] p-3 rounded-lg">
        <p className="text-sm text-gray-600">For</p>
        <p className="text-xl font-bold text-[#00704A] capitalize">{order.name}</p>
      </div>

      {/* Order details */}
      <div className="space-y-3 mb-4">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <p className="font-semibold text-gray-800 capitalize">{order.drinkType}</p>
            <p className="text-sm text-gray-600 capitalize">{order.size}</p>
            <p className="text-sm text-gray-600 capitalize">{order.milk} milk</p>
          </div>
          <p className="font-semibold text-gray-800">${basePrice.toFixed(2)}</p>
        </div>

        {order.extras.map((extra, index) => (
          <div key={index} className="flex justify-between items-center pl-4">
            <p className="text-sm text-gray-600 capitalize">+ {extra}</p>
            <p className="text-sm text-gray-600">$0.75</p>
          </div>
        ))}
      </div>

      <div className="border-t-2 border-dashed border-gray-300 my-4"></div>

      {/* Totals */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <p className="text-gray-600">Subtotal</p>
          <p className="text-gray-800">${subtotal.toFixed(2)}</p>
        </div>
        <div className="flex justify-between text-sm">
          <p className="text-gray-600">Tax (8%)</p>
          <p className="text-gray-800">${tax.toFixed(2)}</p>
        </div>
        <div className="border-t border-gray-300 my-2"></div>
        <div className="flex justify-between text-lg font-bold">
          <p className="text-[#00704A]">Total</p>
          <p className="text-[#00704A]">${total.toFixed(2)}</p>
        </div>
      </div>

      <div className="border-t-2 border-dashed border-gray-300 my-4"></div>

      {/* Footer */}
      <div className="text-center text-xs text-gray-500">
        <p>Thank you for choosing Starbucks!</p>
        <p className="mt-1">Your order will be ready shortly</p>
      </div>
    </motion.div>
  );
}
