from gradio_textlabeler.textlabeler import TextLabelerData
import gradio as gr
from gradio_textlabeler import TextLabeler


example = TextLabeler().example_value()

demo = gr.Interface(
    lambda x: x,
    TextLabeler(
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
    ),  
    TextLabeler(),  
)


if __name__ == "__main__":
    demo.launch()
