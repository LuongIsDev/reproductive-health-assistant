import { useEffect, useRef, useState, KeyboardEvent } from "react";
import { Send, Square } from "lucide-react";
import { cn } from "@/lib/utils";

interface InputBoxProps {
  onSend: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function InputBox({ onSend, disabled, placeholder }: InputBoxProps) {
  const [value, setValue] = useState("");
  const taRef = useRef<HTMLTextAreaElement>(null);

  // Auto-grow
  useEffect(() => {
    const ta = taRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 200) + "px";
  }, [value]);

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="px-3 sm:px-6 pb-4 pt-2 bg-gradient-to-t from-background via-background to-background/0">
      <div className="mx-auto max-w-3xl">
        <div
          className={cn(
            "relative flex items-end gap-2 rounded-2xl border border-border bg-card p-2 shadow-soft transition-smooth",
            "focus-within:border-primary/50 focus-within:shadow-glow"
          )}
        >
          <textarea
            ref={taRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKey}
            disabled={disabled}
            rows={1}
            placeholder={placeholder ?? "Hỏi điều bạn đang băn khoăn về sức khỏe giới tính…"}
            className={cn(
              "flex-1 resize-none bg-transparent px-2 py-2 text-[15px] leading-relaxed",
              "placeholder:text-muted-foreground focus:outline-none",
              "max-h-[200px] scrollbar-thin",
              disabled && "opacity-60 cursor-not-allowed"
            )}
          />
          <button
            onClick={submit}
            disabled={disabled || !value.trim()}
            aria-label="Gửi"
            className={cn(
              "flex h-9 w-9 shrink-0 items-center justify-center rounded-xl transition-smooth",
              "bg-gradient-primary text-primary-foreground shadow-soft",
              "hover:shadow-glow disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none"
            )}
          >
            {disabled ? <Square className="h-4 w-4" fill="currentColor" /> : <Send className="h-4 w-4" />}
          </button>
        </div>
        <p className="mt-2 text-center text-[11px] text-muted-foreground">
          Thông tin chỉ mang tính tham khảo, không thay thế tư vấn y tế chuyên môn.
        </p>
      </div>
    </div>
  );
}
