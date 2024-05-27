import { Routes } from "$application";
import type { FooterItem } from "$lib/components/footer/types";

export const ITEMS: FooterItem[] = [{
	name: "Control",
	path: Routes.Control,
	disabled: false
}, {
	name: "Mnemonic",
	path: Routes.Mnemonic,
	disabled: true
}, {
	name: "Trends",
	path: Routes.Trend,
	disabled: false
}, {
	name: "Log",
	path: Routes.Log,
	disabled: false
}];