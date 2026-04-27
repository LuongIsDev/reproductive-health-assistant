import { Heart, Shield, Sparkles, HeartPulse } from "lucide-react";

interface EmptyStateProps {
  onPick: (text: string) => void;
}

const SUGGESTIONS = [
  {
    icon: Sparkles,
    title: "Sức khỏe sinh sản",
    prompt: "Chu kỳ kinh nguyệt bình thường kéo dài bao lâu và khi nào cần đi khám?",
  },
  {
    icon: Shield,
    title: "Phòng tránh thai",
    prompt: "Các phương pháp tránh thai phổ biến và ưu nhược điểm là gì?",
  },
  {
    icon: HeartPulse,
    title: "Bệnh lây qua đường tình dục",
    prompt: "Làm sao để phòng ngừa các bệnh lây truyền qua đường tình dục?",
  },
  {
    icon: Heart,
    title: "Tâm lý & quan hệ",
    prompt: "Làm sao trò chuyện với bạn đời về sức khỏe giới tính một cách thoải mái?",
  },
];

export function EmptyState({ onPick }: EmptyStateProps) {
  return (
    <div className="flex h-full flex-col items-center justify-center px-4 py-8">
      <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-primary shadow-glow">
        <Heart className="h-8 w-8 text-primary-foreground" fill="currentColor" />
      </div>
      <h2 className="font-display text-2xl sm:text-3xl font-semibold text-center">
        Chào bạn, mình có thể giúp gì?
      </h2>
      <p className="mt-2 max-w-md text-center text-sm text-muted-foreground">
        Một không gian an toàn, riêng tư để hỏi về sức khỏe giới tính.
        Mọi cuộc trò chuyện chỉ lưu trên thiết bị của bạn.
      </p>

      <div className="mt-8 grid w-full max-w-2xl grid-cols-1 sm:grid-cols-2 gap-3">
        {SUGGESTIONS.map((s) => (
          <button
            key={s.title}
            onClick={() => onPick(s.prompt)}
            className="group text-left rounded-xl border border-border bg-card p-4 hover:border-primary/40 hover:shadow-soft transition-smooth"
          >
            <div className="flex items-start gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent text-accent-foreground group-hover:bg-gradient-primary group-hover:text-primary-foreground transition-smooth">
                <s.icon className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <p className="font-medium text-sm">{s.title}</p>
                <p className="mt-0.5 text-xs text-muted-foreground line-clamp-2">
                  {s.prompt}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
