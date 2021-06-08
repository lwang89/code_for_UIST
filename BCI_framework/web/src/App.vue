<template>
    <div id="app">
        <!-- <p>BCI Experiment App</p> -->
        <div>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>

export default {
    name: "App",

    components: {
    },

    data() {
        return {
            next: {name: "start"}
        };
    },

    mounted() {
        this.loadNext(this.next);
    },

    methods: {
        loadNext(next) {
            this.$router.replace(next);
        },
    },
};
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 0px;
        max-width: 1300px;
        margin:auto;
    }
</style>
