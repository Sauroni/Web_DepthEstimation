from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config
conf = get_config("zoedepth_nk", "infer")
model_zoe_nk = build_model(conf)