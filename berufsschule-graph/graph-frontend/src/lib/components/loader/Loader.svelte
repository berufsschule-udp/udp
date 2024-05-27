<script lang="ts">
	export let active: boolean;
</script>

{#if active}
	<div class="loader">
		Loading...
	</div>
{:else}
	<slot />
{/if}

<style>
	.loader {
		align-items: center;
		display: flex;
		height: 100%;
		justify-content: center;
	}
</style>