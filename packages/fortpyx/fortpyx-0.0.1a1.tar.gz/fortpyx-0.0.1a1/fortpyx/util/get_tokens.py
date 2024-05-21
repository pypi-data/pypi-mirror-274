import json
import threading
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Sequence, Tuple
from urllib.parse import urlparse, parse_qs

from fortpyx.fortpyx import Fortpyx

authorization_code = None


class TokenCallbackServer:
    class AuthorizationCodeHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            global authorization_code  # noqa

            qs = urlparse(self.path).query
            parsed_qs = parse_qs(qs)
            state = parsed_qs["state"][0]

            if state != "fortpyx_state":
                msg = "Bad state in redirect query string"
                raise ValueError(msg)

            error = parsed_qs.get("error")
            if error:
                description = parsed_qs["error_description"][0]
                msg = f"An error occured: {error[0]} ({description})"
                raise ValueError(msg)

            code = parsed_qs["code"][0]

            response_body = {"code": code}

            authorization_code = code

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_body).encode())
            self.server.shutdown()

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        server_port: int = 9573,
    ):
        assert server_port
        assert client_id
        assert client_secret

        self.__client_id = client_id
        self.__client_secret = client_secret

        self.__server_port = server_port

    def get_tokens(self, scopes: Sequence[str]) -> Tuple[str, str]:
        assert (
            scopes is not None and len(scopes) > 0
        ), "Scopes must be a sequence with at least one entry"

        auth_code_server_address = ("", self.__server_port)
        auth_code_server = ThreadingHTTPServer(
            auth_code_server_address,
            RequestHandlerClass=TokenCallbackServer.AuthorizationCodeHandler,
        )
        auth_code_server_thread = threading.Thread(
            target=auth_code_server.serve_forever, daemon=True
        )
        auth_code_server_thread.start()

        fortpyx = Fortpyx(
            client_id=self.__client_id,
            client_secret=self.__client_secret,
        )

        redirect_uri = f"http://localhost:{self.__server_port}"
        auth_code_url = fortpyx.get_authorization_url(
            redirect_uri=redirect_uri,
            scopes=scopes,
        )

        webbrowser.open(auth_code_url, new=1)
        auth_code_server_thread.join()

        assert authorization_code is not None
        return fortpyx.get_tokens(
            authorization_code=authorization_code or "",
            redirect_uri=redirect_uri,
        )
