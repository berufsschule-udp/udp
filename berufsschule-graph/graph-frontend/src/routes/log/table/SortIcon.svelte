<script lang="ts">
	import { ColumnState } from "./types";

	export let state: ColumnState;
	export let onClick: () => void;
</script>

<div on:mouseup={onClick} role="button" tabindex="-1">
	{#if state === ColumnState.INITIAL}
		<img alt="⧫" src="/svg/sort/sort-initial.svg" />
	{:else if state === ColumnState.ASCENDING}
		<img alt="▲" src="/svg/sort/sort-asc.svg" />
	{:else}
		<img alt="▼" src="/svg/sort/sort-desc.svg" />
	{/if}
</div>

<style>
	div {
		display: inline;
	}

	img {
		filter: invert();
		float: right;
		height: 2rem;
		padding: .25rem 2rem;
	}
</style>