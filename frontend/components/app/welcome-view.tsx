import { Button } from '@/components/ui/button';
import { ShoppingCart, Mic, Search, Package, Star, Truck, CreditCard } from 'lucide-react';

function ShopVoiceLogo() {
  return (
    <div className="flex items-center justify-center mb-8" role="img" aria-label="ShopVoice Logo">
      <div className="bg-[#FF9900] rounded-xl p-5 shadow-2xl" style={{ boxShadow: '0 0 30px rgba(255, 153, 0, 0.5)' }}>
        <ShoppingCart className="w-14 h-14 text-[#131921]" strokeWidth={2.5} aria-hidden="true" />
      </div>
      <div className="ml-5 flex flex-col items-start">
        <span className="text-4xl font-black text-white tracking-wide">Shop</span>
        <span className="text-4xl font-black text-[#FF9900] tracking-wide" style={{ textShadow: '0 0 20px rgba(255, 153, 0, 0.6)' }}>Voice</span>
      </div>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <main 
        className="bg-[#131921] flex flex-col items-center justify-center text-center px-6 min-h-screen"
        role="main"
        aria-label="ShopVoice - Voice Shopping Assistant - Welcome Page"
      >
        {/* Skip to main content link for screen readers */}
        <a href="#start-shopping" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:bg-[#FF9900] focus:text-[#131921] focus:p-4 focus:rounded-lg focus:z-50">
          Skip to Start Shopping
        </a>

        {/* ShopVoice Logo */}
        <ShopVoiceLogo />

        {/* ACP Badge */}
        <div className="mb-6 px-5 py-2.5 bg-[#232f3e] rounded-lg border-2 border-[#FF9900]" role="status">
          <p className="text-[#FF9900] text-base font-bold flex items-center gap-2">
            <Mic className="w-5 h-5" aria-hidden="true" />
            <span>Voice-Powered Shopping • ACP Enabled</span>
          </p>
        </div>

        {/* Main heading */}
        <h1 className="text-5xl md:text-6xl font-black text-white mb-4 tracking-tight leading-tight shop-text">
          Voice Shopping
        </h1>
        
        <p className="text-[#FF9900] max-w-lg text-xl md:text-2xl mb-4 font-bold">
          Meet Aria, Your Shopping Assistant
        </p>
        
        <p className="text-[#a0a0a0] max-w-xl text-lg mb-10 leading-relaxed">
          Browse products, compare prices, and place orders hands-free. Just speak naturally and Aria will help you find exactly what you need!
        </p>

        {/* Feature Cards - E-commerce theme */}
        <div 
          className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-10 w-full max-w-4xl"
          role="list"
          aria-label="Shopping Features"
        >
          <article 
            className="bg-[#232f3e] p-6 rounded-xl shadow-md border-2 border-[#FF9900]/30 hover:border-[#FF9900] transition-all focus-within:ring-4 focus-within:ring-[#FF9900]/50"
            role="listitem"
            tabIndex={0}
            aria-label="Smart Search - Find products by voice"
          >
            <div className="bg-[#FF9900] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Search className="w-7 h-7 text-[#131921]" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Smart Search</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              "Show me earbuds under ₹3000"
            </p>
          </article>

          <article 
            className="bg-[#232f3e] p-6 rounded-xl shadow-md border-2 border-[#FF9900]/30 hover:border-[#FF9900] transition-all focus-within:ring-4 focus-within:ring-[#FF9900]/50"
            role="listitem"
            tabIndex={0}
            aria-label="Easy Ordering - Buy with your voice"
          >
            <div className="bg-[#FF9900] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Package className="w-7 h-7 text-[#131921]" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Easy Ordering</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              "Buy the second one, size medium"
            </p>
          </article>

          <article 
            className="bg-[#232f3e] p-6 rounded-xl shadow-md border-2 border-[#FF9900]/30 hover:border-[#FF9900] transition-all focus-within:ring-4 focus-within:ring-[#FF9900]/50"
            role="listitem"
            tabIndex={0}
            aria-label="Order Tracking - Check your purchases"
          >
            <div className="bg-[#FF9900] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Truck className="w-7 h-7 text-[#131921]" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Order Tracking</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              "What did I just order?"
            </p>
          </article>
        </div>

        {/* Large, accessible CTA Button */}
        <Button
          id="start-shopping"
          onClick={onStartCall}
          className="bg-[#FF9900] hover:bg-[#FEBD69] text-[#131921] text-xl font-bold px-12 py-7 rounded-xl shadow-xl hover:shadow-2xl transition-all duration-200 focus:ring-4 focus:ring-[#FF9900]/50 focus:outline-none min-h-[70px] uppercase tracking-wider"
          aria-label="Start shopping with Aria, your voice assistant"
        >
          <Mic className="w-7 h-7 mr-3" aria-hidden="true" />
          {startButtonText}
        </Button>

        {/* Trust badges */}
        <div className="mt-6 flex items-center gap-6 text-[#a0a0a0] text-sm" role="note">
          <span className="flex items-center gap-1">
            <Star className="w-4 h-4 text-[#FF9900]" aria-hidden="true" />
            <span>14+ Products</span>
          </span>
          <span className="flex items-center gap-1">
            <CreditCard className="w-4 h-4 text-[#FF9900]" aria-hidden="true" />
            <span>Secure Orders</span>
          </span>
          <span className="flex items-center gap-1">
            <Truck className="w-4 h-4 text-[#FF9900]" aria-hidden="true" />
            <span>Fast Delivery</span>
          </span>
        </div>

        {/* Instructions box - E-commerce style */}
        <div 
          className="mt-8 bg-[#232f3e] p-6 rounded-xl max-w-lg border-2 border-[#FF9900]/40"
          role="region"
          aria-label="Voice command examples"
        >
          <h3 className="font-bold text-[#FF9900] text-lg mb-2">🛒 Try saying:</h3>
          <p className="text-white text-base leading-relaxed">
            <strong className="text-[#FEBD69]">"Show me t-shirts"</strong> • <strong className="text-[#FEBD69]">"I want black hoodies"</strong> • <strong className="text-[#FEBD69]">"Buy the first one"</strong> • <strong className="text-[#FEBD69]">"What's my last order?"</strong>
          </p>
        </div>
      </main>
    </div>
  );
};
