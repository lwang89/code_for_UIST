Rest.vue, the last page rendered in a Task. Every time the Rest is rendered, a
variable named like "counterSerial" will be increase by 1. When this counter
reaches "numberOfSerial", which means all Serials have been executed, the
Session is done.

In the current Serial, this page shows after all the trials (kewdown redords) ends and the current task ends.
<template>
    <div>
        <!-- <h1>This is Rest page</h1> -->
        <h1 v-if="!open_eyes">Please close your eyes and relax</h1>
        <h1 v-if="open_eyes && !last_serial_flag">Please open your eyes and prepare for the next task</h1>
        <!-- <p v-if="open_eyes && last_serial">Please open your eyes</p> -->
    </div>
</template>

<script>
import { Howl } from "howler"; // used to play audio
import axios from "axios";

export default {
    name: "Rest",

    data() {
        return {
            next: {name: "introduction"},
            duration: 1,                    // Int second
            interval: null,
            audio_start: null,
            audio_stop_duration: 4,
            open_eyes: false,
            last_serial_flag: false,
        };
    },

    mounted() {
        this.setupRestDuration();
        this.setupLastSerialFlag();
        this.setupNext();
        this.setupAudio();
        this.playAudio();
    },

    methods: {
        setupRestDuration() {
            let currentSerial = this.$store.state.currentSerial;
            this.duration = currentSerial.serialRestDuration;
        },

        setupLastSerialFlag() {
            let currentSession = this.$store.state.currentSession;
            let numberOfSerials = currentSession.serials.length;

            if (this.$store.state.serialIndex + 1 == numberOfSerials){
                this.last_serial_flag = true;
            } else {
                this.last_serial_flag = false;
            }
        },

        setupNext() {
            if (!this.last_serial_flag) {
                // Load the parameters for next serial
                let currentSession = this.$store.state.currentSession;
                this.$store.state.serialIndex = this.$store.state.serialIndex + 1;
                this.$store.state.currentSerial = currentSession.serials[this.$store.state.serialIndex];

                // Update the next page to show
                this.next = {name: "introduction"};
            }
            else {
                // Terminated current Session when counterSerials reaches numberOfSerials,
                this.next = {name: "session_done"};
            }
        },

        setupAudio() {
            let audio_start_serial_session_file = require("@/../public/static/rest_start.mp3");
            let audio_start_serial_file = require("@/../public/static/rest_start.mp3");
            let audio_stop_do_task_file = require("@/../public/static/rest_stop_do_task.mp3");
            this.audio_start_serial_session = new Howl({src: audio_start_serial_session_file});
            this.audio_start_serial = new Howl({src: audio_start_serial_file});
            this.audio_stop_do_task = new Howl({src: audio_stop_do_task_file});
        },

        playAudio() {
            if (this.last_serial_flag) {
                this.audio_start_serial_session.play();
                this.audio_start_serial_session.on("end", this.startCountDown);
            } else {
                this.audio_start_serial.play();
                this.audio_start_serial.on("end", this.startCountDown);
            }

        },

        startCountDown() {
            this.postRestStart();
            
            // Setup count down for the time left
            this.interval = setInterval(() => {
                this.duration = this.duration - 1;
            }, 1000);

            // Setup timeout for playing audio of end of rest
            setTimeout(() => {
                this.open_eyes = true;

                if (!this.last_serial_flag) {
                    this.audio_stop_do_task.play();
                }

            }, (this.duration - this.audio_stop_duration) * 1000);

            // Setup auto router to the next page
            setTimeout(() => {
                clearInterval(this.interval);
                this.postRestEnd();
            }, this.duration * 1000);
        },

        postRestStart() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/start_rest";

            let SerialInfo = this.$store.state.currentSerialInfo;

            axios
                .post(path, SerialInfo)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        postRestEnd() {
            let backend_url = this.$store.state.backend_url;
            let path = backend_url + "/end_rest";

            // let SerialInfo = this.$store.state.currentSerialInfo;
            let any_data = [];

            axios
                .post(path, any_data)
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

<style lang="scss" scoped>
    h1 {
        color: #ffffff;
        margin-top: 200px;
        font-size: 250%;
    }
</style>
