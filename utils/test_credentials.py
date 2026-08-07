import os


def get_worker_credentials(request):
    """Return credentials for the current pytest-xdist worker.

    Plain pytest runs do not expose ``workerinput``; treat them as the primary
    worker so the same fixtures work both with and without xdist.
    """
    worker_input = getattr(request.config, "workerinput", {}) or {}
    worker_id = worker_input.get("workerid", "master")
    username_var = "USER_NAME_2" if worker_id == "gw1" else "USER_NAME_1"

    email = os.getenv(username_var)
    password = os.getenv("PASSWORD")
    if not email or not password:
        missing = [name for name, value in ((username_var, email), ("PASSWORD", password)) if not value]
        raise RuntimeError(f"Missing required test credentials: {', '.join(missing)}")

    return email, password
