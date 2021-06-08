<template>
    <div>
        <div class="form-container">
            <router-view ref="Child_SubInfo"></router-view>
        </div>

        <center><button @click="child_submit">Next</button></center>
    </div>
</template>

<script>

export default {
    name: "SerialFormContainer",

    data() {
        return {
            next: {name: "questionnaire_uncomfortable_movement"}
        };
    },

    mounted() {
        this.loadNext(this.next);
    },

    methods: {
        child_submit() {
            let children = this.$refs;
            console.log(children);
            this.$refs['Child_SubInfo'].submit();
        },

        loadNext(next) {
            this.$router.replace(next);
        },
    },
};
</script>

<style lang="scss" scoped>
    .form-container {
        background-color:   #ffffff;
        color:              #000000;
        overflow:             auto;
        height:               710px;
        width:                80%;
        margin:               auto;
        text-align:           left;
        padding:              10px;
        font-family:          Lato;
    }

    button {
        width: 100px;
        height: 50px;
        font-size: x-large;
        margin-top: 30px;
    }
</style>