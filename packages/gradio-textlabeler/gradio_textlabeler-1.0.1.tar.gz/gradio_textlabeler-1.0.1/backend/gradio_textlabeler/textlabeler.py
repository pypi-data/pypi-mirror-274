from __future__ import annotations

import warnings
from typing import Any, Callable, List, TypedDict

from pydantic import BaseModel

from gradio.components.base import FormComponent
from gradio.events import Events
from gradio.data_classes import GradioRootModel


class LabeledValue(BaseModel):
    text: str
    label: str | None


class TextLabelerData(GradioRootModel):
    root: List[LabeledValue]


class TextLabeler(FormComponent):
    """
    Creates a dynamic table where text elements can be labeled with a set of predefined labels
    """

    EVENTS = [Events.change, Events.submit]
    data_model = TextLabelerData

    def __init__(
        self,
        label_choices: list[str] | None = None,
        *,
        value: List[LabeledValue] | None = None,
        allow_duplicate_labels: bool = False,
        unlabelled_value_display: str = "Unlabeled",
        text_column_header: str = "Text",
        label_column_header: str = "Label",
        text_column_width: str = "60%",
        label: str | None = None,
        info: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            choices: A list of string options to choose labels from.
            value: Set of text-label pairs in the form of LabeledValues. If a "text" is intentionally not labeled, the "label" should be set to None.
            allow_duplicate_labels: If True, allows the same label to be used for multiple text entries.
            unlabelled_value_display: The label to display for text entries that are not labeled.
            text_column_header: The header to display for the text column.
            label_column_header: The header to display for the label column.
            text_column_width: The width of the text column.
            label: component name in interface.
            info: additional component description.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display the component label.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, choices in this dropdown will be selectable; if False, selection will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
        """
        self.label_choices = label_choices
        self.allow_duplicate_labels = allow_duplicate_labels
        self.unlabelled_value_display = unlabelled_value_display
        self.text_column_width = text_column_width
        self.text_column_header = text_column_header
        self.label_column_header = label_column_header
        if value:
            [self._warn_if_invalid_choice(y) for y in value]
            self._warn_if_duplicate_labels(value)
        super().__init__(
            label=label,
            info=info,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
        )

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        return None

    def preprocess(self, payload: Any) -> TextLabelerData:
        return payload

    def _warn_if_invalid_choice(self, y: LabeledValue):
        if y["label"] not in self.label_choices and y["label"] is not None:
            warnings.warn(
                f"The label '{y['label']}' for text '{y['text']}' passed into TextLabeler() is not in the list of valid labels. Please update the list of choices to include '{y['label']}'."
            )

    def _warn_if_duplicate_labels(self, value: List[LabeledValue]):
        if not self.allow_duplicate_labels:
            labels = [y["label"] for y in value if y["label"] is not None]
            if len(labels) != len(set(labels)):
                warnings.warn(
                    "Duplicate labels detected in TextLabeler(). To allow duplicate labels, set allow_duplicate_labels=True."
                )

    def postprocess(self, value: TextLabelerData):
        if value:
            return value
        else:
            return []
