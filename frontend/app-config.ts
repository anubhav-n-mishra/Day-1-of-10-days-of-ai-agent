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
  companyName: 'PayFlow',
  pageTitle: 'PayFlow SDR - Lead Capture',
  pageDescription: 'Connect with our AI Sales Representative for payment solutions',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#3395FF',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#3395FF',
  startButtonText: 'Connect with Radha',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
