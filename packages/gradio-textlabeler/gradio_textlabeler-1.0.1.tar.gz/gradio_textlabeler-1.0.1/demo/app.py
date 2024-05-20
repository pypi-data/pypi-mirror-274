from gradio_textlabeler.textlabeler import TextLabelerData
import gradio as gr
from gradio_textlabeler import TextLabeler


with gr.Blocks() as demo:
    gr.Markdown("abel the tweets as positive, negative, or neutral and click on Submit Labels")
    inp = TextLabeler(
        label="Label these tweets",
        info="Label the tweets as positive, negative, or neutral.",
        label_choices=["Positive", "Negative", "Neutral"],
        value=[
            {"text": "I am extremely mad", "label": "Negative"},
            {
                "text": "This product is the next best thing since sliced bread",
                "label": "Positive",
            },
            {"text": "I don't know how I feel about this", "label": None},
            {"text": "The weather is nice today", "label": None},
            {"text": "I love this song", "label": "Positive"},
            {"text": "I'm not sure what to think", "label": None},
        ],
        allow_duplicate_labels=True,
        unlabelled_value_display="No Label",
        text_column_width="60%",
        text_column_header="Tweet",
        label_column_header="Sentiment",
    )   
    btn = gr.Button("Submit Labels")
    out = TextLabeler(label="Label output example")
   
    btn.click(fn=lambda x:x, inputs=inp, outputs=out)


if __name__ == "__main__":
    demo.launch()
