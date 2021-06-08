<template>
    <div>
        <!-- <h1>Post-Experiment</h1> -->
        <div class="post-experiment-container">
            <router-view ref="Child_PostExp"></router-view>
        </div>
        <center><button @click="child_submit">Next</button></center>
    </div>
</template>

<script>
export default {
      name: "PostExpFormContainer",

    data() {
        return {
            next: {name: "questionnaire_rating"}
        };
    },

    mounted() {
        this.loadNext(this.next);
    },

    methods: {
        child_submit() {
            let children = this.$refs;
            console.log(children);
            this.$refs['Child_PostExp'].submit();
        },

        loadNext(next) {
            this.$router.replace(next);
        },
    },
};
</script>

<style lang="scss" scoped>
    .post-experiment-container {
        background-color:   #ffffff;
        color:              #000000;
        overflow:             auto;
        height:               600px;
        width:                80%;
        margin:               20px auto;
        text-align:           left;
        padding:              10px;
        font-family:          Lato;
    }

    button {
        width: 100px;
        height: 50px;
        font-size: medium;
        margin-top: 20px;
    }
</style>