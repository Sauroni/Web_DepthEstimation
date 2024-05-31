from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config
import torch
from PIL import Image
from werkzeug.datastructures import FileStorage


def GetDepth(img_path):

    img_input = Image.open(img_path).convert("RGB")
    
    # ZoeD_NK
    conf = get_config("zoedepth_nk", "infer")
    model_zoe_nk = build_model(conf)

    ##### sample prediction
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    zoe = model_zoe_nk.to(DEVICE)

    # image = get_image_from_url(URL)  # fetch
    depth = zoe.infer_pil(img_input)

    print(depth)
    output_path = img_path.replace(".jpg",".png")

    from zoedepth.utils.misc import colorize
    Image.fromarray(colorize(depth)).save(output_path)

    return output_path.replace("uploads/","")

