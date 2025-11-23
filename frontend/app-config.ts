export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Starbucks Voice Barista',
  pageTitle: 'Starbucks Voice Barista - Order with AI',
  pageDescription: 'Order your favorite Starbucks drink using voice AI technology',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#00704A',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#005a3a',
  startButtonText: 'Start Ordering',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
