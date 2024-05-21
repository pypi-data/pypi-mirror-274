import os, contextvars

DEFAULT_API_URL = "https://api.lunary.ai"

class Config:
  def __init__(self, app_id: str | None = None, verbose: bool = False, api_url: str | None = None, disable_ssl_verify: bool | None = None):
      self.app_id = (app_id or
                      os.environ.get("LUNARY_PRIVATE_KEY") or
                      os.environ.get("LUNARY_PUBLIC_KEY") or
                      os.getenv("LUNARY_APP_ID"))
      self.verbose = verbose or (os.getenv('LUNARY_VERBOSE') == "True")
      self.api_url = api_url or os.getenv("LUNARY_API_URL") or DEFAULT_API_URL
      self.disable_ssl_verify = False
      # self.disable_ssl_verify = disable_ssl_verify if disable_ssl_verify is not None else (True if os.environ.get("DISABLE_SSL_VERIFY") == "True" else False)

config_ctx = contextvars.ContextVar("config", default=Config())

def get_config() -> Config:
  return config_ctx.get()

def set_config(app_id: str | None = None, verbose: str | None = None, api_url: str | None = None, disable_ssl_verify: bool | None = None) -> None:
  config_ctx.set(Config(app_id, verbose, api_url, disable_ssl_verify))
