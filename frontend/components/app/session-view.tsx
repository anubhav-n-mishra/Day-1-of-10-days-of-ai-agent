'use client';

import React from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { Shield, Mic, MicOff, Volume2, Phone, AlertTriangle } from 'lucide-react';
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
    <section className="relative z-10 h-full w-full bg-gradient-to-br from-[#FFF5F7] to-white overflow-hidden" {...props}>
      {/* Hidden audio element for agent voice */}
      {agentAudioTrack && (
        <AudioTrack trackRef={agentAudioTrack} />
      )}
      
      <div className="min-h-screen flex flex-col items-center justify-center p-8">
        
        {/* Razorpay SDR Icon with Audio Visualization */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="relative">
            <div className={cn(
              "absolute w-32 h-32 bg-[#9D2235] opacity-10 rounded-full transition-all",
              isAgentSpeaking && "animate-pulse scale-110"
            )}></div>
            <div className="relative bg-gradient-to-br from-[#9D2235] to-[#741A28] p-8 rounded-full shadow-2xl">
              {isAgentSpeaking ? (
                <Volume2 className="w-20 h-20 text-white animate-pulse" strokeWidth={2.5} />
              ) : (
                <Shield className="w-20 h-20 text-white" strokeWidth={2.5} />
              )}
            </div>
          </div>
        </motion.div>
        
        {/* Agent Status */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-6"
        >
          <h2 className="text-5xl font-black text-[#1F1F1F] mb-3 text-center">
            {isAgentSpeaking ? "Aarav is speaking..." : isAgentListening ? "Listening to you..." : "Connected with Aarav"}
          </h2>
          <p className="text-[#9D2235] text-xl text-center font-semibold">
            {isAgentSpeaking ? "Verifying your transaction" : isAgentListening ? "Your turn to speak" : "IDFC Bank Fraud Prevention"}
          </p>
        </motion.div>

        {/* Status Indicator */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.3, type: "spring" }}
          className="mb-8 flex items-center gap-3"
        >
          <div className={cn(
            "w-3 h-3 rounded-full transition-all",
            isAgentSpeaking ? "bg-[#9D2235] animate-pulse scale-125" : 
            isAgentListening ? "bg-[#00D632] animate-pulse" : 
            "bg-gray-400"
          )}></div>
          <span className="text-sm font-medium text-gray-600">
            {isAgentSpeaking ? "Agent Speaking" : isAgentListening ? "You're Speaking" : "Ready"}
          </span>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full max-w-4xl"
        >
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10">
            <Shield className="w-10 h-10 text-[#9D2235] mb-3" />
            <h3 className="text-lg font-bold text-[#1F1F1F] mb-2">Verify Transactions</h3>
            <p className="text-sm text-gray-600">
              Confirm or decline suspicious transactions instantly
            </p>
          </div>

          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10">
            <AlertTriangle className="w-10 h-10 text-[#9D2235] mb-3" />
            <h3 className="text-lg font-bold text-[#1F1F1F] mb-2">Real-Time Alerts</h3>
            <p className="text-sm text-gray-600">
              Get notified immediately about unusual activity
            </p>
          </div>

          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border-2 border-[#9D2235]/10">
            <Phone className="w-10 h-10 text-[#9D2235] mb-3" />
            <h3 className="text-lg font-bold text-[#1F1F1F] mb-2">Block Instantly</h3>
            <p className="text-sm text-gray-600">
              Stop fraudulent transactions and protect your card
            </p>
          </div>
        </motion.div>

        {/* Microphone Control */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring", stiffness: 200 }}
        >
          <button
            onClick={() => toggleMic()}
            className={cn(
              "relative group transition-all duration-300",
              micEnabled 
                ? "bg-gradient-to-r from-[#9D2235] to-[#741A28] hover:shadow-[0_20px_50px_rgba(157,34,53,0.5)]" 
                : "bg-gray-400 hover:bg-gray-500"
            )}
            style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: micEnabled ? '0 10px 40px rgba(157, 34, 53, 0.4)' : '0 10px 30px rgba(0, 0, 0, 0.2)'
            }}
          >
            {micEnabled ? (
              <Mic className="w-10 h-10 text-white" strokeWidth={2.5} />
            ) : (
              <MicOff className="w-10 h-10 text-white" strokeWidth={2.5} />
            )}
            
            {/* Pulse effect when listening */}
            {micEnabled && isAgentListening && (
              <motion.div
                className="absolute inset-0 rounded-full border-4 border-[#00D632]"
                initial={{ scale: 1, opacity: 0.8 }}
                animate={{ scale: 1.5, opacity: 0 }}
                transition={{ duration: 1.5, repeat: Infinity }}
              />
            )}
          </button>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-6 text-gray-600 text-center max-w-md"
        >
          {micEnabled 
            ? "Microphone active - Speak naturally with Aarav" 
            : "Click the microphone to start talking"}
        </motion.p>

        {/* Pro Tip */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-12 bg-white/80 backdrop-blur-sm p-6 rounded-xl max-w-2xl border-2 border-[#9D2235]/20 shadow-lg"
        >
          <p className="text-sm text-gray-700 leading-relaxed text-center">
            <span className="font-bold text-[#9D2235]">💡 Sample Questions:</span> "I need to verify a transaction" • "Can you check if my card is safe?" • "Is this charge legitimate?" • "I want to report suspicious activity" • "Can you block my card?"
          </p>
        </motion.div>
      </div>
    </section>
  );
};
