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
  companyName: 'IDFC Bank',
  pageTitle: 'IDFC Bank - Fraud Alert System',
  pageDescription: 'Secure fraud detection and verification system',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#9D2235',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#9D2235',
  startButtonText: 'Connect with Aarav',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
