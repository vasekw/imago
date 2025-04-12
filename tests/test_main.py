import pytest
from unittest.mock import patch


@pytest.fixture
def mock_uvicorn():
    with patch("uvicorn.run") as mock_run:
        yield mock_run


def test_main(mock_uvicorn):
    from imago.__main__ import main
    from imago.settings import settings

    main()

    # Check if uvicorn.run was called with the correct arguments
    mock_uvicorn.assert_called_once_with(
        "imago.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )
