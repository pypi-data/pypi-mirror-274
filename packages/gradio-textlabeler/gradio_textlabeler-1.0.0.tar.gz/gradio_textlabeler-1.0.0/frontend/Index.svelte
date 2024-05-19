<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block, BlockTitle } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import Labeler from "./Labeler.svelte";

	export let label = "Dropdown";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { text: string; label: string }[];
	export let label_choices: string[];
	export let text_column_width: string;
	export let allow_duplicate_labels: boolean;
	export let unlabelled_value_display: string;
	export let text_column_header: string;
	export let label_column_header: string;

	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{
		change: string;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let interactive: boolean;

	const container = true;

	function handle_change(): void {
		gradio.dispatch("change");
	}

	$: value, handle_change();
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	padding={container}
	allow_overflow={false}
	{scale}
	{min_width}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() =>
				gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<BlockTitle {show_label} info={undefined}>{label}</BlockTitle>
	<Labeler
		labels={label_choices}
		onlySelectLabelOnce={!allow_duplicate_labels}
		textColumnHeader={text_column_header}
		textColumnWidth={text_column_width}
		labelColumnHeader={label_column_header}
		unlabelledValueDisplay={unlabelled_value_display}
		bind:value
		{interactive}
	></Labeler>
</Block>

<style>
</style>
