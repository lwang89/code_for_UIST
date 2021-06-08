<template>
    <div class="container">
        <!-- <p>This is NBackNumberVisual, Type 0</p> -->
        <div class="square center">
            <p style="font-size:200px">{{ current }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: "NBackNumberVisual",
    props: ["current"]
};
</script>

<style scoped>
    .square {
        background-color: white;
        width: 400px;
        height: 400px;
    }
    
    .center {
        margin: auto;
        border: 3px solid transparent;
    }
</style>
