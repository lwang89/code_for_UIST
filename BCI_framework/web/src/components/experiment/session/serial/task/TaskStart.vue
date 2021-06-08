<template>
    <div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "TaskStart",

    data() {
        return {
            next: {name: "task"},
        };
    },

    mounted() {
        this.setupSerialInfo();
        this.postTaskStart();
    },

    methods: {
        setupSerialInfo() {
            let experimentID = this.$store.state.experiment_parameters.experimentID;
            let sessionID = this.$store.state.currentSession.sessionID;
            let serialID = this.$store.state.currentSerial.serialID;
            let bigN = this.$store.state.currentSerial.trial.trialParameters.bigN;

            let SerialInfo = {
                experimentID,
                sessionID,
                serialID,
                bigN,
            };

            this.$store.state.currentSerialInfo = SerialInfo;
        },

        postTaskStart() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/start_task";

            let SerialInfo = this.$store.state.currentSerialInfo;

            axios
                .post(path, SerialInfo)
                .then((response) => {
                    console.log(response);
                    this.loadNext();
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        loadNext() {
            this.$router.replace(this.next);
        },
    }
};
</script>
<style lang="scss" scoped></style>
