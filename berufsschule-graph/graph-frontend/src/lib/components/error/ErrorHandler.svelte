<script lang="ts">
	export let title: string | undefined;
	export let message: string | undefined;
</script>

{#if title || message}
	<div class="error">
		<p class="title">{title}</p>
		<pre class="message">{message}</pre>
	</div>
{:else}
	<slot />
{/if}

<style>
	.error {
		margin: 0 2rem;
	}

	.error > .title {
		font-size: var(--font-xlarge);
		margin-bottom: .5rem;
	}

	.error > .message {
		background-color: var(--dark);
		color: var(--gray);
		font-size: var(--font-normal);
		padding: .5rem;
	}
</style>