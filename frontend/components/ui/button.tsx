"use client";

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = '', variant = 'primary', size = 'md', children, ...props }, ref) => {
    const baseClasses = 'rounded-full font-bold transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
    
    const variantClasses = {
      primary: 'bg-[#1CAC78] text-white hover:bg-[#15936B] focus:ring-[#1CAC78] shadow-lg hover:shadow-xl',
      secondary: 'bg-[#F0FFF4] text-[#1CAC78] hover:bg-[#E6FFFA] focus:ring-[#1CAC78] border-2 border-[#1CAC78]/20',
      outline: 'border-2 border-[#1CAC78] text-[#1CAC78] hover:bg-[#F0FFF4] focus:ring-[#1CAC78]',
    };

    const sizeClasses = {
      sm: 'px-4 py-2 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
    };

    return (
      <button
        ref={ref}
        className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
