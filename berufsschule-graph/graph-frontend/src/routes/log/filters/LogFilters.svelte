<script lang="ts">
	import LogFilter from "./LogFilter.svelte";
	import type { Filter } from "./types";

	export let filters: Filter[];
	export let onFilterClick: () => void;

	function addFilter() {
		if (filters.length < 3) {
			filters = filters.concat({
				field: "id",
				operator: "equals",
				value: ""
			});
		}
	}

	function removeFilter(filter: Filter) {
		if (filters.length > 1) {
			filters = filters.filter(f => f !== filter);
		}
	}
</script>

<div class="filters">
	{#each filters as filter}
		<LogFilter
			{filter}
			onAddClick={addFilter}
			onRemoveClick={() => removeFilter(filter)}
		/>
	{/each}
	<div class="filter-wrapper">
		<button on:click={onFilterClick}>Filter</button>
	</div>
</div>

<style>
	.filters {
		align-items: center;
		border-bottom: .1rem solid var(--dark);
		display: flex;
		flex-direction: column;
		gap: .5rem;
		padding: 1rem;
	}

	.filters > .filter-wrapper > button {
		background: none;
		border: .1rem solid var(--dark);
		color: var(--white);
		cursor: pointer;
		font-size: var(--font-normal);
		padding: .4rem 1rem;
		width: 20rem;
	}

	.filters > .filter-wrapper > button:hover {
		background-color: var(--blue);
	}
</style>