"use client";

import { useState } from "react";
import { SparkleIcon } from "../icons";

interface AutoFillFromTextProps {
  isBusy: boolean;
  onSubmit: (text: string) => void;
}

/**
 * AI chỉ ĐỀ XUẤT giá trị nháp từ mô tả tự nhiên; người dùng luôn review và
 * RuleEngine deterministic vẫn là nơi duy nhất phán quyết khi tiền kiểm.
 */
export default function AutoFillFromText({ isBusy, onSubmit }: AutoFillFromTextProps) {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || isBusy) return;
    onSubmit(trimmed);
  };

  return (
    <div className="rounded-lg border border-dashed border-[var(--vg-accent)]/40 bg-[var(--vg-gold-soft)]/40 p-3 space-y-2">
      <label htmlFor="autofill-text" className="flex items-center gap-1.5 text-[11px] font-bold text-[var(--vg-accent)]">
        <SparkleIcon className="w-3.5 h-3.5" />
        Điền nhanh bằng mô tả tự nhiên
      </label>
      <textarea
        id="autofill-text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={2}
        maxLength={1000}
        placeholder='Ví dụ: "Con tôi tên Nguyễn Văn An, bé trai, sinh ngày 01/06/2026 tại Bệnh viện Từ Dũ. Mẹ là Trần Thị Bình, CCCD 012345678901..."'
        className="w-full px-3 py-2 border border-[var(--vg-border)] rounded-lg text-xs bg-[var(--vg-surface)] text-[var(--vg-text)] focus:outline-none focus:border-[var(--vg-accent)] focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] resize-none"
        onKeyDown={(e) => {
          if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleSubmit();
        }}
      />
      <div className="flex items-center justify-between gap-2">
        <p className="text-[10px] text-[var(--vg-text-muted)]">
          AI chỉ đề xuất giá trị nháp — hãy kiểm tra lại từng trường trước khi tiền kiểm.
        </p>
        <button
          type="button"
          onClick={handleSubmit}
          disabled={isBusy || !text.trim()}
          className="shrink-0 px-3.5 py-1.5 bg-[var(--vg-accent)] text-white text-xs font-bold rounded-lg hover:bg-[var(--vg-accent-hover)] transition-all disabled:bg-zinc-200 disabled:text-zinc-400 focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] outline-none"
        >
          {isBusy ? "Đang trích xuất..." : "Điền tự động"}
        </button>
      </div>
    </div>
  );
}
