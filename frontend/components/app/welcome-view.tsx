import { Button } from '@/components/ui/button';
import { Activity, Heart, TrendingUp, Sparkles } from 'lucide-react';

function HealthifyIcon() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="absolute w-32 h-32 bg-[#1CAC78] opacity-10 rounded-full animate-pulse"></div>
      <div className="relative bg-linear-to-br from-[#1CAC78] to-[#15936B] p-6 rounded-3xl shadow-2xl">
        <Activity className="w-16 h-16 text-white" strokeWidth={2.5} />
      </div>
      <Heart className="w-6 h-6 text-[#FF6B6B] fill-[#FF6B6B] absolute -top-1 -right-1 animate-pulse" />
      <TrendingUp className="w-6 h-6 text-[#1CAC78] absolute -bottom-1 -left-1" />
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
      <section className="bg-linear-to-br from-[#F0FFF4] via-white to-[#E6FFFA] flex flex-col items-center justify-center text-center px-4 min-h-screen relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-[#1CAC78] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-[#FF6B6B] opacity-10 rounded-full blur-xl"></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-[#FFA500] opacity-10 rounded-full blur-xl"></div>

        <div className="mb-10 relative z-10">
          <HealthifyIcon />
        </div>

        {/* Badge */}
        <div className="mb-6 px-4 py-2 bg-white rounded-full shadow-md border border-[#1CAC78]/20">
          <p className="text-[#1CAC78] text-sm font-bold flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            AI-Powered Health Coaching
          </p>
        </div>

        <h1 className="text-6xl font-black text-[#1CAC78] mb-3 tracking-tight leading-tight">
          Your Daily<br />Health Check-In
        </h1>
        <p className="text-gray-700 max-w-md text-xl mb-2 font-semibold">
          Track your wellness journey with AI
        </p>
        <p className="text-gray-500 max-w-lg text-base mb-10 leading-relaxed">
          Start your day right with personalized wellness insights,<br />
          mood tracking, and goal setting - all through voice
        </p>

        {/* Stats/Features */}
        <div className="flex gap-6 mb-10">
          <div className="text-center">
            <div className="text-2xl font-bold text-[#1CAC78]">3-5 min</div>
            <div className="text-xs text-gray-500">Quick Check-in</div>
          </div>
          <div className="w-px bg-gray-300"></div>
          <div className="text-center">
            <div className="text-2xl font-bold text-[#1CAC78]">Daily</div>
            <div className="text-xs text-gray-500">Wellness Tracking</div>
          </div>
          <div className="w-px bg-gray-300"></div>
          <div className="text-center">
            <div className="text-2xl font-bold text-[#1CAC78]">AI Coach</div>
            <div className="text-xs text-gray-500">Personal Support</div>
          </div>
        </div>

        <Button 
          variant="primary" 
          size="lg" 
          onClick={onStartCall} 
          className="w-96 text-lg py-7 bg-linear-to-r from-[#1CAC78] to-[#15936B] hover:from-[#15936B] hover:to-[#127A59] text-white rounded-full font-bold shadow-2xl transition-all hover:scale-105 hover:shadow-[0_10px_40px_rgba(28,172,120,0.4)] uppercase tracking-wide relative overflow-hidden group"
        >
          <span className="relative z-10">{startButtonText}</span>
          <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity"></div>
        </Button>
        
        <div className="mt-8 flex items-center gap-2 text-sm text-gray-500">
          <div className="w-2 h-2 bg-[#1CAC78] rounded-full animate-pulse"></div>
          <span>Secure & Private</span>
          <span className="text-gray-300">•</span>
          <span>No Medical Advice</span>
          <span className="text-gray-300">•</span>
          <span>Supportive Only</span>
        </div>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center px-4">
        <p className="text-gray-400 max-w-2xl text-center text-xs leading-5 font-normal">
          💚 HealthifyMe AI Companion is a supportive wellness tool, not a substitute for professional medical or mental health care. For medical concerns, please consult a healthcare provider.
        </p>
      </div>
    </div>
  );
};
