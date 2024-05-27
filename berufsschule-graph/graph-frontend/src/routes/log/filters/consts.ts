import type { FilterField, FilterOperator } from "./types";

export const FIELD_MAPPER_HTML: Record<FilterField, string> = {
	"id": "Channel id",
	"alarm level": "Alarm level"
};

export const ACTION_MAPPER_HTML: Record<FilterOperator, string> = {
	"equals": "is equal to",
	"not equals": "is not equal to"
};