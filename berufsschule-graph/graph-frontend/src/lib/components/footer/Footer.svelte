<script lang="ts">
	import { page } from "$app/stores";
	import { ITEMS } from "$lib/components/footer/consts";

	function createRipple(event: MouseEvent) {
		const anchor = event.currentTarget as HTMLAnchorElement;
		const circle = document.createElement("span");
		const diameter = Math.max(anchor.clientWidth, anchor.clientHeight);
		const radius = diameter / 2;

		circle.style.width = circle.style.height = `${diameter}px`;
		circle.style.left = `${event.clientX - anchor.offsetLeft - radius}px`;
		circle.style.top = `${event.clientY - anchor.offsetTop - radius}px`;
		circle.classList.add("ripple");

		anchor.querySelector(".ripple")?.remove();
		anchor.appendChild(circle);
	}
</script>

<div class="footer">
	{#each ITEMS as item}
		<a
			href={item.path}
			class="item"
			class:active={
				item.path === $page.url.pathname
				|| $page.url.pathname.startsWith(`${item.path}/`)
			}
			class:disabled="{item.disabled}"
			on:mousedown={createRipple}
		>
			{item.name}
		</a>
	{/each}
</div>

<style>
	.footer {
		align-items: center;
		border-top: .1rem solid var(--dark);
		display: flex;
		height: 5rem;
		justify-content: space-evenly;
		margin-top: auto;
		min-height: 5rem;
		width: 100%;
	}

	.footer .item {
		align-items: center;
		color: var(--white);
		display: flex;
		font-size: var(--font-large);
		height: 100%;
		justify-content: center;
		overflow: hidden;
		position: relative;
		text-decoration: none;
		user-select: none;
		width: 25rem;
	}

	.footer .item.active {
		background-color: var(--blue);
	}

	.footer .item.disabled {
		color: var(--gray);
		pointer-events: none;
	}

	:global(.ripple) {
		animation: ripple 700ms ease-in-out;
		background-color: var(--white);
		border-radius: 50%;
		position: absolute;
		transform: scale(0);
	}

	@keyframes ripple {
		to {
			transform: scale(3);
			opacity: 0;
		}
	}
</style>