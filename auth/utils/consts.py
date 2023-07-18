from auth.handlers import (
    handle_sign_in,
    handle_sign_up
)

USER_INTENT = {
    "sign up": handle_sign_up,
    "sign in": handle_sign_in
}
