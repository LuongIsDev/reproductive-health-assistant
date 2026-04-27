import { Heart, Plus, MessageSquare, Trash2, X, Moon, Sun } from "lucide-react";
import { Conversation } from "@/types/chat";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

interface SidebarProps {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
  onClose?: () => void;
  isMobile?: boolean;
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

function formatDate(ts: number) {
  const d = new Date(ts);
  const now = new Date();
  const sameDay = d.toDateString() === now.toDateString();
  if (sameDay) return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  return d.toLocaleDateString([], { day: "2-digit", month: "short" });
}

export function Sidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
  onDelete,
  onClose,
  isMobile,
  theme,
  onToggleTheme,
}: SidebarProps) {
  return (
    <aside className="flex h-full w-full flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border">
      {/* Header */}
      <div className="flex items-center justify-between gap-2 px-3 py-3 border-b border-sidebar-border">
        <div className="flex items-center gap-2 min-w-0">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-primary shadow-glow shrink-0">
            <Heart className="h-4 w-4 text-primary-foreground" fill="currentColor" />
          </div>
          <div className="min-w-0">
            <h1 className="font-display font-semibold text-sm truncate">HealthChat</h1>
            <p className="text-[11px] text-muted-foreground truncate">Sức khỏe giới tính</p>
          </div>
        </div>
        {isMobile && (
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* New chat */}
      <div className="p-3">
        <Button
          onClick={onNew}
          className="w-full justify-start gap-2 bg-gradient-primary hover:opacity-90 text-primary-foreground border-0 shadow-soft"
        >
          <Plus className="h-4 w-4" />
          Cuộc trò chuyện mới
        </Button>
      </div>

      {/* Conversations list */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-2 pb-2">
        {conversations.length === 0 ? (
          <div className="px-3 py-8 text-center text-xs text-muted-foreground">
            Chưa có cuộc trò chuyện nào.
            <br />
            Bắt đầu hỏi điều bạn quan tâm.
          </div>
        ) : (
          <ul className="space-y-1">
            {conversations.map((c) => {
              const active = c.id === activeId;
              return (
                <li key={c.id}>
                  <div
                    className={cn(
                      "group flex items-center gap-2 rounded-lg px-2.5 py-2 cursor-pointer transition-smooth",
                      active
                        ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-soft"
                        : "hover:bg-sidebar-accent/60"
                    )}
                    onClick={() => onSelect(c.id)}
                  >
                    <MessageSquare
                      className={cn(
                        "h-4 w-4 shrink-0",
                        active ? "text-primary" : "text-muted-foreground"
                      )}
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{c.title || "Cuộc trò chuyện"}</p>
                      <p className="text-[11px] text-muted-foreground truncate">
                        {formatDate(c.updatedAt)}
                      </p>
                    </div>
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <button
                          aria-label="Xóa cuộc trò chuyện"
                          onClick={(e) => e.stopPropagation()}
                          className={cn(
                            "p-1 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-smooth",
                            "opacity-0 group-hover:opacity-100 focus:opacity-100",
                            active && "opacity-100"
                          )}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </AlertDialogTrigger>
                      <AlertDialogContent onClick={(e) => e.stopPropagation()}>
                        <AlertDialogHeader>
                          <AlertDialogTitle>Xóa cuộc trò chuyện?</AlertDialogTitle>
                          <AlertDialogDescription>
                            Hành động này không thể hoàn tác. Toàn bộ tin nhắn của
                            "{c.title}" sẽ bị xóa vĩnh viễn.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>Hủy</AlertDialogCancel>
                          <AlertDialogAction
                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                            onClick={() => onDelete(c.id)}
                          >
                            Xóa
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-sidebar-border p-3 flex items-center justify-between">
        <p className="text-[11px] text-muted-foreground">
          Riêng tư · Lưu cục bộ
        </p>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={onToggleTheme}
          aria-label="Đổi giao diện"
        >
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
      </div>
    </aside>
  );
}
