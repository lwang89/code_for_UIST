<template>
    <div>
        <router-view></router-view>
    </div>
</template>

<script>

export default {
    name: "PreExperiment",

    data() {
        return {
            next: {name: "form_container"}
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

<style lang="scss" scoped></style>