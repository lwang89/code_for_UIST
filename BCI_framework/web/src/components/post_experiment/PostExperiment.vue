<template>
    <div>
        <router-view></router-view>
    </div>
</template>

<script>

export default {
    name: "PostExperiment",

    data() {
        return {
            next: {name: "wait_device_take_off"}
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