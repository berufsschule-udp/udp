import type { Channel } from "$application";

export interface TrendChannel extends Channel {
	color: string;
	isSelected: boolean;
}