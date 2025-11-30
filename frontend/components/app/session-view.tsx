'use client';

import React, { useRef, useEffect } from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { ShoppingBag, Search, Mic, MicOff, Volume2, ShoppingCart, Package, CreditCard, MessageSquare, User, Headphones } from 'lucide-react';
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
    ? "Alexa is speaking. Listen for product recommendations." 
    : isAgentListening 
    ? "Alexa is listening. Tell me what you're looking for!" 
    : "Ready to help you shop.";
  
  return (
    <section 
      className="relative z-10 h-full w-full bg-[#131921] overflow-hidden" 
      role="main"
      aria-label="ShopVoice - Voice Shopping Assistant"
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
              isAgentSpeaking ? "bg-[#FF9900] animate-pulse" : "bg-[#232F3E] border border-[#FF9900]/50"
            )}>
              {isAgentSpeaking ? (
                <Volume2 className="w-6 h-6 text-white" aria-hidden="true" />
              ) : (
                <ShoppingBag className="w-6 h-6 text-[#FF9900]" aria-hidden="true" />
              )}
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-black text-white">ShopVoice</h1>
              <p className="text-sm text-[#FF9900]">
                {isAgentSpeaking ? "Alexa is speaking..." : isAgentListening ? "I'm listening..." : "Voice Shopping Assistant"}
              </p>
            </div>
          </div>
          
          {/* Status Badge */}
          <div className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg border",
            isAgentSpeaking ? "bg-[#FF9900]/20 border-[#FF9900]" : 
            isAgentListening ? "bg-[#FEBD69]/20 border-[#FEBD69]" : 
            "bg-[#232F3E] border-[#3d4f61]"
          )}>
            <div className={cn(
              "w-3 h-3 rounded-full",
              isAgentSpeaking ? "bg-[#FF9900] animate-pulse" : 
              isAgentListening ? "bg-[#FEBD69] animate-pulse" : 
              "bg-gray-500"
            )} />
            <span className="text-sm font-semibold text-white">
              {isAgentSpeaking ? "Speaking" : isAgentListening ? "Listening" : "Ready"}
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
            className="flex-1 flex flex-col bg-[#232F3E] rounded-xl border-2 border-[#FF9900]/40 overflow-hidden"
          >
            {/* Chat Header */}
            <div className="flex items-center gap-2 px-4 py-3 bg-[#131921] border-b border-[#FF9900]/30">
              <MessageSquare className="w-5 h-5 text-[#FF9900]" />
              <span className="font-bold text-white">Shopping Session</span>
              <span className="ml-auto text-xs text-[#a0a0a0]">{messages.length} messages</span>
            </div>
            
            {/* Chat Messages */}
            <div 
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-[#FF9900] scrollbar-track-transparent"
              style={{ maxHeight: 'calc(100vh - 300px)' }}
            >
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center py-10">
                  <ShoppingCart className="w-16 h-16 text-[#FF9900]/50 mb-4" />
                  <p className="text-[#a0a0a0] text-lg">Ready to shop!</p>
                  <p className="text-[#666] text-sm mt-2">Click the microphone and tell me what you're looking for</p>
                </div>
              ) : (
                messages.map((msg, index) => {
                  const isCustomer = msg.from?.isLocal;
                  return (
                    <motion.div
                      key={msg.id || index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={cn(
                        "flex gap-3",
                        isCustomer ? "flex-row-reverse" : "flex-row"
                      )}
                    >
                      {/* Avatar */}
                      <div className={cn(
                        "flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center",
                        isCustomer ? "bg-[#FF9900]" : "bg-gradient-to-br from-[#FEBD69] to-[#FF9900]"
                      )}>
                        {isCustomer ? (
                          <User className="w-5 h-5 text-white" />
                        ) : (
                          <Headphones className="w-5 h-5 text-white" />
                        )}
                      </div>
                      
                      {/* Message Bubble */}
                      <div className={cn(
                        "max-w-[80%] rounded-xl px-4 py-3",
                        isCustomer 
                          ? "bg-[#FF9900] text-white rounded-tr-none" 
                          : "bg-[#37475A] text-white border border-[#FF9900]/30 rounded-tl-none"
                      )}>
                        <div className="flex items-center gap-2 mb-1">
                          <span className={cn(
                            "text-xs font-bold",
                            isCustomer ? "text-[#FEBD69]" : "text-[#FEBD69]"
                          )}>
                            {isCustomer ? "You" : "Alexa"}
                          </span>
                          <span className="text-xs text-[#888]">
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
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#FEBD69] to-[#FF9900] flex items-center justify-center">
                    <Headphones className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-[#37475A] rounded-xl rounded-tl-none px-4 py-3 border border-[#FF9900]/30">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-[#FF9900] rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-[#FF9900] rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-[#FF9900] rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
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
            <div className="bg-[#232F3E] rounded-xl border-2 border-[#FF9900]/40 p-4 flex flex-col items-center">
              <button
                onClick={() => toggleMic()}
                aria-label={micEnabled ? "Microphone is on. Click to turn off." : "Microphone is off. Click to turn on."}
                aria-pressed={micEnabled}
                className={cn(
                  "relative w-20 h-20 rounded-xl flex items-center justify-center transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-[#FF9900]/50",
                  micEnabled 
                    ? "bg-[#FF9900] hover:bg-[#FEBD69]" 
                    : "bg-gray-600 hover:bg-gray-500"
                )}
                style={{
                  boxShadow: micEnabled ? '0 8px 30px rgba(255, 153, 0, 0.5)' : '0 8px 20px rgba(0, 0, 0, 0.3)'
                }}
              >
                {micEnabled ? (
                  <Mic className="w-10 h-10 text-white" strokeWidth={2.5} />
                ) : (
                  <MicOff className="w-10 h-10 text-white" strokeWidth={2.5} />
                )}
                
                {micEnabled && isAgentListening && (
                  <motion.div
                    className="absolute inset-0 rounded-xl border-4 border-[#FEBD69]"
                    initial={{ scale: 1, opacity: 0.8 }}
                    animate={{ scale: 1.2, opacity: 0 }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  />
                )}
              </button>
              <p className="mt-3 text-sm text-center text-[#a0a0a0]">
                {micEnabled ? "🎤 I'm listening" : "Click to talk"}
              </p>
            </div>

            {/* Quick Actions */}
            <div className="bg-[#232F3E] rounded-xl border-2 border-[#FF9900]/40 p-4 space-y-3">
              <h3 className="text-sm font-bold text-[#FF9900] flex items-center gap-2">
                <ShoppingBag className="w-4 h-4" /> Voice Commands
              </h3>
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Search className="w-4 h-4 text-[#FF9900]" />
                  <span>"Show me coffee mugs"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <ShoppingCart className="w-4 h-4 text-[#FF9900]" />
                  <span>"Add it to my cart"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <Package className="w-4 h-4 text-[#FF9900]" />
                  <span>"What's in my cart?"</span>
                </div>
                <div className="flex items-center gap-2 text-[#a0a0a0]">
                  <CreditCard className="w-4 h-4 text-[#FF9900]" />
                  <span>"Checkout please"</span>
                </div>
              </div>
            </div>

            {/* Shopping Tips */}
            <div className="bg-[#1a2533] rounded-xl border border-[#FF9900]/30 p-4">
              <p className="text-xs text-[#FF9900] font-bold mb-2">🛒 TIP</p>
              <p className="text-xs text-[#a0a0a0] leading-relaxed">
                Speak naturally! Say "Find me a tech hoodie under 50 dollars" or "What electronics do you have?"
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
