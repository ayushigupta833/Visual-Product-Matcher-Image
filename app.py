import gradio as gr
from matcher.recommender import get_similar_images  # adjust import path

def recommend(image):
    results = get_similar_images(image)  # return list of image paths/URLs
    return results

demo = gr.Interface(
    fn=recommend,
    inputs=gr.Image(type="filepath"),
    outputs=gr.Gallery(label="Top Matches").style(grid=(2, 2)),
    title="Visual Product Matcher",
    description="Upload an image and get visually similar products."
)

if __name__ == "__main__":
    demo.launch()
