# 임시 문서 생성 도구 Node 모듈 재설치 기록

- 삭제 전 기록 시각: 2026-07-31 21:16
- 원래 사용 위치:
  - `.codex_tmp/ai_quality_workbook`
  - `.codex_tmp/final_reports`
- 두 위치의 최상위 설치 모듈 목록은 동일했습니다.
- 두 위치 모두 `package.json`과 잠금 파일이 없었습니다.
- 설치 모듈 삭제 후 작업용 `.codex_tmp`도 정리했으므로, 필요한 경우 이 폴더의 `installed_modules_codex_tmp_snapshot.txt`를 참고해 새 `package.json`을 만든 뒤 `npm install`을 실행합니다.

이 목록은 강의 프로젝트의 런타임 의존성이 아니라 DOCX·PPTX·PDF·이미지 등을 생성·검토하던 임시 도구 모음입니다.
