import gradio as gr
from tools.MilvusTools import MilvusTools
from tools.ResNetEmbeding import ResNetEmbeding

milvusTool = MilvusTools()
resnet = ResNetEmbeding("C:/TicketMgr/ML_Learning/picSearch-main/model/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5")

def seach(path):
    emb = resnet.extract_feature(path, distant=False)
    res = milvusTool.search("picture", "pic_vec", [emb])
    return res


if __name__ == '__main__':
    demo = gr.Interface(title="Search for images by image",
                        css="",
                        fn=seach,
                        inputs=[gr.Image(type="filepath", label="Picture")],
                        outputs=[gr.Image(type="filepath", label="Picture") for _ in range(4)])

    demo.launch(share=True)
