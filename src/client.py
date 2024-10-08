import os
import grpc

from skimage import io
from utils_mea import img_np_2_pt

from utils import proj_asset, file2json2obj


def single_channel(pt_image):
    return pt_image[:,:,:, 0:1]

def load_prompt():
    import json
    prompt_file = proj_asset("prompt.json")
    f = open(prompt_file, "r")
    prompt = json.load(f)["prompt"]
    return prompt

def load_image(name):
    img_file = proj_asset(name)
    print(img_file)
    img_np = io.imread(img_file)
    img_pt = img_np_2_pt(img_np, transpose=False, one_minus_one=False)
    img_pt = img_pt.unsqueeze(0)
    return img_pt



import proto.comfy_pb2 as pb2
import proto.comfy_pb2_grpc as pb2_grpc
from utils_mea import img_proto_2_pt, img_pt_2_proto, img_proto_2_np

def _load_credential_from_file(filepath):
    real_path = os.path.abspath(filepath)
    with open(real_path, "rb") as f:
        return f.read()


SERVER_CERTIFICATE = _load_credential_from_file("assets/credentials/localhost.crt")
SERVER_CERTIFICATE_KEY = _load_credential_from_file("assets/credentials/localhost.key")
ROOT_CERTIFICATE = _load_credential_from_file("assets/credentials/root.crt")

import time


def start_client():
    port = 50051

    # spawn assets in fs

    print("+++ Client starting...")
    config = file2json2obj(proj_asset("client_config.json"))
    server_address = config["server_addres"]
    endpoint = f"{server_address}:{port}"

    credentials = grpc.ssl_channel_credentials(ROOT_CERTIFICATE)
    channel_options = [('grpc.ssl_target_name_override', 'localhost')] # tmp workaround
    
    channel = grpc.secure_channel(endpoint, credentials, options=channel_options)
    stub = pb2_grpc.ComfyStub(channel)



    img_pt = load_image('img.png')
    img_proto = img_pt_2_proto(img_pt)

    mask_pt = load_image('mask.png')
    mask_pt = single_channel(mask_pt)
    mask_proto = img_pt_2_proto(mask_pt)
    
    prompt = load_prompt()
    print(prompt)
    img_power = 0.2
    gen_opt = pb2.Options(prompts=[prompt], img_power=img_power)

    tick = time.perf_counter()
    stub.SetImage(img_proto)
    stub.SetMask(mask_proto)
    stub.SetOptions(gen_opt)
    result_proto = stub.UberInpaint(pb2.Empty())
    # result_proto = stub.Img2Img(pb2.Empty())
    # result_proto = stub.Txt2Img(pb2.Empty())
    tock = time.perf_counter()

    inpaint_np = img_proto_2_np(result_proto)
    print(f"+++ Inpainting took {(tock - tick)} s")
    io.imsave('fs/out_img.png', inpaint_np)

