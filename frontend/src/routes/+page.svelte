<script>
    import Result from "$lib/Result.svelte"

    let input;
    let results = [];

    function search() {
        let question = input.value;


        fetch('http://localhost:8000/ask/?q=' + question)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            results = data['results']
        });
    }
</script>

<main>
    <h1>Sean Caroll AMA Search</h1>
    <p>Search for answers to your questions.</p>

    <textarea on:keypress={(e) => e.key === 'Enter' && (search() || e.preventDefault())} bind:this={input} name="search" id="search"  placeholder="Type your question here"></textarea>
    <br>
    <button on:click={search}>Search</button>
    <br>
    {#each results as result}
        <Result {result} />
    {/each}
</main>

<style>
    textarea{
        width: 100%;
        height: 10em;
        resize: none;
    }
    
</style>