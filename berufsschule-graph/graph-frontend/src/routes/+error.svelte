<script lang="ts">
	import { page } from "$app/stores";
	import ErrorHandler from "$lib/components/error/ErrorHandler.svelte";
	import Header from "$lib/components/header/Header.svelte";
</script>

<Header />
<ErrorHandler message={$page.error?.message} title="Error occurred" />