
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Define any config here.

    See here for documentation:
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    # KNative assigns a $PORT environment variable to the container
    port: int = Field(default=8082, env="PORT",description="Gradio App Server Port")
    sp_model_path: str = 'models/sp_wav2vec.ckpt'
    labels_path: str = 'misc/total_spkrinfo.list'
    example_dir: str = 'examples'

    # model configs
    slice_seconds: int = 5
    slice_window: int = 1


config = BaseConfig()