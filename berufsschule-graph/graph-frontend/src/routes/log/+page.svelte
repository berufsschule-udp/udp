<script lang="ts">
	import Header from "$lib/components/header/Header.svelte";
	import { onMount } from "svelte";
	import { safeFetch } from "$lib/fetch";
	import type { Event } from "$application";
	import { PUBLIC_LOG_SIZE, PUBLIC_URL_API } from "$env/static/public";
	import ErrorHandler from "$lib/components/error/ErrorHandler.svelte";
	import LogTable from "./table/LogTable.svelte";
	import type { Filter, FilterOperator } from "./filters/types";
	import LogFilters from "./filters/LogFilters.svelte";

	let events: Event[] = [];
	let filters: Filter[] = [{ field: "id", operator: "equals", value: "" }];
	let errorTitle: string | undefined;
	let errorMessage: string | undefined;
	let offset = 0;

	onMount(fetchEvents);

	async function fetchEventsFromUrl(url: string) {
		const [response, error] = await safeFetch<Event[]>({
			fn: fetch,
			url,
			json: true
		});

		if (error) {
			errorTitle = error.message;
			errorMessage = error.stack ?? "";
			return;
		}

		events = response;
	}

	async function fetchEvents() {
		await fetchEventsFromUrl(`${PUBLIC_URL_API}/events?off=${offset}&lim=${PUBLIC_LOG_SIZE}${getChannelAliasFilter()}`);
	}

	function getChannelAliasFilter() {
		const filter = filters.find(f => f.field === "id");

		if (!filter?.value) {
			return "";
		}

		return `&als=${mapChannelAliasFilterOperator(filter.operator)}${filter.value}`;
	}

	function mapChannelAliasFilterOperator(operator: FilterOperator) {
		switch (operator) {
			case "equals":
				return "0";
			case "not equals":
				return "1";
			default:
				throw {};
		}
	}

	function onLeftArrowClick() {
		offset -= Number(PUBLIC_LOG_SIZE);
		fetchEvents();
	}

	function onRightArrowClick() {
		offset += Number(PUBLIC_LOG_SIZE);
		fetchEvents();
	}

	function formatAlarmLevel(alarmLevel: number) {
		switch (alarmLevel) {
			case 0:
				return "Normal";
			case 1:
				return "Alarm 1";
			case 2:
				return "Alarm 2";
			case 3:
				return "Trip";
			default:
				throw new Error(`Unknown alarm level: ${alarmLevel}`);
		}
	}
</script>

<Header
	{onLeftArrowClick}
	{onRightArrowClick}
	withLeftArrow={offset >= Number(PUBLIC_LOG_SIZE)}
>
	<div slot="right">Page: {offset / Number(PUBLIC_LOG_SIZE)}</div>
</Header>
<ErrorHandler message={errorMessage} title={errorTitle}>
	<LogFilters bind:filters onFilterClick={fetchEvents} />
	<div class="table-wrapper">
		<LogTable
			columns={[{
				name: "Date",
				map: e => {
					const date = new Date(e.timestamp);
					date.setTime(
						date.getTime() - date.getTimezoneOffset() * 60000
					);
					return date.toLocaleDateString();
				},
				sort: (a, b) => Date.parse(a.timestamp)
					- Date.parse(b.timestamp)
			}, {
				name: "Time",
				map: e => {
					const date = new Date(e.timestamp);
					date.setTime(
						date.getTime() - date.getTimezoneOffset() * 60000
					);
					return date.toLocaleTimeString();
				},
				sort: (a, b) => Date.parse(a.timestamp) % 86_400_000
					- Date.parse(b.timestamp) % 86_400_000
			}, {
				name: "Channel",
				map: e => e.channelAlias,
				sort: (a, b) => a.channelAlias.toLowerCase()
					.localeCompare(b.channelAlias.toLowerCase()),
				distinct: active => active
					? fetchEvents()
					: fetchEventsFromUrl(`${PUBLIC_URL_API}/events/distinct/id`)
			}, {
				name: "Alarm level",
				map: e => formatAlarmLevel(e.alarmLevel),
				sort: (a, b) => a.alarmLevel - b.alarmLevel
			}]}
			{events}
		/>
	</div>
</ErrorHandler>

<style>
	.table-wrapper {
		margin: 1rem;
	}
</style>