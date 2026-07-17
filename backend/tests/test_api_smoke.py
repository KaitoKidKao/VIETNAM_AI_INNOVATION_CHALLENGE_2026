from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_procedures_lists_the_three_mvp_packs() -> None:
    response = client.get("/v1/procedures")

    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {
        "dang-ky-khai-sinh",
        "dang-ky-thuong-tru",
        "dang-ky-ho-kinh-doanh",
    }


def test_checklist_returns_a_known_pack_and_rejects_an_unknown_pack() -> None:
    known = client.post(
        "/v1/procedures/dang-ky-khai-sinh/checklist",
        json={"procedure_id": "dang-ky-khai-sinh", "clarification_answers": {}},
    )
    unknown = client.post(
        "/v1/procedures/unknown/checklist",
        json={"procedure_id": "unknown", "clarification_answers": {}},
    )

    assert known.status_code == 200
    assert known.json()["procedure_id"] == "dang-ky-khai-sinh"
    assert unknown.status_code == 404


def test_intake_requests_clarification_for_supported_and_unknown_needs() -> None:
    known = client.post(
        "/v1/intake/turn",
        json={
            "session_id": "synthetic-session",
            "messages": [{"role": "user", "content": "Tôi muốn đăng ký khai sinh"}],
        },
    )
    unknown = client.post(
        "/v1/intake/turn",
        json={
            "session_id": "synthetic-session",
            "messages": [{"role": "user", "content": "Tôi cần một thủ tục khác"}],
        },
    )

    assert known.status_code == 200
    assert known.json()["detected_procedure_id"] == "dang-ky-khai-sinh"
    assert known.json()["trust_state"] == "need_more_information"
    assert unknown.status_code == 200
    assert unknown.json()["detected_procedure_id"] is None
    assert unknown.json()["trust_state"] == "need_more_information"


def test_precheck_returns_deterministic_findings() -> None:
    invalid = client.post(
        "/v1/applications/validate",
        json={"procedure_id": "dang-ky-khai-sinh", "form_data": {}},
    )
    valid = client.post(
        "/v1/applications/validate",
        json={
            "procedure_id": "dang-ky-khai-sinh",
            "form_data": {
                "ho_ten_tre": "Nguyễn An",
                "ngay_sinh_tre": "2026-07-01",
                "ho_ten_me": "Nguyễn Bình",
            },
        },
    )

    assert invalid.status_code == 200
    assert invalid.json()["is_valid"] is False
    assert {finding["rule_id"] for finding in invalid.json()["findings"]} >= {
        "R-BIRTH-001",
        "R-BIRTH-002",
    }
    assert valid.status_code == 200
    assert valid.json()["is_valid"] is True
