<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import {
		PUBLIC_TREND_CHART_SAMPLE_DAY,
		PUBLIC_TREND_CHART_SAMPLE_LIVE,
		PUBLIC_TREND_CHART_SAMPLE_MONTH,
		PUBLIC_TREND_CHART_SAMPLE_WEEK,
		PUBLIC_TREND_CHART_UPDATE_MILLISECONDS,
		PUBLIC_URL_API
	} from "$env/static/public";
	import Header from "$lib/components/header/Header.svelte";
	import Dialog from "$lib/components/dialog/Dialog.svelte";
	import Loader from "$lib/components/loader/Loader.svelte";
	import TrendChart from "./Chart.svelte";
	import TrendLegend from "./Legend.svelte";
	import { safeFetch } from "$lib/fetch";
	import { Time } from "$lib/time";
	import type { TrendChannel } from "./types";
	import type { Averages } from "$application";
	import ErrorHandler from "$lib/components/error/ErrorHandler.svelte";

	export let data;

	let channelsAverages: Averages = {};
	let minValue = 0;
	let startTime = Time.ofDirtySeconds($page.url.searchParams.get("startSeconds"), Time.ofEmpty());
	let endTime = Time.ofDirtySeconds($page.url.searchParams.get("endSeconds"), Time.ofMinutes(30));
	let previousSelectedChannelsLength = getSelectedChannels().length;
	let isLiveViewMode = true;
	let isDayViewMode = false;
	let isWeekViewMode = false;
	let isMonthViewMode = false;
	let isChannelsDialogOpened = false;
	let errorTitle: string | undefined;
	let errorMessage: string | undefined;

	$: isChannelsDialogOpened && updateAverages();

	$: {
		if (!isChannelsDialogOpened && getSelectedChannels().length !== previousSelectedChannelsLength) {
			updateAverages();
			previousSelectedChannelsLength = getSelectedChannels().length;
		}
	}

	onMount(() => {
		const interval = setInterval(updateAveragesWhenNeeded, Number(PUBLIC_TREND_CHART_UPDATE_MILLISECONDS));
		return () => clearInterval(interval);
	});

	async function updateAveragesWhenNeeded() {
		if (isLiveViewMode && !isChannelsDialogOpened) {
			await updateAverages();
		}
	}

	async function updateAverages() {
		channelsAverages = getSelectedChannels()
			? await getAveragesForSelectedChannels(getSelectedChannels())
			: {};
	}

	function getSelectedChannels() {
		return data.channels.filter(channel => channel.isSelected);
	}

	async function getAveragesForSelectedChannels(selectedChannels: TrendChannel[]) {
		const [averages, error] = await safeFetch<Averages>({
			fn: fetch,
			url: `${PUBLIC_URL_API}/averages?ids=${selectedChannels.map(selectedChannel => selectedChannel.id)}&off=${startTime.toSeconds()}&lim=${endTime.minus(startTime).toSeconds()}&smp=${getAverageSample()}`,
			json: true
		});

		if (error) {
			errorTitle = error.message;
			errorMessage = error.stack ?? "";
			throw {};
		}

		return averages;
	}

	function getAverageSample() {
		return isLiveViewMode ? PUBLIC_TREND_CHART_SAMPLE_LIVE
			: isDayViewMode ? PUBLIC_TREND_CHART_SAMPLE_DAY
				: isWeekViewMode ? PUBLIC_TREND_CHART_SAMPLE_WEEK
					: PUBLIC_TREND_CHART_SAMPLE_MONTH;
	}

	async function onLeftArrowClick() {
		const timedelta = endTime.minus(startTime);
		startTime = startTime.plus(timedelta);
		endTime = endTime.plus(timedelta);

		channelsAverages = {};
		await updateAverages();
	}

	async function onRightArrowClick() {
		const timedelta = endTime.minus(startTime);
		startTime = startTime.minus(timedelta);
		endTime = endTime.minus(timedelta);

		channelsAverages = {};
		await updateAverages();
	}

	async function onLiveViewModeClick() {
		startTime = Time.ofEmpty();
		endTime = Time.ofMinutes(30);
		isLiveViewMode = true;
		await onViewModeChange();
	}

	async function onDayViewModeClick() {
		startTime = Time.ofEmpty();
		endTime = Time.ofDays(1);
		isLiveViewMode = false;
		await onViewModeChange();
	}

	async function onWeekViewModeClick() {
		startTime = Time.ofEmpty();
		endTime = Time.ofWeeks(1);
		isLiveViewMode = false;
		await onViewModeChange();
	}

	async function onMonthViewModeClick() {
		startTime = Time.ofEmpty();
		endTime = Time.ofMonths(1);
		isLiveViewMode = false;
		await onViewModeChange();
	}

	async function onViewModeChange() {
		minValue = 0;

		isDayViewMode = !isLiveViewMode && Time.ofDays(1).plus(startTime).equals(endTime);
		isWeekViewMode = !isLiveViewMode && Time.ofWeeks(1).plus(startTime).equals(endTime);
		isMonthViewMode = !isLiveViewMode && Time.ofMonths(1).plus(startTime).equals(endTime);

		channelsAverages = {};
		await updateAverages();
	}

	function setChannelSelection(index: number, doSelect: boolean) {
		data.channels[index].isSelected = doSelect;
	}
