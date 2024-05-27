import {
	PUBLIC_TREND_LEGEND_CHANNELS_COLORS,
	PUBLIC_URL_API
} from "$env/static/public";
import { safeFetch } from "$lib/fetch";
import { error as svelteError } from "@sveltejs/kit";
import type { Channel } from "$application";
import type { TrendChannel } from "./types";

export async function load({ params, fetch }) {
	const channel = await getChannel(params.slug, fetch);
	const channels = await getChannels(params.slug, channel.unit, channel.maxValue, fetch);

	return { channels, unit: channel.unit, maxValue: channel.maxValue };
}

async function getChannel(channelId: string, serverSideFetch: typeof fetch) {
	const [channel, error] = await safeFetch<Channel>({
		fn: serverSideFetch,
		url: `${PUBLIC_URL_API}/channels/${channelId}`,
		json: true
	});

	if (error) {
		svelteError(error.status, error.stack);
	}

	return channel;
}

async function getChannels(
	channelId: string,
	unit: string,
	maxValue: number,
	serverSideFetch: typeof fetch
) {
	const [channels, error] = await safeFetch<Channel[]>({
		fn: serverSideFetch,
		url: `${PUBLIC_URL_API}/channels?unt=${unit}&max=${maxValue}`,
		json: true
	});

	if (error) {
		svelteError(error.status, error.stack);
	}

	const colors = PUBLIC_TREND_LEGEND_CHANNELS_COLORS.split(",");

	return channels.map((channel, channelIndex) => ({
		...channel,
		color: colors[channelIndex % colors.length],
		isSelected: channel.id === channelId
	} as TrendChannel));
}