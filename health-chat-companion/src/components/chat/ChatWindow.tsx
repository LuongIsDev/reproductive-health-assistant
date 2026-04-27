import { useEffect, useRef } from "react";
import { Conversation, Message } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { EmptyState } from "./EmptyState";

interface ChatWindowProps {
  conversation: Conversation | null;
  streamingId: string | null;
  onPickSuggestion: (text: string) => void;
}

export function ChatWindow({ conversation, streamingId, onPickSuggestion }: ChatWindowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const messages: Message[] = conversation?.messages ?? [];

  // Auto-scroll on new messages or stream updates
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, conversation?.id]);

  // Continuous scroll while streaming last assistant message
  useEffect(() => {
    if (!streamingId) return;
    const id = window.setInterval(() => {
      endRef.current?.scrollIntoView({ behavior: "auto", block: "end" });
    }, 200);
    return () => window.clearInterval(id);
  }, [streamingId]);

  if (!conversation || messages.length === 0) {
    return (
      <div className="flex-1 overflow-y-auto scrollbar-thin">
        <EmptyState onPick={onPickSuggestion} />
      </div>
    );
  }

  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin">
      <div className="mx-auto max-w-3xl px-3 sm:px-6 py-6 space-y-5">
        {messages.map((m) => (
          <MessageBubble
            key={m.id}
            message={m}
            isStreaming={m.id === streamingId}
          />
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}
