<script lang="ts">
	export let active: boolean;
	export let onClick: () => void;
</script>

<div on:mouseup={onClick} role="button" tabindex="-1">
	{#if active}
		<img alt="Distinct" src="/svg/list/list-sorted.svg" />
	{:else}
		<img alt="Distinct" src="/svg/list/list-unsorted.svg" />
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