SessionDone.vue is a temperary page. It comes out when a Session is done.
<template>
    <div>
        <!-- <p>Session Done</p> -->
        <!-- <p>Please wait for {{showDuration}} seconds</p> -->
        <h1 v-if="!open_eyes">Please close your eyes and relax</h1>
        <h1 v-if="open_eyes && !last_session_flag">Please open your eyes and prepare for the next task</h1>
        <h1 v-if="open_eyes && last_session_flag">Please open your eyes and complete a survey</h1>
    </div>
</template>

<script>
import axios from "axios";
import { Howl } from "howler"; // used to play audio

export default {
    name: "SessionDone",

    data() {
        return {
            next: {name: "session_start"},
            duration: 3,
            interval: null,
            audio_stop_moreserials: null,
            audio_stop_nomoreserials: null,
            audio_stop_duration: 4,
            open_eyes: false,
            last_session_flag: false,
        };
    },

    mounted() {
        this.setupRestDuration();
        this.setupLastSessionFlag();
        this.setupAudio();

        this.interval = setInterval(() => {
            this.duration = this.duration - 1;
        }, 1000);

        this.setupPlayAudio();

        this.postSessionEnd();
    },

    methods: {
        setupRestDuration() {
            this.duration = this.$store.state.currentSession.sessionRestDuration;
        },

        setupLastSessionFlag() {
            if ((this.$store.state.sessionIndex + 1) == this.$store.state.numberOfSessions) {
                this.last_session_flag = true;
            }
        },

        setupAudio() {
            let audio_stop_do_task_file = require("@/../public/static/rest_stop_do_task.mp3");
            let audio_stop_do_survey_file = require("@/../public/static/rest_stop_do_survey.mp3");
            this.audio_stop_do_task = new Howl({src: audio_stop_do_task_file});
            this.audio_stop_do_survey = new Howl({src: audio_stop_do_survey_file});
        },

        setupPlayAudio() {
            // Setup timeout for playing audio of end of rest
            setTimeout(() => {
                this.open_eyes = true;

                if (!this.last_session_flag) {
                    this.audio_stop_do_task.play();
                } else {
                    this.audio_stop_do_survey.play();
                }
            }, (this.duration - this.audio_stop_duration) * 1000);
        },

        postSessionEnd() {
            let backend_url = this.$store.state.backend_url; // url where flask backend is running
            let path = backend_url + "/end_session";

            let  sessionInfo = this.$store.state.currentSessionInfo;
            axios
                .post(path, sessionInfo)
                .then((response) => {
                    console.log(response);

                    this.setupNext();

                    setTimeout(() => {
                        clearInterval(this.interval);
                        this.loadNext();
                    }, this.duration * 1000);
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        setupNext() {
            // There are more sessions, load next session, jump to introduction
            if ((this.$store.state.sessionIndex + 1) < this.$store.state.numberOfSessions) {
                console.log("session done");
                this.updateSession();
                this.next = {name: "session_start"};
            }

            // No more sessions
            else {
                console.log("all sessions are done!!");
                this.postStopRecording();
                this.next = {name: "post_experiment"};
                
            }
        },

        updateSession() {
            let sessionIndex = this.$store.state.sessionIndex;
            sessionIndex = sessionIndex + 1;
            this.$store.state.sessionIndex = sessionIndex;

            let currentSession = this.$store.state.experiment_parameters.sessionParameters[sessionIndex];
            this.$store.state.currentSession = currentSession;
        },

        postStopRecording() {
            let backend_url = this.$store.state.backend_url; // url where flask backend is running
            let path = backend_url + "/stop_recording";

            let any_result = {stop: true};
            axios
                .post(path, any_result)
                .then((response) => {
                    console.log(response);
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

<style lang="scss" scoped>
    h1 {
        color: #ffffff;
        margin-top: 200px;
        font-size: 250%;
    }
</style>
