<script lang="ts">
	import type { TrendChannel } from "./types";

	export let channels: TrendChannel[];
	export let isChannelsDialogOpened: boolean;

	let isOpened = true;

	function deselectChannel(channelIndex: number) {
		channels[channelIndex].isSelected = false;
	}
</script>

<div class="trend-legend" class:closed={!isOpened}>
	<button class="trend-legend-resize" on:click={() => isOpened = !isOpened} />
	<div class="trend-legend-list">
		{#each channels.filter(channel => channel.isSelected) as selectedChannel}
			<div class="trend-legend-item">
				<div class="trend-legend-item-icon"
				     style="--color: var(--{selectedChannel.color})">
					{selectedChannel.alias}
				</div>
				<button
					class="trend-legend-item-close"
					on:click={() => deselectChannel(channels.indexOf(selectedChannel))}
				/>
			</div>
		{/each}
	</div>
	<button class="trend-legend-channels-button"
	        on:click={() => isChannelsDialogOpened = true} />
</div>

<style>
	.trend-legend {
		align-self: start;
		border-left: .1rem solid var(--dark);
		display: flex;
		flex-direction: column;
		height: 100%;
		position: relative;
		transition: 300ms ease;
		width: 10rem;
	}

	.trend-legend.closed {
		width: 2rem;
	}

	.trend-legend.closed > .trend-legend-list, .trend-legend.closed > .trend-legend-channels-button {
		display: none;
	}

	.trend-legend-resize {
		align-items: center;
		background: var(--darker);
		border: .1rem solid var(--dark);
		border-radius: 50%;
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-normal);
		height: 3rem;
		justify-content: center;
		position: absolute;
		top: 50%;
		transform: translateX(-50%);
		transition: 300ms ease;
		width: 3rem;
	}

	.trend-legend-resize::after {
		content: ">";
	}

	.trend-legend.closed > .trend-legend-resize::after {
		content: "<";
	}

	.trend-legend-resize:hover {
		background-color: var(--darker);
	}

	.trend-legend-list {
		margin-bottom: auto;
		max-height: 100%;
		overflow-y: auto;
	}

	.trend-legend-item {
		align-items: center;
		cursor: pointer;
		display: flex;
		font-size: var(--font-medium);
		font-weight: bold;
		justify-content: space-evenly;
		padding: 1rem 0 1rem 1rem;
	}

	.trend-legend-item:hover {
		background-color: var(--darker);
	}

	.trend-legend-item-icon {
		align-items: center;
		background-color: var(--color);
		border-radius: .25rem;
		display: flex;
		font-size: var(--font-normal);
		font-weight: bold;
		height: 5rem;
		justify-content: center;
		text-align: center;
		width: 5rem;
	}

	.trend-legend-item-close {
		align-items: center;
		background: none;
		border: none;
		border-radius: 50%;
		color: var(--white);
		display: flex;
		font-size: var(--font-medium);
		height: 1rem;
		justify-content: center;
		width: 1rem;
	}

	.trend-legend-item-close::before {
		content: "×";
	}

	.trend-legend-item-close:hover {
		background-color: var(--dark);
	}

	.trend-legend-channels-button {
		align-items: center;
		background: none;
		border: none;
		border-top: .1rem solid var(--dark);
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-medium);
		height: 3rem;
		justify-content: center;
	}

	.trend-legend-channels-button::before {
		content: "+";
	}

	.trend-legend-channels-button:hover {
		background-color: var(--dark);
	}
</style>