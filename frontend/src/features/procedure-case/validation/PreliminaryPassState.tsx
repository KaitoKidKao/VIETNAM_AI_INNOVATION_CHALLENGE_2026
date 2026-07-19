"use client";

import type { FeedbackReasonCode, TrustMetadata } from "../procedureCase.types";
import { CheckCircleIcon } from "../icons";
import TrustBadge from "../trust/TrustBadge";
import GuidanceDisclaimer from "../trust/GuidanceDisclaimer";
import FeedbackControls from "../feedback/FeedbackControls";
import { FORM_TEMPLATES, OFFICIAL_PORTAL_URL } from "../procedureCase.constants";

interface PreliminaryPassStateProps {
  summaryMessage: string;
  trustMetadata: TrustMetadata | null;
  onConfirmU3: () => void;
  onFeedback: (vote: "up" | "down", reason?: FeedbackReasonCode, note?: string) => void;
  hasConfirmed?: boolean;
  procedureId?: string;
  onStartNew?: () => void;
}

export default function PreliminaryPassState({
  summaryMessage,
  trustMetadata,
  onConfirmU3,
  onFeedback,
  hasConfirmed = false,
  procedureId,
  onStartNew,
}: PreliminaryPassStateProps) {
  const template = procedureId ? FORM_TEMPLATES[procedureId] : undefined;
  return (
    <div className="border border-[var(--vg-success)]/30 bg-[var(--vg-success-soft)] rounded-xl p-4 text-left space-y-3">
      <h5 className="text-xs font-bold flex items-center gap-2 text-[var(--vg-success)]">
        <CheckCircleIcon className="w-4 h-4 shrink-0" />
        Đã vượt qua kiểm tra sơ bộ
      </h5>
      {summaryMessage && !summaryMessage.includes("demo MVP") && !summaryMessage.includes("K1") && (
        <p className="text-[10px] leading-relaxed font-semibold text-[var(--vg-success)]">{summaryMessage}</p>
      )}
      <TrustBadge
        trustState={trustMetadata?.trust_state ?? null}
        fixtureMode={trustMetadata?.fixture_mode}
        demoMode={trustMetadata?.demo_mode}
      />

      {hasConfirmed ? (
        <div className="space-y-3">
          <div className="text-xs font-bold text-[var(--vg-success)] flex items-center gap-1.5">
            <span>✓ Bạn đã hoàn tất xem trước và kiểm tra hồ sơ thành công.</span>
          </div>

          <div className="rounded-lg border border-[var(--vg-border)] bg-[var(--vg-surface)] p-3.5 text-left space-y-2">
            <h6 className="text-[11px] font-bold uppercase tracking-wide text-[var(--vg-text)]">
              Bước tiếp theo để nộp hồ sơ
            </h6>
            <ol className="list-decimal pl-4 space-y-1.5 text-[11px] leading-relaxed text-[var(--vg-text-secondary)]">
              <li>Tải và điền biểu mẫu chính thức theo thông tin bạn vừa kiểm tra.</li>
              <li>Chuẩn bị đầy đủ giấy tờ theo checklist hồ sơ.</li>
              <li>Nộp trực tuyến trên Cổng Dịch vụ công Quốc gia hoặc trực tiếp tại cơ quan tiếp nhận.</li>
            </ol>
          </div>

          <div className="flex flex-wrap gap-2">
            <a
              href={OFFICIAL_PORTAL_URL}
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2 bg-[var(--vg-accent)] text-white text-xs font-bold rounded-lg hover:bg-[var(--vg-accent-hover)] transition-all focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] outline-none"
            >
              Nộp trên Cổng Dịch vụ công ↗
            </a>
            {template && (
              <a
                href={template.href}
                download
                className="px-4 py-2 border border-[var(--vg-accent)] text-[var(--vg-accent)] text-xs font-bold rounded-lg hover:bg-[var(--vg-gold-soft)] transition-all focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] outline-none"
              >
                Tải biểu mẫu chính thức
              </a>
            )}
            {onStartNew && (
              <button
                type="button"
                onClick={onStartNew}
                className="px-4 py-2 border border-[var(--vg-border)] text-[var(--vg-text)] text-xs font-bold rounded-lg hover:bg-[var(--vg-surface-subtle)] transition-all focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] outline-none"
              >
                Làm thủ tục khác
              </button>
            )}
          </div>
        </div>
      ) : (
        <button
          type="button"
          onClick={onConfirmU3}
          className="px-4 py-2 bg-[var(--vg-accent)] text-white text-xs font-bold rounded-lg hover:bg-[var(--vg-accent-hover)] transition-all focus-visible:ring-2 focus-visible:ring-[var(--vg-accent)] outline-none"
        >
          Đã hiểu, hoàn tất xem trước
        </button>
      )}
      <FeedbackControls context="precheck" onSubmit={onFeedback} />
      <GuidanceDisclaimer />
    </div>
  );
}
