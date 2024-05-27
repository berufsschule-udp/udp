import { redirect } from "@sveltejs/kit";
import { Routes } from "$application";

export async function load() {
	redirect(302, Routes.Control);
}