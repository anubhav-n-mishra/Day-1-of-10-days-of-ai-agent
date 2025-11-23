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
  companyName: 'Coffee Shop Voice Barista',
  pageTitle: 'Coffee Shop Voice Barista',
  pageDescription: 'Voice-powered coffee ordering experience',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#00704A',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#005a3a',
  startButtonText: 'Start Your Order',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
