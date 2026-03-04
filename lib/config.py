from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_level: str = "DEBUG"
    log_module_name: str = "roku-api"
    roku_hosts: str = ""
    host: str = "0.0.0.0"
    port: int = 8080

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def get_roku_devices(self) -> list[dict]:
        devices = []
        for entry in self.roku_hosts.split(","):
            parts = entry.strip().split(":")
            if len(parts) == 2:
                devices.append({"id": parts[0], "host": parts[1]})
        return devices

    def get_roku_lookup(self) -> dict[str, str]:
        lookup = {}
        for entry in self.roku_hosts.split(","):
            parts = entry.strip().split(":")
            if len(parts) == 2:
                lookup[parts[0]] = parts[1]
        return lookup


settings = Settings()
