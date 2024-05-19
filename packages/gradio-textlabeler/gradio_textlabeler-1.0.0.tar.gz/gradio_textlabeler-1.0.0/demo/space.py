
import gradio as gr
from app import demo as app
import os

_docs = {'TextLabeler': {'description': 'Creates a dynamic table where text elements can be labeled with a set of predefined labels', 'members': {'__init__': {'label_choices': {'type': 'list[str] | None', 'default': 'None', 'description': None}, 'value': {'type': 'list[LabeledValue] | None', 'default': 'None', 'description': 'Set of text-label pairs in the form of LabeledValues. If a "text" is intentionally not labeled, the "label" should be set to None.'}, 'allow_duplicate_labels': {'type': 'bool', 'default': 'False', 'description': 'If True, allows the same label to be used for multiple text entries.'}, 'unlabelled_value_display': {'type': 'str', 'default': '"Unlabeled"', 'description': 'The label to display for text entries that are not labeled.'}, 'text_column_header': {'type': 'str', 'default': '"Text"', 'description': 'The header to display for the text column.'}, 'label_column_header': {'type': 'str', 'default': '"Label"', 'description': 'The header to display for the label column.'}, 'text_column_width': {'type': 'str', 'default': '"60%"', 'description': 'The width of the text column.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'component name in interface.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display the component label.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, choices in this dropdown will be selectable; if False, selection will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}}, 'postprocess': {'value': {'type': 'TextLabelerData', 'description': "The output data received by the component from the user's function in the backend."}}, 'preprocess': {'return': {'type': 'TextLabelerData', 'description': "The preprocessed input data sent to the user's function in the backend."}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the TextLabeler changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the TextLabeler is focused.'}}}, '__meta__': {'additional_interfaces': {'LabeledValue': {'source': 'class LabeledValue(BaseModel):\n    text: str\n    label: str | None'}, 'TextLabelerData': {'source': 'class TextLabelerData(GradioRootModel):\n    root: List[LabeledValue]', 'refs': ['LabeledValue']}}, 'user_fn_refs': {'TextLabeler': ['TextLabelerData']}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_textlabeler`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%201.0.0%20-%20orange"> <a href="https://github.com/amithkk/gradio_textlabeler/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 
</div>

A Gradio custom component to help you label text snippets inline
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_textlabeler
```

## Usage

```python
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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `TextLabeler`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["TextLabeler"]["members"]["__init__"], linkify=['LabeledValue', 'TextLabelerData'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["TextLabeler"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, the preprocessed input data sent to the user's function in the backend.
- **As output:** Should return, the output data received by the component from the user's function in the backend.

 ```python
def predict(
    value: TextLabelerData
) -> TextLabelerData:
    return value
```
""", elem_classes=["md-custom", "TextLabeler-user-fn"], header_links=True)




    code_LabeledValue = gr.Markdown("""
## `LabeledValue`
```python
class LabeledValue(BaseModel):
    text: str
    label: str | None
```""", elem_classes=["md-custom", "LabeledValue"], header_links=True)

    code_TextLabelerData = gr.Markdown("""
## `TextLabelerData`
```python
class TextLabelerData(GradioRootModel):
    root: List[LabeledValue]
```""", elem_classes=["md-custom", "TextLabelerData"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            LabeledValue: [], 
            TextLabelerData: ['LabeledValue'], };
    const user_fn_refs = {
          TextLabeler: ['TextLabelerData'], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
