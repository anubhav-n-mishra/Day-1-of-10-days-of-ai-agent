import { Button } from '@/components/ui/button';
import { Sword, Shield, Mic, Sparkles, Scroll, Skull, Crown, Dice6 } from 'lucide-react';

function EldoriaLogo() {
  return (
    <div className="flex items-center justify-center mb-8" role="img" aria-label="Realm of Eldoria Logo">
      <div className="bg-[#107C10] rounded-xl p-5 shadow-2xl" style={{ boxShadow: '0 0 30px rgba(16, 124, 16, 0.6)' }}>
        <Sword className="w-14 h-14 text-white" strokeWidth={2.5} aria-hidden="true" />
      </div>
      <div className="ml-5 flex flex-col items-start">
        <span className="text-3xl font-black text-[#9BDB4D] tracking-wide drop-shadow-lg">REALM OF</span>
        <span className="text-5xl font-black text-white tracking-widest" style={{ textShadow: '0 0 20px rgba(155, 219, 77, 0.8)' }}>ELDORIA</span>
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
        className="bg-[#0a0a0a] flex flex-col items-center justify-center text-center px-6 min-h-screen"
        role="main"
        aria-label="Realm of Eldoria - Voice D&D Adventure - Welcome Page"
      >
        {/* Skip to main content link for screen readers */}
        <a href="#start-quest" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:bg-[#107C10] focus:text-white focus:p-4 focus:rounded-lg focus:z-50">
          Skip to Begin Quest
        </a>

        {/* Eldoria Logo */}
        <EldoriaLogo />

        {/* D&D Style Badge */}
        <div className="mb-6 px-5 py-2.5 bg-[#1a3d1a] rounded-lg border-2 border-[#9BDB4D]" role="status">
          <p className="text-[#9BDB4D] text-base font-bold flex items-center gap-2">
            <Dice6 className="w-5 h-5" aria-hidden="true" />
            <span>Voice-Powered D&D Adventure</span>
          </p>
        </div>

        {/* Main heading - Large and epic */}
        <h1 className="text-5xl md:text-6xl font-black text-white mb-4 tracking-tight leading-tight game-text">
          Voice Adventure
        </h1>
        
        <p className="text-[#9BDB4D] max-w-lg text-xl md:text-2xl mb-4 font-bold">
          Meet Aldric, Your Dungeon Master
        </p>
        
        <p className="text-[#a0a0a0] max-w-xl text-lg mb-10 leading-relaxed">
          Embark on an epic quest using just your voice. Roll dice, battle monsters, collect treasures, and save the realm from the Shadow Dragon Malachar!
        </p>

        {/* Feature Cards - Dark fantasy theme */}
        <div 
          className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-10 w-full max-w-4xl"
          role="list"
          aria-label="Game Features"
        >
          <article 
            className="bg-[#1a1a1a] p-6 rounded-xl shadow-md border-2 border-[#107C10]/40 hover:border-[#9BDB4D] transition-all focus-within:ring-4 focus-within:ring-[#107C10]/50"
            role="listitem"
            tabIndex={0}
            aria-label="D20 Dice Rolling - Real skill checks with modifiers"
          >
            <div className="bg-[#107C10] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Dice6 className="w-7 h-7 text-white" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">D20 Dice Rolling</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              Real skill checks with attribute modifiers
            </p>
          </article>

          <article 
            className="bg-[#1a1a1a] p-6 rounded-xl shadow-md border-2 border-[#107C10]/40 hover:border-[#9BDB4D] transition-all focus-within:ring-4 focus-within:ring-[#107C10]/50"
            role="listitem"
            tabIndex={0}
            aria-label="Voice Commands - Speak naturally to play"
          >
            <div className="bg-[#107C10] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Mic className="w-7 h-7 text-white" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Voice Commands</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              Speak naturally - "I attack the goblin!"
            </p>
          </article>

          <article 
            className="bg-[#1a1a1a] p-6 rounded-xl shadow-md border-2 border-[#107C10]/40 hover:border-[#9BDB4D] transition-all focus-within:ring-4 focus-within:ring-[#107C10]/50"
            role="listitem"
            tabIndex={0}
            aria-label="Epic Story - Three acts of adventure"
          >
            <div className="bg-[#107C10] w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Scroll className="w-7 h-7 text-white" aria-hidden="true" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Epic Story</h2>
            <p className="text-[#a0a0a0] text-base leading-relaxed">
              Three acts of adventure await you
            </p>
          </article>
        </div>

        {/* Large, accessible CTA Button */}
        <Button
          id="start-quest"
          onClick={onStartCall}
          className="bg-[#107C10] hover:bg-[#9BDB4D] hover:text-[#0a0a0a] text-white text-xl font-bold px-12 py-7 rounded-xl shadow-xl hover:shadow-2xl transition-all duration-200 focus:ring-4 focus:ring-[#107C10]/50 focus:outline-none min-h-[70px] uppercase tracking-wider"
          aria-label="Begin your quest with Dungeon Master Aldric"
        >
          <Sword className="w-7 h-7 mr-3" aria-hidden="true" />
          {startButtonText}
        </Button>

        {/* Quest info note */}
        <p className="mt-6 text-[#a0a0a0] text-base flex items-center gap-2" role="note">
          <Crown className="w-5 h-5 text-[#9BDB4D]" aria-hidden="true" />
          <span>Defeat Malachar and become the Hero of Eldoria</span>
        </p>

        {/* Instructions box - Dark fantasy style */}
        <div 
          className="mt-8 bg-[#1a1a1a] p-6 rounded-xl max-w-lg border-2 border-[#107C10]/50"
          role="region"
          aria-label="Voice command examples"
        >
          <h3 className="font-bold text-[#9BDB4D] text-lg mb-2">⚔️ Voice Commands:</h3>
          <p className="text-white text-base leading-relaxed">
            Say things like: <strong className="text-[#9BDB4D]">"My name is Thorin"</strong>, <strong className="text-[#9BDB4D]">"I roll to attack"</strong>, <strong className="text-[#9BDB4D]">"Check my inventory"</strong>, or <strong className="text-[#9BDB4D]">"What's my health?"</strong>
          </p>
        </div>
      </main>
    </div>
  );
};
