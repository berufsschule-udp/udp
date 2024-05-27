<script lang="ts">
	import { goto } from "$app/navigation";
	import Header from "$lib/components/header/Header.svelte";
	import Loader from "$lib/components/loader/Loader.svelte";
	import { Routes } from "$application";

	export let data;

	function onChannelClick(channelId: string) {
		goto(`${Routes.Trend}/${channelId}`);
	}
</script>

<Header />
<Loader active={!data.channels}>
	<div class="trend-channels-grid-wrapper">
		<div class="trend-channels-grid">
			{#each data.channels as channel}
				<button
					class="item"
					on:click={() => onChannelClick(channel.id)}
				>
					{channel.alias}
				</button>
			{/each}
		</div>
	</div>
</Loader>

<style>
	.trend-channels-grid-wrapper {
		align-items: center;
		display: flex;
		height: 100%;
		justify-content: center;
	}

	.trend-channels-grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(8, 1fr);
	}

	.trend-channels-grid .item {
		align-items: center;
		background: var(--dark);
		border: none;
		border-radius: .2rem;
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-medium);
		font-weight: bold;
		gap: 1rem;
		justify-content: center;
		padding: 1rem;
	}
</style>