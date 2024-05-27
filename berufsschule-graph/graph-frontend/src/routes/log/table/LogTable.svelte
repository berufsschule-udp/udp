<script lang="ts">
	import type { Event } from "$application";
	import SortIcon from "./SortIcon.svelte";
	import { type Column, ColumnState, type EnhancedColumn } from "./types";
	import DistinctIcon from "./DistinctIcon.svelte";

	export let events: Event[];
	export let columns: Column[];

	let sortedEvents: Event[];
	let enhancedColumns = getEnhancedColumns();

	$: sortedEvents = [...events];

	function getEnhancedColumns() {
		return columns.map(c => ({
			...c,
			state: ColumnState.INITIAL,
			activeDistinct: false
		} as EnhancedColumn));
	}

	function sort(columnIndex: number) {
		switch (enhancedColumns[columnIndex].state) {
			case ColumnState.INITIAL:
				sortedEvents.sort(enhancedColumns[columnIndex].sort);
				enhancedColumns = enhancedColumns.map((c, i) => ({
					...c,
					state: i === columnIndex
						? ColumnState.ASCENDING
						: ColumnState.INITIAL,
					activeDistinct: false
				}));
				break;
			case ColumnState.ASCENDING:
				sortedEvents.sort((a, b) =>
					-enhancedColumns[columnIndex].sort(a, b));
				enhancedColumns[columnIndex].state = ColumnState.DESCENDING;
				break;
			case ColumnState.DESCENDING:
				sortedEvents = [...events];
				enhancedColumns[columnIndex].state = ColumnState.INITIAL;
				break;
		}
	}
</script>

<table>
	<thead>
	<tr>
		{#each enhancedColumns as column, i}
			<th>
				{column.name}
				<SortIcon state={column.state} onClick={() => sort(i)} />
				{#if column.distinct}
					<DistinctIcon active={column.activeDistinct} onClick={() => {
						column.distinct && column.distinct(column.activeDistinct);

						enhancedColumns = enhancedColumns.map((c, j) => ({
							...c,
							activeDistinct:	j === i
								? !column.activeDistinct
								: false
						}));
					}} />
				{/if}
			</th>
		{/each}
	</tr>
	</thead>
	<tbody>
	{#each sortedEvents as event}
		<tr>
			{#each enhancedColumns as column}
				<td>{column.map(event)}</td>
			{/each}
		</tr>
	{/each}
	</tbody>
</table>

<style>
	table {
		border-collapse: collapse;
		font-family: monospace;
		overflow-x: hidden;
		text-align: left;
		width: 100%;
	}

	th, td {
		border: .1rem solid var(--dark);
		padding: .2rem 0 .2rem 1rem;
	}

	th {
		background-color: var(--blue);
		font-weight: normal;
		position: sticky;
		top: 0;
	}
</style>