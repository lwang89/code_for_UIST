<template>
    <div>
        <h1>Start the experiment when you are ready</h1>
        <button v-if="isExperimentOn" @click="loadNext">Start</button>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Start",

    data() {
        return {
            next: { name: "pre_experiment" },
            isExperimentOn: false,
        };
    },

    mounted() {
        this.getExperimentParameters();
    },

    methods: {
        getExperimentParameters() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/get_experiment_parameters";
            axios
                .get(path)
                .then((res) => {
                    let experiment_parameters = res.data;
                    // Store the experiment parameters to global var
                    this.$store.state.experiment_parameters = experiment_parameters;
                    // Show the button to start
                    this.isExperimentOn = true;
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        // jump to pre-experiment
        loadNext() {
            this.$router.replace(this.next);
        },
    },
};
</script>

<style lang="scss" scoped>
    h1 {
        color: #ffffff;
        margin-top: 200px;
        font-size: 250%;
    }

    button {
        width: 100px;
        height: 50px;
        font-size: x-large;
        margin-top: 20px;
    }
</style>