</script>

<Header
	{onLeftArrowClick}
	{onRightArrowClick}
	withRightArrow={endTime.minus(startTime).isBefore(endTime)}
>
	<div class="trend-header-right" slot="right">
		<button class="trend-header-right-button" class:active={isLiveViewMode}
				on:click={onLiveViewModeClick}>
			L
		</button>
		<button class="trend-header-right-button" class:active={isDayViewMode}
				on:click={onDayViewModeClick}>
			D
		</button>
		<button class="trend-header-right-button" class:active={isWeekViewMode}
				on:click={onWeekViewModeClick}>
			W
		</button>
		<button class="trend-header-right-button" class:active={isMonthViewMode}
				on:click={onMonthViewModeClick}>
			M
		</button>
	</div>
</Header>
<ErrorHandler message={errorMessage} title={errorTitle}>
	<Loader active={!channelsAverages}>
		<div id="content">
			<TrendChart
				bind:maxValue={data.maxValue}
				bind:minValue
				channels={data.channels}
				{channelsAverages}
				{endTime}
				{startTime}
			/>
			<TrendLegend bind:channels={data.channels}
			             bind:isChannelsDialogOpened />
			<Dialog bind:isOpened={isChannelsDialogOpened} title="Channels">
				<div class="trend-channels-dialog-grid">
					{#each data.channels as channel, channelIndex}
						<div class="trend-channels-dialog-item"
						     class:active={channel.isSelected}>
							<div>{channel.alias}</div>
							<input
								type="checkbox"
								class="trend-channels-dialog-item-checkbox"
								checked={channel.isSelected}
								on:change={() => setChannelSelection(channelIndex, !channel.isSelected)}
							/>
						</div>
					{/each}
				</div>
			</Dialog>
		</div>
	</Loader>
</ErrorHandler>

<style>
	#content {
		align-items: center;
		display: flex;
		height: 100%;
		overflow-y: auto;
	}

	.trend-header-right {
		display: flex;
		gap: 1rem;
	}

	.trend-header-right-button {
		align-items: center;
		background: none;
		border: none;
		border-radius: 50%;
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-normal);
		height: 3.5rem;
		justify-content: center;
		width: 3.5rem;
	}

	.trend-header-right-button:hover {
		background-color: var(--dark);
	}

	.trend-header-right-button.active {
		background-color: var(--blue);
	}

	.trend-channels-dialog-grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(4, 1fr);
	}

	.trend-channels-dialog-item {
		align-items: center;
		border-radius: .2rem;
		display: flex;
		font-size: var(--font-medium);
		font-weight: bold;
		gap: 1rem;
		padding: 1rem;
	}

	.trend-channels-dialog-item.active {
		background-color: var(--dark);
	}

	.trend-channels-dialog-item-checkbox {
		accent-color: var(--white);
		height: 1.5rem;
		width: 1.5rem;
	}
</style>