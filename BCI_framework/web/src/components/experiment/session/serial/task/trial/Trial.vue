<template>
    <div>
        <NBackNumberVisual v-if="type == 0" v-bind:current="current" />
    </div>
</template>

<script>
import NBackNumberVisual from "./types/NBackNumberVisual.vue";

export default {
    name: "Trial",

    props: ["type", "current"],

    components: {
        NBackNumberVisual,
    },
};
</script>

<style lang="scss" scoped></style>
