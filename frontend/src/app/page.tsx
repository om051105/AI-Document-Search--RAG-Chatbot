"use client";

import { useState, useRef, useEffect } from "react";
import { Upload, Send, FileText, Bot, User, Loader2 } from "lucide-react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { motion, AnimatePresence } from "framer-motion";

// INTERFACES
// Defining types is crucial for Industrial/TypeScript projects.
interface Message {
  role: "user" | "bot";
  content: string;
}

export default function Home() {
  // STATE MANAGEMENT
  // We use React State to manage the UI interactions.
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", content: "Hello! Upload a PDF document and ask me anything about it." }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  // Refs for auto-scrolling
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // HANDLERS

  // 1. File Upload Logic
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;

    const file = e.target.files[0];
    setFileName(file.name);
    setIsUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // We send the file to our FastAPI backend
      // Note: In production, you'd use an env var for the API URL
      await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessages(prev => [...prev, { role: "bot", content: `I've read **${file.name}**. What would you like to know?` }]);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Failed to upload file. Make sure the backend is running.");
      setFileName(null);
    } finally {
      setIsUploading(false);
    }
  };

  // 2. Chat Logic
  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // Send question to RAG endpoint
      const response = await axios.post("http://localhost:8000/query", {
        question: userMessage
      });

      setMessages(prev => [...prev, { role: "bot", content: response.data.answer }]);
    } catch (error) {
      console.error("Query failed", error);
      setMessages(prev => [...prev, { role: "bot", content: "Sorry, I encountered an error connecting to the brain." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* SIDEBAR - Doc Management */}
      <div className="w-80 border-r border-slate-800 p-6 flex flex-col bg-slate-900">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent mb-8">
          DocuMind AI
        </h1>

        <div className="mb-8">
          <label className="block text-sm font-medium text-slate-400 mb-2">
            Knowledge Base
          </label>

          <div className="relative group">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              disabled={isUploading}
            />
            <div className={`
              border-2 border-dashed rounded-xl p-8 transition-all duration-300 flex flex-col items-center justify-center text-center
              ${isUploading ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-500 hover:bg-slate-800/50'}
            `}>
              {isUploading ? (
                <Loader2 className="w-8 h-8 text-blue-400 animate-spin mb-2" />
              ) : (
                <Upload className="w-8 h-8 text-slate-400 mb-2 group-hover:text-blue-400 transition-colors" />
              )}
              <span className="text-sm text-slate-400 group-hover:text-slate-200">
                {isUploading ? "Indexing..." : "Drop PDF here"}
              </span>
            </div>
          </div>
        </div>

        {fileName && (
          <div className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700 animate-in fade-in slide-in-from-left-5">
            <FileText className="w-5 h-5 text-blue-400" />
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-medium truncate">{fileName}</p>
              <p className="text-xs text-green-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-green-400" />
                Indexed
              </p>
            </div>
          </div>
        )}
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <AnimatePresence initial={false}>
            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'bot' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                )}

                <div className={`
                  max-w-[80%] rounded-2xl p-4 shadow-sm
                  ${msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-tl-none'}
                `}>
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown
                      components={{
                        p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>

                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
                    <User className="w-5 h-5 text-slate-300" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-4"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-tl-none p-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 pt-0">
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask a question about the document..."
              className="w-full bg-slate-800/80 backdrop-blur border border-slate-700 rounded-xl py-4 pl-6 pr-14 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all shadow-lg"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              className="absolute right-3 top-3 p-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 rounded-lg transition-colors text-white"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <p className="text-center text-xs text-slate-600 mt-3">
            Industrial RAG Project • Powered by LangChain, FastAPI & Next.js
          </p>
        </div>
      </div>
    </div>
  );
}
