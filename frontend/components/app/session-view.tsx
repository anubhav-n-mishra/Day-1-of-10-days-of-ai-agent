'use client';

import React from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { Sword, Shield, Mic, MicOff, Volume2, Dice6, Scroll, Heart, Backpack } from 'lucide-react';
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
  
  // Status text for screen readers
  const statusText = isAgentSpeaking 
    ? "Dungeon Master Aldric is speaking. Listen carefully." 
    : isAgentListening 
    ? "Aldric awaits your command. Speak now, adventurer!" 
    : "Ready to continue your quest.";
  
  return (
    <section 
      className="relative z-10 h-full w-full bg-[#0a0a0a] overflow-hidden" 
      role="main"
      aria-label="D&D Voice Adventure with Dungeon Master Aldric"
      {...props}
    >
      {/* Hidden audio element for agent voice */}
      {agentAudioTrack && (
        <AudioTrack trackRef={agentAudioTrack} />
      )}
      
      {/* Live region for screen reader announcements */}
      <div 
        role="status" 
        aria-live="polite" 
        aria-atomic="true"
        className="sr-only"
      >
        {statusText}
      </div>
      
      <div className="min-h-screen flex flex-col items-center justify-center p-6">
        
        {/* Dungeon Master Icon */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-6"
          role="img"
          aria-label={isAgentSpeaking ? "Aldric is narrating your adventure" : "Dungeon Master Aldric"}
        >
          <div className="relative">
            <div className={cn(
              "absolute w-28 h-28 bg-[#107C10] opacity-30 rounded-full transition-all -inset-2",
              isAgentSpeaking && "animate-pulse scale-110"
            )} aria-hidden="true"></div>
            <div className="relative bg-[#107C10] p-6 rounded-xl shadow-xl dice-glow">
              {isAgentSpeaking ? (
                <Volume2 className="w-16 h-16 text-white animate-pulse" strokeWidth={2.5} aria-hidden="true" />
              ) : (
                <Dice6 className="w-16 h-16 text-white" strokeWidth={2.5} aria-hidden="true" />
              )}
            </div>
          </div>
        </motion.div>
        
        {/* Agent Status - Epic fantasy style */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-4 text-center"
        >
          <h1 className="text-4xl md:text-5xl font-black text-white mb-2 game-text">
            {isAgentSpeaking ? "The Tale Unfolds..." : isAgentListening ? "Your Move, Adventurer" : "Realm of Eldoria"}
          </h1>
          <p className="text-[#9BDB4D] text-xl font-semibold">
            {isAgentSpeaking ? "Dungeon Master Aldric narrates" : isAgentListening ? "Speak your action" : "Voice D&D Adventure"}
          </p>
        </motion.div>

        {/* Status Indicator - Game style */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.3, type: "spring" }}
          className="mb-8 flex items-center gap-3 bg-[#1a3d1a] px-5 py-2.5 rounded-lg border border-[#9BDB4D]/50"
          role="status"
          aria-label={statusText}
        >
          <div className={cn(
            "w-4 h-4 rounded-full transition-all",
            isAgentSpeaking ? "bg-[#9BDB4D] animate-pulse scale-125" : 
            isAgentListening ? "bg-green-400 animate-pulse" : 
            "bg-gray-500"
          )} aria-hidden="true"></div>
          <span className="text-base font-semibold text-white">
            {isAgentSpeaking ? "Aldric Speaks" : isAgentListening ? "Your Turn" : "Ready"}
          </span>
        </motion.div>

        {/* Action Cards - Dark fantasy */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10 w-full max-w-4xl"
          role="list"
          aria-label="Game actions"
        >
          <article 
            className="bg-[#1a1a1a] p-5 rounded-xl border-2 border-[#107C10]/40"
            role="listitem"
            tabIndex={0}
          >
            <Sword className="w-8 h-8 text-[#9BDB4D] mb-2" aria-hidden="true" />
            <h2 className="text-lg font-bold text-white mb-1">Combat</h2>
            <p className="text-sm text-[#a0a0a0]">
              "I attack" or "Roll strength"
            </p>
          </article>

          <article 
            className="bg-[#1a1a1a] p-5 rounded-xl border-2 border-[#107C10]/40"
            role="listitem"
            tabIndex={0}
          >
            <Backpack className="w-8 h-8 text-[#9BDB4D] mb-2" aria-hidden="true" />
            <h2 className="text-lg font-bold text-white mb-1">Inventory</h2>
            <p className="text-sm text-[#a0a0a0]">
              "Check inventory" or "Use potion"
            </p>
          </article>

          <article 
            className="bg-[#1a1a1a] p-5 rounded-xl border-2 border-[#107C10]/40"
            role="listitem"
            tabIndex={0}
          >
            <Heart className="w-8 h-8 text-[#9BDB4D] mb-2" aria-hidden="true" />
            <h2 className="text-lg font-bold text-white mb-1">Status</h2>
            <p className="text-sm text-[#a0a0a0]">
              "What's my health?" or "Game summary"
            </p>
          </article>
        </motion.div>

        {/* Large Microphone Control - Epic style */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring", stiffness: 200 }}
        >
          <button
            onClick={() => toggleMic()}
            aria-label={micEnabled ? "Microphone is on. Click to turn off." : "Microphone is off. Click to turn on."}
            aria-pressed={micEnabled}
            className={cn(
              "relative group transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-[#107C10]/50",
              micEnabled 
                ? "bg-[#107C10] hover:bg-[#9BDB4D]" 
                : "bg-gray-600 hover:bg-gray-500"
            )}
            style={{
              width: '100px',
              height: '100px',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: micEnabled ? '0 10px 40px rgba(16, 124, 16, 0.5)' : '0 10px 30px rgba(0, 0, 0, 0.3)'
            }}
          >
            {micEnabled ? (
              <Mic className="w-12 h-12 text-white" strokeWidth={2.5} aria-hidden="true" />
            ) : (
              <MicOff className="w-12 h-12 text-white" strokeWidth={2.5} aria-hidden="true" />
            )}
            
            {/* Pulse effect when listening */}
            {micEnabled && isAgentListening && (
              <motion.div
                className="absolute inset-0 rounded-xl border-4 border-[#9BDB4D]"
                initial={{ scale: 1, opacity: 0.8 }}
                animate={{ scale: 1.3, opacity: 0 }}
                transition={{ duration: 1.5, repeat: Infinity }}
                aria-hidden="true"
              />
            )}
          </button>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-5 text-[#a0a0a0] text-lg text-center max-w-md font-medium"
        >
          {micEnabled 
            ? "⚔️ Microphone ON - Speak to Aldric" 
            : "Click to speak with the Dungeon Master"}
        </motion.p>

        {/* Voice commands help - Fantasy style */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-8 bg-[#1a1a1a] p-5 rounded-xl max-w-2xl border-2 border-[#107C10]/40"
          role="region"
          aria-label="Voice command examples"
        >
          <p className="text-base text-white leading-relaxed text-center">
            <span className="font-bold text-[#9BDB4D]">⚔️ Commands:</span> "My name is..." • "I roll for perception" • "Attack the goblin" • "Check my inventory" • "What's my health?"
          </p>
        </motion.div>
      </div>
    </section>
  );
};
