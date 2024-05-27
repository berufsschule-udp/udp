export type FilterField =
	| "id"
	| "alarm level";

export type FilterOperator =
	| "equals"
	| "not equals";

export interface Filter {
	field: FilterField;
	operator: FilterOperator;
	value: string;
}