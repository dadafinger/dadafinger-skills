---
name: jp-capture-text-consistency
description: Verify whether Japanese capture labels and surrounding text are reflected consistently between manual documents and requirement sources. Use when the user asks to validate screenshot/capture language, UI label updates, or asks if Japanese capture text matches the specification.
disable-model-invocation: true
---

> Sharing scope: General
> Share policy: share
> Notes: 일본어 캡처 텍스트 정합; 범용

# JP Capture Text Consistency Review

## Goal

Check whether Japanese capture-related terms from the requirements sheet are reflected in manual artifacts, then write a report under `검토 결과 md`.

## Inputs

- Root folder: prefer `~/Desktop/305매뉴얼/`, fallback `~/Desktop/manual/305매뉴얼/`
- Requirements file: `요구사항_*.xlsx` latest non-temp file
- Target files: Japanese manual `.docx` and paired `.pdf` (same base name if available)
- Sheet: `WEB_UI_캡처_Product(TMN 요구사항)`

## Workflow

1. Resolve root and list Japanese manual candidates (`[3.0.5_日本語] ... .docx`), excluding `~$` temp files.
2. Read sheet2 rows with `As-is` and `To-be` values.
3. Extract searchable text:
   - DOCX: flatten `word/document.xml` after removing tags.
   - PDF: use PyMuPDF (`fitz`) when available.
4. For each row, compute:
   - `asis_count` in target text
   - `tobe_count` in target text
   - status:
     - `APPLIED`: `asis_count == 0` and `tobe_count > 0`
     - `RESIDUAL`: `asis_count > 0`
     - `N/A`: both zero
5. Summarize counts and list top residual terms with counts.
6. Write a report to:
   - `검토 결과 md/manual_capture_text_consistency_<YYYY-MM-DD>_<target-id>.md`

## Guardrails

- Do not edit original xlsx/docx/pdf.
- Do not infer text from images with OCR unless explicitly requested.
- Treat frequent generic terms (`削除`, `前に`) as likely context-sensitive; report as residual candidates, not auto-fix directives.
- If PDF is missing, run DOCX-only check and mark PDF section as skipped.

## Report Template

```markdown
# 일본어 캡처-텍스트 일치 검수 보고서

- 대상: <docx filename>
- 기준: <xlsx filename> / 시트2
- 실행 시각: <ISO>

## 요약
- APPLIED: <n>
- RESIDUAL: <n>
- N/A: <n>

## 잔존 대표 항목
- row <n>: `As-is` -> `To-be` (asis=<n>, tobe=<n>)

## 판단
- 캡처/라벨 반영 상태: <문장>
- 후속 확인 필요 항목: <문장>
```
