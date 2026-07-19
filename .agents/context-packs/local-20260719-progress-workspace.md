# Context Pack - local-20260719-progress-workspace

## Identity

- Task ID: `local-20260719-progress-workspace`
- Owner tam thoi: Codex / user-requested
- Mode hien tai: `verify-demo`
- Base ref / commit: `cao` / `f681e21`
- Branch / worktree: `feature/local-20260719-progress-workspace` / `C:\tmp\vaic-progress-workspace`
- AI Log member / tool binding / readiness: `cao-codex` / `codex manual` / doctor strict pass

## Muc tieu va ranh gioi

- Muc tieu: thay khoang trong ben trai cua khu vuc to khai bang timeline tien trinh day du; giu form va tien kiem ben phai.
- Non-goals: khong sua backend, API, schema, data, trust policy, luong U1/U2/U3 hoac deploy.
- Acceptance criteria:
  - Desktop hien timeline doc 6 buoc, buoc hien tai va buoc da hoan thanh lay tu state hien co.
  - Form va precheck giu nguyen hanh vi, co them khong gian doc huu dung.
  - Mobile/tablet dung progress summary gon, khong co horizontal overflow.
  - Khong lam thay doi session state khi responsive layout thay doi.
  - Frontend test, typecheck, lint va build pass.
- Constraints: frontend-only; dung token `--vg-*`; light-only; khong them dependency; giu mot primary action cho moi trang thai.
- Stop condition / blocker can hoi peer: dung neu can doi API/schema, them asset/dependency, hoac thay doi nghiep vu cua review gate.

## Scope da claim

- Files/areas duoc phep cham:
  - `frontend/src/features/procedure-case/ProcedureWorkspace.tsx`
  - `frontend/src/features/procedure-case/progress/**`
  - `frontend/src/features/procedure-case/procedureCase.selectors.ts`
  - `frontend/src/features/procedure-case/procedureCase.selectors.test.ts`
  - `frontend/src/features/procedure-case/form/DynamicFormRenderer.tsx`
  - test frontend lien quan neu can
  - context pack va design review cua task
- API, schema hoac contract lien quan: khong co.
- Khong duoc cham: `backend/**`, `data/**`, provider/env, deploy, public API contract.
- Risk: `isolated`
- Decision Log lien quan: D-022 (light-only); khong can Decision moi.

## Context duoc chon loc

| Nguon | File / line / ref | Ly do can doc |
| --- | --- | --- |
| Product | `docs/PRODUCT.md` | Doi tuong, clarity va accessibility. |
| Design | `docs/DESIGN.md` | Civic palette, responsive, panel va empty-state rules. |
| Architecture | `docs/ai/ARCHITECTURE.md` | Giu nguyen frontend/backend boundary. |
| Decision | `docs/ai/DECISIONS.md` D-022 | Giao dien light-only. |
| Workspace | `frontend/src/features/procedure-case/ProcedureWorkspace.tsx` | Layout hien tai va diem tich hop. |
| Selectors | `frontend/src/features/procedure-case/procedureCase.selectors.ts` | Nguon stage hien co, khong tao state moi. |

## Dependencies va resource claim

- Depends on / blocked by: commit `f681e21` da co tren `cao`.
- Shared resource: none.
- Claim owner + thoi han: Codex trong task hien tai.
- Release: khi handoff sau test va UI audit.

## Kiem chung va handoff

- Commands / manual checks: `npm run test`, `npm run typecheck`, `npm run lint`, `npm run build`, `python scripts/ci/validate_repo.py`, Impeccable target audit; fixture preview tai desktop/mobile neu browser local san sang.
- Demo impact va rollback: chi thay layout; rollback bang revert commit task.
- Evidence / ket qua:
  - `npm run test`: 5 files, 97 tests passed, gom regression test cho U3 completion.
  - `npm run typecheck`: passed.
  - `npm run lint`: passed.
  - `npm run build -- --webpack`: production build passed trong worktree.
  - Impeccable `layout,type`: 0 findings; report tai `docs/design/reviews/local-20260719-progress-workspace-impeccable.md`.
  - Dev preview tra HTTP 200 tai fixture `form_editing`; browser-control khong khoi tao duoc nen chua co screenshot runtime desktop/mobile.
- AI-Log ID + capture status: manual prompt `prompt-881043d7e5aecdc723c68d4b` da ghi; commit hook se sinh log ID va trailers.
- Files, API va resources da cham:
  - `frontend/src/features/procedure-case/ProcedureWorkspace.tsx`
  - `frontend/src/features/procedure-case/progress/ProgressWorkspaceRail.tsx`
  - `frontend/src/features/procedure-case/form/DynamicFormRenderer.tsx`
  - `frontend/src/features/procedure-case/procedureCase.selectors.ts`
  - `frontend/src/features/procedure-case/procedureCase.selectors.test.ts`
  - `docs/design/reviews/local-20260719-progress-workspace-impeccable.md`
  - Context Pack nay
- Claims da release: source claim release sau khi commit/handoff.
- Viec tiep theo: repo guard, commit, tich hop vao `cao`, chay lai frontend checks trong workspace chinh.
