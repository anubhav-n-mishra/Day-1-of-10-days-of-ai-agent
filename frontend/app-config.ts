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
  companyName: 'Zepto Express',
  pageTitle: 'Zepto Express - Voice Shopping Assistant',
  pageDescription: 'Shop for groceries and essentials using just your voice',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/ccd-logo.svg',
  accent: '#8B5CF6',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#A78BFA',
  startButtonText: 'Start Shopping with Zara',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
