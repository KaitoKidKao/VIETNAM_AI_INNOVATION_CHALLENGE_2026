"use client";

import type { TrustState } from "../procedureCase.types";

const VARIANTS: Record<TrustState, { icon: string; label: string; className: string }> = {
  verified_guidance: {
    icon: "✅",
    label: "Đã xác minh nguồn",
    className: "bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200/60 text-emerald-600",
  },
  need_more_information: {
    icon: "❓",
    label: "Cần thêm thông tin",
    className: "bg-warning-bg border-warning-border text-warning",
  },
  official_review_required: {
    icon: "⚠️",
    label: "Cần cơ quan xem xét",
    className: "bg-error-bg border-error-border text-error",
  },
};

interface TrustBadgeProps {
  trustState: TrustState | null;
  fixtureMode?: boolean;
}

export function resolveDisplayedTrustState(
  trustState: TrustState,
  fixtureMode?: boolean,
): TrustState {
  if (fixtureMode && trustState === "verified_guidance") {
    return "official_review_required";
  }
  return trustState;
}

export default function TrustBadge({ trustState, fixtureMode }: TrustBadgeProps) {
  if (!trustState) return null;
  const variant = VARIANTS[resolveDisplayedTrustState(trustState, fixtureMode)];

  return (
    <div className="inline-flex items-center gap-1.5 flex-wrap">
      <span
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl border text-[10px] font-bold ${variant.className}`}
      >
        <span aria-hidden="true">{variant.icon}</span>
        <span>{variant.label}</span>
      </span>
      {fixtureMode && (
        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-xl border border-border-slate bg-neutral-bg text-[10px] font-bold text-foreground/60">
          <span aria-hidden="true">🧪</span>
          <span>Chế độ demo dữ liệu mẫu</span>
        </span>
      )}
    </div>
  );
}
