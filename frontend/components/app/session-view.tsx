'use client';

import React, { useRef, useEffect } from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { Sword, Shield, Mic, MicOff, Volume2, Dice6, Scroll, Heart, Backpack, MessageSquare, User, Crown } from 'lucide-react';
import { useVoiceAssistant, AudioTrack, useTrackToggle } from '@livekit/components-react';
import { Track } from 'livekit-client';
import { cn } from '@/lib/utils';
import { useChatMessages } from '@/hooks/useChatMessages';

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
  
  // Get chat messages
  const messages = useChatMessages();
  const chatContainerRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);
  
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
      
      <div className="min-h-screen flex flex-col p-4 md:p-6">
        
        {/* Header with Status */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex items-center justify-between mb-4"
        >
          <div className="flex items-center gap-3">
            <div className={cn(
              "p-3 rounded-xl",
              isAgentSpeaking ? "bg-[#107C10] animate-pulse" : "bg-[#1a1a1a] border border-[#107C10]/50"
            )}>
              {isAgentSpeaking ? (
                <Volume2 className="w-6 h-6 text-white" aria-hidden="true" />
              ) : (
                <Dice6 className="w-6 h-6 text-[#9BDB4D]" aria-hidden="true" />
              )}
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-black text-white">Realm of Eldoria</h1>
              <p className="text-sm text-[#9BDB4D]">
                {isAgentSpeaking ? "Aldric is speaking..." : isAgentListening ? "Your turn, adventurer!" : "Voice D&D Adventure"}
              </p>
            </div>
          </div>
          
          {/* Status Badge */}
          <div className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg border",
            isAgentSpeaking ? "bg-[#107C10]/20 border-[#107C10]" : 
            isAgentListening ? "bg-green-500/20 border-green-500" : 
            "bg-[#1a1a1a] border-[#3d3d3d]"
          )}>
            <div className={cn(
              "w-3 h-3 rounded-full",
              isAgentSpeaking ? "bg-[#9BDB4D] animate-pulse" : 
              isAgentListening ? "bg-green-400 animate-pulse" : 
              "bg-gray-500"
            )} />
            <span className="text-sm font-semibold text-white">
              {isAgentSpeaking ? "Narrating" : isAgentListening ? "Listening" : "Ready"}
            </span>
          </div>
        </motion.div>

        {/* Main Content - Chat Area */}
        <div className="flex-1 flex flex-col md:flex-row gap-4 min-h-0">
          
          {/* Chat Transcript - Main Focus */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="flex-1 flex flex-col bg-[#1a1a1a] rounded-xl border-2 border-[#107C10]/40 overflow-hidden"
          >
            {/* Chat Header */}
            <div className="flex items-center gap-2 px-4 py-3 bg-[#0d0d0d] border-b border-[#107C10]/30">
              <MessageSquare className="w-5 h-5 text-[#9BDB4D]" />
              <span className="font-bold text-white">Adventure Log</span>
              <span className="ml-auto text-xs text-[#a0a0a0]">{messages.length} messages</span>
            </div>
            
            {/* Chat Messages */}
            <div 
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-[#107C10] scrollbar-track-transparent"
              style={{ maxHeight: 'calc(100vh - 300px)' }}
            >
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-10">
                  <Scroll className="w-16 h-16 text-[#107C10]/50 mb-4" />
                  <p className="text-[#a0a0a0] text-lg">Your adventure awaits...</p>
                  <p className="text-[#666] text-sm mt-2">Click the microphone and speak to begin!</p>
                </div>
              ) : (
                messages.map((msg, index) => {
                  const isPlayer = msg.from?.isLocal;
                  return (
                    <motion.div
                      key={msg.id || index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={cn(
                        "flex gap-3",
                        isPlayer ? "flex-row-reverse" : "flex-row"
                      )}
                    >
                      {/* Avatar */}
                      <div className={cn(
                        "flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center",
                        isPlayer ? "bg-[#107C10]" : "bg-gradient-to-br from-[#9BDB4D] to-[#107C10]"
                      )}>
                        {isPlayer ? (
                          <User className="w-5 h-5 text-white" />
                        ) : (
                          <Crown className="w-5 h-5 text-white" />
                        )}
                      </div>
                      
                      {/* Message Bubble */}
                      <div className={cn(
                        "max-w-[80%] rounded-xl px-4 py-3",
                        isPlayer 
                          ? "bg-[#107C10] text-white rounded-tr-none" 
                          : "bg-[#2a2a2a] text-white border border-[#107C10]/30 rounded-tl-none"
                      )}>
                        <div className="flex items-center gap-2 mb-1">
                          <span className={cn(
                            "text-xs font-bold",
                            isPlayer ? "text-[#9BDB4D]" : "text-[#9BDB4D]"
                          )}>
                            {isPlayer ? "You" : "Dungeon Master Aldric"}
                          </span>
                          <span className="text-xs text-[#666]">
                            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.message}</p>
                      </div>
                    </motion.div>
                  );
                })
              )}
              
              {/* Typing Indicator when agent is speaking */}
              {isAgentSpeaking && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-3"
                >
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#9BDB4D] to-[#107C10] flex items-center justify-center">
                    <Crown className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-[#2a2a2a] rounded-xl rounded-tl-none px-4 py-3 border border-[#107C10]/30">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-[#9BDB4D] rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-[#9BDB4D] rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-[#9BDB4D] rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Side Panel - Quick Actions & Mic */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="w-full md:w-72 flex flex-col gap-4"
          >
            {/* Microphone Control */}
            <div className="bg-[#1a1a1a] rounded-xl border-2 border-[#107C10]/40 p-4 flex flex-col items-center">
              <button
                onClick={() => toggleMic()}
                aria-label={micEnabled ? "Microphone is on. Click to turn off." : "Microphone is off. Click to turn on."}
                aria-pressed={micEnabled}
                className={cn(
                  "relative w-20 h-20 rounded-xl flex items-center justify-center transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-[#107C10]/50",
                  micEnabled 
                    ? "bg-[#107C10] hover:bg-[#9BDB4D]" 
                    : "bg-gray-600 hover:bg-gray-500"
                )}
                style={{
                  boxShadow: micEnabled ? '0 8px 30px rgba(16, 124, 16, 0.5)' : '0 8px 20px rgba(0, 0, 0, 0.3)'
                }}
              >
                {micEnabled ? (
                  <Mic className="w-10 h-10 text-white" strokeWidth={2.5} />
                ) : (
                  <MicOff className="w-10 h-10 text-white" strokeWidth={2.5} />
                )}
                
                {micEnabled && isAgentListening && (
                  <motion.div
                    className="absolute inset-0 rounded-xl border-4 border-[#9BDB4D]"
                    initial={{ scale: 1, opacity: 0.8 }}
                    animate={{ scale: 1.2, opacity: 0 }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  />
                )}
              </button>
              <p className="mt-3 text-sm text-center text-[#a0a0a0]">
                {micEnabled ? "🎤 Speaking to Aldric" : "Click to speak"}
              </p>
            </div>

            {/* Quick Actions */}
            <div className="bg-[#1a1a1a] rounded-xl border-2 border-[#107C10]/40 p-4 space-y-3">
              <h3 className="text-sm font-bold text-[#9BDB4D] flex items-center gap-2">
                <Sword className="w-4 h-4" /> Quick Commands
              </h3>
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Dice6 className="w-4 h-4 text-[#107C10]" />
                  <span>"Roll for perception"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Backpack className="w-4 h-4 text-[#107C10]" />
                  <span>"Check inventory"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Heart className="w-4 h-4 text-[#107C10]" />
                  <span>"What's my health?"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Scroll className="w-4 h-4 text-[#107C10]" />
                  <span>"Game summary"</span>
                </div>
              </div>
            </div>

            {/* Game Tips */}
            <div className="bg-[#0d1a0d] rounded-xl border border-[#107C10]/30 p-4">
              <p className="text-xs text-[#9BDB4D] font-bold mb-2">💡 TIP</p>
              <p className="text-xs text-[#a0a0a0] leading-relaxed">
                Speak naturally! Say "I want to attack the goblin" or "I search the room for treasure"
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
