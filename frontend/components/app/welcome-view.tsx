import { Button } from '@/components/ui/button';
import { Shield, AlertTriangle, Lock, CheckCircle, Phone } from 'lucide-react';

function IDFCSecurityIcon() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute w-32 h-32 bg-[#9D2235] opacity-10 rounded-full animate-pulse"></div>
      <div className="relative bg-gradient-to-br from-[#9D2235] to-[#741A28] p-6 rounded-3xl shadow-2xl">
        <Shield className="w-16 h-16 text-white" strokeWidth={2.5} />
      </div>
      <AlertTriangle className="w-6 h-6 text-[#9D2235] absolute -top-1 -right-1 animate-pulse fill-[#9D2235]" />
      <Lock className="w-6 h-6 text-[#9D2235] fill-[#9D2235] absolute -bottom-1 -left-1" />
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
      <section className="bg-gradient-to-br from-[#FFF5F7] via-white to-[#FFE5E9] flex flex-col items-center justify-center text-center px-4 min-h-screen relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-[#9D2235] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-[#9D2235] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-[#741A28] opacity-10 rounded-full blur-xl"></div>

        <div className="mb-10 relative z-10">
          <IDFCSecurityIcon />
        </div>

        {/* Badge */}
        <div className="mb-6 px-4 py-2 bg-white rounded-full shadow-md border border-[#9D2235]/20">
          <p className="text-[#9D2235] text-sm font-bold flex items-center gap-2">
            <Shield className="w-4 h-4" />
            Fraud Prevention System
          </p>
        </div>

        <h1 className="text-7xl font-black text-[#1F1F1F] mb-4 tracking-tight leading-tight">
          IDFC Bank Security
        </h1>
        <p className="text-[#9D2235] max-w-md text-2xl mb-3 font-bold">
          Meet Aarav, Your Fraud Prevention Specialist
        </p>
        <p className="text-[#666666] max-w-2xl text-lg mb-10 leading-relaxed">
          Connect with our AI security specialist to verify suspicious transactions and protect your account from fraud.
        </p>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full max-w-4xl">
          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#9D2235] to-[#741A28] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Transaction Verification</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Verify suspicious transactions with our AI security specialist
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#9D2235] to-[#741A28] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Lock className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">Instant Card Protection</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Block fraudulent transactions immediately for your security
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10 hover:shadow-2xl hover:scale-105 transition-all duration-300">
            <div className="bg-gradient-to-br from-[#9D2235] to-[#741A28] w-12 h-12 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <CheckCircle className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">24/7 Fraud Monitoring</h3>
            <p className="text-[#666666] text-sm leading-relaxed">
              Round-the-clock protection for your peace of mind
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <Button
          onClick={onStartCall}
          className="bg-gradient-to-r from-[#9D2235] to-[#741A28] hover:from-[#741A28] hover:to-[#5A1420] text-white text-xl font-bold px-12 py-8 rounded-2xl shadow-2xl hover:shadow-[0_20px_50px_rgba(157,34,53,0.5)] transition-all duration-300 hover:scale-105"
        >
          <Phone className="w-6 h-6 mr-3" />
          {startButtonText}
        </Button>

        {/* Trust Badge */}
        <div className="mt-8 flex items-center gap-2 text-sm text-[#666666]">
          <Shield className="w-5 h-5 text-[#9D2235]" />
          <span>Trusted by millions of customers across India</span>
        </div>

        {/* Pro Tip */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm p-6 rounded-xl max-w-md border-2 border-[#9D2235]/20 shadow-lg">
          <p className="text-[#333333] text-sm leading-relaxed">
            <span className="font-bold text-[#9D2235]">🔒 Security Note:</span> Aarav will never ask for your full card number, PIN, CVV, or password. We only verify transactions using your security question.
          </p>
        </div>
      </section>
    </div>
  );
};
