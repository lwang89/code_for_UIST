Serial.vue. One Serial has serveral parts: Introduction, Task, Rest and maybe
else. These parts will be executed consecutively.
<template>
    <div>
        <!-- <h1>Serial</h1> -->
        <router-view></router-view>
    </div>
</template>

<script>
export default {
    name: "Serial",

    data() {
        return {
            next: {name: "introduction"},
        };
    },
    
    created() {
        this.loadNext();
    },

    methods: {
        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped></style>