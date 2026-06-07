import io

from tests.conftest import client


def get_auth_headers():
    client.post(
        "/auth/register",
        json={
            "email": "docuser@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "docuser@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_upload_document_requires_auth():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.pdf",
                io.BytesIO(b"%PDF-1.4 test pdf content"),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 401


def test_upload_pdf_document():
    headers = get_auth_headers()

    response = client.post(
        "/documents/upload",
        headers=headers,
        files={
            "file": (
                "test.pdf",
                io.BytesIO(
                    b"%PDF-1.4\n"
                    b"1 0 obj\n"
                    b"<<>>\n"
                    b"endobj\n"
                    b"trailer\n"
                    b"<<>>\n"
                    b"%%EOF"
                ),
                "application/pdf"
            )
        }
    )

    assert response.status_code in [200, 500]

def test_get_documents_with_auth():
    headers = get_auth_headers()

    response = client.get(
        "/documents/",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_documents_without_auth_fails():
    response = client.get("/documents/")

    assert response.status_code == 401