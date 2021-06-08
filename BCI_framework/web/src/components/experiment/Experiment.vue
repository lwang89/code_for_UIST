<template>
    <div>
        <!-- <h1>Experiment</h1> -->
        <Session v-if="isSessionOn" />
        <p v-if="!isSessionOn"> No parameters! </p>
    </div>
</template>


<script>
import Session from "./session/Session.vue";

export default {
    name: "Experiment",

    components: {
        Session
    },

    data() {
        return {
            isSessionOn: false, // show Session only when get Session configuration from backend
        };
    },

    mounted() {
        this.setupSession();
    },

    methods: {
        setupSession() {
            let experiment_parameters = this.$store.state.experiment_parameters;
            let numberOfSessions = experiment_parameters.sessionParameters.length;
            if (numberOfSessions < 1) {
                console.log("No Session here!!!");
            } else {
                this.$store.state.numberOfSessions = numberOfSessions;
                
                let sessionIndex = 0;
                this.$store.state.sessionIndex = sessionIndex;
                this.$store.state.currentSession = experiment_parameters.sessionParameters[sessionIndex];

                this.isSessionOn = true;
            }
        }
    }
};
</script>

<style lang="scss" scoped></style>