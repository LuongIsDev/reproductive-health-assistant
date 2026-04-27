import { Conversation } from "@/types/chat";

const STORAGE_KEY = "healthchat.conversations.v1";
const ACTIVE_KEY = "healthchat.activeId.v1";
const THEME_KEY = "healthchat.theme.v1";

export function loadConversations(): Conversation[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Conversation[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveConversations(items: Conversation[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {
    /* ignore quota */
  }
}

export function loadActiveId(): string | null {
  return localStorage.getItem(ACTIVE_KEY);
}

export function saveActiveId(id: string | null) {
  if (id) localStorage.setItem(ACTIVE_KEY, id);
  else localStorage.removeItem(ACTIVE_KEY);
}

export function loadTheme(): "light" | "dark" {
  const t = localStorage.getItem(THEME_KEY);
  if (t === "light" || t === "dark") return t;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function saveTheme(t: "light" | "dark") {
  localStorage.setItem(THEME_KEY, t);
}
