import gradio as gr

from pipelines.model import ControlAnimationModel, ModelType
from app_pose import create_demo as create_demo_pose
from app_text_to_video import create_demo as create_demo_text_to_video
from app_control_animation import create_demo as create_demo_animation
import argparse
import os
import jax.numpy as jnp

huggingspace_name = os.environ.get("SPACE_AUTHOR_NAME") 
on_huggingspace = huggingspace_name if huggingspace_name is not None else False

model = ControlAnimationModel(device='cuda', dtype=jnp.float16)

parser = argparse.ArgumentParser()
parser.add_argument('--public_access',
                    action='store_true',
                    help="if enabled, the app can be access from a public url",
                    default=False)
args = parser.parse_args()


with gr.Blocks(css='style.css') as demo:

    # gr.HTML(
    #     """
    #     <div style="text-align: center; max-width: 1200px; margin: 20px auto;">
    #     <h1 style="font-weight: 900; font-size: 3rem; margin: 0rem">
    #         <a href="https://github.com/Picsart-AI-Research/Text2Video-Zero" style="color:blue;">Text2Video-Zero</a> 
    #     </h1>
    #     <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
    #     Levon Khachatryan<sup>1*</sup>, Andranik Movsisyan<sup>1*</sup>, Vahram Tadevosyan<sup>1*</sup>, Roberto Henschel<sup>1*</sup>, Zhangyang Wang<sup>1,2</sup>, Shant Navasardyan<sup>1</sup>
    #     and <a href="https://www.humphreyshi.com/home">Humphrey Shi</a><sup>1,3,4</sup>
    #     </h2>
    #     <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
    #     <sup>1</sup>Picsart AI Resarch (PAIR), <sup>2</sup>UT Austin, <sup>3</sup>U of Oregon, <sup>4</sup>UIUC
    #     </h2>
    #     <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
    #     [<a href="https://arxiv.org/abs/2303.13439" style="color:blue;">arXiv</a>] 
    #     [<a href="https://github.com/Picsart-AI-Research/Text2Video-Zero" style="color:blue;">GitHub</a>]
    #     </h2>
    #     <h2 style="font-weight: 450; font-size: 1rem; margin-top: 0.5rem; margin-bottom: 0.5rem">
    #     We built <b>Text2Video-Zero</b>,  a first zero-shot text-to-video synthesis diffusion framework, that enables low cost yet high-quality and consistent video generation with only pre-trained text-to-image diffusion models without any training on videos or optimization!
    #     Text2Video-Zero also naturally supports cool extension works of pre-trained text-to-image models such as Instruct Pix2Pix, ControlNet and DreamBooth, and based on which we present Video Instruct Pix2Pix, Pose Conditional, Edge Conditional and, Edge Conditional and DreamBooth Specialized applications.
    #     We hope our Text2Video-Zero will further democratize AI and empower the creativity of everyone by unleashing the zero-shot video generation and editing capacity of the amazing text-to-image models and encourage future research!
    #     </h2>
    #     </div>
    #     """)

    if on_huggingspace:
        gr.HTML("""
        <p>For faster inference without waiting in queue, you may duplicate the space and upgrade to GPU in settings.
        <br/>
        <a href="https://huggingface.co/spaces/PAIR/Text2Video-Zero?duplicate=true">
        <img style="margin-top: 0em; margin-bottom: 0em" src="https://bit.ly/3gLdBN6" alt="Duplicate Space"></a>
        </p>""")

    # NOTE: In our final demo we should consider removing zero-shot t2v and pose conditional
    with gr.Tab('Control Animation'):
        create_demo_animation(model)
    with gr.Tab('Zero-Shot Text2Video'):
        create_demo_text_to_video(model)
    with gr.Tab('Pose Conditional'):
        create_demo_pose(model)

if on_huggingspace:
    demo.queue(max_size=20)
    demo.launch(debug=True)
else:
    _, _, link = demo.queue(api_open=False).launch(
        file_directories=['temporal'], share=args.public_access,
        debug=True)
    print(link)