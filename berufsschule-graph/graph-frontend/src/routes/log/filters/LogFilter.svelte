<script lang="ts">
	import type { Filter } from "./types";
	import { ACTION_MAPPER_HTML, FIELD_MAPPER_HTML } from "./consts";

	export let filter: Filter;
	export let onAddClick: () => void;
	export let onRemoveClick: () => void;
</script>

<div class="filter">
	<select bind:value={filter.field}>
		{#each Object.entries(FIELD_MAPPER_HTML) as [field, text]}
			<option selected={filter.field === field} value={field}>
				{text}
			</option>
		{/each}
	</select>
	<select bind:value={filter.operator}>
		{#each Object.entries(ACTION_MAPPER_HTML) as [action, text]}
			<option selected={filter.operator === action} value={action}>
				{text}
			</option>
		{/each}
	</select>
	<input bind:value={filter.value} />
	<div class="add-remove-wrapper">
		<button class="add" on:click={onAddClick}>+</button>
		<button class="remove" on:click={onRemoveClick}>-</button>
	</div>
</div>

<style>
	.filter {
		display: flex;
		gap: .375rem;
	}

	.filter > select, .filter > input {
		background-color: var(--darker);
		border: .1rem solid var(--dark);
		border-bottom-width: .2rem;
		color: var(--white);
		font-size: var(--font-normal);
		padding: .4rem;
	}

	.filter > select:hover, .filter > input:hover {
		background-color: var(--dark);
	}

	.filter > .add-remove-wrapper {
		align-items: center;
		border: .05rem solid var(--dark);
		border-radius: .375rem;
		display: flex;
		padding: .3rem;
	}

	.filter > .add-remove-wrapper > .add,
	.filter > .add-remove-wrapper > .remove {
		align-items: center;
		border: none;
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-normal);
		height: 2rem;
		justify-content: center;
		width: 2rem;
	}

	.filter > .add-remove-wrapper > .add {
		background-color: var(--blue);
		border-radius: 50%;
	}

	.filter > .add-remove-wrapper > .remove {
		background: none;
	}
</style>