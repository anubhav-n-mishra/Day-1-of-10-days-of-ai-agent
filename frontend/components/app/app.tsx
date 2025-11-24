'use client';

import type { AppConfig } from '@/app-config';
import { ViewController } from '@/components/app/view-controller';

interface AppProps {
  appConfig: AppConfig;
}

export function App({ appConfig }: AppProps) {
  return (
    <main className="grid h-svh grid-cols-1 place-content-center bg-white">
      <ViewController appConfig={appConfig} />
    </main>
  );
}
