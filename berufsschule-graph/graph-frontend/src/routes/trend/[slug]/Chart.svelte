<script lang="ts">
	import { onMount } from "svelte";
	import { type EChartsOption, type EChartsType, init } from "echarts";
	import { Time } from "$lib/time";
	import type { Averages } from "$application";
	import type { TrendChannel } from "./types";

	export let channelsAverages: Averages;
	export let channels: TrendChannel[] = [];
	export let minValue: number;
	export let maxValue: number;
	export let startTime: Time;
	export let endTime: Time;

	let chartParentElement: HTMLDivElement | null = null;
	let chartElement: EChartsType | null = null;

	$: chartElement && channelsAverages && updateChart();

	onMount(() => {
		chartElement = init(chartParentElement);
	});

	function updateChart() {
		chartElement?.setOption({
			legend: getChartLegend(),
			tooltip: getChartTooltip(),
			toolbox: getChartToolbox(),
			dataZoom: getChartDataZoom(),
			xAxis: getChartXAxis(),
			yAxis: getChartYAxis(),
			series: getChartSeries()
		} as EChartsOption);
	}

	function getChartLegend() {
		return {
			textStyle: {
				color: "white"
			},
			top: 15
		} as EChartsOption["legend"];
	}

	function getChartTooltip() {
		return {
			trigger: "axis",
			backgroundColor: "var(--darker)",
			borderColor: "var(--dark)",
			textStyle: {
				color: "var(--white)"
			},
			axisPointer: {
				type: "cross",
				label: {
					formatter: params => params.axisDimension === "x"
						? Time.ofSeconds(Math.round(params.value as number))
						.toPrettyString()
						: Math.round((params.value as number) * 100) / 100
				}
			}
		} as EChartsOption["tooltip"];
	}

	function getChartToolbox() {
		return {
			right: 170,
			itemSize: 40,
			feature: {
				saveAsImage: {
					backgroundColor: 'auto',
					name: new Date().toLocaleString(),
					excludeComponents: ['toolbox', 'dataZoom']
				},
				dataZoom: {}
			}
		} as EChartsOption["toolbox"];
	}

	function getChartDataZoom() {
		return [{
			xAxisIndex: [0]
		}, {
			yAxisIndex: [0],
			right: 100
		}] as EChartsOption["dataZoom"];
	}

	function getChartXAxis() {
		return {
			type: "value",
			inverse: true,
			min: startTime.toSeconds(),
			max: endTime.toSeconds(),
			axisLabel: {
				formatter: seconds => Time.ofSeconds(Number(seconds)).toPrettyString()
			},
			interval: (endTime.toSeconds() - startTime.toSeconds()) / 20,
			splitLine: {
				lineStyle: {
					width: .1
				}
			}
		} as EChartsOption["xAxis"];
	}

	function getChartYAxis() {
		return {
			type: "value",
			min: minValue,
			max: maxValue,
			interval: (maxValue - minValue) / 10,
			splitLine: {
				lineStyle: {
					width: .1
				}
			}
		} as EChartsOption["yAxis"];
	}

	function getChartSeries() {
		return Object.entries(channelsAverages).map(([channelId, channelAverages]) => ({
			name: channels.find(channel => channel.id === channelId)?.alias,
			type: "line",
			showSymbol: false,
			smooth: true,
			data: channelAverages.map(average => [average.seconds, average.value]),
			lineStyle: {
				width: 1.2,
				color: channels.find(channel => channel.id === channelId)?.color
			},
			markLine: {
				label: {
					color: 'white'
				},
				symbol: 'none',
				data: channels.find(c => c.isSelected)?.limits.map(l => ({
					yAxis: l.value,
					lineStyle: {
						color: mapAlarmLevelToColor(l.alarmLevel)
					}
				}))
			}
		} as EChartsOption["series"]));
	}

	function mapAlarmLevelToColor(alarmLevel: number) {
		switch (alarmLevel) {
			case 1:
				return 'yellow';
			case 2:
				return 'orange';
			case 3:
				return 'red';
			default:
				throw {};
		}
	}
</script>

<div bind:this={chartParentElement} class="trend-chart" />

<style>
	.trend-chart {
		height: 100%;
		width: 100%;
	}
</style>