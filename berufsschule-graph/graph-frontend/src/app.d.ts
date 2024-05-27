export enum Routes {
	Control = "/control",
	Mnemonic = "/mnemonic",
	Trend = "/trend",
	Log = "/log"
}

export interface Averages {
	[channelId: string]: {
		value: number | null;
		seconds: number;
	}[];
}

export interface Channel {
	id: string;
	alias: string;
	unit: string;
	maxValue: number;
	limits: {
		alarmLevel: number;
		value: number;
	}[];
}

export interface Layout {
	[pageIndex: number]: {
		id: string;
		alias: string;
		unit: string;
		alarmLevel: number;
		offset: number;
		span: number;
		lastValue: number | null;
	}[];
}

export interface Event {
	channelId: string;
	channelAlias: string;
	channelUnit: string;
	channelMaxValue: number | null;
	alarmLevel: number;
	timestamp: string;
}