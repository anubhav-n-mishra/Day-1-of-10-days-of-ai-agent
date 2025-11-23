import { Button } from '@/components/livekit/button';
import CoffeeFoamVisualizer from '@/components/coffee/CoffeeFoamVisualizer';

function WelcomeImage() {
  return (
    <svg
      width="80"
      height="64"
      viewBox="0 0 80 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="text-fg0 mb-4 size-20"
    >
      <g fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M8 44c0 6.627 5.373 12 12 12h28c6.627 0 12-5.373 12-12V22H8v22z" />
        <path d="M48 18c6 0 10-3 10-8s-4-8-10-8H20v16h28z" />
        <path d="M60 30c6 0 12-3 12-10" strokeLinecap="round" />
      </g>
    </svg>
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
      <section className="bg-background flex flex-col items-center justify-center text-center px-4">
        <div className="mb-8">
          <CoffeeFoamVisualizer isActive={false} />
        </div>

        <h1 className="text-3xl font-bold text-foreground mb-2">Cafe Coffee Day</h1>
        <p className="text-foreground max-w-prose pt-1 leading-6 font-medium text-lg">
          Place your order with our barista
        </p>

        <Button variant="primary" size="lg" onClick={onStartCall} className="mt-8 w-64 font-mono text-lg py-6">
          {startButtonText}
        </Button>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Need help getting set up? Check out the{' '}
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://docs.livekit.io/agents/start/voice-ai/"
            className="underline"
          >
            Voice AI quickstart
          </a>
          .
        </p>
      </div>
    </div>
  );
};
