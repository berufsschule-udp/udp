import type { Event } from "$application";

export enum ColumnState {
	INITIAL,
	ASCENDING,
	DESCENDING
}

export interface Column {
	name: string;
	map: (data: Event) => string;
	sort: (a: Event, b: Event) => number;
	distinct?: (active: boolean) => Promise<void>;
}

export interface EnhancedColumn extends Column {
	state: ColumnState;
	activeDistinct: boolean;
}