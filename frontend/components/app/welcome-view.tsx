import { Button } from '@/components/ui/button';
import { CreditCard, Zap, Shield, TrendingUp, Sparkles, Phone } from 'lucide-react';

function RazorpayIcon() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute w-32 h-32 bg-[#3395FF] opacity-10 rounded-full animate-pulse"></div>
      <div className="relative bg-gradient-to-br from-[#3395FF] to-[#0066CC] p-6 rounded-3xl shadow-2xl">
        <CreditCard className="w-16 h-16 text-white" strokeWidth={2.5} />
      </div>
      <Zap className="w-6 h-6 text-[#3395FF] absolute -top-1 -right-1 animate-pulse fill-[#3395FF]" />
      <Shield className="w-6 h-6 text-[#00D632] fill-[#00D632] absolute -bottom-1 -left-1" />
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
      <section className="bg-gradient-to-br from-[#F0F7FF] via-white to-[#E6F4FF] flex flex-col items-center justify-center text-center px-4 min-h-screen relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-[#3395FF] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-[#3395FF] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-[#00D632] opacity-10 rounded-full blur-xl"></div>

        <div className="mb-10 relative z-10">
          <RazorpayIcon />
        </div>

        {/* Badge */}
        <div className="mb-6 px-4 py-2 bg-white rounded-full shadow-md border border-[#3395FF]/20">
          <p className="text-[#3395FF] text-sm font-bold flex items-center gap-2">
            <Phone className="w-4 h-4" />
            AI-Powered SDR
          </p>
        </div>

        <h1 className="text-7xl font-black text-[#1F1F1F] mb-4 tracking-tight leading-tight">
          Razorpay SDR
        </h1>
        <p className="text-[#3395FF] max-w-md text-2xl mb-3 font-bold">
          Meet Priya, Your Virtual Sales Representative
        </p>
        <p className="text-[#666666] max-w-2xl text-lg mb-10 leading-relaxed">
          Connect instantly with our AI sales representative to learn about Razorpay's payment solutions, 
          business banking, and more. Get answers to your questions and discover how we can help your business grow.
        </p>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full max-w-4xl">
          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#3395FF]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#3395FF] to-[#0066CC] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <CreditCard className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Payment Gateway</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Accept 100+ payment methods with instant settlements and 99.99% uptime
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#3395FF]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#3395FF] to-[#0066CC] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Business Banking</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Complete banking platform with payroll, vendor payments, and corporate cards
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#3395FF]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#3395FF] to-[#0066CC] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Instant Credit</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Get business loans up to ₹1 crore with minimal documentation
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <Button
          onClick={onStartCall}
          className="bg-gradient-to-r from-[#3395FF] to-[#0066CC] hover:from-[#0066CC] hover:to-[#004D99] text-white text-xl font-bold px-12 py-8 rounded-2xl shadow-2xl hover:shadow-[0_20px_50px_rgba(51,149,255,0.5)] transition-all duration-300 hover:scale-105"
        >
          <Phone className="w-6 h-6 mr-3" />
          {startButtonText}
        </Button>

        {/* Trust Badge */}
        <div className="mt-8 flex items-center gap-2 text-sm text-[#666666]">
          <Shield className="w-5 h-5 text-[#00D632]" />
          <span>Trusted by 10+ million businesses across India</span>
        </div>

        {/* Pro Tip */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm p-6 rounded-xl max-w-md border-2 border-[#3395FF]/20 shadow-lg">
          <p className="text-[#333333] text-sm leading-relaxed">
            <span className="font-bold text-[#3395FF]">💡 Pro tip:</span> Priya will ask you a few questions 
            to understand your business needs and recommend the best solutions for you.
          </p>
        </div>
      </section>
    </div>
  );
};
