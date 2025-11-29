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
  companyName: 'Realm of Eldoria',
  pageTitle: 'Realm of Eldoria - Voice D&D Adventure',
  pageDescription: 'Embark on an epic voice-guided D&D adventure with Dungeon Master Aldric. Roll dice, battle monsters, and save the realm from the Shadow Dragon Malachar!',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/eldoria-logo.svg',
  accent: '#107C10',
  logoDark: '/eldoria-logo.svg',
  accentDark: '#9BDB4D',
  startButtonText: 'Begin Your Quest',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
