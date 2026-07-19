import type { ProgressStage } from "../procedureCase.selectors";
import { CheckCircleIcon, ShieldIcon } from "../icons";

const WORKFLOW_STAGES = [
  {
    id: 1,
    label: "Xác định thủ tục",
    description: "Mô tả nhu cầu để xác định đúng thủ tục cần thực hiện.",
  },
  {
    id: 2,
    label: "Bổ sung điều kiện",
    description: "Trả lời các câu hỏi cần thiết cho trường hợp của bạn.",
  },
  {
    id: 3,
    label: "Chuẩn bị giấy tờ",
    description: "Rà soát thành phần hồ sơ bắt buộc và tùy chọn.",
  },
  {
    id: 4,
    label: "Điền tờ khai",
    description: "Hoàn thiện thông tin trên biểu mẫu của thủ tục.",
  },
  {
    id: 5,
    label: "Kiểm tra sơ bộ",
    description: "Phát hiện dữ liệu thiếu hoặc chưa đúng trước khi nộp.",
  },
  {
    id: 6,
    label: "Hoàn tất xem trước",
    description: "Xem lại kết quả và tiếp tục trên kênh chính thức.",
  },
] as const;

interface ProgressWorkspaceRailProps {
  stage: ProgressStage & { total: number };
  procedureName?: string;
  degraded?: boolean;
}

export default function ProgressWorkspaceRail({
  stage,
  procedureName,
  degraded = false,
}: ProgressWorkspaceRailProps) {
  const completedCount = stage.id === stage.total ? stage.total : stage.id - 1;
  const activeStep = WORKFLOW_STAGES.find((item) => item.id === stage.id) ?? WORKFLOW_STAGES[0];

  return (
    <>
      <section
        aria-label="Tiến trình hồ sơ"
        className="xl:hidden rounded-xl border border-[var(--vg-border)] bg-[var(--vg-surface)] p-4"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-[10px] font-bold uppercase text-[var(--vg-text-muted)]">Tiến trình hồ sơ</p>
            <h2 className="mt-1 truncate text-sm font-bold text-[var(--vg-text)]">{activeStep.label}</h2>
            <p className="mt-1 text-xs leading-relaxed text-[var(--vg-text-secondary)]">
              {activeStep.description}
            </p>
          </div>
          <span className="shrink-0 text-xs font-bold text-[var(--vg-accent)]">
            {completedCount}/{stage.total}
          </span>
        </div>
        <div className="mt-4 grid grid-cols-6 gap-1.5" aria-hidden="true">
          {WORKFLOW_STAGES.map((item) => (
            <span
              key={item.id}
              className={`h-1.5 rounded-full ${
                item.id <= stage.id ? "bg-[var(--vg-accent)]" : "bg-[var(--vg-border)]"
              }`}
            />
          ))}
        </div>
        {degraded && (
          <p className="mt-3 text-[11px] font-semibold text-[var(--vg-error)]">Kết nối đang gián đoạn</p>
        )}
      </section>

      <section
        aria-label="Tiến trình hồ sơ"
        className="hidden min-h-[560px] flex-col rounded-xl border border-[var(--vg-border)] bg-[var(--vg-surface)] p-5 xl:flex"
      >
        <header className="border-b border-[var(--vg-border)] pb-5">
          <p className="text-[11px] font-bold uppercase text-[var(--vg-text-muted)]">Tiến trình hồ sơ</p>
          <div className="mt-4 flex items-center gap-4">
            <div
              className={`flex h-16 w-16 shrink-0 items-center justify-center rounded-full border-4 text-sm font-bold ${
                completedCount === stage.total
                  ? "border-[var(--vg-success)] text-[var(--vg-success)]"
                  : "border-[var(--vg-accent-soft)] border-t-[var(--vg-accent)] text-[var(--vg-accent)]"
              }`}
              aria-label={`${completedCount} trên ${stage.total} bước hoàn thành`}
            >
              {completedCount}/{stage.total}
            </div>
            <div className="min-w-0">
              <h2 className="text-sm font-bold leading-snug text-[var(--vg-text)]">
                {procedureName ? `${procedureName} đang được chuẩn bị` : "Hồ sơ của bạn đang được chuẩn bị"}
              </h2>
              <p className="mt-1 text-xs text-[var(--vg-text-secondary)]">
                Bước hiện tại: {activeStep.label}
              </p>
            </div>
          </div>
          {degraded && (
            <p className="mt-3 text-[11px] font-semibold text-[var(--vg-error)]">Kết nối đang gián đoạn</p>
          )}
        </header>

        <ol className="mt-5 flex-1" aria-label="Các bước chuẩn bị hồ sơ">
          {WORKFLOW_STAGES.map((item, index) => {
            const isComplete = item.id < stage.id || completedCount === stage.total;
            const isCurrent = item.id === stage.id;

            return (
              <li
                key={item.id}
                className="flex gap-3"
                aria-current={isCurrent ? "step" : undefined}
              >
                <div className="flex w-7 shrink-0 flex-col items-center">
                  <span
                    className={`flex h-7 w-7 items-center justify-center rounded-full border text-xs font-bold ${
                      isComplete
                        ? "border-[var(--vg-success)] bg-[var(--vg-success)] text-white"
                        : isCurrent
                          ? "border-[var(--vg-accent)] bg-[var(--vg-accent-soft)] text-[var(--vg-accent)]"
                          : "border-[var(--vg-border-strong)] bg-[var(--vg-surface)] text-[var(--vg-text-muted)]"
                    }`}
                  >
                    {isComplete ? <CheckCircleIcon className="h-4 w-4" /> : item.id}
                  </span>
                  {index < WORKFLOW_STAGES.length - 1 && (
                    <span
                      className={`min-h-8 w-px flex-1 ${
                        item.id < stage.id ? "bg-[var(--vg-success)]" : "bg-[var(--vg-border)]"
                      }`}
                      aria-hidden="true"
                    />
                  )}
                </div>
                <div className="min-w-0 pb-4 pt-0.5">
                  <h3
                    className={`text-xs font-bold ${
                      isCurrent ? "text-[var(--vg-accent)]" : "text-[var(--vg-text)]"
                    }`}
                  >
                    {item.id}. {item.label}
                  </h3>
                  <p className="mt-1 text-[11px] leading-relaxed text-[var(--vg-text-muted)]">
                    {item.description}
                  </p>
                </div>
              </li>
            );
          })}
        </ol>

        <div className="mt-2 flex items-start gap-2.5 border-t border-[var(--vg-border)] pt-4 text-[11px] leading-relaxed text-[var(--vg-text-muted)]">
          <ShieldIcon className="mt-0.5 h-4 w-4 shrink-0 text-[var(--vg-gold)]" />
          <span>Dữ liệu bản thử nghiệm chỉ được lưu tạm trong phiên trình duyệt.</span>
        </div>
      </section>
    </>
  );
}
