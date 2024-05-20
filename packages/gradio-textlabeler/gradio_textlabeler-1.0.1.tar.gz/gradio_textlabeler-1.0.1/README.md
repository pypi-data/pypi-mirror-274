---
tags: [gradio-custom-component, TextLabeler]
title: gradio_textlabeler
short_description: A Gradio custom component to help you label text snippets
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_textlabeler`
<a href="https://pypi.org/project/gradio_textlabeler/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_textlabeler"></a> <a href="https://github.com/amithkk/gradio_textlabeler/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 

A Gradio custom component to help you label text snippets inline

## Installation

```bash
pip install gradio_textlabeler
```

## Usage

```python
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

```

## `TextLabeler`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>label_choices</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
list[LabeledValue] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Set of text-label pairs in the form of LabeledValues. If a "text" is intentionally not labeled, the "label" should be set to None.</td>
</tr>

<tr>
<td align="left"><code>allow_duplicate_labels</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, allows the same label to be used for multiple text entries.</td>
</tr>

<tr>
<td align="left"><code>unlabelled_value_display</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"Unlabeled"</code></td>
<td align="left">The label to display for text entries that are not labeled.</td>
</tr>

<tr>
<td align="left"><code>text_column_header</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"Text"</code></td>
<td align="left">The header to display for the text column.</td>
</tr>

<tr>
<td align="left"><code>label_column_header</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"Label"</code></td>
<td align="left">The header to display for the label column.</td>
</tr>

<tr>
<td align="left"><code>text_column_width</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"60%"</code></td>
<td align="left">The width of the text column.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">component name in interface.</td>
</tr>

<tr>
<td align="left"><code>info</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">additional component description.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display the component label.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, choices in this dropdown will be selectable; if False, selection will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the TextLabeler changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `submit` | This listener is triggered when the user presses the Enter key while the TextLabeler is focused. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, the preprocessed input data sent to the user's function in the backend.
- **As input:** Should return, the output data received by the component from the user's function in the backend.

 ```python
 def predict(
     value: TextLabelerData
 ) -> TextLabelerData:
     return value
 ```
 

## `LabeledValue`
```python
class LabeledValue(BaseModel):
    text: str
    label: str | None
```

## `TextLabelerData`
```python
class TextLabelerData(GradioRootModel):
    root: List[LabeledValue]
```
