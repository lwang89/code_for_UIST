<template>
    <div>
        <h1 v-if="!open_eyes">Please close your eyes and relax</h1>
        <h1 v-if="open_eyes">Please open your eyes and prepare for the experiment</h1>
    </div>
</template>

<script>
import axios from "axios";
import { Howl } from "howler"; // used to play audio

export default {
    name: "RestBeforeExperiment",

    data() {
        return {
            next: {name: "experiment"},
            calibration_start_time: 5,
            calibration_end_time: 20,
            interval: null,
            audio_start: null,
            audio_stop: null,
            audio_stop_duration: 5,
            open_eyes: false,
            // show_button: false,
        };
    },

    mounted() {
        this.setupAudio();
        this.setupTimeVars();
        this.setupSignalTimeout();
        this.setupAudioTimeout();

        this.audio_start.play();

        this.interval = setInterval(() => {
            this.calibration_end_time = this.calibration_end_time - 1;
        }, 1000);
    },

    computed: {
        receiverCalibrationEnd: function() {
            return this.calibration_end_time;
        }
    },

    methods: {
        setupAudio() {
            let audio_start_file = require("@/../public/static/rest_before_experiment_start.mp3");
            let audio_stop_file = require("@/../public/static/rest_before_experiment_stop.mp3");
            this.audio_start = new Howl({src: audio_start_file});
            this.audio_stop = new Howl({src: audio_stop_file});
        },

        setupTimeVars() { 
            this.calibration_start_time = this.$store.state.experiment_parameters.receiverCalibrationStart;
            let calibration_duration = this.$store.state.experiment_parameters.receiverCalibrationDuration;
            this.calibration_end_time = this.calibration_start_time + calibration_duration;
        },

        setupSignalTimeout() {
            setTimeout(() => {
                this.sendSignal("start");
                }, this.calibration_start_time * 1000);

            setTimeout(() => {
                this.sendSignal("end");
                }, this.calibration_end_time * 1000);
        },

        setupAudioTimeout() {
            // Setup timeout for playing audio of end of rest
            setTimeout(() => {
                this.open_eyes = true;
                this.audio_stop.play();
            }, (this.calibration_end_time - this.audio_stop_duration) * 1000);
        },

        sendSignal(signal) {
            let backend_url = this.$store.state.backend_url; // url where flask backend is running
            let path = backend_url + "/" + signal + "_rest_before_experiment";

            let data = "nothing";

            axios
                .post(path, data)
                .then((response) => {
                    console.log(response);

                    // Show the button to start experiment after the backend end the rest
                    if (signal == "end") {
                        // this.show_button = true;
                        clearInterval(this.interval);
                        this.loadNext();
                    }
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
