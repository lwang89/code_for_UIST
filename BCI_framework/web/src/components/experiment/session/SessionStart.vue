SessionDone.vue is a temperary page. It comes out when a Session is done.
<template>
    <div>
        <!-- <p>Session Start</p> -->
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "SessionStart",

    data() {
        return {
            next: { name: "serial" },
        };
    },

    mounted() {
        this.setupSerial();
        this.setupSessionInfo();
        this.postSessionStart();
    },

    methods: {
        setupSerial() {
            // check if numberOfSerials is less than 1.
            // If so, go head to "seseion_done"
            // if not (there are Serials), increase serialIndex by one, from -1 to 0. Jump to introduction
            // Initialize serialIndex to be 0 and load currentSerial.
            let currentSession = this.$store.state.currentSession;
            let numberOfSerials = currentSession.serials.length;

            if (numberOfSerials < 1) {
                let sessionIndex = this.$store.state.sessionIndex;
                console.log("Zero serial for current session", sessionIndex);
                this.next = "session_done";
            } else {
                let serialIndex = 0;
                this.$store.state.serialIndex = serialIndex;
                this.$store.state.currentSerial = currentSession.serials[serialIndex];
            }
        },

        setupSessionInfo() {
            let experimentID = this.$store.state.experiment_parameters.experimentID;
            let sessionID = this.$store.state.currentSession.sessionID;
            let sessionType = this.$store.state.currentSession.sessionType;
            let sessionInfo = {
                experimentID,
                sessionID,
                sessionType,
            };
            this.$store.state.currentSessionInfo = sessionInfo;
        },

        postSessionStart() {
        let backend_url = this.$store.state.backend_url; // url where flask backend is running
        let path = backend_url + "/start_session";
        let sessionInfo = this.$store.state.currentSessionInfo;
        axios
            .post(path, sessionInfo)
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
    },
};
</script>

<style lang="scss" scoped></style>
