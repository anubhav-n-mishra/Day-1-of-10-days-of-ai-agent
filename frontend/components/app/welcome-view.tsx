import { Button } from '@/components/ui/button';
import { ShoppingCart, Package, Zap, Clock, Sparkles, Mic } from 'lucide-react';

function ZeptoShoppingIcon() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute w-32 h-32 bg-[#8B5CF6] opacity-10 rounded-full animate-pulse"></div>
      <div className="relative bg-gradient-to-br from-[#8B5CF6] to-[#7C3AED] p-6 rounded-3xl shadow-2xl">
        <ShoppingCart className="w-16 h-16 text-white" strokeWidth={2.5} />
      </div>
      <Package className="w-6 h-6 text-[#8B5CF6] absolute -top-1 -right-1 animate-pulse fill-[#8B5CF6]" />
      <Zap className="w-6 h-6 text-[#8B5CF6] fill-[#8B5CF6] absolute -bottom-1 -left-1" />
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
      <section className="bg-gradient-to-br from-[#FAF5FF] via-white to-[#EDE9FE] flex flex-col items-center justify-center text-center px-4 min-h-screen relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-[#8B5CF6] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-[#8B5CF6] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-[#7C3AED] opacity-10 rounded-full blur-xl"></div>

        <div className="mb-10 relative z-10">
          <ZeptoShoppingIcon />
        </div>

        {/* Badge */}
        <div className="mb-6 px-4 py-2 bg-white rounded-full shadow-md border border-[#8B5CF6]/20">
          <p className="text-[#8B5CF6] text-sm font-bold flex items-center gap-2">
            <Zap className="w-4 h-4" />
            10-Minute Delivery
          </p>
        </div>

        <h1 className="text-7xl font-black text-[#1F1F1F] mb-4 tracking-tight leading-tight">
          Zepto Express
        </h1>
        <p className="text-[#8B5CF6] max-w-md text-2xl mb-3 font-bold">
          Meet Zara, Your Voice Shopping Assistant
        </p>
        <p className="text-[#666666] max-w-2xl text-lg mb-10 leading-relaxed">
          Shop for groceries, snacks, and essentials using just your voice. Add items, manage your cart, and place orders effortlessly!
        </p>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full max-w-4xl">
          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#8B5CF6]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#8B5CF6] to-[#7C3AED] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Lightning Fast</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Delivery in 10 minutes flat - faster than you can cook!
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#8B5CF6]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#8B5CF6] to-[#7C3AED] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Smart Suggestions</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Ask for "ingredients for pasta" and we'll add them all!
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#8B5CF6]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#8B5CF6] to-[#7C3AED] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Clock className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">24/7 Available</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Shop anytime, day or night - we're always open!
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <Button
          onClick={onStartCall}
          className="bg-gradient-to-r from-[#8B5CF6] to-[#7C3AED] hover:from-[#7C3AED] hover:to-[#6D28D9] text-white text-xl font-bold px-12 py-8 rounded-2xl shadow-2xl hover:shadow-[0_20px_50px_rgba(139,92,246,0.5)] transition-all duration-300 hover:scale-105"
        >
          <Mic className="w-6 h-6 mr-3" />
          {startButtonText}
        </Button>

        {/* Trust Badge */}
        <div className="mt-8 flex items-center gap-2 text-sm text-[#666666]">
          <ShoppingCart className="w-5 h-5 text-[#8B5CF6]" />
          <span>Join 10 million happy shoppers</span>
        </div>

        {/* Pro Tip */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm p-6 rounded-xl max-w-md border-2 border-[#8B5CF6]/20 shadow-lg">
          <p className="text-[#333333] text-sm leading-relaxed">
            <span className="font-bold text-[#8B5CF6]">💡 Pro Tip:</span> Try saying "I need ingredients for a sandwich" or "Add 2 bottles of milk" - Zara understands natural conversation!
          </p>
        </div>
      </section>
    </div>
  );
};
