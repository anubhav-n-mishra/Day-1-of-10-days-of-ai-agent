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
  companyName: 'HealthifyMe',
  pageTitle: 'HealthifyMe AI Wellness Companion',
  pageDescription: 'Your personal AI health coach - Daily check-ins powered by voice',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#1CAC78',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#159A68',
  startButtonText: 'Start Your Check-In',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
