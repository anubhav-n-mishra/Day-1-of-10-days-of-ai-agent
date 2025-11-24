'use client';

import React from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { Activity, Heart, Mic, MicOff, Volume2, CheckCircle2 } from 'lucide-react';
import { useVoiceAssistant, AudioTrack, useTrackToggle } from '@livekit/components-react';
import { Track } from 'livekit-client';
import { cn } from '@/lib/utils';

interface SessionViewProps {
  appConfig: AppConfig;
}

export const SessionView = ({
  appConfig,
  ...props
}: React.ComponentProps<'section'> & SessionViewProps) => {
  const { state: agentState, audioTrack: agentAudioTrack } = useVoiceAssistant();
  const { enabled: micEnabled, toggle: toggleMic } = useTrackToggle({ source: Track.Source.Microphone });
  const isAgentSpeaking = agentState === 'speaking';
  const isAgentListening = agentState === 'listening';
  
  return (
    <section className="relative z-10 h-full w-full bg-linear-to-br from-[#F0FFF4] to-white overflow-hidden" {...props}>
      {/* Hidden audio element for agent voice */}
      {agentAudioTrack && (
        <AudioTrack trackRef={agentAudioTrack} />
      )}
      
      <div className="min-h-screen flex flex-col items-center justify-center p-8">
        
        {/* Wellness Icon with Audio Visualization */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="relative">
            <div className={cn(
              "absolute w-32 h-32 bg-[#1CAC78] opacity-10 rounded-full transition-all",
              isAgentSpeaking && "animate-pulse scale-110"
            )}></div>
            <div className="relative bg-linear-to-br from-[#1CAC78] to-[#15936B] p-8 rounded-full shadow-2xl">
              {isAgentSpeaking ? (
                <Volume2 className="w-20 h-20 text-white animate-pulse" strokeWidth={2.5} />
              ) : (
                <Activity className="w-20 h-20 text-white" strokeWidth={2.5} />
              )}
            </div>
            <Heart className="w-8 h-8 text-[#FF6B6B] fill-[#FF6B6B] absolute -top-2 -right-2 animate-pulse" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-6 max-w-2xl"
        >
          <h2 className="text-4xl font-bold text-[#1CAC78]">
            Ready for Your Check-In
          </h2>
          <p className="text-gray-600 text-lg">
            Click the microphone to start your daily wellness conversation
          </p>

          {/* Features */}
          <div className="grid grid-cols-3 gap-4 mt-8 mb-8">
            <div className="bg-white rounded-2xl p-4 shadow-md">
              <Activity className="w-8 h-8 text-[#1CAC78] mx-auto mb-2" />
              <p className="text-sm font-semibold text-gray-700">Mood Check</p>
            </div>
            <div className="bg-white rounded-2xl p-4 shadow-md">
              <CheckCircle2 className="w-8 h-8 text-[#1CAC78] mx-auto mb-2" />
              <p className="text-sm font-semibold text-gray-700">Set Goals</p>
            </div>
            <div className="bg-white rounded-2xl p-4 shadow-md">
              <Heart className="w-8 h-8 text-[#FF6B6B] mx-auto mb-2" />
              <p className="text-sm font-semibold text-gray-700">Get Support</p>
            </div>
          </div>

          {/* Microphone Button with Clear States */}
          <div className="flex flex-col items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleMic()}
              className={cn(
                "p-8 rounded-full shadow-2xl transition-all border-0",
                micEnabled 
                  ? "bg-linear-to-br from-[#1CAC78] to-[#15936B] hover:shadow-[0_10px_40px_rgba(28,172,120,0.4)]"
                  : "bg-gray-400 hover:shadow-[0_10px_40px_rgba(0,0,0,0.2)]"
              )}
            >
              {micEnabled ? (
                <Mic className="w-12 h-12 text-white" strokeWidth={2.5} />
              ) : (
                <MicOff className="w-12 h-12 text-white" strokeWidth={2.5} />
              )}
            </motion.button>
            <div className="text-center">
              <p className="text-sm font-semibold text-gray-700">
                {micEnabled ? (isAgentListening ? '🎤 Listening...' : 'Microphone Active') : 'Click to Start'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {isAgentSpeaking ? '🔊 Agent is speaking...' : micEnabled ? 'Speak naturally' : 'Enable your microphone'}
              </p>
            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
};
