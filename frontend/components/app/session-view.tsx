'use client';

import React from 'react';
import { motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { BookOpen, Brain, MessageSquare, Mic, MicOff, Volume2 } from 'lucide-react';
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
    <section className="relative z-10 h-full w-full bg-linear-to-br from-[#EBF5FF] to-white overflow-hidden" {...props}>
      {/* Hidden audio element for agent voice */}
      {agentAudioTrack && (
        <AudioTrack trackRef={agentAudioTrack} />
      )}
      
      <div className="min-h-screen flex flex-col items-center justify-center p-8">
        
        {/* Learning Mode Icon with Audio Visualization */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="relative">
            <div className={cn(
              "absolute w-32 h-32 bg-[#0056D2] opacity-10 rounded-full transition-all",
              isAgentSpeaking && "animate-pulse scale-110"
            )}></div>
            <div className="relative bg-linear-to-br from-[#0056D2] to-[#004099] p-8 rounded-full shadow-2xl">
              {isAgentSpeaking ? (
                <Volume2 className="w-20 h-20 text-white animate-pulse" strokeWidth={2.5} />
              ) : (
                <Brain className="w-20 h-20 text-white" strokeWidth={2.5} />
              )}
            </div>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-8 h-8 text-[#FFB800] fill-[#FFB800] absolute -top-2 -right-2"
            >
              ✨
            </motion.div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-6 max-w-3xl"
        >
          <h2 className="text-5xl font-black text-[#1F1F1F] tracking-tight">
            Active Learning Session
          </h2>
          <p className="text-[#0056D2] text-xl font-bold">
            Choose your mode: Learn, Quiz, or Teach Back
          </p>

          {/* Three Learning Modes */}
          <div className="grid grid-cols-3 gap-6 mt-10 mb-10">
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border-2 border-transparent hover:border-[#0056D2]/30 cursor-pointer hover:scale-105">
              <BookOpen className="w-12 h-12 text-[#0056D2] mx-auto mb-4" strokeWidth={2.5} />
              <p className="text-lg font-bold text-gray-800 mb-2">Learn</p>
              <p className="text-sm text-gray-500 mb-4">Concepts explained</p>
              <div className="h-1.5 bg-[#0056D2]/20 rounded-full">
                <div className="h-1.5 bg-[#0056D2] rounded-full w-0"></div>
              </div>
            </div>
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border-2 border-transparent hover:border-[#0056D2]/30 cursor-pointer hover:scale-105">
              <MessageSquare className="w-12 h-12 text-[#0056D2] mx-auto mb-4" strokeWidth={2.5} />
              <p className="text-lg font-bold text-gray-800 mb-2">Quiz</p>
              <p className="text-sm text-gray-500 mb-4">Test knowledge</p>
              <div className="h-1.5 bg-[#0056D2]/20 rounded-full">
                <div className="h-1.5 bg-[#0056D2] rounded-full w-0"></div>
              </div>
            </div>
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border-2 border-transparent hover:border-[#0056D2]/30 cursor-pointer hover:scale-105">
              <Brain className="w-12 h-12 text-[#0056D2] mx-auto mb-4" strokeWidth={2.5} />
              <p className="text-lg font-bold text-gray-800 mb-2">Teach</p>
              <p className="text-sm text-gray-500 mb-4">Explain back</p>
              <div className="h-1.5 bg-[#0056D2]/20 rounded-full">
                <div className="h-1.5 bg-[#0056D2] rounded-full w-0"></div>
              </div>
            </div>
          </div>

          {/* Microphone Button with Clear States */}
          <div className="flex flex-col items-center gap-5 mt-12">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleMic()}
              className={cn(
                "p-10 rounded-full shadow-2xl transition-all border-0 relative",
                micEnabled 
                  ? "bg-linear-to-br from-[#0056D2] to-[#004099] hover:shadow-[0_15px_50px_rgba(0,86,210,0.5)]"
                  : "bg-gray-400 hover:shadow-[0_15px_50px_rgba(0,0,0,0.3)] hover:bg-gray-500"
              )}
            >
              {micEnabled ? (
                <Mic className="w-14 h-14 text-white" strokeWidth={2.5} />
              ) : (
                <MicOff className="w-14 h-14 text-white" strokeWidth={2.5} />
              )}
              {isAgentListening && (
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="absolute inset-0 rounded-full border-4 border-[#FFB800] opacity-50"
                />
              )}
            </motion.button>
            <div className="text-center">
              <p className="text-lg font-bold text-gray-800">
                {micEnabled ? (isAgentListening ? '🎤 Listening...' : '✓ Microphone Active') : '🔇 Click to Start'}
              </p>
              <p className="text-base text-gray-600 mt-2">
                {isAgentSpeaking ? '🔊 AI Coach is speaking...' : micEnabled ? 'Say "learn", "quiz", or "teach back"' : 'Activate your microphone to begin'}
              </p>
            </div>
          </div>

          {/* Mode Switching Hint */}
          <div className="mt-10 p-6 bg-white rounded-2xl shadow-lg border-2 border-[#0056D2]/20">
            <p className="text-base text-gray-700 leading-relaxed">
              <span className="font-bold text-[#0056D2] text-lg">Pro Tip:</span> You can switch between modes anytime by saying "switch to learn mode" or "let's do a quiz"
            </p>
          </div>
        </motion.div>

      </div>
    </section>
  );
};
