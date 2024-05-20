<script>
    export let onlySelectLabelOnce = false;
    export let value;
    export let interactive = false;
    export let labels;
    export let unlabelledValueDisplay;
    export let textColumnHeader;
    export let textColumnWidth;
    export let labelColumnHeader;
    let selectedLabels = new Set();

    function handleLabelChange(event, index) {
        let oldLabel = value[index].label;
        let newLabel =
            event.target.value === "!!unlabeled" ? null : event.target.value;

        if (onlySelectLabelOnce) {
            selectedLabels.delete(oldLabel);
            selectedLabels.add(newLabel);
            selectedLabels = new Set(selectedLabels);
        }

        value = [
            ...value.slice(0, index),
            { ...value[index], label: newLabel },
            ...value.slice(index + 1),
        ];
    }

    $: {
        if (onlySelectLabelOnce) {
            selectedLabels = new Set(value.map((value) => value.label));
        }
    }
</script>

{#if value.length === 0}
    {#if interactive}
        <p>No data to label</p>
    {:else}
        <p>No labeling data to show</p>
    {/if}
{:else}
    <table width="100%" style="text-align: left;">
        <thead>
            <tr>
                <th>{textColumnHeader}</th>
                <th>{labelColumnHeader}</th>
            </tr>
        </thead>
        <tbody>
            {#each value as valueItem, i}
                <tr>
                    <td style="width: {textColumnWidth};">{valueItem.text}</td>
                    <td>
                        {#if interactive}
                            <select
                                value={valueItem.label === null
                                    ? "!!unlabeled"
                                    : valueItem.label}
                                on:change={(e) => handleLabelChange(e, i)}
                            >
                                <option value="!!unlabeled"
                                    >{unlabelledValueDisplay}</option
                                >
                                {#each labels as label}
                                    {#if !onlySelectLabelOnce || !selectedLabels.has(label) || label === valueItem.label}
                                        <option value={label}>{label}</option>
                                    {/if}
                                {/each}
                            </select>
                        {:else if valueItem.label === null}
                            {unlabelledValueDisplay}
                        {:else}
                            {valueItem.label}
                        {/if}
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
{/if}

<style>
    thead tr {
        background: var(--primary-300);
        color: var(--body-text-color);
        text-align: left;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        border-radius: var(--radius-lg);
        border-style: hidden; /* hide standard table (collapsed) border */
        box-shadow: 0 0 0 1px var(--block-border-color); /* this draws the table border  */
        overflow: hidden;
        margin: 10px 0;
        /* border-radius: var(--radius-lg); */
        font-size: 0.9em;
        font-family: sans-serif;
    }
    th,
    td {
        padding: 12px 15px;
    }

    tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    tbody tr:last-of-type {
        border-bottom: 2px solid var(--color-accent);
    }

    select {
        --ring-color: transparent;
        display: block;
        position: relative;
        outline: none !important;
        box-shadow:
            0 0 0 var(--shadow-spread) var(--ring-color),
            var(--shadow-inset);
        border: var(--input-border-width) solid var(--border-color-primary);
        border-radius: var(--radius-lg);
        background-color: white;
        padding: var(--size-2-5);
        width: 100%;
        color: var(--color-text-body);
        font-size: var(--scale-00);
        line-height: var(--line-sm);
    }

    select:focus {
        --ring-color: var(--color-focus-ring);
        border-color: var(--input-border-color-focus);
    }

    select::placeholder {
        color: var(--color-text-placeholder);
    }

</style>
