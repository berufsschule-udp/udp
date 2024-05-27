<script lang="ts">
	import Footer from "../footer/Footer.svelte";
</script>

<div class="layout">
	<div class="content">
		<slot />
	</div>
	<Footer />
</div>

<style>
	.layout {
		display: flex;
		flex-direction: column;
		height: 100vh;
		margin: 0;
		overflow-x: hidden;
		width: 100vw;
	}

	.layout .content {
		display: flex;
		flex: 1;
		flex-direction: column;
		overflow-y: auto;
	}
</style>