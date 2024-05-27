<script lang="ts">
	import { goto } from "$app/navigation";
	import {
		PUBLIC_CONTROL_LAYOUT_UPDATE_MILLISECONDS,
		PUBLIC_URL_API
	} from "$env/static/public";
	import Header from "$lib/components/header/Header.svelte";
	import Loader from "$lib/components/loader/Loader.svelte";
	import { safeFetch } from "$lib/fetch";
	import { onMount } from "svelte";
	import { type Layout, Routes } from "$application";
	import ErrorHandler from "$lib/components/error/ErrorHandler.svelte";

	const COLUMNS_COUNT = 4;
	let pagesChannels: Layout = [];
	let pageIndex = 1;
	let errorTitle: string | undefined;
	let errorMessage: string | undefined;

	onMount(() => {
		const interval = setInterval(
			updateLayout,
			Number(PUBLIC_CONTROL_LAYOUT_UPDATE_MILLISECONDS)
		);

		return () => clearInterval(interval);
	});

	async function updateLayout() {
		const [response, error] = await safeFetch<Layout>({
			fn: fetch,
			url: `${PUBLIC_URL_API}/layout`,
			json: true
		});

		if (error) {
			errorTitle = error.message;
			errorMessage = error.stack ?? "";
			return;
		}

		pagesChannels = response;
	}

	function onChannelClick(channelId: string) {
		goto(`${Routes.Trend}/${channelId}`);
	}

	function onLeftArrowClick() {
		if (pageIndex !== Number(Object.keys(pagesChannels)[0])) {
			pageIndex--;
		}
	}

	function onRightArrowClick() {
		if (pageIndex !== Number(Object.keys(pagesChannels).at(-1))) {
			pageIndex++;
		}
	}

	function getStyleForChannelOffsetAndSpan(offset: number, span: number) {
		const x = offset % COLUMNS_COUNT;
		const y = Math.floor(offset / COLUMNS_COUNT);

		return `grid-area: ${y} / ${x} / ${y} / ${x + span}; grid-column: span ${span};`;
	}

	function isSpaceAfter(offset: number, span: number, channelIndex: number) {
		return channelIndex !== pagesChannels[pageIndex].length - 1
			&& offset + span !== pagesChannels[pageIndex][channelIndex + 1].offset;
	}

	function getStyleForSpaceAfter(offset: number, span: number, channelIndex: number, rowOffset: number) {
		const nextChannel = pagesChannels[pageIndex][channelIndex + 1];
		const startRow = Math.floor(offset / COLUMNS_COUNT) + rowOffset;
		const endRow = Math.floor(nextChannel.offset / COLUMNS_COUNT);

		const isCurrentRowEqualsStartRow = rowOffset === 0 && (offset + span) % COLUMNS_COUNT !== 1;
		const isCurrentRowEqualsEndRow = startRow === endRow;

		return "grid-column: span " + (
			isCurrentRowEqualsStartRow
				? isCurrentRowEqualsEndRow
					? nextChannel.offset % COLUMNS_COUNT - (offset + span - 1) % COLUMNS_COUNT
					: COLUMNS_COUNT - offset % COLUMNS_COUNT
				: isCurrentRowEqualsEndRow
					? nextChannel.offset % COLUMNS_COUNT - 1
					: COLUMNS_COUNT
		);
	}

	function getSpacesAfterAmountAsArray(offset: number, span: number, channelIndex: number) {
		const nextChannel = pagesChannels[pageIndex][channelIndex + 1];
		const startRow = Math.floor(offset / COLUMNS_COUNT);
		const endRow = Math.floor(nextChannel.offset / COLUMNS_COUNT);

		const spaceAfterFromStartBorder = (offset + span) % COLUMNS_COUNT === 1 ? 0 : 1;
		const spaceBeforeEndToBorder = nextChannel.offset % COLUMNS_COUNT === 1 ? 0 : 1;

		const spacesCount = endRow - startRow + spaceAfterFromStartBorder + spaceBeforeEndToBorder - 1;
		return Array.from<unknown, number>({ length: spacesCount }, (_, index) => index);
	}

	function nullableToFixed(value: number | null, decimals: number) {
		return value ? value.toFixed(decimals) : "N/A";
	}
</script>

<Header
	{onLeftArrowClick}
	{onRightArrowClick}
	withLeftArrow={pageIndex !== Number(Object.keys(pagesChannels)[0])}
	withRightArrow={pageIndex !== Number(Object.keys(pagesChannels).at(-1))}
/>
<ErrorHandler message={errorMessage} title={errorTitle}>
	<Loader active={!Object.keys(pagesChannels).length}>
		<div class="channels-grid">
			{#each pagesChannels[pageIndex] as channel, index}
				<div
					class="item level-{channel.alarmLevel}"
					style={getStyleForChannelOffsetAndSpan(channel.offset, channel.span)}
					on:mouseup={() => onChannelClick(channel.id)}
					role="button"
					tabindex="-1"
				>
					<div class="name">{channel.alias}</div>
					<div class="content">
						<div class="value">
							{nullableToFixed(channel.lastValue, 2)}
						</div>
						<div class="unit">{channel.unit}</div>
					</div>
				</div>
				{#if isSpaceAfter(channel.offset, channel.span, index)}
					{#each getSpacesAfterAmountAsArray(
						channel.offset,
						channel.span,
						index
					) as rowOffset}
						<div style={
							getStyleForSpaceAfter(
								channel.offset,
								channel.span,
								index,
								rowOffset
							)
						} />
					{/each}
				{/if}
			{/each}
		</div>
	</Loader>
</ErrorHandler>

<style>
	.channels-grid {
		display: grid;
		grid-gap: 1rem;
		grid-row-gap: 1rem;
		grid-template-columns: repeat(4, 1fr);
		grid-template-rows: repeat(4, 1fr);
		height: 100%;
		padding: 1rem;
	}

	.channels-grid > .item {
		background-color: var(--blue);
		border-radius: .25rem;
		display: flex;
		flex-direction: column;
		user-select: none;
	}

	.channels-grid > .item:hover > .content {
		background-color: var(--dark);
		cursor: pointer;
	}

	.channels-grid > .item > .name {
		align-items: center;
		display: flex;
		font-size: var(--font-medium);
		justify-content: center;
	}

	.channels-grid > .item > .content {
		background-color: var(--darker);
		border-radius: .25rem;
		display: flex;
		gap: .5rem;
		height: 100%;
		justify-content: flex-end;
		margin: .1rem;
		position: relative;
	}

	.channels-grid > .item > .content > .value {
		align-self: center;
		color: var(--white);
		flex: 2;
		font-size: var(--font-xxlarge);
		text-align: right;
	}

	.channels-grid > .item.level-1 {
		background-color: #70ea70;
	}

	.channels-grid > .item.level-2 {
		background-color: yellow;
		color: var(--black);
	}

	.channels-grid > .item.level-3 {
		background-color: red;
	}

	.channels-grid > .item > .content > .unit {
		align-self: flex-end;
		color: var(--gray);
		flex: 1;
		font-size: var(--font-medium);
		margin-bottom: 2rem;
	}
</style>