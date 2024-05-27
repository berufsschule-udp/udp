<script lang="ts">
	import { onMount } from "svelte";
	import { TITLE } from "$lib/components/header/consts";

	export let onLeftArrowClick = () => {};
	export let onRightArrowClick = () => {};
	export let withLeftArrow = true;
	export let withRightArrow = true;

	let time = "";

	onMount(() => {
		const interval = setInterval(updateTime, 1000);
		return () => clearInterval(interval);
	});

	function updateTime() {
		time = new Date().toLocaleString();
	}
</script>

<div class="header">
	{#if withLeftArrow}
		<button class="arrow left enabled" on:click={onLeftArrowClick} />
	{:else}
		<div class="arrow left" />
	{/if}
	<div class="item">
		<div class="item time">{time}</div>
		<slot name="left" />
	</div>
	<div class="item title">{TITLE}</div>
	<div class="item">
		<slot name="right" />
	</div>
	{#if withRightArrow}
		<button class="arrow right enabled" on:click={onRightArrowClick} />
	{:else}
		<div class="arrow right" />
	{/if}
</div>

<style>
	.header {
		align-items: center;
		border-bottom: .1rem solid var(--dark);
		display: flex;
		justify-content: center;
		min-height: 5rem;
	}

	.header .item {
		display: flex;
		flex: 2;
		justify-content: center;
	}

	.header .item.title {
		color: var(--cyan);
		flex: 3;
		font-size: var(--font-large);
		font-weight: bold;
		letter-spacing: 1rem;
	}

	.header .item.time {
		font-family: monospace;
		font-size: var(--font-medium);
	}

	.header .arrow {
		background: none;
		border: none;
		color: var(--white);
		height: 100%;
		width: 8rem;
	}

	.header .arrow.enabled {
		align-items: center;
		cursor: pointer;
		display: flex;
		font-size: var(--font-medium);
		justify-content: center;
	}

	.header .arrow.enabled:hover {
		background-color: var(--darker);
	}

	.header .arrow.left {
		border-right: .1rem solid var(--dark);
	}

	.header .arrow.left.enabled::after {
		content: "<";
		font-family: "Montserrat", sans-serif;
	}

	.header .arrow.right {
		border-left: .1rem solid var(--dark);
	}

	.header .arrow.right.enabled::after {
		content: ">";
		font-family: "Montserrat", sans-serif;
	}
</style>