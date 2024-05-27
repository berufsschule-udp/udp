<script lang="ts">
	export let isOpened: boolean;
	export let title: string;

	let dialogHtml: HTMLDialogElement | null;

	$: isOpened ? dialogHtml?.showModal() : dialogHtml?.close();
</script>

<dialog bind:this={dialogHtml} on:close={() => isOpened = false}>
	<div class="header">{title}</div>
	<div class="content">
		<slot />
	</div>
	<div class="footer">
		<button class="close" on:click={() => isOpened = false}>
			Close
		</button>
	</div>
</dialog>

<style>
	dialog {
		background-color: var(--darker);
		border: none;
		color: var(--white);
	}

	dialog[open] {
		animation: dialog-opening 300ms cubic-bezier(.3, 1.5, .6, 1);
	}

	@keyframes dialog-opening {
		from {
			transform: scale(.8);
		}
		to {
			transform: scale(1);
		}
	}

	dialog > .header {
		border-bottom: .1rem solid var(--gray);
		font-size: var(--font-medium);
		padding-bottom: .5rem;
	}

	dialog > .content {
		margin: 1rem;
	}

	dialog > .footer {
		border-top: .1rem solid var(--gray);
		display: flex;
		flex-direction: row-reverse;
		padding-top: .5rem;
	}

	dialog > .footer > .close {
		align-items: center;
		background-color: var(--dark);
		border: none;
		border-radius: .5rem;
		color: var(--white);
		cursor: pointer;
		display: flex;
		font-size: var(--font-small);
		height: 2.5rem;
		justify-content: center;
		padding: 0 2rem;
	}

	dialog > .footer > .close:hover {
		background-color: var(--gray);
	}
</style>