<script>
	import Header from "$lib/components/header/Header.svelte";
</script>

<Header />
<div class="mnemonic-image-wrapper">
	<img alt="Mnemonic" class="mnemonic-image" src="/images/mnemonic.png" />
</div>

<style>
	.mnemonic-image-wrapper {
		height: 100%;
		overflow: hidden;
	}

	.mnemonic-image {
		height: 100%;
		object-fit: contain;
		width: 100%;
	}
</style>