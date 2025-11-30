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
  companyName: 'ShopVoice',
  pageTitle: 'ShopVoice - Voice-Powered Shopping Assistant',
  pageDescription: 'Shop smarter with Aria, your AI voice shopping assistant. Browse products, compare prices, and place orders hands-free using just your voice.',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/shopvoice-logo.svg',
  accent: '#FF9900',
  logoDark: '/shopvoice-logo.svg',
  accentDark: '#FEBD69',
  startButtonText: 'Start Shopping',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
